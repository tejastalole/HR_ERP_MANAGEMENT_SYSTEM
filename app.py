from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL   # For Database Library

app = Flask(__name__)


# Database Configuration
app.secret_key='mysecretkey'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'hr_erp_db'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about-us')
def about_us():
    return render_template('about-us.html')

@app.route('/admin-login')
def admin_login():
    return render_template('admin-login.html')

@app.route('/contact-us')
def contact_us():
    return render_template('contact-us.html')

@app.route('/admin-dashboard' , methods=['POST'])
def admin_dashboard():

    session['name'] = 'Tejas'

    u = request.form['txtUsername']
    p = request.form['txtPassword']

    if(u == "admin" and p == "super"):
        
        return render_template('admin-dashboard.html')
    else:
        msg = "Invalid Username or Password"
        return render_template('admin-login.html', message=msg)


@app.route('/admin-add-employee')
def admin_add_employee():
    return render_template('admin-add-employee.html')

@app.route('/save', methods=['POST'])
def save():

    empid = request.form['txtempId']
    empname = request.form['txtName']
    email = request.form['txtEmail']
    mobile = request.form['txtMobile']
    designation = request.form['txtDesignation']
    salary = request.form['txtSalary']

    # Database Connection
    cur = mysql.connection.cursor()

    # Insert Data into Database
    cur.execute("INSERT INTO registration (empid, empname, email, mobile, designation, salary) VALUES (%s, %s, %s, %s, %s, %s)", (empid, empname, email, mobile, designation, salary))

    # Commit the changes to the database
    mysql.connection.commit()

    # Close the cursor
    cur.close()


    return render_template ('admin-reg-success.html')

@app.route('/admin-show-employee')
def admin_show_employee():

    cur = mysql.connection.cursor()

    # Insert Data into Database
    cur.execute('SELECT empid, empname, designation FROM registration')

    emplist = cur.fetchall()

    return render_template('admin-show-employee.html', recordlist=emplist)

@app.route('/admin-search-employee')
def admin_search_employee():
    return render_template('admin-search-employee.html')

@app.route('/logout')
def admin_logout():
    session["name"] = None
    return render_template('admin-login.html')

@app.route('/view-profile')
def view_profile():

    id = request.args.get('eid')
    cur = mysql.connection.cursor()
    cur.execute('SELECT empid, empname, email, mobile, designation, salary FROM registration WHERE empid =' + id)
    fetch_data = cur.fetchall()
    cur.close()

    return render_template('view-profile.html', gather_data=fetch_data)

@app.route('/admin-emp-update', methods=['POST'])
def admin_emp_update():

    empid = request.form['txtempId']
    empname = request.form['txtName']
    email = request.form['txtEmail']
    mobile = request.form['txtMobile']
    designation = request.form['txtDesignation']
    salary = request.form['txtSalary']

    cur = mysql.connection.cursor()

    # cur.execute('UPDATE registration SET designation=%s',(designation,))
    cur.execute('UPDATE registration SET empname=%s, email=%s, mobile=%s, designation=%s, salary=%s WHERE empid=%s', (empname, email, mobile, designation, salary, empid))

    mysql.connection.commit()
    cur.close() 
    
    return render_template('admin-emp-update-success.html')

@app.route('/admin-emp-delete')
def admin_emp_delete():
    empid = request.args.get('id')
    
    cur = mysql.connection.cursor()

    cur.execute('DELETE FROM registration WHERE empid=%s',(empid,))

    mysql.connection.commit()
    cur.close()

    return render_template('admin-emp-delete-success.html')


@app.route('/admin-emp-searchprocess', methods=['POST'])
def admin_emp_searchprocess():
    name = request.form['txtName']
    print(name)

    cur = mysql.connection.cursor()

    q = "SELECT * FROM registration WHERE empname LIKE'" +name+  "%'"
    # q = cur.execute("SELECT * FROM registration WHERE empname LIKE %s", ('%' + name + '%',))
    # print(q)
    cur.execute(q)
    emplist=cur.fetchall()
    cur.close()


    return render_template ('admin-emp-searchresult.html', recordlist=emplist)



app.run(debug=True)



