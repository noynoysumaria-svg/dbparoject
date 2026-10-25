
# Import necessary modules from Flask framework for web routing, rendering templates, and managing sessions
from flask import Flask, redirect, render_template, request, session, url_for

# Import the custom function from db.py to connect to the MySQL database
from db import connect_db

# Initialize the Flask application instance
app = Flask(__name__)
# makita ang name sang website

# Secret key used for securely signing session cookies (keeps user login state safe)
app.secret_key = 'super_secret_xadmin_key_2026'
# to protect the app flask and secure the admin log in safety


# LOGIN ROUTE
@app.route('/login', methods=['GET', 'POST'])
# GET is gina kwa ya ang log in form para mapa kita
# POST gina check ya kong sakto ang user name nga naka butang sa db
def login():
    # Check if the user is already logged in
    if 'admin_logged_in' in session:
        return redirect(url_for('index'))
    # gina check if ang admin naka log in tapos sa index na sa ma kadto ang sa front end

    error = None

    if request.method == 'POST':
        # Retrieve form data submitted from the login HTML input fields
        username = request.form['username']
        password = request.form['password']
        # Ga kwa danay sang user name kg password sa html form

        # Open connection to the MySQL database
        conn = connect_db()
        # Para maka connect sa database

        # Create a cursor that returns query results as Python dictionaries
        cursor = conn.cursor(dictionary=True)# cursor command para maka execute sa data base
        # Para makuha ang data sa database gamit ang column names

        # Execute SQL query to check if admin credentials match database records
        cursor.execute(
            "SELECT * FROM admin WHERE username = %s AND password = %s",
            (username, password)
        )
        # Gina check ya sa database kong sakto ang username kag password

        # Fetch matching admin row from database
        admin = cursor.fetchone()
        # Gina kwa ya ang matching record sa database kung may ara

        # Close database cursor and connection
        cursor.close()
        conn.close()
        # Para ma close ang connection sa database

        if admin:
            # Set session variables to keep user logged in
            session['admin_logged_in'] = True
            session['admin_username'] = admin['username']
            # Para ma remember sang system nga naka log in ang admin

            # Redirect to main dashboard page
            return redirect(url_for('index'))
            # Kong sakto ang login, ma kadto na sa dashboard
        else:
            # Show error message if credentials do not match
            error = "Invalid Username or Password!"
            # Kong sala ang username or password, may error message nga makita

    # Render login HTML template
    return render_template("login.html", error=error)
    # Para makita ang login page kag ang error message


# LOGOUT ROUTE
@app.route('/logout')
# Para maka logout ang admin
def logout():
    # Clear all session data
    session.clear()
    # Gina kwa ya ang session data para ma logout ang admin

    # Redirect user back to login page
    return redirect(url_for('login'))
    # Pagkatapos mag logout, balik sa login page


# READ: DASHBOARD ROUTE
@app.route('/')
# Para makita ang tanan nga student records sa dashboard
def index():
    # Security check if the admin is logged in
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    # Kong wala naka log in, ibalik sa login page

    # Connect to MySQL database
    conn = connect_db()
    # Para maka connect sa database

    cursor = conn.cursor(dictionary=True)
    # Para makuha ang data gamit ang column names

    # Query all student records ordered by newest ID first
    cursor.execute("SELECT * FROM students ORDER BY id DESC")
    # Gina kwa ya tanan nga student records kag ang pinaka bag-o una

    # Fetch all records from database
    students = cursor.fetchall()
    # Gina kwa ya tanan nga student data kag ginabutang sa students variable

    # Count total student records
    total_students = len(students)
    # Gina count ya kong pila tanan ka students

    # Close database cursor and connection
    cursor.close()
    conn.close()
    # Para ma close ang connection sa database

    # Render index.html and pass student data to HTML
    return render_template(
        "index.html",
        students=students,
        total_students=total_students
    )
    # Para makita ang dashboard kag ang student records sa front end


