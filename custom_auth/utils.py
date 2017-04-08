import requests
from django.utils.http import urlencode

CLIENT_ID = 5973649
SECRET_KEY = 'vQoiE2RdCLGwRqIp5vsi'
REDIRECT_URI = 'https://schedule-api-v1.herokuapp.com/api/auth_vk'
VK_OAUTH_URL = 'https://oauth.vk.com/'


def get_auth_vk_url():
    data = {'client_id': CLIENT_ID,
            'display': 'mobile',
            'redirect_uri': REDIRECT_URI,
            'scope': 'email',
            'response_type': 'code',
            'v': 5.63}
    return VK_OAUTH_URL + 'authorize/?' + urlencode(data)


def get_user_info(code):
    data = {'client_id': CLIENT_ID,
            'client_secret': SECRET_KEY,
            'redirect_uri': REDIRECT_URI,
            'code': code}
    url = VK_OAUTH_URL + 'access_token?' + urlencode(data)
    resp = requests.get(url)

    print('RESPONSE:\n%s' % resp.__dict__)
    print('JSON:\n%s' % resp.json())
    data = resp.json()

    return data


