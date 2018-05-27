from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

import requests

from .models import Teacher, University, Faculty, Group, Lesson, LessonName, LessonTime, LessonDate


# Correct names for faculties from BSUIR by local_id
faculty_name = {'20040': 'ФИК',
                '20017': 'ФКП',
                '20012': 'ИЭФ',
                '20005': 'ФИТиУ',
                '20035': 'ФРЭ',
                '20054': 'Магистратура',
                '20004': 'ФЗО',
                '20026': 'ФКСиС',
                '20033': 'ФКТ (ИИТ)',
                '20034': 'ФИНО',
                '20000': 'ВФ', }


def select_type(type_name):
    if type_name == 'ПЗ':
        return 2
    if type_name == 'ЛК':
        return 1
    if type_name == 'ЛР':
        return 5
    return 5


def select_day(day_name):
    if day_name == 'Понедельник':
        return 0
    if day_name == 'Вторник':
        return 1
    if day_name == 'Среда':
        return 2
    if day_name == 'Четверг':
        return 3
    if day_name == 'Пятница':
        return 4
    if day_name == 'Суббота':
        return 5


def get_cur_week():
    url = 'http://students.bsuir.by/api/v1/week'
    resp = requests.get(url)
    return int(resp.text)


def get_week_start():
    weekday = datetime.today().isocalendar()[2]
    return datetime.today() - timedelta(days=weekday-1)


def get_all_teachers():
    url = 'https://students.bsuir.by/api/v1/employees'
    university, _ = University.objects.get_or_create(name='БГУИР')
    resp = requests.get(url)
    teacher_objects = resp.json()
    for item in teacher_objects:
        fullname = '%s %s %s' % (item['lastName'], item['firstName'], item['middleName'])
        bsuir_key = str(item['id'])
        Teacher.objects.get_or_create(university=university,
                                      full_name=fullname,
                                      local_id=bsuir_key)


def get_all_groups():
    groups = []
    url = 'https://students.bsuir.by/api/v1/groups'
    resp = requests.get(url)
    data = resp.json()
    for group in data:
        group_info = {
            'local_id': str(group['id']),
            'name': group['name'],
            'faculty_local_id': str(group['facultyId'])
        }
        groups.append(group_info)
    university, _ = University.objects.get_or_create(name='БГУИР')
    glob_id_from_local = dict()
    for local_id in set(map(lambda g: g['faculty_local_id'], groups)):
        faculty, _ = Faculty.objects.get_or_create(university=university,
                                                   local_id=local_id,
                                                   name=faculty_name[local_id])
        glob_id_from_local.update({local_id: faculty.id})

    for group in groups:
        Group.objects.get_or_create(name=group['name'],
                                    local_id=group['local_id'],
                                    faculty_id=glob_id_from_local[group['faculty_local_id']])


def get_schedule_for(local_group_id):
    group_schedule = []
    university, _ = University.objects.get_or_create(name='БГУИР')

    resp = requests.get('https://students.bsuir.by/api/v1/studentGroup/schedule?id=%s' % local_group_id)
    data = resp.json()

    times = set()
    names = set()
    teachers = set()
    if not data['schedules']:
        return
    for day_schedule in data['schedules']:
        lessons = day_schedule['schedule']
        day = select_day(day_schedule['weekDay'])
        for lesson in lessons:
            lesson_time = lesson['lessonTime']
            start_time, end_time = map(lambda t: datetime.strptime(t, '%H:%M').time(), lesson_time.split('-'))
            times.add((start_time, end_time))

            lesson_type = select_type(lesson['lessonType'])
            subject = lesson['subject']
            sub_group = lesson['numSubgroup'] or ''
            main_notes = lesson['note']
            notes = '%s, %s' % (sub_group, main_notes) if (sub_group and main_notes) else '%s' % (sub_group or main_notes)
            names.add(subject)
            teacher = lesson['employee']
            if teacher:
                teachers.add(str(teacher[0]['id']))
            location = lesson['auditory'][0] if lesson['auditory'] else None
            weeks = map(str, set(lesson['weekNumber']) - {0, })
            lesson_info = {'start_time': start_time,
                           'end_time': end_time,
                           'teacher': str(teacher[0]['id']) if teacher else None,
                           'type': lesson_type,
                           'name': subject,
                           'location': location,
                           'weeks': weeks,
                           'note': notes,
                           'week_day': day}
            group_schedule.append(lesson_info)

    lt_indices = dict()
    ln_indices = dict()
    teacher_indices = dict()

    for lesson_time in times:
        lt, _ = LessonTime.objects.get_or_create(university=university,
                                                 beginning_at=lesson_time[0],
                                                 ended_at=lesson_time[1])
        lt_indices.update({lesson_time: lt.id})

    for lesson_name in names:
        ln, _ = LessonName.objects.get_or_create(university=university,
                                                 name=lesson_name)
        ln_indices.update({lesson_name: ln.id})

    for teacher in teachers:
        _teacher, _ = Teacher.objects.get_or_create(university=university,
                                                    local_id=teacher)
        teacher_indices.update({teacher: _teacher.id})
    group = Group.objects.get(faculty__university=university,
                              local_id=local_group_id)
    cur_week = get_cur_week()

    week_start = get_week_start()
    for lesson in group_schedule:
        for week in lesson['weeks']:
            week = int(week)
            week = week if week >= cur_week else (week + 4)
            lesson_dt = (week_start + timedelta(days=(7 * (week-cur_week)+lesson['week_day']))).date()
            lesson_date, _ = LessonDate.objects.get_or_create(date=lesson_dt, group_id=group.id)
            Lesson.objects.get_or_create(group_id=group.id,
                                         name_id=ln_indices[lesson['name']],
                                         time_id=lt_indices[(lesson['start_time'], lesson['end_time'])],
                                         teacher_id=teacher_indices[lesson['teacher']] if lesson['teacher'] else None,
                                         location=lesson['location'],
                                         type=lesson['type'],
                                         note=lesson['note'],
                                         date_id=lesson_date.id)


def update_faculty(faculty_id):
    logfile = open('logfile%s.txt' % datetime.now(), 'w+')
    for group in Group.objects.filter(faculty=faculty_id):
        try:
            get_schedule_for(group.local_id)
            msg = '[ OK ] Group [%s]\n' % (group.local_id, )
            logfile.write(msg)
        except Exception as e:
            msg = '[FAIL] Group [%s]:\n%s\n\n' % (group.local_id, e)
            logfile.write(msg)
    logfile.close()
