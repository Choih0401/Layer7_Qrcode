from flask import Flask, render_template, json, request,redirect,session, send_from_directory
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import datetime
import os

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ch04010508'
app.config['MYSQL_DATABASE_DB'] = 'userlist'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'../static/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showSignin')
def showSignin():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('signin.html')

@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']



        # connect to mysql

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()




        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')


    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/score')
def score():
    try:
        _uid = session.get('user')

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_score',(_uid,))
        data = cursor.fetchall()

        con.commit()
        cursor.close()
        con.close()
        return render_template('score.html', score = str(data[0]).split(',')[0].split('(')[1])


    except Exception as e:
        return render_template('error.html',error = str(e))

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                cursor.close()
                conn.close()
                return render_template('error.html', error = 'Success')
            else:
                cursor.close()
                conn.close()
                return render_template('error.html', error = str(data[0]).split('\'')[1].split('\'')[0])

        else:
            cursor.close()
            conn.close()
            return render_template('error.html', error = 'Required Fileds')

    except Exception as e:
        return render_template('error.html', error = str(e))



@app.route('/answerSubmit',methods=['POST','GET'])
def answerSubmit():
    try:
        now = datetime.datetime.now()
        _uid = session.get('user')
        _flag = request.form['inputFlag']
        _time = now.strftime('%Y-%m-%d %H:%M:%S')

        # connect to mysql

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_result',(_uid,_time,_flag))
        data = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        conn2 = mysql.connect()
        cursor2 = conn2.cursor()
        cursor2.callproc('sp_submit',(_uid,_flag))
        data2 = cursor2.fetchall()
        conn2.commit()
        cursor2.close()
        conn2.close()
        return render_template('result.html', error = str(data2[0]).split('\'')[1].split('\'')[0])

    except Exception as e:
        return render_template('result.html', error = str(e))


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=7777, threaded=True)
