from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

# Connect to MongoDB Atlas
client = MongoClient('mongodb+srv://niraj:nd27@gems.h1udfuz.mongodb.net/')
db = client['employee_database']
employee_collection = db['employee_collection']

# Define the routes
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = employee_collection.find()
    return jsonify([{'Emp Code': emp['Emp Code'],
                     'Employee Name': emp['Employee Name'],
                     'Employee Email': emp['Employee Email'],
                     'Batch': emp['Batch'],
                     'Project Name': emp['Project Name'],
                     'Lead Name': emp['Lead Name'],
                     'PM Name': emp['PM Name']}
                    for emp in employees])

@app.route('/employees', methods=['POST'])
def create_employee():
    employee = {
        'Emp Code': request.json['Emp Code'],
        'Employee Name': request.json['Employee Name'],
        'Employee Email': request.json['Employee Email'],
        'Batch': request.json['Batch'],
        'Project Name': request.json['Project Name'],
        'Lead Name': request.json['Lead Name'],
        'PM Name': request.json['PM Name']
    }
    employee_collection.insert_one(employee)
    return jsonify({'message': 'Employee created successfully'})

@app.route('/employees/<emp_code>', methods=['PUT'])
def update_employee(emp_code):
    employee = employee_collection.find_one({'Emp Code': int(emp_code)})
    if employee:
        employee_collection.update_one(
            {'Emp Code': int(emp_code)},
            {'$set': {
                'Employee Name': request.json['Employee Name'],
                'Employee Email': request.json['Employee Email'],
                'Batch': request.json['Batch'],
                'Project Name': request.json['Project Name'],
                'Lead Name': request.json['Lead Name'],
                'PM Name': request.json['PM Name']
            }})
        return jsonify({'message': 'Employee updated successfully'})
    else:
        return jsonify({'error': 'Employee not found'})

@app.route('/employees/<emp_code>', methods=['DELETE'])
def delete_employee(emp_code):
    employee = employee_collection.find_one({'Emp Code': int(emp_code)})
    if employee:
        employee_collection.delete_one({'Emp Code': int(emp_code)})
        return jsonify({'message': 'Employee deleted successfully'})
    else:
        return jsonify({'error': 'Employee not found'})

if __name__ == '__main__':
    app.run(debug=True)
