# import modules for flask model
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, session, abort
from flask_restful import Resource, Api
from flask_cors import CORS
from functools import wraps
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt

# import modules for chat-bot model
from deeppavlov import build_model, configs
from keras.models import load_model
from helper import *
import numpy as np
import tensorflow as tf
from nltk.corpus import stopwords
from string import punctuation
from nltk import word_tokenize

import sqlite3
import re
import random

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading


app = Flask(__name__)
app.secret_key = b'U\x80\xfe\xd4\xe5\xff\x0c\xb1X\x7f\xac\xdc\x06\x13\x1b&'
CORS(app)
api = Api(app)


@app.after_request
def add_security_headers(resp):
    resp.headers.add('Access-Control-Allow-Headers',
                     "Origin, X-Requested-With, Content-Type, Accept, x-auth")
    return resp


session_ids = dict()
fallback_message = "Looks like your question is out of my scope. Kindly enter your email Id and our admin will " \
                   "resolve your query. "


# The mail addresses and password
sender_address = 'bunnysmarty98@gmail.com'
sender_pass = ''

model = None
model_basic_response = None
paragraph = None
values = dict()
word_to_index = None
index_to_word = None
word_to_vec_map = None

# g1 and g2 are two graphs to load both models
g1 = tf.Graph()
g2 = tf.Graph()


@app.before_first_request
def init_stuff():
    """
    Initialize the data and the model before first request is processed.
    :return: None
    """
    load_data()
    # load_all_model()


class ChatBot(Resource):
    def post(self):
        """
        Return response for the questions asked
        :return: answer -> str
        """
        global session_ids
        threshold = 60000   # 45000
        minimum_match = 1
        max_length = 10

        orig_question = request.form['question']
        orig_question = orig_question.strip()

        curr_session_id = request.form['curr_session_id']
        if curr_session_id not in session_ids:
            session_ids[curr_session_id] = list()
        print("{}".format(curr_session_id))

        if len(session_ids[curr_session_id])>0 and session_ids[curr_session_id][-1].message_ == fallback_message:
            # send email
            print("SEND EMAIL")
            email_thread = threading.Thread(target=send_email, args=(curr_session_id, orig_question))   # orig_question will contain user's email
            # send_email(curr_session_id, "patrawalamurtaza52@gmail.com")
            email_thread.start()
            return "Thank you, admin will resolve your query via email shortly."

        session_ids[curr_session_id].append(Message("user", orig_question))

        print(session_ids)

        # append '?' to the question asked
        question = orig_question
        if question[-1] != "?":
            question += '?'
        words = question.split(' ')
        # add question word in front, if not present
        question_words = ['what', 'why', 'how', 'where', 'when']
        counter = 0
        for word in words:
            if word.lower() in question_words:
                counter += 1

        if counter == 0:
            question = 'what '+ question
        print('QUESTION:', question)

        response = ''

        # get answer from paragraph model
        with g2.as_default():
            answer = model([paragraph.lower()], [question.lower()])
            answer_main = answer[0][0]
        print('PARAGRAPH MODEL:', answer)

        # Substitute actual values from database in place of keys
        keys = re.findall('zxyw[^\s.]*', answer_main)
        if keys:
            print(keys)
            for k in keys:
                answer_main = re.sub(k, values[k[4:].lower()], answer_main)

        # select response from basic response and paragraph model if the confidence is less than the threshold
        if answer[2][0] < threshold:
            # remove unnecessary stopwords from question and answer for comparison
            question_list = remove_stop_words(question.lower())
            answer_list = remove_stop_words(answer_main.lower())

            # find number of words matching in question and anwer
            count = 0
            for i in question_list:
                for j in answer_list:
                    if i == j:
                        count += 1
            if count >= minimum_match:
                # return response from paragraph model if more number of words are matched in question and answer
                print('ANSWER:', answer_main)
                response = answer_main
            else:
                # return response from basic response model if few words are matched in question and answer
                with g1.as_default():
                    x_test = sentences_to_indices(np.array([question]), word_to_index, max_length)
                    pred = model_basic_response.predict(x_test)
                    pred_index = int(np.argmax(pred, axis=1)[0])

                    basic_reply = ['Hi there, how can I help?', 'See you later, thanks for visiting', 'Happy to help!']

                    if pred_index in [0, 1, 2]:
                        print('BASIC MODEL ANSWER:', basic_reply[pred_index])
                        response = basic_reply[pred_index]
                    else:
                        # default response
                        response = fallback_message
        else:
            # model confidence greater than threshold
            print('ANSWER:', answer_main)
            response = answer_main

        # save the chatbot response
        session_ids[curr_session_id].append(Message("SAHEB Bot", response))

        return response


