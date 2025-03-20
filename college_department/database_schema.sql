create database college_db ;
use college_db ;
CREATE TABLE departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    num_students INT DEFAULT 0,        -- Number of students in the department
    num_faculties INT DEFAULT 0,       -- Number of faculties in the department
    num_labs INT DEFAULT 0,            -- Number of labs in the department
    num_courses INT DEFAULT 0
);

CREATE TABLE faculty (
    faculty_id INT AUTO_INCREMENT, 
    name VARCHAR(100), 
    email VARCHAR(255) NOT NULL UNIQUE, 
    graduation_course VARCHAR(255) NOT NULL, 
    graduation_complete_year YEAR NOT NULL, 
    post_graduation_specialisation VARCHAR(255) NOT NULL, 
    post_graduation_complete_year YEAR NOT NULL, 
    phd_research VARCHAR(255), 
    phd_complete_year YEAR NOT NULL, 
    graduation_college VARCHAR(255) NOT NULL, 
    post_graduation_college VARCHAR(255) NOT NULL, 
    phd_college VARCHAR(255) NOT NULL, 
    age INT NOT NULL CHECK (age > 25), 
    department_id INT, 
    salary INT, 
    PRIMARY KEY (faculty_id), 
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE department_courses (
    department_id INT, 
    course_id INT,
    course_name VARCHAR(255) , 
    no_of_faculties INT, 
    credits INT, 
    FOREIGN KEY (department_id) REFERENCES departments(id), 
    PRIMARY KEY (department_id, course_id)
);

CREATE TABLE department_faculty (
    department_id INT, 
    faculty_id INT,
    course_id INT,
    FOREIGN KEY (department_id, course_id) REFERENCES department_courses(department_id, course_id), 
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id), 
    PRIMARY KEY (department_id, faculty_id, course_id)
);

CREATE TABLE course_prerequisite (
    department_id INT, 
    course_id INT, 
    prerequisite_course_id INT, 
    FOREIGN KEY (department_id, course_id) REFERENCES department_courses(department_id, course_id), 
    FOREIGN KEY (department_id, prerequisite_course_id) REFERENCES department_courses(department_id, course_id), 
    PRIMARY KEY (course_id, prerequisite_course_id)
);

CREATE TABLE student(
	student_id INT AUTO_INCREMENT PRIMARY KEY, 
    name VARCHAR(50) NOT NULL, 
    email VARCHAR(50) NOT NULL UNIQUE, 
    branch VARCHAR(100) NOT NULL, 
    year_of_joining YEAR NOT NULL, 
    graduation_year YEAR AS (year_of_joining + 4) STORED, 
    semester INT, 
    FOREIGN KEY (branch) REFERENCES departments(name)
);

CREATE INDEX idx_course_id ON department_courses(course_id);

CREATE TABLE student_courses(
	student_id INT, 
    course_id INT, 
    theory_marks INT, 
    lab_marks INT, 
    final_grade ENUM('10','9','8','7','6','5','4','Fail') NOT NULL, 
    semester INT NOT NULL, 
    FOREIGN KEY (student_id) REFERENCES student(student_id), 
    FOREIGN KEY (course_id) REFERENCES department_courses(course_id), 
    PRIMARY KEY (student_id, course_id)
);

CREATE TABLE available_course (
	semester INT NOT NULL, 
    course_id INT, 
    department_id INT , 
    FOREIGN KEY (course_id) REFERENCES department_courses(course_id), 
    foreign key (department_id) REFERENCES departments(id) ,
    PRIMARY KEY (semester, course_id , department_id)
);

CREATE TABLE fees (
    student_id int,
    total_fees DECIMAL(10,2) NOT NULL,
    fees_paid DECIMAL(10,2) DEFAULT 0,
    remaining_fees DECIMAL(10,2) AS (total_fees - fees_paid) STORED,
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    PRIMARY KEY (student_id)
);

SELECT count(*) FROM student_courses;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    name VARCHAR(100), 
    email VARCHAR(100) UNIQUE, 
    password VARCHAR(255), 
    department ENUM('Computer Science', 'Electronics and Communication', 'Basic Science', 'None of the above'),
    user_type ENUM('Faculty', 'Student', 'Supporting Staff', 'Management'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME DEFAULT NULL
);

CREATE TABLE admin (
	name VARCHAR(255) ,
    email VARCHAR(100) UNIQUE,
    user_type VARCHAR(255), 
    rights VARCHAR(255),
    FOREIGN KEY (email) REFERENCES users(email)
);

