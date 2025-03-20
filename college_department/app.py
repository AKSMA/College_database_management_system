from flask import Flask, render_template , request, redirect , url_for , session , flash 
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash 
import MySQLdb.cursors
import MySQLdb

app = Flask(__name__)


# Configuring MYSQL 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Vidhya@2004'
app.config['MYSQL_DB'] = 'college_db'

#Initalize MySQL 
mysql = MySQL(app)

app.secret_key = 'your_secret_key'

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        department = request.form['department']
        user_type = request.form['user_type']
        hashed_password = generate_password_hash(password)
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        
        if user:
            return 'Email already exists'
        
        cursor.execute('''
            INSERT INTO users (name, email, password, department, user_type)
            VALUES (%s, %s, %s, %s, %s)
        ''', (name, email, hashed_password, department, user_type))
        
        mysql.connection.commit()
        
        if user_type == 'Student':
            rights = 'srfrm'
            
        if user_type == 'Faculty':
            rights = 'srwafrm'
        
        if user_type == 'Management':
            rights = 'srwafrwamrwa'
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    
        print(name , email , user_type , rights)
        try:
            cursor.execute('''
                INSERT INTO admin (name, email, user_type, rights)
                VALUES (%s, %s, %s, %s)
            ''', (name, email, user_type, rights))
        except MySQLdb.IntegrityError as e:
            print(f"Error: {e}")
        
        mysql.connection.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['POST' , 'GET'])

def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        
        if user_type == 'Admin':
            if password == 'mananjain2468@gmail.com':
                return redirect(url_for('admin_dashboard'))
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM users where email = %s' , (email,))
        user = cursor.fetchone()
        
        if not user or not check_password_hash(user['password'], password):
            return 'Incorrect email or password'
        
        session['logged_in'] = True
        session['id'] = user['id']
        session['email'] = user['email']
        session['department'] = user['department']
        
        cursor.execute('UPDATE users SET last_login = NOW() WHERE email = %s', (email,))
        mysql.connection.commit()
        
        if user_type == 'Student':
            return redirect(url_for('student_dashboard', email=email , user_type = user_type))
        
        if user_type == 'Faculty':
            return redirect(url_for('faculty_dashboard', email=email , user_type = user_type))
        
        if user_type == 'Supporting Staff':
            return redirect(url_for('supporting_Staff_dashboard', email=email , user_type = user_type))
        
        if user_type == 'Management':
            return redirect(url_for('management_dashboard', email=email , user_type = user_type))
    
    return render_template('login.html')


def authentication(email, right_asked):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM admin WHERE email = %s', (email,))
    data = cursor.fetchone()
    
    if data is None:
        # No record found for the given email
        return False
    
    # Now that we know data is not None, we can safely access its 'rights' key
    if right_asked in data['rights']:
        return True
    else:
        return False

        


def fetch_student_data(email_):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
    cursor.execute('SELECT * FROM student WHERE email = %s', (email_, ))
    user = cursor.fetchone()
    return user

def fetch_student_course_data(student_data):
    department = student_data['branch']  # Ensure department is an integer
    
    if department=='Computer Science':
        department_id = 1
    elif department=='Electronics and Communication':
        department_id = 2
    else:
        department_id = 3 
        
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT sc.course_id , dc.course_name , sc.theory_marks , sc.lab_marks , sc.final_grade , dc.credits, sc.semester FROM student_courses sc JOIN department_courses dc ON sc.course_id = dc.course_id WHERE sc.student_id=%s', (int(student_data['student_id']),))  # Add comma to make it a tuple
    data_ = cursor.fetchall()
    cursor.execute("""
        SELECT SUM(sc.final_grade * dc.credits) / SUM(dc.credits) AS cgpa 
        FROM student_courses sc 
        JOIN department_courses dc ON sc.course_id = dc.course_id 
        WHERE sc.student_id=%s AND sc.final_grade > 3
    """, (int(student_data['student_id']),))
    cgpa = cursor.fetchone()
    return [data_ , cgpa]

def fetch_fees_data(student_data):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM fees WHERE student_id = %s', (student_data['student_id'], ))    
    data_ = cursor.fetchall()
    return data_



