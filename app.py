from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
db = SQLAlchemy(app)
# Create the database tables

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(10), nullable=False)
    contact = db.Column(db.String(100), nullable=False)


@app.route('/')
def index():
    db.create_all()
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register_student():
    name = request.form['name']
    age = request.form['age']
    grade = request.form['grade']
    contact = request.form['contact']

    student = Student(name=name, age=age, grade=grade, contact=contact)
    

    db.session.add(student)
    db.session.commit()
    # flash('Registration successful')
    return redirect(url_for('index'))


@app.route('/retrieve')
def retrieve_student():
    students = Student.query.all()
    return render_template('retrieve.html', students=students)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get(id)

    if request.method == 'POST':
        student.name = request.form['name']
        student.age = request.form['age']
        student.grade = request.form['grade']
        student.contact = request.form['contact']

        db.session.commit()
        
        return redirect(url_for('retrieve_student'))

    return render_template('update.html', student=student)


@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get(id)

    db.session.delete(student)
    db.session.commit()

    return redirect(url_for('retrieve_student'))


@app.route('/search', methods=['GET', 'POST'])
def search_students():
    if request.method == 'POST':
        criteria = request.form['criteria']
        value = request.form['value']

        students = Student.query.filter(getattr(Student, criteria) == value).all()

        return render_template('search.html', students=students)

    return render_template('search.html')


@app.route('/report')
def generate_report():
    students = Student.query.all()
    return render_template('report.html', students=students)


if __name__ == '__main__':
    app.run(debug=True)
