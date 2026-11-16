# PITSTOP - Automobile Dealership Management System
import mysql.connector as con
import random

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
        cust_name VARCHAR(31) NOT NULL,
        car_id INT NOT NULL,
        emp_id INT NOT NULL,
        dealership_id INT NOT NULL,
        date_of_buying DATE
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
    num = int(input('Enter the number of Pitstop dealerships in UAE: '))
    for i in range(num):
        print()
        dealership_id = int(input('Enter the dealership ID: '))
        location = input('Enter the location: ')
        cur.execute("""
        INSERT INTO DealershipBranch VALUES (%s, %s, %s);""", (dealership_id, location, 0))
    db.commit()
    print()

def add_employees():
    print()
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
        cur.execute('UPDATE DealershipBranch SET number_of_cars = number_of_cars + 1 WHERE dealership_id = %s;', (dealership_id,))
    db.commit()
    print()

create_db()

print("Welcome to PITSTOP's Database System! Please follow the initialization steps before proceeding to the functions...")
add_dealership()
add_employees()
add_cars()
print('You may now choose your functions: ')

print('MENU:')
print('1.  Add new cars.')
print('2.  Buy new car.')
print('3.  Delete car by name.')
print('4.  Update car specifications.')
print('5.  Update customer history information.')
print('6.  Display all cars bought by a specific customer.')
print('7.  Display all cars meeting the specified budget.')
print('8.  Display all cars in a specified dealership location.')
print('9.  Display employees from each dealership with highest number of cars sold.')
print('10. Display the most profitable car in each dealership.')
print('11. Exit.')
print()

while True:
    ch = int(input('Enter your choice: '))
    print()
    if ch == 1:
        add_cars()
    elif ch == 2:
        print()
        car_name = input('Enter the name of the car you want to buy: ')
        print()
        car_name = car_name.title()
        cur.execute('SELECT car_id, dealership_id FROM CarInfo WHERE car_name = %s;', (car_name,))
        data = cur.fetchall()
        if not data:
            print(f'{car_name} is not available at any branch of Pitstop. We are sorry for the inconvenience.')
        else:
            # car_name is there in the garage
            car_id = data[0][0]
            dealership_id = data[0][1]
            cur.execute('SELECT MAX(cust_id) FROM CustomerHistory;')
            data = cur.fetchone()
            if data[0] is None: cust_id = 1
            else:
                cust_id = data[0] + 1
            cust_name = input('Enter your name: ')
            cust_name = cust_name[:31]
            cur.execute('SELECT emp_id FROM EmployeeRecords WHERE dealership_id = %s;', (dealership_id,))
            emp_records = cur.fetchall()
            if not emp_records:
                print('No employees are available at this dealership.')
                continue
            random_number_1 = random.randint(0, len(emp_records)-1)
            emp_id = emp_records[random_number_1][0]
            date_of_buying = input('Enter today\'s date in YYYY-MM-DD: ')
            cur.execute('INSERT INTO CustomerHistory VALUES (%s, %s, %s, %s, %s, %s);',
            (cust_id, cust_name, car_id, emp_id, dealership_id, date_of_buying))
            cur.execute('SELECT MAX(profit_id) FROM ProfitEarned;')
            data = cur.fetchone()
            if data[0] is None: profit_id = 1
            else:
                profit_id = data[0] + 1
            cur.execute('SELECT price FROM CarInfo WHERE car_id = %s;', (car_id,))
            price = cur.fetchone()[0]
            profit_earned = round(price * 0.15) # assuming profit earned on each car is 15% of the price of the car
            cur.execute('INSERT INTO ProfitEarned VALUES (%s, %s, %s, %s);', (profit_id, car_id, cust_id, profit_earned))
            cur.execute('DELETE FROM CarInfo WHERE car_id = %s;', (car_id,))
            cur.execute('UPDATE DealershipBranch SET number_of_cars = number_of_cars - 1 WHERE dealership_id = %s;',
            (dealership_id,))
            cur.execute('UPDATE EmployeeRecords SET number_of_cars_sold = number_of_cars_sold + 1 WHERE emp_id = %s;', (emp_id,))
            db.commit()
    elif ch == 3:
        print()
        car_name = input('Enter the name of the car you want to delete: ')
        car_name = car_name.title()
        cur.execute('SELECT car_id FROM CarInfo WHERE car_name = %s;', (car_name,))
        data = cur.fetchall()
        if not data: print(f'{car_name} was not found in Pitstop\'s garage.')
        else:
            print()
            dealer = input('Enter the dealership location: ')
            dealer = dealer.title()
            cur.execute('SELECT location, dealership_id FROM DealershipBranch WHERE location = %s', (dealer,))
            data = cur.fetchone()
            if not data: print(f'{dealer} is not a branch under Pitstop.')
            else:
                dealership_id = data[1]
                cur.execute('SELECT car_id FROM CarInfo WHERE car_name = %s AND dealership_id = %s;', (car_name, dealership_id))
                data = cur.fetchall()
                if not data:
                    print(f'{car_name} was not found at the {dealer} branch.')
                else:
                    car_id = data[0][0]
                    cur.execute('DELETE FROM CarInfo WHERE car_id = %s;', (car_id, ))
                    cur.execute('UPDATE DealershipBranch SET number_of_cars = number_of_cars - 1 WHERE dealership_id = %s', (dealership_id,))
                    db.commit()

    elif ch == 4:
        pass
    elif ch == 5:
        pass
    elif ch == 6:
        pass
    elif ch == 7:
        pass
    elif ch == 8:
        pass
    elif ch == 9:
        pass
    elif ch == 10:
        pass
    elif ch == 11:
        print()
        print('Thank you for choosing PITSTOP! We hope to see you soon.')
        print('Exiting...')
        break
    else:
        print()
        print('Invalid choice, please try again...')
        print()

cur.close()
db.close()