# CREATE: ADD STUDENT ROUTE
@app.route('/add', methods=['GET', 'POST'])
# Para makadugang sang bag-o nga student
def add_student():
    # Check if the admin is logged in
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    # Kong wala naka log in, ibalik sa login page

    if request.method == 'POST':
        # Retrieve all input values from the HTML form
        student_id = request.form['student_id']
        fullname = request.form['fullname']
        age = request.form['age']
        gender = request.form['gender']
        course = request.form['course']
        year_level = request.form['year_level']
        address = request.form['address']
        contact = request.form['contact']
        # Gina kwa ya ang tanan nga information sang student sa html form

        # Connect to MySQL database
        conn = connect_db()
        # Para maka connect sa database

        cursor = conn.cursor()
        # Para makapadala sang SQL command sa database

        # Execute SQL INSERT query to save new student record
        cursor.execute("""
            INSERT INTO students
            (student_id, fullname, age, gender, course, year_level, address, contact) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            student_id, fullname, age, gender,
            course, year_level, address, contact
        ))
        # Gina insert ya ang bag-o nga student information sa database
        #s place holder

        # Save changes permanently to database
        conn.commit()
        # Para ma save ang bag-o nga record

        # Close database cursor and connection
        cursor.close()
        conn.close()
        # Para ma close ang connection sa database

        # Redirect back to main dashboard
        return redirect(url_for('index'))
        # Pagkatapos mag add, balik sa dashboard

    # Render add_student.html template
    return render_template("add_student.html")
    # Para makita ang add student form


# UPDATE: EDIT STUDENT ROUTE
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
# Para ma edit ang existing student information
def edit_student(id):
    # Check if the admin is logged in
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    # Kong wala naka log in, ibalik sa login page

    # Connect to MySQL database
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    # Para makuha kag ma update ang student record

    if request.method == 'POST':
        # Retrieve modified input values from HTML form
        student_id = request.form['student_id']
        fullname = request.form['fullname']
        age = request.form['age']
        gender = request.form['gender']
        course = request.form['course']
        year_level = request.form['year_level']
        address = request.form['address']
        contact = request.form['contact']
        # Gina kwa ya ang bag-o nga information sa edit form

        # Execute SQL UPDATE query to modify record
        cursor.execute("""
            UPDATE students
            SET student_id=%s, fullname=%s, age=%s, gender=%s,
                course=%s, year_level=%s, address=%s, contact=%s
            WHERE id=%s
        """, (
            student_id, fullname, age, gender,
            course, year_level, address, contact, id
        ))
        # Gina update ya ang student information sa database
        # Ang WHERE id=%s para ma identify kon diin nga student ang i update

        # Save changes permanently to database
        conn.commit()
        # Para ma save ang changes

        # Close database cursor and connection
        cursor.close()
        conn.close()
        # Para ma close ang connection sa database

        # Redirect back to dashboard
        return redirect(url_for('index'))
        # Pagkatapos mag update, balik sa dashboard

    # Fetch specific student data from database
    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    student = cursor.fetchone()
    # Gina kwa ya ang specific student information para makita sa edit form

    # Close database cursor and connection
    cursor.close()
    conn.close()
    # Para ma close ang connection sa database

    # Render edit_student.html passing retrieved student data
    return render_template("edit_student.html", student=student)
    # Para makita ang edit page nga may ara na nga student information


# DELETE: DELETE STUDENT ROUTE
@app.route('/delete/<int:id>')
# Para ma delete ang student record sa database
def delete_student(id):
    # Check if the admin is logged in
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    # Kong wala naka log in, ibalik sa login page

    # Connect to MySQL database
    conn = connect_db()
    cursor = conn.cursor()
    # Para maka connect sa database kag makapadala sang SQL command

    # Execute SQL DELETE query for specific student ID
    cursor.execute("DELETE FROM students WHERE id = %s", (id,))
    # Gina delete ya ang student record nga may matching ID

    # Save changes permanently to database
    conn.commit()
    # Para ma save ang pag delete

    # Close database cursor and connection
    cursor.close()
    conn.close()
    # Para ma close ang connection sa database

    # Redirect back to dashboard
    return redirect(url_for('index'))
    # Pagkatapos mag delete, balik sa dashboard


# Run application server on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # Para ma run ang Flask website sa port 5000
    # host='0.0.0.0' = pwede ma access sa network kon sakto ang settings
    # port=5000 = port nga ginagamit sang website
    # debug=True = para makita ang errors kag automatic mag reload samtang nagadevelop
