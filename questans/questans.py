#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.web
import os.path
import uuid


all_questions = {}
next_quest = 1

class Answer:
    def __init__(self, auth, content):
        self.auth = auth
        self.content = content

class Question:
    def __init__(self, auth, content):
        #self.id = str(uuid.uuid4())
        self.id = self.next_id()
        self.auth = auth
        self.content = content
        self.ans = []
    
    def save(self):
        all_questions[self.id] = self

    def add_answer(self, answer):
        self.ans.append(answer)

    @classmethod
    def next_id(cls):
        global next_quest
        i = next_quest
        next_quest = next_quest + 1
        return i

    @classmethod
    def all(cls):
        return all_questions.values()

    @classmethod
    def get(cls, id):
        return all_questions.get(id)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        #user_json = self.get_secure_cookie('quas_user')
        #if not user_json: return None
        #return tornado.escap.json_decode(user_json)
        return self.get_secure_cookie('quas_user')

class AuthLoginHandler(BaseHandler):
    # @tornado.web.asynchronous
    # @gen.coroutine
    def get(self):
        self.render('login.html')

    def post(self):
        self.set_secure_cookie('quas_user', self.get_argument('name'))
        self.redirect('/')

class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('quas_user')
        self.write('You are logged out!')

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        # self.write('Hellow world' + self.current_user)
        self.render('index.html', all_ques=Question.all())

class QuestionNewHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('question_new.html')
    @tornado.web.authenticated
    def post(self):
        qtxt = self.get_argument("question")
        au = self.current_user
        question = Question(au, qtxt)
        question.save()
        self.redirect('/')

class QuestionShowHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, q_id):
        quest = Question.get(int(q_id))
        if quest is None:
            self.redirect('/')
        else:
            self.render('question_show.html', question=quest)

class QuestionAnsHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, q_id):
        question = Question.get(int(q_id))
        if question is not None:
            ans = Answer(self.current_user, self.get_argument('answer'))
            question.add_answer(ans)
        self.redirect('/q/%s/'%(q_id,))

def main():
    settings = {
        'cookie_secret':'__TODO: something secure only',
        'login_url':'/auth/login',
        'template_path':os.path.join(os.path.dirname(__file__), 'templates'),
        'static_path':os.path.join(os.path.dirname(__file__), 'static'),
        #'xsrf_cookies':True
    }
    application = tornado.web.Application([
        (r'/', MainHandler),
        (r'/auth/login', AuthLoginHandler),
        (r'/auth/logout', AuthLogoutHandler),
        (r'/q/', QuestionNewHandler),
        (r'/q/([0-9]+)/', QuestionShowHandler),
        (r'/q/([0-9]+)/answer/', QuestionAnsHandler),
    ], **settings)

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()

