from faker import Faker
import random
import mysql.connector

# Initialize Faker
faker = Faker()

# Connect to your MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vidhya@2004",
    database="college_db"
)

cursor = db.cursor()

departments = [
    {"name": "Computer Science", "description": faker.text(), "num_students": random.randint(0, 100), "num_faculties": random.randint(0, 20), "num_labs": random.randint(0, 10), "num_courses": random.randint(0, 50)},
    {"name": "Electronics and Communication", "description": faker.text(), "num_students": random.randint(0, 100), "num_faculties": random.randint(0, 20), "num_labs": random.randint(0, 10), "num_courses": random.randint(0, 50)},
    {"name": "Basic Sciences", "description": faker.text(), "num_students": random.randint(0, 100), "num_faculties": random.randint(0, 20), "num_labs": random.randint(0, 10), "num_courses": random.randint(0, 50)}
]

# Insert departments and fetch their IDs
department_ids = {}

for dept in departments:
    cursor.execute("""
        INSERT INTO departments (name, description, num_students, num_faculties, num_labs, num_courses) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (dept["name"], dept["description"], dept["num_students"], dept["num_faculties"], dept["num_labs"], dept["num_courses"]))
    
    dept_id = cursor.lastrowid
    department_ids[dept["name"]] = dept_id

print("Department IDs:", department_ids)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Insert faculties
graduation_courses = [
    'Bachelor of Technology in Computer Science', 'Bachelor of Technology in Electronics and Communication',
    'Bachelor of Science in Physics', 'Bachelor of Science in Mathematics', 'Bachelor of Science in Chemistry',
    'Bachelor of Engineering in Computer Science', 'Bachelor of Engineering in Electronics', 'Bachelor of Engineering in Electrical Engineering'
]

post_graduation_specializations = [
    'Master of Technology in Data Science', 'Master of Technology in VLSI Design',
    'Master of Science in Physics', 'Master of Science in Applied Mathematics',
    'Master of Technology in Signal Processing', 'Master of Technology in Artificial Intelligence',
    'Master of Engineering in Software Engineering'
]

phd_research_topics = [
    'Machine Learning Algorithms for Image Recognition', 'Optimization Techniques in Wireless Networks',
    'Quantum Computing in Cryptography', 'Nonlinear Dynamics in Complex Systems',
    'Applications of AI in Healthcare', 'Data Mining in Large Databases',
    'Nanotechnology for Semiconductor Devices', 'Mathematical Modelling in Physics'
]

colleges = [
    'Indian Institute of Technology (IIT Delhi)', 'Indian Institute of Technology (IIT Bombay)', 
    'Indian Institute of Technology (IIT Madras)', 'Indian Institute of Science (IISc Bangalore)', 
    'National Institute of Technology (NIT Trichy)', 'Birla Institute of Technology and Science (BITS Pilani)', 
    'Delhi Technological University (DTU)', 'Jadavpur University', 'Vellore Institute of Technology (VIT)', 
    'Anna University', 'University of Hyderabad'
]

for _ in range(75):  # 75 faculty members
    dept_name = random.choice(departments)
    dept_id = department_ids[dept_name['name']]  # Get the department ID from the dictionary

    cursor.execute(
        """
        INSERT INTO faculty 
        (name, email, graduation_course, graduation_complete_year, post_graduation_specialisation, 
        post_graduation_complete_year, phd_research, phd_complete_year, graduation_college, 
        post_graduation_college, phd_college, age, department_id, salary) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            faker.name(),
            faker.email(),
            random.choice(graduation_courses),
            random.randint(1995, 2015),  # Graduation completion year
            random.choice(post_graduation_specializations),
            random.randint(2000, 2020),  # Post-graduation completion year
            random.choice(phd_research_topics),
            random.randint(2010, 2023),  # PhD completion year
            random.choice(colleges),
            random.choice(colleges),
            random.choice(colleges),
            random.randint(26, 60),  # Age between 26 and 60
            dept_id,  # Use the department ID from the dictionary
            random.randint(50000, 150000)  # Random salary
        )
    )

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Define courses for each department
cs_courses = [
    "Introduction to Programming", "Data Structures", "Algorithms", "Computer Networks", 
    "Operating Systems", "Database Management Systems", "Software Engineering", 
    "Artificial Intelligence", "Machine Learning", "Computer Graphics", "Theory of Computation",
    "Compiler Design", "Web Technologies", "Distributed Systems", "Data Mining", 
    "Cyber Security", "Mobile Application Development", "Blockchain Technologies", 
    "Cloud Computing", "Big Data Analytics", "Natural Language Processing", 
    "Human-Computer Interaction", "Parallel Computing", "Cryptography", 
    "Game Development", "Augmented Reality", "Virtual Reality", "Internet of Things", 
    "Information Retrieval", "Deep Learning", "Pattern Recognition", 
    "Quantum Computing", "Neural Networks", "Bioinformatics", "Robotics", 
    "Software Testing", "DevOps", "Advanced Algorithms", "Multimedia Systems", 
    "Compiler Optimization", "Open Source Software Development", "Functional Programming", 
    "Web Security", "Ethical Hacking", "Information Theory", "Digital Signal Processing", 
    "Network Security", "High-Performance Computing", "Data Visualization", "Cloud Architecture"
]

