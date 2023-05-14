# app.py

from flask import Flask, render_template, request, session, redirect, flash
import pymysql


app = Flask(__name__)
app.secret_key = 'software_service_secret_key_cdac'


conn = pymysql.connect(host='localhost', user='root', password='root', db='samp')
cursor = conn.cursor()


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']


        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))

        user = cursor.fetchone()

        if user:

            session['user_id'] = user[0]

            flash('Login successful! Welcome, {}'.format(user[1]), 'success')
            return redirect('/dashboard')

        else:
            flash('Invalid credentials', 'error')
            return render_template('login.html')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        return render_template('dashboard.html', user_id=user_id)
    else:
        return redirect('/login')



@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        cursor.execute("INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
        conn.commit()

        return redirect('/thankyou')

    return render_template('contact.html')


@app.route('/profile')
def profile():
    if 'user_id' in session:
        user_id = session['user_id']

        cursor.execute("SELECT name, email FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()

        if user:
            name = user[0]
            email = user[1]

            return render_template('profile.html', name=name, email=email)

    return redirect('/login')


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


@app.route('/service')
def services():
    return render_template('service.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/projects')
def project():
    if 'user_id' in session:
        return render_template('projects.html')
    else:
        return 'Unauthorized', 401


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