def fetch_available_course_data(student_data):
    semester = student_data['semester']
    department = student_data['branch']  # Ensure department is an integer
    
    if department=='Computer Science':
        department_id = 1
    elif department=='Electronics and Communication':
        department_id = 2
    else:
        department_id = 3 
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute("""
        SELECT ac.course_id, dc.course_name , ac.semester , dc.credits
        FROM available_course ac
        JOIN department_courses dc ON ac.course_id = dc.course_id
        WHERE ac.semester > %s AND dc.department_id = %s and ac.department_id = dc.department_id
    """, (semester, department_id))
    
    data = cursor.fetchall()
    cursor.close()
    return data

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def fetch_faculty_data(email_):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
    cursor.execute('SELECT * FROM faculty WHERE email = %s', (email_, ))
    user = cursor.fetchone()
    return user

def fetch_courses_taught_data(fac_data):
    dep_id = fac_data['department_id']
    fac_id = fac_data['faculty_id']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT df.department_id , df.faculty_id , df.course_id , dc.course_name FROM department_faculty df JOIN department_courses dc ON dc.course_id = df.course_id AND dc.department_id = df.department_id WHERE df.department_id = %s AND df.faculty_id = %s', (dep_id ,fac_id))
    courses_taught = cursor.fetchall()
    cursor.close()
    return courses_taught

def fetch_salary_details(data_):
    total_salary = data_['salary'] 
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT AVG(salary) FROM faculty WHERE department_id = %s AND AGE < %s AND AGE > %s', (data_['department_id'] , data_['age']+5 , data_['age']-5))
    result = cursor.fetchone()
    avg_salary = result['AVG(salary)']
    cursor.execute('SELECT MAX(salary) FROM faculty WHERE department_id = %s' , (data_['department_id'] ,))
    result = cursor.fetchone()
    max_salary = result['MAX(salary)']

    return {'total_salary_': total_salary , 'avg_salary_': avg_salary , 'max_salary_':  max_salary}


@app.route('/admin_dashboard')
def admin_dashboard():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
    cursor.execute('SELECT * FROM admin ')
    user = cursor.fetchall()
    return render_template('admin_dashboard.html', data_=user)

@app.route('/admin_change_rights>', methods=['GET', 'POST'])
def admin_change_rights():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        rights = request.form['rights']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('UPDATE admin SET rights = %s where email = %s', (rights, email))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_change_right.html')
@app.route('/student_dashboard')

def student_dashboard():
    student = {
        'name': 'Manan Jain',
        'branch': 'Computer Science',
        'grad_year': 2025
    }
    
    email = request.args.get('email')
    user_type = request.args.get('user_type')
    
        
    student_data = fetch_student_data(email) 
    grades_data = fetch_student_course_data(student_data)
    fees_data = fetch_fees_data(student_data)
    courses_avail = fetch_available_course_data(student_data)
    return render_template('student_dashboard.html', student=student_data , course_data_ = grades_data[0] , fees = fees_data , avail_courses = courses_avail , cgpa_data = grades_data[1])


@app.route('/faculty_dashboard')

def faculty_dashboard():
    student = {
        'name': 'Manan Jain',
        'branch': 'Computer Science',
        'grad_year': 2025
    }
    
    email = request.args.get('email')
    user_type = request.args.get('user_type')
    
        
    faculty_data = fetch_faculty_data(email) 
    courses_taught_data = fetch_courses_taught_data(faculty_data)
    salary_data = fetch_salary_details(faculty_data)
    # courses_avail = fetch_available_course_data(faculty_data)
    return render_template('faculty_dashboard.html', faculty=faculty_data , course_taught = courses_taught_data, salary_data_ = salary_data) 

@app.route('/supporting_staff_dashboard')

def supporting_staff_dashboard():
    return 'Supporting Staff Dashboard'

@app.route('/management_dashboard', methods=['GET', 'POST'])


def management_dashboard():
    if request.method == 'POST':
        operation = request.form.get('operation')
        entity = request.form.get('entity')
        
        return redirect(url_for('handle_management_operation', operation = operation , entity = entity))
    
    return render_template('management_dashboard.html')

@app.route('/handle_management_operation/<operation>/<entity>', methods = ['POST' , 'GET'])