ece_courses = [
    "Analog Electronics", "Digital Electronics", "Electromagnetics", "Signals and Systems", 
    "Control Systems", "Communication Systems", "VLSI Design", "Embedded Systems", 
    "Microprocessors and Microcontrollers", "Digital Signal Processing", 
    "Wireless Communication", "Antenna and Wave Propagation", "RF and Microwave Engineering", 
    "Satellite Communication", "Optoelectronics", "Nanotechnology", "Power Electronics", 
    "Fiber Optic Communication", "Telecommunication Networks", "Radar Engineering", 
    "Signal Analysis", "Biomedical Signal Processing", "Sensors and Actuators", 
    "Internet of Things (IoT)", "Microelectronics", "Communication Networks", 
    "Semiconductor Devices", "Quantum Electronics", "Photonics", "Digital Image Processing", 
    "Robotics and Automation", "Nanoelectronics", "Mobile Communication", 
    "Microfabrication Techniques", "Advanced Control Systems", "MEMS and NEMS", 
    "Mixed-Signal Circuit Design", "Digital System Design", "Power Systems", 
    "Solid-State Electronics", "Analog Integrated Circuits", "Signal Detection and Estimation", 
    "Wavelet Theory", "Plasma Electronics", "Digital Communication", "Radio Frequency Circuits", 
    "Analog Communication", "Advanced Microcontrollers", "Microwave Circuits"
]

basic_sciences_courses = [
    "Physics for Engineers", "Chemistry for Engineers", "Mathematics I", 
    "Mathematics II", "Mathematics III", "Biology for Engineers", 
    "Environmental Science", "Engineering Physics", "Engineering Chemistry", 
    "Introduction to Quantum Mechanics", "Linear Algebra", "Statistics and Probability", 
    "Thermodynamics", "Organic Chemistry", "Physical Chemistry", "Inorganic Chemistry", 
    "Computational Mathematics", "Waves and Optics", "Fluid Dynamics", "Classical Mechanics"
]

# Define semester-wise course IDs
semester_courses = {
    1: list(range(1, 7)),    
    2: list(range(7, 13)),   
    3: list(range(13, 19)),  
    4: list(range(19, 25)),  
    5: list(range(25, 31)),  
    6: list(range(31, 37)),  
    7: list(range(37, 43)),  
    8: list(range(43, 51))   
}

# Map realistic courses to IDs
def map_courses_to_ids(courses, dept_id):
    course_ids = {}
    for i, course in enumerate(courses, start=1):
        cursor.execute("INSERT INTO department_courses (department_id, course_id, course_name, credits) VALUES (%s, %s, %s, %s)",
                       (dept_id, i, course, random.randint(3, 6)))
        course_ids[course] = i
    return course_ids


cs_course_ids = map_courses_to_ids(cs_courses, department_ids['Computer Science'])
ece_course_ids = map_courses_to_ids(ece_courses, department_ids['Electronics and Communication'])
basic_sciences_course_ids = map_courses_to_ids(basic_sciences_courses, department_ids['Basic Sciences'])

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



# Function to insert student 

cursor.execute("SELECT name FROM departments")
branches = [row[0] for row in cursor.fetchall()]


