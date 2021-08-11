from hashlib import new
import requests
from bs4 import BeautifulSoup
import re

from flask import url_for, render_template, redirect, flash, abort

from . forms import UpdateNewsForm 
from flaskapp.flask import app
from flaskapp.models import News, NewsOwner, MyNewsList


@app.route('/')
def home():
    newses = News.objects.all().order_by('?')[:10]
    return render_template('home.html', newses=newses)



@app.route('/yahoo', methods=['GET', 'POST'])
def get_yahoo_news():
    form = UpdateNewsForm()
    obj, created = NewsOwner.objects.get_or_create(name="Yahoo")

    if form.validate_on_submit():
        # ヤフーニュースのトップページ情報を取得する
        URL = "https://www.yahoo.co.jp/"
        r = requests.get(URL)
        # BeautifulSoupにヤフーニュースのページ内容を読み込ませる
        soup = BeautifulSoup(r.text, "html.parser")

        # ヤフーニュースの見出しとURLの情報を取得して出力する
        data_list = soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))
        for data in data_list:
            title = data.span.string
            url = data.attrs["href"]
            news = News.objects.filter(title=title).first()
            if news is None:
                news = News.objects.create(title=title, news_url=url, news_owner=obj)
        flash('Newsを更新しました！', 'success')

    newses = News.objects.filter(news_owner=obj).all()
    return render_template('get_news.html', title='Yahoo', newses=newses, form=form)


@app.route('/nikkei', methods=['GET', 'POST'])
def get_nikkei_news():
    form = UpdateNewsForm()
    obj, created = NewsOwner.objects.get_or_create(name="日経新聞")
    
    if form.validate_on_submit():
        URL = 'https://www.nikkei.com/news/category/'
        r = requests.get(URL)
        for i in range(5):    
            soup = BeautifulSoup(r.text, 'html.parser')
            url = 'https://www.nikkei.com/news/category/?bn=' + str(i*30+1)
            items = soup.find_all('h3', class_='m-miM09_title') + soup.find_all(class_='m-miM32_itemTitleText')
            for item in items:
                title = item.find('a').text
                url = 'https://www.nikkei.com/' + item.find('a')['href']
                news = News.objects.filter(title=title).first()
                if news is None:
                    news = News.objects.create(title=title, news_url=url, news_owner=obj)
        flash('Newsを更新しました！', 'success')

    newses = News.objects.filter(news_owner=obj).all()
    return render_template('get_news.html', title='日経新聞', newses=newses, form=form)


@app.route('/google', methods=['GET', 'POST'])
def get_google_news():
    form = UpdateNewsForm()
    obj, created = NewsOwner.objects.get_or_create(name="Google")
    
    if form.validate_on_submit():
        URL = "https://news.google.com/topstories?hl=ja&gl=JP&ceid=JP:ja"
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, "html.parser")
        articles = soup.select(".xrnccd")
        for article in articles:
            title = article.find("h3").text
            url = article.find('a', class_='VDXfz')
            url = url.get('href')
            url = 'https://news.google.com/' + url
            news = News.objects.filter(title=title).first()
            if news is None:
                    news = News.objects.create(title=title, news_url=url, news_owner=obj)
        flash('Newsを更新しました！', 'success')

    newses = News.objects.filter(news_owner=obj).all()
    return render_template('get_news.html', title='Google', newses=newses, form=form)


@app.route('/news/<int:news_id>/delete', methods=['POST'])
def delete_news(news_id):
    print(news_id)
    try:
        news = News.objects.get(id=news_id)
        print(news)
    except:
        abort(403)
    news_owener = news.news_owner.name
    title = news.title    
    news.delete()
    flash(f'{title}のニュースは削除されました!', 'success')
    if news_owener == "Yahoo":
        return redirect(url_for('get_yahoo_news'))
    elif news_owener == "Google":
        return redirect(url_for('get_google_news'))
    elif news_owener == "日経新聞":
        return redirect(url_for('get_nikkei_news'))
    return redirect(url_for('home'))


@app.route('/mylist')
def my_news_list():
    my_news_list = MyNewsList.objects.all()
    return render_template('my_news_list.html', title='MyNewsList', my_news_list=my_news_list)


@app.route('/news/<int:news_id>/add_my_list_news', methods=['POST'])
def add_my_list_news(news_id):
    try:
        news = News.objects.get(id=news_id)
    except:
        abort(403)
    if MyNewsList.objects.filter(news=news):
        flash('既にMyNewsListに追加されています!', 'warning')
        return redirect(url_for('my_news_list'))
    MyNewsList.objects.create(news=news)
    flash('MyNewsListに追加されました!', 'success')
    return redirect(url_for('my_news_list'))


@app.route('/news/<int:news_id>/remove_my_list_news', methods=['POST'])
def remove_my_list_news(news_id):
    try:
        news = News.objects.get(id=news_id)
        my_news_list = MyNewsList.objects.get(news=news)
    except:
        abort(403)
    my_news_list.delete()
    flash('MyNewsListから削除されました!', 'success')
    return redirect(url_for('my_news_list'))