def handle_management_operation(operation,entity):
    if entity == 'faculty':
        if operation == 'create':
            if request.method == 'POST':
                email = request.form['email']
                if authentication(email  , 'frwa'):
                    return redirect(url_for('submit_create_faculty'))
                else:
                    flash('You are not authorised for updating faculty data.') 
                    return redirect(url_for('management_dashboard'))
            return render_template('authentication.html')
        
            
        
        elif operation == 'read':
            if request.method == 'POST':
                faculty_id = request.form['faculty_id']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
                cursor.execute('SELECT * FROM faculty WHERE faculty_id = %s', (faculty_id, ))
                faculty_data = cursor.fetchone() 
                courses_taught_data = fetch_courses_taught_data(faculty_data)
                
                return render_template('management_read_faculty.html', faculty=faculty_data , course_taught = courses_taught_data)
            
            return render_template('management_read_faculty_input.html')
            
        
        elif operation == 'update':
            if request.method == 'POST':
                email = request.form['email']
                if authentication(email  , 'frwa'):
                    return redirect(url_for('submit_update_faculty'))
                else:
                    flash('You are not authorised for updating faculty data.') 
                    return redirect(url_for('management_dashboard'))
            return render_template('authentication.html')
        
        elif operation == 'delete':
            if request.method == 'POST':
                email = request.form['email']
                if authentication(email  , 'frwa'):
                    return redirect(url_for('submit_delete_faculty'))
                else:
                    flash('You are not authorised for deleting faculty data.') 
                    return redirect(url_for('management_dashboard'))
            return render_template('authentication.html')
   
   
    elif entity == 'student':
        if operation == 'create':
            if request.method == 'POST':
                email = request.form['email']
                if authentication(email  , 'srwa'):
                    return redirect(url_for('submit_create_option_student'))
                else:
                    flash('You are not authorised for updating student data.') 
                    return redirect(url_for('management_dashboard'))
            return render_template('authentication.html')
                
        
        elif operation == 'read':
            if request.method == 'POST':
                student_id = request.form['student_id']
                option = request.form['option']
                if option == 'view_marks':
                    return redirect(url_for('view_student_marks', student_id=student_id))
                if option == 'view_fees_record':
                    return redirect(url_for('view_student_fees', student_id=student_id))
                else:
                    return redirect(url_for('view_student_profile', student_id=student_id))
            return render_template('management_read_student.html')
        
        
        elif operation == 'update':
            if request.method == 'POST':
                email = request.form['email']
                if authentication(email  , 'srwa'):
                    return redirect(url_for('submit_update_option_student'))
                else:
                    flash('You are not authorised for updating student data.') 
                    return redirect(url_for('management_dashboard'))
            return render_template('authentication.html')
        
        elif operation == 'delete':
            if request.method == 'POST':
                email = request.form['email']
                if authentication(email  , 'srwa'):
                    return redirect(url_for('submit_delete_option_student'))
                else:
                    flash('You are not authorised for deleting student data.') 
                    return redirect(url_for('management_dashboard'))
            return render_template('authentication.html')
    
    
    elif entity == 'supporting_staff':
        if operation == 'create':
            return render_template('management_create_supporting_staff.html')
        elif operation =='read':
            return render_template('management_read_supporting_staff.html')
        elif operation == 'update':
            return render_template('management_update_supporting_staff.html')
        elif operation == 'delete':
            return render_template('management_delete_supporting_staff.html')
    
    
    elif entity=='management':
        if operation == 'create':
            print('Work in progress')
            return redirect(url_for('management_dashboard'))
            # return render_template('management_create_management.html')
        elif operation =='read':
            return render_template('management_read_management.html')
        elif operation == 'update':
            return render_template('management_update_management.html')
        elif operation == 'delete':
            return render_template('management_delete_management.html') 
    
    return "Invalid operation or entity."


