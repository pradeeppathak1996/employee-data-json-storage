import csv
import threading
import requests

CSV_FILE = "employee_data.csv"
SERVER_URL = "http://127.0.0.1:5000/add_employee"

def process_even_rows():
    with open(CSV_FILE, mode='r', encoding='utf-8') as file:
        reader = list(csv.DictReader(file))  
        for index, row in enumerate(reader):
            if index % 2 == 0:  
                row["Salary"] = float(row["Salary"])  
                row["Employee ID"] = int(row["Employee ID"])  
                response = requests.post(SERVER_URL, json=row)
                print(f"Thread-1 (Even): {response.json()}")

def process_odd_rows():
    with open(CSV_FILE, mode='r', encoding='utf-8') as file:
        reader = list(csv.DictReader(file))
        for index, row in enumerate(reader):
            if index % 2 != 0: 
                row["Salary"] = float(row["Salary"])
                row["Employee ID"] = int(row["Employee ID"])
                response = requests.post(SERVER_URL, json=row)
                print(f"Thread-2 (Odd): {response.json()}")

def main():
    thread1 = threading.Thread(target=process_even_rows)
    thread2 = threading.Thread(target=process_odd_rows)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()
