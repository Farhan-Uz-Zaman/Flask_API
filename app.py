from flask import Flask, request, jsonify
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
db = SQLAlchemy(app)

#classes for the database that will hold the data

#The Table Parents to hold data of the parents
class Parents(db.Model):
    __tablename__ = "Parents"
    ssn = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    street = db.Column(db.String(50),nullable=False)
    city = db.Column(db.String(50),nullable=False)
    state = db.Column(db.String(50),nullable=False)
    zip_code = db.Column(db.Integer,nullable=False)
    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

#The Table Student to hold data of the student
class Student(db.Model):
    __tablename__ = "Student"
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    parent = db.Column(db.String(50),nullable=False)
    street = db.Column(db.String(50),nullable=False)
    city = db.Column(db.String(50),nullable=False)
    state = db.Column(db.String(50),nullable=False)
    zip_code = db.Column(db.Integer,nullable=False)
    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

#the home page    
@app.route('/')
def index():
        return "Hello! To The Flask API"

# This page displays all the users, both students and parents
@app.route('/users')  
def get_user():
    
    #Getting all students from the Student table
    students = Student.query.all()
    
    #Getting all parents from the Parents table
    parents = Parents.query.all()
    
    output = []
    #looping through the parents to get all the parents into the output array
    for student in students:
        student_data = {'First Name' : student.first_name,'Last Name' : student.last_name,"Street": student.street,"City" : student.city,"State" : student.state, "Zip Code" : student.zip_code}
        output.append(student_data)
     
        #looping through the students to get all the studnets into the output array
    for parent in parents:
        parent_data = {'First Name' : parent.first_name,'Last Name' : parent.last_name,"Street": parent.street,"City" : parent.city,"State" : parent.state, "Zip Code" : parent.zip_code}
        output.append(parent_data)
        
    return {"Users": output}
    
@app.route('/user',methods=['POST'])
def add_user():
    
    req = request.get_json(['token'])
    
    #getting token to verify what to add
    token = req.get('token')
    
    #token will have to be provided by the frontend based on what the user chooses
    #verifying whether to add a student or a parent from the token
    #Adding parent if token says parent
    if token == "Parent":
        parent = Parents(ssn = req.get('ssn'), first_name = req.get('first_name'), last_name = req.get('last_name'),street = req.get('street'),city=req.get('city'), state = req.get('state'), zip_code = req.get('zip_code') )
        db.session.add(parent)
        db.session.commit()
        return "Added Parent"
    
    #adding student if token says student
    if token == "Student":
        student = Student(id = req.get('id'), first_name = req.get('first_name'), last_name = req.get('last_name'),parent=req.get('parent'),street =  req.get('street'),city=req.get('city'), state = req.get('state'), zip_code = req.get('zip_code') )
        db.session.add(student)
        db.session.commit()
        return "Added Student"
    
@app.route('/student/<id>',methods=['DELETE'])  
def deleteStudent(id):
    #Deleting a student having the particular id
    student = Student.query.get(id)
    if student is None:
        return "No such student exists"
    db.session.delete(student)
    db.session.commit()
    return "Student Deleted!"
    
@app.route('/parent/<ssn>',methods=['DELETE'])  
def deleteParent(ssn):
    #Deleting parent having that ssn
    parent = Parents.query.get(ssn)
    if parent is None:
        return "No such parent exists"
    db.session.delete(parent)
    db.session.commit()  
    return "Parent Deleted!"    

@app.route('/update/<ssn>', methods=['POST'])
def updateParent(ssn):
    req = request.get_json(['token'])
    
    #getting token to see what to update
    token = req.get('token')
    
    #checking what to update
    if token == "Parent":
    #updating parent
        parent = Parents.query.filter_by(ssn=ssn).first()
        parent.ssn = req.get('ssn')
        parent.first_name = req.get('first_name')
        parent.last_name = req.get('last_name')
        parent.street = req.get('street')
        parent.city=req.get('city')
        parent.state = req.get('state')
        parent.zip_code = req.get('zip_code')
        db.session.commit()
        return "Parent Updated"
        
    if token == "Student":
        student = Student.query.filter_by(id=ssn).first()
        student.ssn = req.get('id')
        student.first_name = req.get('first_name')
        student.last_name = req.get('last_name')
        student.parent=req.get('parent')
        student.street = req.get('street')
        student.city=req.get('city')
        student.state = req.get('state')
        student.zip_code = req.get('zip_code')
        db.session.commit()
        return "Student Updated"
    
if __name__ == "__main__":
    app.run(debug=True)
