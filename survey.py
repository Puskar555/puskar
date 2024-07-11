#DO NOT TYPE ANYTHING ABOVE
import sqlite3
from sqlite3 import IntegrityError
import matplotlib
matplotlib.use('Agg')  # Set matplotlib to non-interactive state
import matplotlib.pyplot as plt  # Import matplotlib's pyplot module
from flask import Flask, render_template, request, redirect, url_for, flash, g
import os
from flask import send_from_directory
import datetime
import logging
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#END OF IMPORTS SECTION
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Project Assignment
#EBA3420 Databases, Spring 2024
#BI Norwegian Business School
#Hand-out date and time: 24-04-2024, 09:00
#Hand-in date and time: 08-05-2024, 12:00
#Group size: 1 - 3 students
#Weight: 60% of the total grade
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#DATABASE VARIABLE
DATABASE = 'survey.db'
app = Flask(__name__)
#CREATE A SECRET KEY
app.secret_key = 'c428a1a33258df654280e6bc8832c138'
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#CONNECT TO THE DATABASE USING THE SPECIAL OBJECT g FROM FLASK
def getDB():
    dbCONN = getattr(g, '_database', None)
    if dbCONN is None:
        dbCONN = g._database = sqlite3.connect(DATABASE)
        dbCONN.row_factory = sqlite3.Row
        dbCONN.execute('PRAGMA foreign_keys=ON')
    return dbCONN
#TO INITIATE A CONNECTION, WE SHALL SIMPLY CALL THIS FUNCTION

@app.teardown_appcontext
def closeDB(exception):
    dbCONN = getattr(g, '_database', None)
    if dbCONN is not None:
        dbCONN.close()
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++







#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#START OF ROUTE DECORATORS
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#1. THE INDEX ROUTE DECORATOR MAPPING THE FUNCTION TO INDEX.HTML
@app.route('/')
@app.route('/index')
def index():

    def get_indexData(class_ids):
        db = getDB()
        with db:
            cursor = db.cursor()
            try:       
                index_data_sql = f'''
                SELECT 
                learner.class_id AS id,
                class.teacher_fname AS fname,
                class.teacher_lname AS lname,
                COUNT(DISTINCT learner.learner_id) AS total_learners,
                COUNT(DISTINCT course_preference.learner_id) AS engaged_learners,
                COUNT(DISTINCT learner.learner_id) - COUNT(DISTINCT course_preference.learner_id) AS pending
                FROM learner
                JOIN class ON learner.class_id = class.class_id
                LEFT JOIN course_preference ON learner.learner_id = course_preference.learner_id
                WHERE learner.class_id = '{class_ids}'
                GROUP BY learner.class_id;
                '''
                cursor.execute(index_data_sql)
                index_data = cursor.fetchall()
                return index_data
            except Exception as e:
                print(f"An error occurred: {e}")
    data = [get_indexData('1A'), get_indexData('1B'), get_indexData('1C')]

    return render_template('index.html', data=data)








