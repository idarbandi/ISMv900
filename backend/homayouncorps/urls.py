from django.contrib import admin
from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from filter.api.schema import schema
from django.conf import settings
from django.shortcuts import redirect

def redirect_to_vue_dev(request, path=''):
    vue_dev_server_url = settings.VUE_DEV_SERVER_URL
    # Ensure path starts with a slash
    full_path = f'/{path}' if path and not path.startswith('/') else path
    return redirect(f'{vue_dev_server_url}{full_path}')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('filter/graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]

if settings.DEBUG:
    # In debug mode, let the Vue dev server handle all other paths
    urlpatterns += [
        re_path(r'^(?P<path>.*)$', redirect_to_vue_dev),
    ]
else:
    # In production, serve Django views and static files
    urlpatterns += [
        path('', include('myapp.urls')),
        path('invoice/', include('invoice.urls')),
    ] 