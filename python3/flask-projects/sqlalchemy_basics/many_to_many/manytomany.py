import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, __file__)
db = SQLAlchemy(app)

stu_subs = db.Table('stu_subs', db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
                    db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id')))


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    subj = db.relationship('Subjects', secondary=stu_subs, backref=db.backref('student', lazy='dynamic'))

    def __init__(self, name):
        self.name = name


class Subjects(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self, name):
        self.name = name


if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    stu1 = Student('Jay')
    stu2 = Student('Kay')
    stu3 = Student('El')
    stu4 = Student('Em')
    stu5 = Student('Qu')

    sub1 = Subjects('Physics')
    sub2 = Subjects('Chemistry')
    sub3 = Subjects('Maths')
    sub4 = Subjects('Computers')
    sub5 = Subjects('Biology')

    stu1.subj.extend([sub1, sub2, sub5])
    stu2.subj.extend([sub1, sub3, sub4])
    stu3.subj.extend([sub2, sub4])
    stu4.subj.extend([sub2, sub3])
    stu5.subj.extend([sub1, sub3, sub5])

    db.session.add_all([stu1, stu2, stu3, stu4, stu5, sub1, sub2, sub3, sub4, sub5])
    db.session.commit()

    phy = Subjects.query.filter_by(name='Physics').first()
    print('Students with Physics')
    for i in phy.student:
        print(i.name, end=',')

    math = Subjects.query.filter_by(name='Maths').first()
    print('\nStudents with Maths')
    for i in math.student:
        print(i.name, end=',')

    jay = Student.query.filter_by(name='Jay').first()
    print("\nJay's Subjects")
    for i in jay.subj:
        print(i.name)
