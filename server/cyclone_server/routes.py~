import string
from cyclone.web import URLSpec
from cyclone_server import views
from cyclone_server import api


API_VERSIONS = ['v0.1.0', 'latest']


def APIURLSpec(url, *args, **kwargs):
    l = []
    template = string.Template(url)
    for version in API_VERSIONS:
        l.append(template.substitute(apiver=version))
    l = sorted(list(set(l)))
    if len(l) == 1:
        return URLSpec(l[0], *args, **kwargs)
    return [URLSpec(x, *args, **kwargs) for x in l]


def munge_route_list(rl):
    new_l = []
    for item in rl:
        if isinstance(item, list):
            new_l.extend(munge_route_list(item))
        else:
            new_l.append(item)
    return new_l


routes = munge_route_list([
    URLSpec(r'/', views.IndexHandler, name='home'),
    APIURLSpec(r'/api/$apiver/collaborative/filtering', api.CollaborativeFilteringHandler)
])
