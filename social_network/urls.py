from django.contrib import admin
from django.urls import path, include

urlpatterns = [
        # Khan Diary url config.
        path('', include(('ncubook.urls', 'ncubook'), namespace='ncubook')),

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
admin.site.site_header = 'NCUbook Adminstration'
admin.site.index_title = 'Site Administration'
admin.site.site_title = "NCUbook - Admin"