@app.route('/management_create_faculty', methods=['GET', 'POST'])
def submit_create_faculty():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department_id = request.form['department_id']
        graduation_course = request.form['graduation_course']
        graduation_complete_year = request.form['graduation_complete_year']
        graduation_college = request.form['graduation_college']
        post_graduation_specialisation = request.form['post_graduation_specialisation']
        post_graduation_complete_year = request.form['post_graduation_complete_year']
        post_graduation_college = request.form['post_graduation_college']
        phd_research = request.form['phd_research']
        phd_complete_year = request.form['phd_complete_year']
        phd_college = request.form['phd_college']
        age = request.form['age']
        salary = request.form['salary']
        course1 = request.form['course1']
        course2 = request.form['course2']
        course3 = request.form['course3']
        course4 = request.form['course4']
        
        # Filter out any empty course IDs
        courses_taught = [course for course in [course1, course2, course3, course4] if course]

        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Insert into faculty table
            cursor.execute('''INSERT INTO faculty (name, email, graduation_course, graduation_complete_year, graduation_college,
                post_graduation_specialisation, post_graduation_complete_year, phd_research, phd_complete_year, post_graduation_college, 
                phd_college, age, department_id, salary)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (name, email, graduation_course, graduation_complete_year, graduation_college, post_graduation_specialisation,
                post_graduation_complete_year, phd_research, phd_complete_year, post_graduation_college, phd_college, age, 
                department_id, salary))

            # Get the last inserted faculty_id
            faculty_id = cursor.lastrowid

            # Insert into department_faculty table for each course taught
            for course_id in courses_taught:
                cursor.execute('INSERT INTO department_faculty (department_id, faculty_id, course_id) VALUES (%s, %s, %s)', 
                               (department_id, faculty_id, course_id))

            mysql.connection.commit()
            cursor.close()
        except Exception as e:
            print("Error inserting data:", e)
            mysql.connection.rollback()
        
        return redirect(url_for('management_dashboard'))
    
    return render_template('management_create_faculty.html')



@app.route('/management_update_faculty', methods=['GET', 'POST'])
def submit_update_faculty():
    if request.method == 'POST':
        
        faculty_id = request.form['faculty_id']
        updated_data = {}
        
        name = request.form.get('name')
        if name: updated_data['name'] = name

        graduation_course = request.form.get('graduation_course')
        if graduation_course: updated_data['graduation_course'] = graduation_course

        graduation_complete_year = request.form.get('graduation_complete_year')
        if graduation_complete_year: updated_data['graduation_complete_year'] = graduation_complete_year

        graduation_college = request.form.get('graduation_college')
        if graduation_college: updated_data['graduation_college'] = graduation_college

        post_graduation_specialisation = request.form.get('post_graduation_specialisation')
        if post_graduation_specialisation: updated_data['post_graduation_specialisation'] = post_graduation_specialisation

        post_graduation_complete_year = request.form.get('post_graduation_complete_year')
        if post_graduation_complete_year: updated_data['post_graduation_complete_year'] = post_graduation_complete_year

        phd_research = request.form.get('phd_research')
        if phd_research: updated_data['phd_research'] = phd_research

        phd_complete_year = request.form.get('phd_complete_year')
        if phd_complete_year: updated_data['phd_complete_year'] = phd_complete_year

        post_graduation_college = request.form.get('post_graduation_college')
        if post_graduation_college: updated_data['post_graduation_college'] = post_graduation_college

        phd_college = request.form.get('phd_college')
        if phd_college: updated_data['phd_college'] = phd_college

        age = request.form.get('age')
        if age: updated_data['age'] = age

        department_id = request.form.get('department_id')
        if department_id: updated_data['department_id'] = department_id

        salary = request.form.get('salary')
        if salary: updated_data['salary'] = salary
        
        if updated_data:
            set_clause = ", ".join([f"{key} = %s" for key in updated_data.keys()])
            values = list(updated_data.values())
            values.append(faculty_id)
            
            query = f'UPDATE faculty SET {set_clause} WHERE faculty_id = %s' 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, values)
            mysql.connection.commit()
            cursor.close()
            
            # Step 4: Flash success message and redirect to dashboard
            flash('Faculty details updated successfully.')        
        else:
            flash('No changes were made.')
        
        return redirect(url_for('management_dashboard'))
    return render_template('management_update_faculty.html')


@app.route('/management_student_create_option' , methods = ['GET', 'POST'])
def submit_create_option_student():
    if request.method == 'POST':
        option = request.form['option']
        if option == 'generate_marks':
            return redirect(url_for('submit_student_marks'))
        if option == 'generate_fees_record':
            return redirect(url_for('submit_student_fees'))
        else:
            return redirect(url_for('submit_student_profile'))
                
    return render_template('management_create_student.html')
        

@app.route('/management_student_update_option' , methods = ['GET', 'POST'])
def submit_update_option_student():
    if request.method == 'POST':
               
        option = request.form['option']
        if option == 'update_marks':
            return redirect(url_for('submit_update_student_marks'))
        if option == 'update_fees_record':
            return redirect(url_for('submit_update_student_fees'))
        else:
            return redirect(url_for('submit_update_student_profile'))
        
    return render_template('management_student_update_option.html')
    



@app.route('/management_update_student_profile', methods=['GET', 'POST'])
def submit_update_student_profile():
    if request.method == 'POST':
        
        student_id = request.form['student_id']
        updated_data = {}
        
        name = request.form.get('name')
        if name: updated_data['name'] = name
        
        email = request.form.get('email')
        if email: updated_data['email'] = email
        
        branch = request.form.get('branch')
        if branch: updated_data['branch'] = branch
        
        year_of_joining = request.form.get('year_of_joining')
        if year_of_joining: updated_data['year_of_joining'] = year_of_joining

        graduation_year = request.form.get('graduation_year')
        if graduation_year: updated_data['graduation_year'] = graduation_year

        semester = request.form.get('semester')
        if semester: updated_data['semester'] = semester
        
        if updated_data:
            set_clause = ", ".join([f"{key} = %s" for key in updated_data.keys()])
            values = list(updated_data.values())
            values.append(student_id)
            
            query = f'UPDATE student SET {set_clause} WHERE student_id = %s' 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, values)
            mysql.connection.commit()
            cursor.close()
            
            # Step 4: Flash success message and redirect to dashboard
            flash('Student details updated successfully.')        
        else:
            flash('No changes were made.')
        
        return redirect(url_for('management_dashboard'))
    return render_template('management_update_student_profile.html')

@app.route('/management_update_student_fees', methods=['GET', 'POST'])
def submit_update_student_fees():
    if request.method == 'POST':
        
        student_id = request.form['student_id']
        updated_data = {}
        
        fees_paid = request.form.get('fees_paid')
        if fees_paid: updated_data['fees_paid'] = fees_paid
        
        
        if updated_data:
            set_clause = ", ".join([f"{key} = %s" for key in updated_data.keys()])
            values = list(updated_data.values())
            values.append(student_id)
            
            query = f'UPDATE fees SET {set_clause} WHERE student_id = %s' 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, values)
            mysql.connection.commit()
            cursor.close()
            
            # Step 4: Flash success message and redirect to dashboard
            flash('Student details updated successfully.')        
        else:
            flash('No changes were made.')
        
        return redirect(url_for('management_dashboard'))
    return render_template('management_update_student_fees.html')

@app.route('/management_update_student_marks', methods=['GET', 'POST'])
def submit_update_student_marks():
    if request.method == 'POST':
        
        student_id = request.form['student_id']
        updated_data = {}
        
        course_id = request.form.get('course_id')
        if course_id: updated_data['course_id'] = course_id
        
        theory_marks = request.form.get('theory_marks')
        if theory_marks: updated_data['theory_marks'] = theory_marks
        
        lab_marks = request.form.get('lab_marks')
        if lab_marks: updated_data['lab_marks'] = lab_marks
        
        final_grade = request.form.get('final_grade')
        if final_grade: updated_data['final_grade'] = final_grade
        
        semester = request.form.get('semester')
        if semester: updated_data['semester'] = semester
        
        
        if updated_data:
            set_clause = ", ".join([f"{key} = %s" for key in updated_data.keys()])
            values = list(updated_data.values())
            values.append(student_id)
            values.append(course_id)
            
            query = f'UPDATE student_courses SET {set_clause} WHERE student_id = %s AND course_id = %s' 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, values)
            mysql.connection.commit()
            cursor.close()
            
            # Step 4: Flash success message and redirect to dashboard
            flash('Student details updated successfully.')        
        else:
            flash('No changes were made.')
        
        return redirect(url_for('management_dashboard'))
    return render_template('management_update_student_marks.html')


@app.route('/management_delete_faculty', methods=['GET', 'POST'])
def submit_delete_faculty():
    if request.method == 'POST':
        faculty_id = request.form.get('faculty_id')
        
        if faculty_id:
            try:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('DELETE FROM department_faculty WHERE faculty_id = %s', (faculty_id,))
                cursor.execute('DELETE FROM faculty WHERE faculty_id = %s', (faculty_id,))
                mysql.connection.commit()
                cursor.close()
                flash('Faculty details deleted successfully.', 'success')

            except Exception as e:
                mysql.connection.rollback()
                flash(f'Error deleting faculty details: {str(e)}', 'danger')

        return redirect(url_for('management_dashboard'))
    return render_template('management_delete_faculty.html')

@app.route('/management_student_delete_option' , methods = ['GET', 'POST'])
def submit_delete_option_student():
    if request.method == 'POST':
               
        option = request.form['option']
        if option == 'delete_marks':
            return redirect(url_for('submit_delete_student_marks'))
        if option == 'delete_fees_record':
            return redirect(url_for('submit_delete_student_fees'))
        else:
            return redirect(url_for('submit_delete_student_profile'))
        
    return render_template('management_student_delete_option.html')

@app.route('/management_delete_student_profile', methods=['GET', 'POST'])
def submit_delete_student_profile():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        
        if student_id:
            try:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('DELETE FROM student WHERE student_id = %s', (student_id,))
                mysql.connection.commit()
                cursor.close()
                flash('Student details deleted successfully.', 'success')

            except Exception as e:
                mysql.connection.rollback()
                flash(f'Error deleting faculty details: {str(e)}', 'danger')

        return redirect(url_for('management_dashboard'))
    return render_template('management_delete_student_profile.html')

@app.route('/management_delete_student_fees', methods=['GET', 'POST'])
def submit_delete_student_fees():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        
        if student_id:
            try:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('DELETE FROM fees WHERE student_id = %s', (student_id,))
                mysql.connection.commit()
                cursor.close()
                flash('Student details deleted successfully.', 'success')

            except Exception as e:
                mysql.connection.rollback()
                flash(f'Error deleting faculty details: {str(e)}', 'danger')

        return redirect(url_for('management_dashboard'))
    return render_template('management_delete_student_fees.html')

@app.route('/management_delete_student_marks', methods=['GET', 'POST'])
def submit_delete_student_marks():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        course_id = request.form.get('course_id')
        
        if student_id:
            try:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('DELETE FROM student_courses WHERE student_id = %s and course_id', (student_id,course_id))
                mysql.connection.commit()
                cursor.close()
                flash('Student details deleted successfully.', 'success')

            except Exception as e:
                mysql.connection.rollback()
                flash(f'Error deleting faculty details: {str(e)}', 'danger')

        return redirect(url_for('management_dashboard'))
    return render_template('management_delete_student_marks.html')



@app.route('/management_create_profile_student', methods=['GET', 'POST'])
def submit_student_profile():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        branch = request.form['branch']
        year_of_joining = request.form['year_of_joining']
        semester = request.form['semester']
        
        # Assuming `faculty_id` is auto-increment or you generate it separately
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''INSERT INTO student (name, email, branch, year_of_joining, semester) 
            VALUES (%s, %s, %s, %s, %s)''',
            (name, email, branch, year_of_joining, semester))
        student_id = cursor.lastrowid 
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('management_dashboard'))
    return render_template('management_create_profile_student.html')