#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#2. THE Questionnaire ROUTE DECORATOR MAPPING THE FUNCTION TO Questionnaire.HTML
@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    div1 = '' #Message Dash board for FORM!
    div2 = False #Visibility status for FORM1
    data_from_form1 = [] #Data Collected from FORM1
    div3 =  '' #Message Dash board for FORM2
    div4 = False #Visibility status of the Progress bar and second form

    students = []  
    teachers = []  
    courses = []   
    friends = []
    class_id = []
    teacherLName = []
    teacherFName = []

    if request.method == 'POST':
        db = getDB()
        with db:
            cursor = db.cursor()
            #START code Logic for when the submit button ON FORM1 is clicked
            if 'form1_btn' in request.form: 
                if 'learner' in request.form:
                    learner_data = request.form['learner'].split('|')
                    learnerID = learner_data[0]
                    lName = learner_data[1]
                    fName = learner_data[2]
                    learner_classID = learner_data[3]
                    
                if 'teacher' in request.form:
                    teacher_data = request.form['teacher'].split('|')
                    class_id = teacher_data[0]
                    teacherLName = teacher_data[1]
                    teacherFName = teacher_data[2]
                if 'course' in request.form:
                    course_data = request.form['course'].split('|')
                    courseID = course_data[0]
                    course_name = course_data[1]
                #Store Data from Form1
                data_from_form1 = [learnerID, lName, fName, learner_classID, class_id, teacherLName, teacherFName, courseID, course_name]

                # Check if the learner has already taken the survey
                cursor.execute('SELECT COUNT(*) FROM course_preference WHERE learner_id = ?', (learnerID,))
                if cursor.fetchone()[0] > 0:
                    div1 = '<i class="bi bi-dash-circle-fill"></i> ACCESS DENIED! You are not allowed to retake the Survey. One Trial is Enough!'
                else:
                    #Check if the selected teacher matches the learner's class   
                    if learner_classID != class_id:
                        div1 = f'''
                        <h3><i class="bi bi-sign-stop-fill redden"></i> WARNING! You are a 
                        learner in {learner_classID}. But, you selected teacher {teacherLName} {teacherFName}
                        who is responsible for {class_id}. Please try again!</h3>
                        '''
                        students, teachers, courses = get_form1_data()  # Reload form data
                        div2 = True  # Make div2 visible
                    else:
                        div2 = False  # Make div2 invisible
                        div4 = True # Make div4 for Progress Report Visible
                        #Customize a message to send back to the HTML document div1
                        div1 = f'''<div class='alert alert-info add-padding'><h3>
                        <i class="bi bi-check-circle-fill redden"></i> CONGRATULATIONS! {lName} {fName}, 
                        you are Close to completing all the necessary
                        questions set in this Questionnaire.</h3>
                        <div class="progress"><div class="progress-bar" style="width:52%">52% Completed</div></div>
                        </div>'''
                        #Populate Form 2 with students from the same Class as The Learner. But Remove the learner
                        students = get_classmates_data(learnerID, learner_classID)
                        #Populate DIV4 to show a message on how to proceed
                        div3 = f'''<div><img class='teacher-photo' src="../static/images/friends.png">
                        </div>'''
                

            #END code Logic for when the submit button ON FORM1 is clicked
            #START code Logic for when the form2_btn submit button is clicked
            if 'form2_btn' in request.form: 
                data_from_form1 = get_stored_form1Data()
                learnerID = data_from_form1[0]
                learner_classID = data_from_form1[3]
                courseID = data_from_form1[7]
                #Make Div1 and Div2 Invinsible
                div1 = ''
                div2 = False
                #Test to make sure each column has a unique selected friend
                if 'friend1' in request.form:
                    friend1_data = request.form['friend1'].split('|')
                    f1_chosen_id = friend1_data[0]
                    f1_class_id = friend1_data[3]
                    f1_social_id = 1
                if 'friend2' in request.form:
                    friend2_data = request.form['friend2'].split('|')
                    f2_chosen_id = friend2_data[0]
                    f2_class_id = friend2_data[3]
                    f2_social_id = 2
                if 'friend3' in request.form:
                    friend3_data = request.form['friend3'].split('|')
                    f3_chosen_id = friend3_data[0]
                    f3_class_id = friend3_data[3]
                    f3_social_id = 3
                if (f1_chosen_id == f2_chosen_id) or (f1_chosen_id == f3_chosen_id) or (f2_chosen_id == f3_chosen_id):
                    div3 = f'''
                    <div class='add-padding'><h3><i class="bi bi-sign-stop-fill redden"></i> WARNING! You can not choose a friend more than once in any of the categories.
                    Try Again. Uniquely select your best friend in column 1 first, then select your second best friend in column 2, 
                    and finally, select your 3rd best friend in column 3</h3>
                    <div class="progress"><div class="progress-bar" style="width:52%">52% Completed</div></div>
                    </div>
                    '''
                    div4 = True
                    #RE-Populate Form 2 with students from the same Class as The Learner. But Remove the learner
                    students = get_classmates_data(learnerID, learner_classID)
                else:
                    #Time to commit the database
                    try:                        
                        #INSERT DATA IN a_preferences TABLE                            
                        social_preference1 = (f1_social_id, learnerID, f1_chosen_id)
                        social_preference2 = (f2_social_id, learnerID, f2_chosen_id)
                        social_preference3 = (f3_social_id, learnerID, f3_chosen_id)

                        if f1_class_id == f2_class_id == f3_class_id == '1A':
                            bond_123_sql = '''
                            INSERT INTO a_preferences 
                            ('social_id', 'the_choosing_id', 'chosen_id') VALUES (?, ?, ?)
                            '''
                        elif f1_class_id == f2_class_id == f3_class_id == '1B':
                            bond_123_sql = '''
                            INSERT INTO b_preferences 
                            ('social_id', 'the_choosing_id', 'chosen_id') VALUES (?, ?, ?)
                            '''
                        else:
                            bond_123_sql = '''
                            INSERT INTO c_preferences 
                            ('social_id', 'the_choosing_id', 'chosen_id') VALUES (?, ?, ?)
                            '''

                        course_preference_sql = '''
                        INSERT INTO course_preference ('learner_id', 'course_id') VALUES (?, ?)
                        '''

                        cursor.execute(bond_123_sql, social_preference1)
                        cursor.execute(bond_123_sql, social_preference2)
                        cursor.execute(bond_123_sql, social_preference3)
                        cursor.execute(course_preference_sql, (learnerID, courseID))
                        
                        db.commit()
                        return redirect(url_for('successful'))
                    except Exception as e:
                        print(f'Error Saving Data: {e}')
                        db.rollback()
                    finally:
                        cursor.close()

        #Close the cursor
        cursor.close()
    #IF the Method is NOT POST [What happens when this route is inialized]
    else:
        students, teachers, courses = get_form1_data()
        div2 = True  # Make div2 visible

    return render_template('questionnaire.html', div1=div1, div2=div2, div3=div3, div4=div4, students=students, teachers=teachers, courses=courses, data_from_form1=data_from_form1)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#None Route Function To Fetch student, teacher, and course data from the database
