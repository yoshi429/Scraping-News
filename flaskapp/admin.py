from django.contrib import admin

from .models import News, NewsOwner, MyNewsList


class NewsAdmin(admin.ModelAdmin):
    list_filter = ('news_owner', )



admin.site.register(News, NewsAdmin)
admin.site.register(NewsOwner)
admin.site.register(MyNewsList)