@app.route('/generate_marks_student_', methods=['GET', 'POST'])
def submit_student_marks():
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        theory_marks = request.form['theory_marks']
        lab_marks = request.form['lab_marks']
        final_grade = request.form['final_grade']
        semester = request.form['semester']
        
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''INSERT INTO student_courses (student_id,course_id,theory_marks,lab_marks,final_grade, semester) 
            VALUES (%s, %s, %s, %s, %s, %s)''',
            (student_id,course_id,theory_marks,lab_marks,final_grade, semester))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('management_dashboard'))
    return render_template('generate_marks_student.html')

@app.route('/generate_fees_student_', methods=['GET', 'POST'])
def submit_student_fees():
    if request.method == 'POST':
        student_id = request.form['student_id']
        total_fees = 1500000.00
        fees_paid = request.form['fees_paid']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''INSERT INTO fees (student_id,total_fees,fees_paid) 
            VALUES (%s, %s,%s)''',
            (student_id,total_fees,fees_paid))
        student_id = cursor.lastrowid
        mysql.connection.commit()
        
        cursor.close()
        return redirect(url_for('management_dashboard'))

        
    return render_template('generate_fees_student.html ')


@app.route('/management_view_profile_student/<int:student_id>', methods=['GET', 'POST'])
def view_student_profile(student_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''SELECT * FROM student WHERE student_id = %s''', (student_id,))
    data_ = cursor.fetchone()
    cursor.close()
    return render_template('management_view_profile_student.html', student=data_)


@app.route('/management_view_marks_student/<int:student_id>', methods=['GET', 'POST'])
def view_student_marks(student_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''SELECT * FROM student_courses WHERE student_id = %s''', (student_id,))
    data_ = cursor.fetchall()
    cursor.close()
    return render_template('management_view_marks_student.html', course_data_=data_)


