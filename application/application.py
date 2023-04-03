from flask import Flask, render_template, request, flash, redirect, url_for
from flaskext.mysql import MySQL
import pymysql

app = Flask(__name__)
mysql = MySQL()
app.secret_key = "Hello-world"


app.config['MYSQL_DATABASE_USER'] = 'varijsaini'
app.config['MYSQL_DATABASE_PASSWORD'] = '#password'
app.config['MYSQL_DATABASE_DB'] = 'varijsaini$2023'
app.config['MYSQL_DATABASE_HOST'] = 'varijsaini.mysql.pythonanywhere-services.com'
mysql.init_app(app)

@app.route('/')
def index():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute('select * from rooms')
    result = cur.fetchall()
    cur.close()
    return render_template('index.html', data = result)

@app.route('/customers')
def index_c():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute('select * from customer')
    result = cur.fetchall()
    cur.close()
    return render_template('index_c.html', data = result)

@app.route('/bookings')
def index_b():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('select * from books')
    result = cur.fetchall()
    conn.close()
    return render_template('index_b.html', data=result)

@app.route('/employees')
def index_e():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('select * from employees')
    result = cur.fetchall()
    conn.close()
    return render_template('index_e.html', data=result)


@app.route('/add_customer', methods=['GET', 'POST'])
def add_cust():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    try:
        if request.method=='POST':
            data = request.form
            firstname  = data['firstname']
            lastname = data['lastname']
            address = data['address']
            cardinfo = data['cardinfo']
            phone = data['phone']
            cur.execute("insert into customer (firstname, lastname, address, cardinfo, phone) values (%s, %s, %s, %s, %s)",
            (firstname, lastname, address, cardinfo, phone))
            conn.commit()
            flash('Customer added successfully!')
    except pymysql.Error as e:
            conn.rollback()
            if e.args[0] == 1062:
                flash ("Invalid Customer id: Customer ID already exists!")
            return redirect(url_for('index_c'))
    return redirect(url_for('index_c'))

@app.route('/add_booking', methods=['GET', 'POST'])
def add_booking():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    try:
        if request.method=='POST':
            data = request.form
            check_in = data['check_in']
            check_out = data['check_out']
            cust_id = data['cust_id']
            room_id = data['room_id']
            cur.execute("insert into books (check_in, check_out, cust_id, room_id) values (%s, %s, %s, %s)",
            (check_in, check_out, cust_id, room_id))
            conn.commit()
            flash('Booking added successfully!')
    except pymysql.Error as e:
            conn.rollback()
            if e.args[0] == 1062:
                flash ("Invalid booking id: Booking ID already exists!")
            return redirect(url_for('index_b'))
    return redirect(url_for('index_b'))

@app.route('/add_rooms', methods=['POST'])
def add_rooms():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    try:
        if request.method=='POST':
            data = request.form
            floor = data['floor']
            room_type = data['type']
            price = data['price']
            cur.execute("insert into rooms (floor, type, price) values (%s, %s, %s)", (floor, room_type, price))
            conn.commit()
            flash('Room added successfully!')
    except pymysql.Error as e:
            conn.rollback()
            if e.args[0] == 1062:
                flash ("Invalid room id: Room ID already exists!")
            return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    try:
        if request.method=='POST':
            data = request.form
            name = data['name']
            salary = data['salary']
            cur.execute("insert into employees (name, salary) values (%s, %s)",
            (name, salary))
            conn.commit()
            flash('Employee added successfully!')
    except pymysql.Error as e:
            conn.rollback()
            if e.args[0] == 1062:
                return "Invalid employee id: Employee ID already exists!"
            return f"Error: {e}"
    return redirect(url_for('index_e'))

