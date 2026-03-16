from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="172.31.12.82",
    user="flaskuser",
    password="flask123",
    database="studentdb"
)

cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    course = request.form['course']

    sql = "INSERT INTO students (name,email,course) VALUES (%s,%s,%s)"
    val = (name,email,course)

    cursor.execute(sql,val)
    db.commit()

    return redirect('/students')


@app.route('/students')
def students():
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    return render_template('students.html',students=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
