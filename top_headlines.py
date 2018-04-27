
from flask import Flask, render_template, url_for
from secrets_example import *
import requests
import json
import datetime

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/user/<user>')
@app.route('/user/<user>/<topic>')
def show_user(user,topic=None):
    if not topic:
        topic='technology'
    base_url = "https://api.nytimes.com/svc/topstories/v2/"+topic+".json"
    params={'api-key': api_key}
    results = json.loads(requests.get(base_url, params).text)['results']
    return_value=[ {'title':i['title'],'url':i['url']} for i in results][:5]
    return render_template('user.html', name=user, newsdata=return_value, topic=topic)

@app.route('/user/<user>/time')
def greeter(user):
    base_url = "https://api.nytimes.com/svc/topstories/v2/technology.json"
    params={'api-key': api_key}
    results = json.loads(requests.get(base_url, params).text)['results']
    return_value=[ {'title':i['title'],'url':i['url']} for i in results][:5]
    currentTime = datetime.datetime.now()
    if currentTime.hour < 12:     
        greeting = 'Good morning,'
    elif 12 <= currentTime.hour < 16:
        greeting = 'Good afternoon,'
    elif 16 <= currentTime.hour < 20:
        greeting = 'Good evening,'
    else:
        greeting = 'Good night,'
    return render_template('greeter.html', name=user, newsdata=return_value, greeting=greeting)


if __name__ == '__main__':
    app.run(debug=True)