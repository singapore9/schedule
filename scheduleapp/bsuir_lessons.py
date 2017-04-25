from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

import requests

from .models import Teacher, University, Faculty, Group, Lesson, LessonName, LessonTime, LessonDate


# Correct names for faculties from BSUIR by local_id
faculty_name = {'20040': 'ФТК',
                '20017': 'ФКП',
                '20012': 'ИЭФ',
                '20005': 'ФИТиУ',
                '20035': 'ФРЭ',
                '20054': 'Магистратура',
                '20004': 'ФЗО',
                '20026': 'ФКСиС',
                '20033': 'ФКТ (ИИТ)',
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
    url = 'https://www.bsuir.by/schedule/rest/currentWeek/date/%s' % datetime.today().strftime("%d.%m.%Y")
    resp = requests.get(url)
    return int(resp.text)


def get_week_start():
    weekday = datetime.today().isocalendar()[2]
    return datetime.today() - timedelta(days=weekday-1)


def get_all_teachers():
    url = 'https://www.bsuir.by/schedule/rest/employee'
    university, _ = University.objects.get_or_create(name='БГУИР')
    resp = requests.get(url)
    root = ET.fromstring(resp.text)
    teacher_objects = root.findall('employee')
    for item in teacher_objects:
        fullname = '%s %s %s' % (item.find('lastName').text, item.find('firstName').text, item.find('middleName').text)
        bsuir_key = item.find('id').text
        Teacher.objects.get_or_create(university=university,
                                      full_name=fullname,
                                      local_id=bsuir_key)


def get_all_groups():
    groups = []
    url = 'http://www.bsuir.by/schedule/rest/studentGroup'
    resp = requests.get(url)
    data = resp.text
    root = ET.fromstring(data)
    for group_xml in root:
        if group_xml.tag != 'studentGroup':
            continue
        group_info = {}
        for child_xml in group_xml:
            tag = child_xml.tag
            if tag == 'id':
                group_info.update({'local_id': child_xml.text})
            elif tag == 'name':
                group_info.update({'name': child_xml.text})
            elif tag == 'facultyId':
                group_info.update({'faculty_local_id': child_xml.text})
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

    resp = requests.get('https://www.bsuir.by/schedule/rest/schedule/%s' % local_group_id)
    data = resp.text
    root = ET.fromstring(data)

    times = set()
    names = set()
    teachers = set()

    for day_schedule in root:
        lessons = day_schedule[:-1]
        day = select_day(day_schedule[-1].text)
        for lesson in lessons:
            lesson_time = lesson.find('lessonTime').text
            start_time, end_time = map(lambda t: datetime.strptime(t, '%H:%M').time(), lesson_time.split('-'))
            times.add((start_time, end_time))

            lesson_type = select_type(lesson.find('lessonType').text)
            subject = lesson.find('subject').text
            sub_group = lesson.find('numSubgroup')
            sub_group = str(sub_group.text) if int(sub_group.text) else ''
            notes = sub_group
            names.add(subject)
            teacher = lesson.find('employee')
            if teacher:
                teachers.add(teacher.find('id').text)
            location = lesson.find('auditory').text if lesson.find('auditory') else None
            weeks = set(list((map(lambda elem: elem.text, lesson.findall('weekNumber'))))) - {'0', }
            lesson_info = {'start_time': start_time,
                           'end_time': end_time,
                           'teacher': teacher.find('id').text if teacher else None,
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
