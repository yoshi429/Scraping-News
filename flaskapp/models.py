from django.db import models
from django.utils import timezone


class NewsOwner(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=100)
    news_url = models.CharField(max_length=1000)
    news_owner = models.ForeignKey(NewsOwner, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.datetime.today)

    def __str__(self):
        return f"{self.title}-{self.news_owner.name}"

    class Meta:
        ordering = ['-date']


class MyNewsList(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.news.title}-{self.news.news_owner.name}"





