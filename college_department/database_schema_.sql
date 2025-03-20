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

ALTER TABLE department_courses
ADD COLUMN course_image_url VARCHAR(255);

UPDATE department_courses
SET course_image_url = 'https://www.globalfocusmagazine.com/wp-content/uploads/2020/02/Engaging_with_technology-2048x1365.jpg' where course_id <100000;

ALTER TABLE department_courses
ADD COLUMN Course_Coordinator INT,
ADD FOREIGN KEY (Course_Coordinator) REFERENCES faculty(faculty_id);

-- ALTER TABLE department_courses DROP FOREIGN KEY department_courses_ibfk_2;

-- ALTER TABLE department_courses DROP COLUMN Course_Coordinator;


DELIMITER //

CREATE PROCEDURE AssignCourseCoordinator()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE dept_id, crs_id, fac_id INT;

    -- Cursor to loop through each department and course
    DECLARE dept_course_cursor CURSOR FOR
        SELECT department_id, course_id FROM department_courses;

    -- Handler to exit the loop
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN dept_course_cursor;

    read_loop: LOOP
        FETCH dept_course_cursor INTO dept_id, crs_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Find a suitable faculty member based on the department and course coordinator count
        SELECT df.faculty_id INTO fac_id
        FROM department_faculty AS df
        JOIN faculty AS f ON df.faculty_id = f.faculty_id
        WHERE df.department_id = dept_id
          AND f.department_id = dept_id
          AND (SELECT COUNT(*) FROM department_courses WHERE Course_Coordinator = f.faculty_id) < 10
        ORDER BY RAND() -- Randomly select a faculty member
        LIMIT 1;

        -- Update the department_courses table with the selected faculty member as the Course_Coordinator
        IF fac_id IS NOT NULL THEN
            UPDATE department_courses
            SET Course_Coordinator = fac_id
            WHERE department_id = dept_id AND course_id = crs_id;
        END IF;
    END LOOP;

    CLOSE dept_course_cursor;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS AssignCourseCoordinator;


CALL AssignCourseCoordinator();

ALTER TABLE department_courses
ADD COLUMN Duration INT,
ADD COLUMN Lectures INT,
ADD COLUMN Quizzes INT;

UPDATE department_courses
SET Duration = FLOOR(10 + (RAND() * (40 - 10))),
    Lectures = FLOOR(20 + (RAND() * (40 - 20))),
    Quizzes = FLOOR(2 + (RAND() * (5 - 2))) where department_id < 1000;


CREATE VIEW department_course_student_counts AS
SELECT 
    dc.department_id,
    dc.course_id,
    dc.course_name,
    COUNT(sc.student_id) AS student_count
FROM 
    department_courses AS dc
LEFT JOIN 
    student_courses AS sc ON dc.course_id = sc.course_id
GROUP BY 
    dc.department_id, dc.course_id;




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
    total_fees DECIMAL(10,2) default 1500000.00,
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

