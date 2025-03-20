from faker import Faker 
import random 
import mysql.connector
# import database_generation_script

faker = Faker()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vidhya@2004",
    database="college_db"
)

cursor = db.cursor()

faculty_id = [i for i in range(1, 76)]

for j in faculty_id:
    cursor.execute("""SELECT department_id FROM faculty WHERE faculty_id = %s""", (j,))
    user = cursor.fetchone()
    print(user[0])
    
    if user:
        department_id = user[0]  # since cursor.fetchone() returns a tuple, use the first element
        
        if department_id == 2:
            course_ids = random.sample(range(1, 50), 5)
            
            for course_id in course_ids:
                cursor.execute(
                    """INSERT INTO department_faculty (department_id, faculty_id, course_id) 
                    VALUES (%s, %s, %s)""", 
                    (department_id, j, course_id)
            )
        
        elif department_id ==1:
            course_ids = random.sample(range(1, 51), 5)
            
            for course_id in course_ids:
                cursor.execute(
                    """INSERT INTO department_faculty (department_id, faculty_id, course_id) 
                    VALUES (%s, %s, %s)""", 
                    (department_id, j, course_id)
                )
        
        else:
            course_ids = random.sample(range(1, 21), 5)
            
            for course_id in course_ids:
                cursor.execute(
                    """INSERT INTO department_faculty (department_id, faculty_id, course_id) 
                    VALUES (%s, %s, %s)""", 
                    (department_id, j, course_id)
            )
    
    # Commit once per faculty member after all course_ids are inserted
    db.commit()

db.close()  # Close the connection after the work is done