def get_form1_data():
    db = getDB()
    with db:
        cursor = db.cursor()
        try:
            # Fetch student, teacher, and course data
            students = cursor.execute('SELECT * FROM learner').fetchall()
            teachers = cursor.execute('SELECT * FROM class').fetchall()
            courses = cursor.execute('SELECT * FROM course').fetchall()
            return students, teachers, courses
        except Exception as e:
            print(f'Error fetching data: {e}')
            return [], [], []
        finally:
            cursor.close()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#None Route Fuction to get deactivated data from the second form when the Submit button is clicked
def get_stored_form1Data():
    try:
        learnerID = request.form.get('learnerID', '')
        lName = request.form.get('lName', '')
        fName = request.form.get('fName', '')
        learner_classID = request.form.get('learner_classID', '')
        class_id = request.form.get('class_id', '')
        teacherLName = request.form.get('teacherLName', '')
        teacherFName = request.form.get('teacherFName', '')
        courseID = request.form.get('courseID', '')
        course_name = request.form.get('course_name', '')
        #Initialize a list to store
        data_from_form1 = []
        #Populate
        data_from_form1 = [learnerID, lName, fName, learner_classID, class_id, teacherLName, teacherFName, courseID, course_name]
        return data_from_form1
    except Exception as e:
        print(f'Error fetching data: {e}')
        return []

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#None Route Fuction to get list of classmates excluding the person taking the Questionnaire
def get_classmates_data(interviewee_id, interviewee_classID):
        #Connect to the database
        db = getDB()
        with db:
            cursor = db.cursor()
            #Populate Form2 with students from the same Class as The Learner being interviewed
            #The learner Shouldn't be in the list
            try:
                # Fetch All Students from each class
                students_sql = 'SELECT * FROM learner WHERE learner_id != ? AND class_id == ?'
                students = cursor.execute(students_sql, (interviewee_id, interviewee_classID)).fetchall()
                return students
            except Exception as e:
                print(f'Error fetching data: {e}')
                return []
            finally:
                cursor.close()






# End of Questionnaire






#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#3. THE CONGRATULATORY ROUTE DECORATOR MAPPING THE FUNCTION TO successful.html
@app.route('/questionnaire/success')
def successful():
    
    return render_template('successful.html')
  








#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#4. THE SUMMARY ROUTE DECORATOR MAPPING THE FUNCTION TO SUMMARY.HTML
@app.route('/summary')
def summary():
    # Call the function to retrieve course popularity    
    mutual_friends_1a = get_mutual_friends("a_preferences")
    mutual_friends_1b = get_mutual_friends("b_preferences")
    mutual_friends_1c = get_mutual_friends("c_preferences")

    courses = get_course_preference()
    #Labels and Values for the Graph
    course_label = []
    course_count = []
    for i in courses:
        course_label.append(i['course'])
        course_count.append([i['score']])
    course_count = [item[0] for item in course_count]

    #Draw a graph using non interactive matplotlib and save it on the system
    #Check if the image file exists
    image_path = 'static/images/reports/graphs/courses.png'
    if os.path.exists(image_path):
        #If it exists, delete it
        os.remove(image_path)

    #Generate the new graph (bar chart)
    fig = plt.figure(figsize=(8, 6)) 
    plt.bar(course_label, course_count)
    plt.title('Course Likings', color='brown')
    plt.xlabel('Courses', color='blue')
    plt.ylabel('Likings', color='blue')

    #Save the graph image
    plt.savefig(image_path)

    #Close the plot to release memory
    plt.close()

    # Call the function with different table names
    class_1a = get_learner_likes('a_preferences')
    class_1b = get_learner_likes('b_preferences')
    class_1c = get_learner_likes('c_preferences')

    return render_template('summary.html', courses=courses, mutual_friends_1a=mutual_friends_1a, mutual_friends_1b=mutual_friends_1b, mutual_friends_1c=mutual_friends_1c, class_1a=class_1a, class_1b=class_1b, class_1c=class_1c)



#A Function to all the 3 Results table of Mutual Friends alongside Favourite Courses
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# NON ROUTE function to retrieve learners who chose each other from the database
# get MUTUAL FRIENDS from a_preferences, b_preferences, c_preferences by calling the 

