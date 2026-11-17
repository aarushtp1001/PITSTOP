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
        make VARCHAR(30),
        model VARCHAR(30),
        car_name VARCHAR(60),
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
        location = location.title()
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
        emp_name = emp_name.title()
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
        make = make.title()
        model = input('Enter the model: ')
        model = model.title()
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
print('You may now choose your functions.')
print()

print('MENU:')
print('1.  Add new cars.')
print('2.  Buy new car.')
print('3.  Delete car by name.')
print('4.  Update car specifications.')
print('5.  Display all cars meeting the specified budget.')
print('6.  Display all cars in a specified dealership location.')
print('7.  Display employees from each dealership with highest number of cars sold.')
print('8. Exit.')
print()

while True:
    ch = int(input('Enter your choice: '))
    print()

    if ch == 1: add_cars()

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
                if not data: print(f'{car_name} was not found at the {dealer} branch.')
                else:
                    car_id = data[0][0]
                    cur.execute('DELETE FROM CarInfo WHERE car_id = %s;', (car_id, ))
                    cur.execute('UPDATE DealershipBranch SET number_of_cars = number_of_cars - 1 WHERE dealership_id = %s', (dealership_id,))
                    db.commit()

    elif ch == 4:
        print()
        print('Please note that only specifications like make, model, car_name, horsepower, and top_speed_kmh can be changed.')
        car_name = input('Enter the name of the car whose specifications you want to update:')
        car_name = car_name.title()
        cur.execute('SELECT car_id FROM CarInfo WHERE car_name = %s;', (car_name,))
        data = cur.fetchone()
        if not data: print(f'{car_name} is not in Pitstop\'s garage.')
        else:
            car_id = data[0]
            cur.execute('SELECT make, model, car_name, horsepower, top_speed_kmh FROM CarInfo WHERE car_id = %s;', (car_id,))
            data = cur.fetchall()
            print('Enter data in respective fields if required, else just press Enter...')
            print()
            make = input('Enter the new make: ')
            if not make: make = data[0][0]
            model = input('Enter the new model: ')
            if not model: model = data[0][1]
            car_name = make + ' ' + model
            horsepower = input('Enter the new horsepower: ')
            if not horsepower: horsepower = data[0][3]
            else: horsepower = int(horsepower)
            top_speed_kmh = input('Enter the new top speed in kmh: ')
            if not top_speed_kmh: top_speed_kmh = data[0][4]
            else: top_speed_kmh = int(top_speed_kmh)
            cur.execute('UPDATE CarInfo SET make = %s, model = %s, car_name = %s, horsepower = %s, top_speed_kmh = %s WHERE car_id = %s;',
            (make, model, car_name, horsepower, top_speed_kmh, car_id))
            db.commit()

    elif ch == 5:
        print()
        budget = int(input('Enter your budget in AED: '))
        cur.execute('SELECT * FROM CarInfo WHERE price <= %s ORDER BY car_name DESC;', (budget,))
        data = cur.fetchall()
        if not data:
            print('No cars met the specified budget. Sorry for the inconvenience.')
        else:
            print()
            print('The cars meeting the specified budget are:')
            for car in data: print(car)

    elif ch == 6:
        print()
        loc = input('Enter location of dealership: ')
        loc = loc.title()
        cur.execute('SELECT dealership_id FROM DealershipBranch WHERE location = %s;', (loc,))
        data = cur.fetchone()
        if not data:
            print(f'Pitstop does not have a branch at the location: {loc}')
        else:
            dealership_id = data[0]
            cur.execute('SELECT * FROM CarInfo WHERE dealership_id = %s;', (dealership_id,))
            print('The cars in the specified location are: ')
            for car in cur.fetchall(): print(car)

    elif ch == 7:
        print()
        cur.execute('''
        SELECT dealership_id, MAX(number_of_cars_sold)
        FROM EmployeeRecords
        GROUP BY dealership_id
        ORDER BY dealership_id;''')
        data = cur.fetchall()
        print('The employees with the most number of cars sold in their respective dealerships are: ')
        for employee in data:
            cur.execute('SELECT emp_id, emp_name, dealership_id, number_of_cars_sold FROM EmployeeRecords WHERE dealership_id = %s AND number_of_cars_sold = %s;', (employee[0], employee[1]))
            for record in cur.fetchall(): print(record)

    elif ch == 8:
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