def send_email(client_session_id, client_email):
    mail_content = generate_mail_content(client_session_id, client_email)

    receiver_address = client_email
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = client_email
    message['Subject'] = 'SAHEB chatbot user query, user email -> ' + client_email   # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) # use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


def generate_mail_content(client_session_id, client_email):
    mail_content = 'CLIENT MAIL ID ---- {}\n\n\nUSER CHATS HISTORY\n\n'.format(client_email)
    for msg in session_ids[client_session_id]:
        mail_content += str(msg) + "\n"
    return mail_content


def remove_stop_words(words) -> list:
    """
    remove stopwords from the question asked and answer of paragraph model
    :param words: str
    :return: list (words tokenized string)
    """
    custom_stopwords = set(stopwords.words('english') + list(punctuation))
    return [word for word in word_tokenize(words) if word not in custom_stopwords]


def load_all_model():
    """
    load paragraph model and basic response model in memory
    :return: None
    """
    global model
    global model_basic_response
    global word_to_index, index_to_word, word_to_vec_map
    global g1
    global g2

    with g1.as_default():
        # basic response model
        model_basic_response = load_model('./model/basic_response_model/trained_lstm_128_128_dropout_4_3.h5')

    with g2.as_default():
        # paragraph model
        model = build_model(configs.squad.squad, download=True)

    # glove embedding
    word_to_index, index_to_word, word_to_vec_map = read_glove_vecs('./model/glove/glove.6B.50d.h5')


def load_data():
    """
    retrieves paragraph and key-value data from database
    :return: None
    """
    global paragraph
    global values
    try:
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        para_sql = "select * from paragraph;"
        values_sql = "select * from blank_data;"
        cursor.execute(para_sql)
        paragraph = cursor.fetchall()[0][0]
        cursor.execute(values_sql)
        values_list = cursor.fetchall()
        for i in values_list:
            values.update({i[1].lower(): i[2]})
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()


# def is_logged_in(f):
#     @wraps(f)
#     def wrap(*args,**kwargs):
#         print(session)
#         if('logged_in' in session):
#             return f(*args,**kwargs)
#         else:
#             flash('Unauthorized, Please login','danger')
#             return redirect(url_for('login'))
#     return wrap


@app.route('/', methods=['GET', 'POST'])
def index():
    """ Display home page """
    if 'logged_in' in session:
        if session['logged_in']:
            return redirect('/para/')
        else:
            render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/key_values/')
def key_values():
    """ Display key-value pair table """
    if 'logged_in' in session:
        if session['logged_in']:
            return render_template('key_vals.html', js_files=['key-vals.js', ], css_files=['key-vals.css', ])
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/read/values/')
def read_values():
    """ Read key-value pair from the database """
    print(session)
    if 'logged_in' in session:
        if session['logged_in']:
            formatted_data = []
            try:
                connection = sqlite3.connect('test.db')
                c = connection.cursor()
                c.execute('SELECT * FROM blank_data')
                table_data = c.fetchall()
                for items in table_data:
                    formatted_data.append(dict(id=items[0], key=items[1], value=items[2]))
                connection.commit()
                resp = jsonify(formatted_data)
                resp.headers.add('Access-Control-Allow-Origin', '*')
                load_data()
            except Exception as exception:
                print(exception)
                resp = jsonify(success=False)
                resp.headers.add('Access-Control-Allow-Origin', '*')
            finally:
                if connection:
                    connection.close()
            return resp
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/edit_para/', methods=['POST', 'GET'])
def edit_para():
    """ Update edited paragraph in the database """
    if request.form['str']:
        new_paragraph = request.form['str']
    try:
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute('UPDATE paragraph SET para="' + new_paragraph + '";')
        # conn.commit()
        keys_para = re.findall('zxyw[^\s.]*', new_paragraph)
        print(keys_para)
        c.execute('SELECT key FROM blank_data')
        keys_db = c.fetchall()
        print(keys_db)
        for item in keys_db:
            print(item[0])
            if 'zxyw'+item[0] not in keys_para:
                print('not in', item[0])
                c.execute("DELETE FROM blank_data WHERE key='"+item[0]+"';")
        conn.commit()
        load_data()
        c.execute('select * from paragraph;')
        new_paragraph = c.fetchall()
        print(new_paragraph[0][0])
    except Exception as exception:
        print(exception)

    finally:
        if conn:
            conn.close()

    return jsonify(para=new_paragraph[0][0])