@app.route('/management_view_fees_student/<int:student_id>', methods=['GET', 'POST'])
def view_student_fees(student_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''SELECT * FROM fees WHERE student_id = %s''', (student_id,))
    data_ = cursor.fetchall()
    cursor.close()
    return render_template('management_view_fees_student.html', fees=data_)


@app.route('/logout')

def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/teacher_single/<int:teacher_id>')
def teacher_single(teacher_id):
    # Fetch teacher information from the database based on the teacher_id
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM faculty WHERE faculty_id = %s', (teacher_id,))
    teacher = cursor.fetchone()
    cursor.execute('SELECT df.department_id , df.faculty_id , df.course_id , dc.course_name FROM department_faculty df JOIN department_courses dc ON dc.course_id = df.course_id AND dc.department_id = df.department_id WHERE df.department_id = %s AND df.faculty_id = %s', (teacher['department_id'] ,teacher_id))
    course_taught = cursor.fetchall()
    cursor.close()

    # Render the 'teacher_single.html' template and pass the teacher data
    return render_template('teacher_single.html', teacher=teacher , c_t = course_taught)



@app.route('/teachers', defaults={'page': 1})
@app.route('/teachers/<int:page>')
def teachers(page):
    teachers_per_page = 8
    offset = (page - 1) * teachers_per_page
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM faculty LIMIT %s OFFSET %s', (teachers_per_page, offset))
    teachers_list = cursor.fetchall()  # Fetch 6 teachers at a time
    cursor.close()

    # Fetch total number of teachers to calculate number of pages
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT COUNT(*) FROM faculty')
    total_teachers = cursor.fetchone()['COUNT(*)']
    cursor.close()
    
    total_pages = (total_teachers // teachers_per_page) + (1 if total_teachers % teachers_per_page > 0 else 0)
    
    return render_template('teachers.html', teachers=teachers_list, page=page, total_pages=total_pages)





@app.route('/courses')
def courses():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''SELECT DISTINCT c.course_id, c.course_name, c.course_image_url, f.faculty_id, f.name AS course_coordinator
                      FROM department_courses AS c
                      LEFT JOIN faculty AS f ON c.Course_Coordinator = f.faculty_id
                      LEFT JOIN department_faculty AS df ON df.faculty_id = f.faculty_id''')
    data_ = cursor.fetchall()
    cursor.close()
    
    
    
    return render_template('courses.html' , courses= data_)



