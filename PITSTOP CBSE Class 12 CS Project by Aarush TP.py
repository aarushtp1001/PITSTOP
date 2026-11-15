# PITSTOP - Automobile Dealership Management System
import mysql.connector as con

entered_password = input('Enter the password: ')
db = con.connect(host='localhost', password=entered_password, user='root')
cur = db.cursor()

# FUNCTIONS
def create_db():
    cur.execute('DROP DATABASE IF EXISTS Pitstop;')
    cur.execute('CREATE DATABASE Pitstop;')
    cur.execute('USE Pitstop;')
    cur.execute('''
    CREATE TABLE DealershipBranch (
        dealership_id INT PRIMARY KEY,
        location VARCHAR(20) UNIQUE,
        number_of_cars INT NOT NULL
    );''')
    cur.execute('''
    CREATE TABLE CarInfo (
        car_id INT PRIMARY KEY,
        dealership_id INT NOT NULL,
        make VARCHAR(15),
        model VARCHAR(30),
        car_name VARCHAR(50),
        year INT,
        number_of_km INT,
        horsepower INT,
        top_speed_kmh INT,
        price INT
    );''')
    cur.execute('''
    CREATE TABLE CustomerHistory (
        cust_id INT PRIMARY KEY,
        cust_name VARCHAR(30) NOT NULL,
        car_id INT NOT NULL,
        emp_id INT NOT NULL,
        dealership_id INT NOT NULL,
        date_of_buying DATE,
    );''')
    cur.execute('''
    CREATE TABLE EmployeeRecords (
        emp_id INT PRIMARY KEY,
        emp_name VARCHAR(30) NOT NULL,
        dealership_id INT NOT NULL,
        number_of_cars_sold INT
    );''')
    cur.execute('''
    CREATE TABLE ProfitEarned (
        profit_id INT PRIMARY KEY,
        car_id INT NOT NULL,
        cust_id INT,
        profit_earned INT
    );''')
    db.commit()

def add_dealership():
    print()
    print('First, add dealerships...')
    num = int(input('Enter the number of Pitstop dealerships in UAE: '))
    for i in range(num):
        print()
        dealership_id = int(input('Enter the dealership ID: '))
        location = input('Enter the location: ')
        cur.execute("""
        INSERT INTO DealershipBranch (dealership_id, location) VALUES (%s, %s);""", (dealership_id, location))
    db.commit()
    print()

def add_employees():
    print()
    print('Next, add employees...')
    num = int(input('Enter the number of employees to add: '))
    for i in range(num):
        print()
        emp_id = int(input('Enter the employee ID: '))
        emp_name = input('Enter the employee name: ')
        dealership_id = int(input('Enter the dealership ID: '))
        number_of_cars_sold = int(input(f'Enter the number of cars sold by {emp_name.split()[0]}: '))
        cur.execute("""
        INSERT INTO EmployeeRecords VALUES (%s, %s, %s, %s);""", (emp_id, emp_name, dealership_id, number_of_cars_sold))
    db.commit()
    print()

def add_cars():
    print()
    print('Next, add cars currently in the dealerships...')
    num = int(input('How many cars do you want to add? '))
    for i in range(num):
        print()
        car_id = int(input('Enter the car ID: '))
        dealership_id = int(input('Enter the dealership ID: '))
        make = input('Enter the make: ')
        model = input('Enter the model: ')
        car_name = make + ' ' + model
        year = int(input('Which year\'s model is the car? '))
        number_of_km = int(input('Enter the number of km travelled by the car: '))
        horsepower = int(input('Enter the horsepower of the car: '))
        top_speed_kmh = int(input('Enter the top speed of the car in kmh: '))
        price = int(input('Enter the price of the car in AED: '))
        cur.execute("""
        INSERT INTO CarInfo VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (car_id, dealership_id, make, model, car_name, year, number_of_km, horsepower, top_speed_kmh, price))
    db.commit()
    print()
    

create_db()



print("Welcome to PITSTOP's Database System! Please follow the initialization steps before proceeding to the functions...")
add_dealership()

print('1. Add cars.')
print()

cur.close()
db.close()