#Function and changing the variable to the names table
def get_mutual_friends(class_table):
    try:
        db = getDB()  
        with db:
            cursor = db.cursor()
            mutual_sql = f'''
            SELECT DISTINCT
                CASE WHEN the_choosing_id < chosen_id THEN learner_info_1 ELSE learner_info_2 END AS learner_info,
                CASE WHEN the_choosing_id < chosen_id THEN learner_info_2 ELSE learner_info_1 END AS friend_info
            FROM (
                SELECT
                    a1.the_choosing_id,
                    a1.chosen_id,
                    CONCAT(l1.learner_fname, ' ', l1.learner_lname) || ' - ' || c1.course_name AS learner_info_1,
                    CONCAT(l2.learner_fname, ' ', l2.learner_lname) || ' - ' || c2.course_name AS learner_info_2
                FROM {class_table} AS a1
                JOIN {class_table} AS a2 ON a1.the_choosing_id = a2.chosen_id AND a1.chosen_id = a2.the_choosing_id
                JOIN  learner AS l1 ON a1.the_choosing_id = l1.learner_id
                JOIN  learner AS l2 ON a1.chosen_id = l2.learner_id
                JOIN  course_preference AS cp1 ON a1.the_choosing_id = cp1.learner_id
                JOIN  course_preference AS cp2 ON a1.chosen_id = cp2.learner_id
                JOIN  course AS c1 ON cp1.course_id = c1.course_id
                JOIN  course AS c2 ON cp2.course_id = c2.course_id
            ) AS mutual_friends

            '''
            mutual_data = cursor.execute(mutual_sql).fetchall()
        return mutual_data
    except Exception as e:
        print(f"Error occurred while retrieving mutual friends: {e}")
        return []







#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#NONE ROUTE function to retrieve course popularity from the database
def get_course_preference():
    try:
        db = getDB()
        with db:
            cursor = db.cursor()
            # Retrieve course popularity
            course_sql = '''
            SELECT c.course_name AS course, COUNT(*) AS score
            FROM course AS c
            JOIN course_preference AS p ON c.course_id = p.course_id
            GROUP BY c.course_name
            ORDER BY score DESC
            '''
            cursor.execute(course_sql)
            course_count = cursor.fetchall()
            return course_count
    except Exception as e:
        print(f"Error occurred: {e}")
        return []
    
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#NONE ROUTE FUNCTION TO retrieve most liked learners in each class
def get_learner_likes(table_name):
        try:
            db = getDB()
            with db:
                cursor = db.cursor()
                #SQL query with table_name inserted
                sql_query = f'''
                SELECT l.learner_id, l.learner_fname, l.learner_lname, SUM(b.social_value) AS total_social_value
                FROM {table_name} AS c
                JOIN social_preference AS b ON c.social_id = b.social_id
                JOIN learner AS l ON c.chosen_id = l.learner_id
                GROUP BY l.learner_id
                ORDER BY 
                    total_social_value DESC
                LIMIT 3
                '''
                cursor.execute(sql_query)
                bond_count = cursor.fetchall()
                return bond_count
        except Exception as e:
            print(f"Error occurred: {e}")
            return []
    


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#5. THIS ROUTE IS NOT EXAMINABLE BUT WE USED IT FOR ADDING NEW STUDENTS SO AS 
#TO EXPAND THE NUMBER OF RECORDS TO ENSURE THAT THE SUMMARY PROVIDE MEANINGFUL INSIGHTS
@app.route('/adminstration/admins', methods=['GET', 'POST'])
def admins():
    message = None
    if request.method == 'POST':    
        db = getDB()
        with db:
            cursor = db.cursor()
            try:
                if 'addbtn' in request.form:
                    fname = request.form['fname']
                    lname = request.form['lname']
                    class_id = request.form['class_id'] 
                    learner_sql = '''
                    INSERT INTO learner (learner_fname, learner_lname, class_id) 
                    VALUES (?, ?, ?)
                    '''
                    cursor.execute(learner_sql, (fname, lname, class_id))
                    db.commit()
                    message = f"<div class='jumbotron'><h3><i class='bi bi-database-fill-add redit'></i> {class_id} - {lname} {fname} Added Successfully</h3></div>"
            except IntegrityError as e:
                print(f"Error adding Learner: {e}")
                db.rollback()
                message = f"<div class='jumbotron'><h3 class='redit'><i class='bi bi-database-slash redit'></i> {class_id} - {lname} {fname} Addition Failed!</h3></div>"
            finally:
                cursor.close()
        
    return render_template('admins.html', message=message)

  


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #END OF THE APPLICATION
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#DO NOT TYPE ANYTHING BENEATH THIS
if __name__ == '__main__':
    app.run(debug=True)