# @app.route('/course/<int:course_id>')
# def course_single(course_id):
#     # Fetch the specific course data by `course_id`
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute('''SELECT * FROM department_courses WHERE course_id = %s''', (course_id,))
#     course = cursor.fetchone()
#     cursor.close()
#     return render_template('course_single.html', course=course)

@app.route('/course_single/<int:course_id>')
def course_single(course_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Query for course details
    cursor.execute('''
        SELECT c.course_id, c.course_name, c.course_image_url, c.Course_Coordinator, 
               c.Duration, c.Lectures, c.Quizzes, f.faculty_id, f.name, c.department_id
        FROM department_courses AS c
        LEFT JOIN faculty AS f ON c.course_coordinator = f.faculty_id
        WHERE c.course_id = %s
    ''', (course_id,))
    course = cursor.fetchone()

    # Query for student count from the view
    cursor.execute('''
        SELECT student_count 
        FROM department_course_student_counts 
        WHERE course_id = %s AND department_id = %s
    ''', (course_id, course['department_id']))
    student_count = cursor.fetchone()
    
    cursor.execute('''
    SELECT c.course_id, c.course_name, 
           COUNT(sc.student_id) AS enrolled_students
    FROM department_courses AS c
    LEFT JOIN student_courses AS sc ON c.course_id = sc.course_id
    WHERE c.course_id > %s AND c.department_id = %s
    GROUP BY c.course_id
    LIMIT 3
    ''', (course_id, course['department_id']))
    related_courses = cursor.fetchall()

    
    
    cursor.close()

    # Pass data to the template
    return render_template('course_single.html', course=course, student_count=student_count , related_courses = related_courses )







if __name__ == '__main__':
    app.run(debug=True)
    


