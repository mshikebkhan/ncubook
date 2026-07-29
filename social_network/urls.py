from django.contrib import admin
from django.urls import path, include

urlpatterns = [
        # CampusBook url config.
        path('', include(('campusbook.urls', 'campusbook'), namespace='campusbook')),

        # Users url config.
        path('', include(('users.urls', 'users'), namespace='users')),

        # Posts url config.
        path('', include(('posts.urls', 'posts'), namespace='posts')),

        # Messenger url config.
        path('', include(('messenger.urls', 'messenger'), namespace='messenger')),

        # Notifications url config.
        path('', include(('notifications.urls', 'notifications'), namespace='notifications')),

        # Admin url config
        path('admin/', admin.site.urls), 

        # Detect Timezone
        path('tz_detect/', include('tz_detect.urls')),
]

# Admin portal config.
admin.site.site_header = 'CampusBook Adminstration'
admin.site.index_title = 'Site Administration'
admin.site.site_title = "CampusBook - Admin"