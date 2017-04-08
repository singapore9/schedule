from django.http import HttpResponseRedirect

from .utils import get_auth_vk_url


def vk_view(request):
    return HttpResponseRedirect(get_auth_vk_url())