@app.route('/update/values/', methods=['POST', ])
def update_values():
    """ Update edited key-value in the database """
    try:
        connection = sqlite3.connect('test.db')
        c = connection.cursor()
        if request.form['id'] and request.form['value']:
            i = request.form['id']
            value = request.form['value']
            sql = 'update blank_data set `value` = "'+value+'" where `id` = "'+i+'";'
            c.execute(sql)
            connection.commit()
            resp = jsonify(success=True, id=i, value=value)
    except Exception as exception:
        print(exception)
        resp = jsonify(success=False)
    finally:
        if connection:
            connection.close()
        return resp


@app.route('/insert/values/', methods=['POST', ])
def insert_values():
    """ Insert new key-value pair in the database  """
    if request.form['key'] and request.form['value']:
        key = request.form['key']
        value = request.form['value']
        try:
            connection = sqlite3.connect('test.db')
            c = connection.cursor()
            sql = 'INSERT INTO blank_data (`key`, `value`) VALUES("' + key + '", "' + value + '");'
            c.execute(sql)
            connection.commit()
            sql = 'select * from blank_data where `key` = "'+key+'";'
            c.execute(sql)
            data = c.fetchall()
            formatted_data = {"id": data[0][0], "key": data[0][1], "value": data[0][2]}
            resp = jsonify(success=True, data=formatted_data)
        except sqlite3.IntegrityError as e:
            print(e)
            resp = jsonify(success=False, error="Key already exists!")
        finally:
            if connection:
                connection.close()
        return resp


@app.route('/delete/values', methods=['POST', ])
def delete_values():
    """ Delete key value pair from the database """
    if request.form['key']:
        key = request.form['key']

        try:
            connection = sqlite3.connect('test.db')
            c = connection.cursor()
            sql = 'delete from blank_data where `key` = "'+key+'";'
            c.execute(sql)
            connection.commit()
            resp = jsonify(success=True)
        except Exception as e:
            print(e)
            resp = jsonify(success=False)
        finally:
            if connection:
                connection.close()
            return resp


@app.route('/para/')
def read_para():
    """ Read paragraph from the database """
    if 'logged_in' in session:
        if session['logged_in']:
            try:
                conn = sqlite3.connect('test.db')
                c = conn.cursor()
                c.execute('select * from paragraph')
                paragraph = c.fetchall()
                conn.commit()
            except sqlite3.IntegrityError:
                return {"error"}
            except Exception as exception:
                print(exception)
            finally:
                if conn:
                    conn.close()

            return render_template('view_para.html', para=paragraph[0][0], js_files=['para.js', ])
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


class RegisterForm(Form):
    """ Registration form for new admin user """
    name = StringField('Name', [validators.Length(min=1, max=50)])
    # username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Register new admin user """
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        # username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        try:
            connection = sqlite3.connect('test.db')
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users(name,email,password) VALUES('"+name+"','"+email+"','"+password+"')")
            connection.commit()
            connection.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError as ie:
            print(ie)
        except Exception as e:
            print(e)

    return render_template('register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """ Log in to the admin site """
    if request.method == 'POST':
        email = request.form['email']
        password_candidate = request.form['password']
        connection = sqlite3.connect('test.db')
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM users WHERE email = '"+email+"'")
        data = result.fetchall()[0]
        if result.arraysize > 0:
            password = data[2]
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('PASSWORD MATCHED')

                session['logged_in'] = True
                session['email'] = email

                flash('You are now logged in', 'success')
                cursor.close()
                return redirect('/para/')

            else:
                app.logger.info('PASSWORD NOT MATCHED')
                error = 'Incorrect Password'
                cursor.close()
                return render_template('login.html', error=error)
        else:
            app.logger.info('NO USER')
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/logout')
def logout():
    """ Log out from the site """
    if 'logged_in' in session:
        if session['logged_in']:
            session.clear()
            flash('You are now logged out ', 'success')
            return redirect(url_for('login'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/create_session')
def create_session():
    global session_ids

    # generate a random no not in session_ids
    curr_session_id = str(random.randint(100, 10000000))
    while curr_session_id in session_ids:
        curr_session_id = random.randint(100, 10000000)

    session_ids[curr_session_id] = list()

    return str(curr_session_id)


class Message:
    def __init__(self, from_, message):
        self.from_ = from_
        self.message_ = message

    def __repr__(self):
        return "{} :- {}".format(self.from_, self.message_)


api.add_resource(ChatBot, '/chat/')


if __name__ == '__main__':
    # load_all_model()
    app.run(host='127.0.0.1', port=5000, debug=True)
