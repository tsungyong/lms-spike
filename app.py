#!/usr/bin/env python

from flask import Flask, redirect, make_response, jsonify, render_template

import json
import time
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

app = Flask(__name__)
URL = 'https://inv999abc.docebosaas.com'
CLIENT_ID = 'acaspike'
CLIENT_SECRET = 'e06504ec7b8e8a8696ccc83f942445d5c2752fcc'
SSO_SECRET = '123456'

client = BackendApplicationClient(client_id=CLIENT_ID)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url='%s/oauth2/token' % URL,
                          client_id=CLIENT_ID,
                          client_secret=CLIENT_SECRET)


def get_userid(username):
    r = oauth.post('%s/api/user/checkUsername' % URL, data={'userid': username})
    j = json.loads(r.text)
    if 'idst' in j:
        return j['idst']
    return None

def get_enrolled_courses(userid):
    r = oauth.post('%s/api/user/enrollments' % URL, data={'id_user': userid})
    j = json.loads(r.text)
    return j["courses"]


def authenticate_user(userid, password):
    r = oauth.post('%s/api/user/authenticate' % URL,
                   data={'username': userid, 'password': password})
    j = json.loads(r.text)
    return j

def get_user_token(username):
    r = oauth.post('%s/api/user/getToken' % URL,
                   data={'username': username})
    j = json.loads(r.text)
    return j['token']

def get_sso_url(username):
    current_time = int(time.time())
    import hashlib
    m = hashlib.md5()
    m.update("%s,%s,%s" % (username, current_time, SSO_SECRET))
    token = m.hexdigest()
    return "%s/lms/index.php?r=site/sso&login_user=%s&time=%s&token=%s" % (
                URL, username, current_time, token)

@app.route('/login/<username>')
def login(username):
    sso_url = get_sso_url(username)
    return redirect(sso_url)

@app.route('/user/create/<username>')
def user_create(username):
    r = oauth.post('%s/api/user/create' % URL, data = {'userid': username})
    return r.text

@app.route('/login/v1/<username>')
def loginv1(username):
    r = oauth.post('%s/manage/v1/user/login' % URL, data={'username': 'john.mcglinchey@investopedia.com', 'password': 'GtA-was-wd4-BA3'})
    j = json.loads(r.text)
    return redirect('/session/%s' % j['data']['access_token'])

@app.route('/login/api/<username>')
def login_api(username):
    user_auth_token = get_user_token(username)
    print ('%s/lms/index.php?r=site/actionAutoLogin&userId=%s&authToken=%s' %
                        (URL, username, user_auth_token))
    return "blah"
    return redirect('%s/lms/index.php?r=site/actionAutoLogin&userId=%s&authToken=%s' %
                    (URL, username, user_auth_token))

@app.route('/logout/<username>')
def logout(username):
    return redirect('%s/manage/v1/user/logout' % URL)

@app.route('/session/<token>')
def session(token):
    return render_template('login.html', token=token)

@app.route('/info/enrolled/<username>')
def enrolled(username):
    userid = get_userid(username)
    if userid is None:
        return "User %s does not exist in InvestoAcademy." % userid

    enrolled_courses = get_enrolled_courses(userid)
    return jsonify(enrolled_courses)

@app.route('/ecommerce/listTransactions')
def list_transactions():
    r = oauth.post('%s/api/ecommerce/listTransactions' % URL, data={'from':0, 'count':100})
    return r.text

@app.route('/courses')
def list_courses():
    r = oauth.post('%s/api/course/courses' % URL)
    return jsonify(json.loads(r.text))

@app.route('/enroll/<username>/<course_id>')
def enroll(username, course_id):
    r = oauth.post('%s/learn/v1/enrollments' % URL, data={'course_ids': [course_id], 'user_ids': [username]})
    return jsonify(json.loads(r.text))

@app.route('/')
def main():
    #user_token = authenticate_user(oauth, 'john.mcglinchey@investopedia.com', 'GtA-was-wd4-BA3')
    return render_template('main.html')

if __name__ == "__main__":
    app.run()
