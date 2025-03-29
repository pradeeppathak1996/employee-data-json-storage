from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

EVEN_FILE = "even_employees.json"
ODD_FILE = "odd_employees.json"

def load_data(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:  
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_data(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:  
        json.dump(data, file, indent=4)

@app.route('/add_employee', methods=['POST'])
def add_employee():
    data = request.json
    employees_even = load_data(EVEN_FILE)
    employees_odd = load_data(ODD_FILE)
    
    required_fields = ["Employee ID", "Name", "Email", "Department", "Designation", "Salary", "Date of Joining"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    data["Salary"] = float(data["Salary"])
    
    if int(data["Employee ID"]) % 2 == 0:
        employees_even.append(data)
        save_data(EVEN_FILE, employees_even)
    else:
        employees_odd.append(data)
        save_data(ODD_FILE, employees_odd)
    
    return jsonify({"message": "Employee added successfully"}), 201

# Perform CRUD -------------------------------------------------------------

@app.route('/employees', methods=['GET'])
def get_all_employees():
    employees_even = load_data(EVEN_FILE)
    employees_odd = load_data(ODD_FILE)

    all_employees = employees_even + employees_odd
    return jsonify(all_employees), 200

@app.route('/employee/<int:employee_id>', methods=['GET'])
def get_employee_by_id(employee_id):
    employees_even = load_data(EVEN_FILE)
    employees_odd = load_data(ODD_FILE)

    for emp in employees_even + employees_odd:
        if emp["Employee ID"] == employee_id:
            return jsonify(emp), 200
        
    return jsonify({"error": "Employee not found"}), 404

@app.route('/del_employee/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employees_even = load_data(EVEN_FILE)
    employees_odd = load_data(ODD_FILE)

    for emp in employees_even:
        if int(emp["Employee ID"]) == employee_id:
            employees_even.remove(emp)
            save_data(EVEN_FILE, employees_even)
            return jsonify({"message": "Employee deleted successfully"}), 200

    for emp in employees_odd:
        if int(emp["Employee ID"]) == employee_id:
            employees_odd.remove(emp)
            save_data(ODD_FILE, employees_odd)
            return jsonify({"message": "Employee deleted successfully"}), 200

    return jsonify({"error": "Employee not found"}), 404

@app.route('/update_employee/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    employees_even = load_data(EVEN_FILE)
    employees_odd = load_data(ODD_FILE)

    for emp in employees_even:
        if int(emp["Employee ID"]) == employee_id:
            emp.update(request.json)
            save_data(EVEN_FILE, employees_even)
            return jsonify({"message": "Employee updated successfully"}), 200

    for emp in employees_odd:
        if int(emp["Employee ID"]) == employee_id:
            emp.update(request.json)
            save_data(ODD_FILE, employees_odd)
            return jsonify({"message": "Employee updated successfully"}), 200

    return jsonify({"error": "Employee not found"}), 404

if __name__ == '__main__': 
    app.run(debug=True)