@app.route('/edit/<room_id>', methods = ['POST','GET'])
def edit_room(room_id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute('select * from rooms where room_id = %s', (room_id))
    result = cur.fetchall()
    cur.close()

    return render_template('editroom.html', rooms = result[0])

@app.route('/edit_employee/<employ_id>', methods = ['POST','GET'])
def edit_employee(employ_id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute('select * from employees where employ_id = %s', (employ_id))
    result = cur.fetchall()
    cur.close()

    return render_template('editemp.html', employee = result[0])

@app.route('/edit_cust/<cust_id>', methods = ['POST','GET'])
def edit_cust(cust_id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute('select * from customer where cust_id = %s', (cust_id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('editcust.html', customer = data[0])

@app.route('/edit_booking/<book_id>', methods = ['POST','GET'])
def edit_booking(book_id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute('select * from books where book_id = %s', (book_id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('editbooking.html', books = data[0])

@app.route('/update/<room_id>', methods= ['POST'])
def update_room(room_id):
    if request.method == 'POST':
        data = request.form
        floor = data['floor']
        room_type = data['type']
        price = data['price']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            update rooms
            set floor = %s,
                type = %s,
                price = %s
            where room_id = %s
        """, (floor, room_type, price, room_id))
        flash('Room Updated Successfully!')
        conn.commit()
        return redirect(url_for('index'))

@app.route('/update_employee/<employ_id>', methods= ['POST'])
def update_employee(employ_id):
    if request.method == 'POST':
        data = request.form
        name = data['name']
        salary = data['salary']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            update employees
            set name = %s,
                salary = %s
            where employ_id = %s
        """, (name, salary, employ_id))
        flash('Employee Updated Successfully!')
        conn.commit()
        return redirect(url_for('index_e'))

@app.route('/update_cust/<cust_id>', methods= ['POST'])
def update_cust(cust_id):
    if request.method == 'POST':
        data = request.form
        firstname = data['firstname']
        lastname = data['lastname']
        address = data['address']
        cardinfo = data['cardinfo']
        phone = data['phone']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            update customer
            set firstname = %s,
                lastname = %s,
                address = %s,
                cardinfo = %s,
                phone = %s
            where cust_id = %s
        """, (firstname, lastname, address, cardinfo, phone, cust_id))
        flash('Customer Updated Successfully!')
        conn.commit()
        return redirect(url_for('index_c'))

@app.route('/update_booking/<book_id>', methods= ['POST'])
def update_booking(book_id):
    if request.method == 'POST':
        data = request.form
        check_in = data['check_in']
        check_out = data['check_out']
        cust_id = data['cust_id']
        room_id = data['room_id']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            update books
            set check_in = %s,
                check_out = %s,
                cust_id = %s,
                room_id = %s
            where book_id = %s
        """, (check_in, check_out, cust_id, room_id, book_id))
        flash('Booking Updated Successfully!')
        conn.commit()
        return redirect(url_for('index_b'))

@app.route('/delete/<room_id>', methods = ['POST', 'GET'])
def delete_room(room_id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cur.execute(f'delete from rooms where room_id = {room_id}')
        conn.commit()
        flash('Room Removed')
    except pymysql.Error as e:
            conn.rollback()
            if e.args[0] == 1451:
                flash('A booking exists for this room, cannot delete!')
            return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/delete_cust/<cust_id>', methods = ['POST', 'GET'])
def delete_cust(cust_id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(f'delete from customer where cust_id = {cust_id}')
    conn.commit()
    flash('Customer Removed')
    return redirect(url_for('index_c'))

@app.route('/delete_booking/<book_id>', methods = ['POST', 'GET'])
def delete_booking(book_id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(f'delete from books where book_id = {book_id}')
    conn.commit()
    flash('Booking Removed')
    return redirect(url_for('index_b'))

@app.route('/delete_employee/<employ_id>', methods = ['POST', 'GET'])
def delete_employee(employ_id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(f'delete from employees where employ_id = {employ_id}')
    conn.commit()
    flash('Employee Removed')
    return redirect(url_for('index_e'))


