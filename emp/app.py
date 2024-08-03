from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from waitress import serve
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    position = db.Column(db.String(100), nullable=False)

@app.route('/api/employees', methods=['POST'])
@jwt_required()
def add_employee():
    data = request.get_json()
    new_employee = Employee(name=data['name'], email=data['email'], position=data['position'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Employee added successfully'}), 201

@app.route('/api/employees', methods=['GET'])
@jwt_required()
def get_employees():
    employees = Employee.query.all()
    return jsonify([{'name': emp.name, 'email': emp.email, 'position': emp.position} for emp in employees])

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    # Here you would normally verify the username and password
    access_token = create_access_token(identity=data['username'])
    return jsonify(access_token=access_token)

@app.route('/')
def serve_index():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