def calculate_semester(year_of_joining):
    from datetime import datetime

    current_month = datetime.now().month
    current_year = datetime.now().year
    year_difference = current_year - year_of_joining

    if current_month >= 7:  # July to December is the 1st semester
        semester = (year_difference * 2) + 1
    else:  # January to June is the 2nd semester
        semester = (year_difference * 2) + 2

    
    return min(semester, 8)


unique_emails = set()

# Function to generate unique email
def generate_unique_email():
    email = faker.email()
    while email in unique_emails:  
        email = faker.email()
    unique_emails.add(email)
    return email

# Insert 1200 student records
for _ in range(1200):
    name = faker.name()
    email = generate_unique_email()  
    branch = random.choice(branches)
    year_of_joining = random.randint(2021, 2024)  # Adjust the range as needed
    semester = calculate_semester(year_of_joining)

    cursor.execute("""
        INSERT INTO student (name, email, branch, year_of_joining, semester)
        VALUES (%s, %s, %s, %s, %s)
        """, (name, email, branch, year_of_joining, semester))
    
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



 # Define a function to insert student courses

def insert_student_courses():
    for student_id in range(1, 1200):
        # Retrieve the student's current semester and branch from the student table
        cursor.execute("SELECT * FROM student WHERE student_id = %s", (student_id,))
        data_ = cursor.fetchone()
        student_semester = data_[-1]  
        student_department = data_[3]
        
        # If semester is not set (None), skip this student
        if student_semester is None:
            print(f"Skipping student {student_id} as semester is not set.")
            continue

        # Insert courses for each semester up to `student_semester - 1`
        for semester in range(1, student_semester):
            valid_semester_course_ids = semester_courses.get(semester, [])

            # Ensure there are valid courses to insert for this semester
            if not valid_semester_course_ids:
                continue

            # Fetch department-specific courses for the student's department
            query = '''
                SELECT course_id 
                FROM department_courses 
                WHERE department_id = %s AND course_id IN ({})
            '''.format(','.join(['%s'] * len(valid_semester_course_ids)))

            # Execute the query, first binding the department_id, then course_ids
            cursor.execute(query, (department_ids[student_department], *valid_semester_course_ids))   
            selected_courses = [course[0] for course in cursor.fetchall()]

            # Ensure selected courses is not empty
            if not selected_courses:
                continue

            # Insert courses for the student, avoiding duplicates
            for course_id in selected_courses:
                try:
                    cursor.execute(
                        """
                        INSERT INTO student_courses 
                        (student_id, course_id, semester, theory_marks, lab_marks, final_grade) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                            student_id,
                            course_id,
                            semester,
                            random.randint(0, 100),  # Random theory marks
                            random.randint(0, 100),  # Random lab marks
                            random.choice(['10', '9', '8', '7', '6', '5', '4', '3', '2', '1', 'Fail'])  # Random final grade
                        )
                    )
                except mysql.connector.errors.IntegrityError as e:
                    # Catch duplicate entry errors and skip this entry
                    if e.errno == 1062:
                        print(f"Duplicate entry for student_id {student_id} and course_id {course_id} in semester {semester}. Skipping...")
                        continue

        # Commit after each student's courses are inserted
        db.commit()
insert_student_courses()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------





# Define a function to insert available courses for each department
def insert_available_course(department_id, total_courses):
    existing_course_ids = set()
    for semester, course_ids in semester_courses.items():
        available_course = [course_id for course_id in course_ids if course_id not in existing_course_ids]
        available_course = available_course[:total_courses]
        for course_id in available_course:
            cursor.execute("INSERT INTO available_course (course_id, semester, department_id) VALUES (%s, %s, %s)", 
                           (course_id, semester, department_id))
            existing_course_ids.add(course_id)

# Insert available courses for each department
insert_available_course(department_ids['Computer Science'], 50)
insert_available_course(department_ids['Electronics and Communication'], 50)
insert_available_course(department_ids['Basic Sciences'], 15)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





for student_id in range(1, 1200):
    total_fees = 1500000
    fees_paid = random.uniform(0, total_fees)
    
    cursor.execute(
        """
        INSERT INTO fees (student_id, total_fees, fees_paid) 
        VALUES (%s, %s, %s)
        """,
        (student_id, total_fees, fees_paid)
    )

# Commit the transactions
db.commit()

# Close the connection
cursor.close()
db.close()





