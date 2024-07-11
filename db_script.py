#WE USED .PY INSTEAD OF .SQL
import sqlite3

try:
    db = sqlite3.connect('survey.db') 
    db.execute('PRAGMA foreign_keys = ON;')
    dbcursor = db.cursor()


    #SECTION 1 : TABLE CREATION SQL STATEMENTS
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++


    #TABLE 1: class
    #++++++++++++++++++++++++++
    #Class ID = 1A, 1B, 1C
    class_sql = '''
    CREATE TABLE IF NOT EXISTS class (
    class_id CHAR(2) PRIMARY KEY NOT NULL, 
    teacher_lname VARCHAR(50) NOT NULL,
    teacher_fname VARCHAR(50) NOT NULL
    );
    '''
 
    #TABLE 2: learner
    #++++++++++++++++++++++++++
    learner_sql = '''
    CREATE TABLE IF NOT EXISTS learner (    
    learner_id INTEGER PRIMARY KEY AUTOINCREMENT,
    learner_fname VARCHAR(50) NOT NULL,
    learner_lname VARCHAR(50) NOT NULL,
    class_id CHAR(2) NOT NULL,
    FOREIGN KEY (class_id) REFERENCES class(class_id),
    UNIQUE (learner_fname, learner_lname)
    );
    '''

    #TABLE 3: course_preference
    #++++++++++++++++++++++++++
    course_preference_sql = '''
    CREATE TABLE IF NOT EXISTS course_preference (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    learner_id INT NOT NULL,
    course_id CHAR(3) NOT NULL,
    FOREIGN KEY (learner_id) REFERENCES learner(learner_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
    );
    '''

    #TABLE 4: course
    #++++++++++++++++++++++++++
    #MAT for Mathematics, LAN for Language, SCI for Science, ART for Art and GYM for Gym
    course_sql = '''
    CREATE TABLE IF NOT EXISTS course (
    course_id CHAR(3) PRIMARY KEY NOT NULL,
    course_name VARCHAR(50) NOT NULL
    );
    '''


    #TABLE 5: social_preference
    #++++++++++++++++++++++++++
    social_preference_sql = '''
    CREATE TABLE IF NOT EXISTS social_preference (
    social_id INTEGER PRIMARY KEY AUTOINCREMENT,
    social_value DECIMAL(5, 2) NOT NULL,  
    social_name VARCHAR(255) NOT NULL
    );
    '''

    #TABLE 6: a_preferences
    #++++++++++++++++++++++++++
    a_preferences_sql = '''
    CREATE TABLE IF NOT EXISTS a_preferences (
    bond INTEGER PRIMARY KEY AUTOINCREMENT,
    social_id INTEGER NOT NULL,
    the_choosing_id INTEGER NOT NULL,
    chosen_id INTEGER NOT NULL,
    FOREIGN KEY (social_id) REFERENCES social_preference(social_id), 
    FOREIGN KEY (the_choosing_id) REFERENCES learner(learner_id),
    FOREIGN KEY (chosen_id) REFERENCES learner(learner_id)
    );
    '''

    #TABLE 7: b_preferences
    #++++++++++++++++++++++++++
    b_preferences_sql = '''
    CREATE TABLE IF NOT EXISTS b_preferences (
    bond INTEGER PRIMARY KEY AUTOINCREMENT,
    social_id INTEGER NOT NULL,
    the_choosing_id INTEGER NOT NULL,
    chosen_id INTEGER NOT NULL,
    FOREIGN KEY (social_id) REFERENCES social_preference(social_id),
    FOREIGN KEY (the_choosing_id) REFERENCES learner(learner_id),
    FOREIGN KEY (chosen_id) REFERENCES learner(learner_id)
    );
    '''

    #TABLE 8: c_preferences
    #++++++++++++++++++++++++++
    c_preferences_sql = '''
    CREATE TABLE IF NOT EXISTS c_preferences (
    bond INTEGER PRIMARY KEY AUTOINCREMENT,
    social_id INTEGER NOT NULL,
    the_choosing_id INTEGER NOT NULL,
    chosen_id INTEGER NOT NULL,
    FOREIGN KEY (social_id) REFERENCES social_preference(social_id),
    FOREIGN KEY (the_choosing_id) REFERENCES learner(learner_id),
    FOREIGN KEY (chosen_id) REFERENCES learner(learner_id)
    );
    '''






    #SECTION 2 : INSERTING SAMPLE DATA 
    #A) SOCIAL_PREFERENCE, CLASS, LEARNER, COURSE
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++


    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #SQL STATEMENT FOR INSERTING SAMPLE DATA
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
    data_social_preference = '''
    INSERT INTO social_preference (social_value, social_name) 
    VALUES 
        (1.00, 'First Best Friend'),
        (0.50, 'Second Best Friend'),
        (0.25, 'Third Best Friend');
    '''

    data_class = '''
    INSERT INTO class (class_id, teacher_lname, teacher_fname)
    VALUES 
        ('1A', 'Richard', 'Black'),
        ('1B', 'Jan', 'White'),
        ('1C', 'Magda', 'Christina');
    '''

    data_course = '''
    INSERT INTO course (course_id, course_name) 
    VALUES 
        ('SCI', 'SCIENCE'),
        ('MAT', 'MATHEMATICS'),
        ('LAN', 'LANGUAGE'),
        ('GYM', 'GYM'),
        ('ART', 'ART');
    '''

    data_learner = '''
    INSERT INTO learner (learner_fname, learner_lname, class_id)
    VALUES 
        ('Acharya', 'Puskar', '1A'), ('Muhammad', 'Saad', '1B'), ('Danielle', 'Raposon', '1C'),
        ('Emine', 'Burcu', '1C'), ('Akcadag', 'Bakiskan', '1C'),
        ('Jørgen', 'Tveranger', '1A'), ('Altantuya', 'Temuulen', '1C'),
        ('Arakelyan', 'Khazhak', '1C'), ('Rolf', 'Kristian', '1C'),
        ('Rolf', 'Benah', '1C'), ('Namukhula', 'Shikanga', '1C'),
        ('Ida', 'Høyland', '1C'), ('Bjerke', 'Aleksandra', '1B'),
        ('Blanco', 'Sofía', '1C'), ('Blankvoll', 'Eivind', '1C'),
        ('Blix', 'Karl', '1C'), ('Julie', 'Anethe', '1C'),
        ('Róbert', 'Andri', '1C'), ('Cao', 'Johnny', '1C'),
        ('Xuan', 'Hong', '1C'), ('Marion', 'Ara', '1C'),
        ('Cecilia', 'Marion', '1C'), ('Chanbat', 'Onpriya', '1B'),
        ('Cui', 'Qianqian', '1C'), ('Do', 'Ngan', '1C'),
        ('Duijst', 'Benjamin', '1C'), ('Ellefsen', 'Benedicte', '1B'),
        ('Elliott', 'Stephanie', '1C'), ('Elvebu', 'Tommy', '1C'),
        ('Engvik', 'Johan' , '1B'),  ('Filatova', 'Alena', '1C'),
        ('Fjørtoft', 'Elias', '1B'), ('Gaddipati', 'Anudeep', '1C'),
        ('Halvorsen', 'Magnus', '1B'), ('Harizi', 'Ani', '1A'),
        ('Haugedal', 'Peder', '1A'), ('Helberg', 'Jacob', '1A'),
        ('Hjelmeland', 'FilipJonas', '1A'), ('Hsieh', 'Anderson', '1A'),
        ('Huse', 'Erik', '1A'), ('Igesund', 'Viktor' , '1A'), ('Isabelle', 'Tambago', '1B'),
        ('Kalajoqa', 'Abdullah', '1A'), ('Kalekar', 'Aditya', '1B'), ('Karlsen', 'Casper', '1B'),
        ('Kjellesvik', 'Even', '1B'), ('Koch', 'Hagen', '1B'), ('Krechnak', 'Tomas', '1C'),
        ('Lade', 'Simon', '1B'), ('LIU', 'TIANJUN', '1B'), ('Lopez', 'Sæve', '1B'),
        ('Meschan', 'Berina', '1B'), ('Mishra', 'Advaita', '1B'), ('Mojapelo', 'Mogwang', '1B'),
        ('Muratbekova', 'Umidakhon', '1B'), ('Chykova', 'Daryna', '1B'),
        ('Emilie', 'Thuy', '1B'), ('Rodahl', 'Odin', '1A'),
        ('Nguyen', 'Hieu', '1A'), ('Northrup', 'Sofia', '1A'),
        ('Ormset', 'Vebjørn', '1A'), ('Paikar', 'Siam', '1A'), ('Peterson', 'William', '1B'),
        ('Pham', 'Joakim', '1A'), ('Pikelyte', 'Smilte', '1A'),
        ('Pires', 'Duro', '1C'), ('Zacky', 'Dhaffa', '1A'),
        ('Pylypenko', 'Oleksii', '1C'), ('Raibrová', 'Dominika', '1A'), ('Pasidu', 'Kesara', '1B'),
        ('Zara', 'Yuhana', '1A'), ('Audun', 'Meisingset', '1A'),
        ('Alexander', 'Johansson', '1A'), ('Shahbazi', 'Mahdi', '1A'),
        ('Shamtsyan', 'Daniel', '1A'), ('Sharif', 'Ali', '1A'),
        ('Lotfi', 'Aden', '1A'), ('Marib', 'Hasan', '1A'),
        ('Karoline', 'Gundersen', '1A'), ('Henrik', 'Pais', '1A'),
        ('Slåen', 'Kristian', '1A'), ('Sognli', 'Sigurd', '1B'),
        ('Song', 'Xianwen', '1B'), ('Vetle', 'Walekhwa', '1B'),
        ('Vetle', 'Nordli', '1B'), ('Adrian', 'Clark', '1B'),
        ('Louie', 'Carl', '1B'), ('Siddhant', 'Shailendra', '1B'),
        ('Turatsinze', 'Achille', '1B'), ('Tvedte', 'Christoffer', '1B'),
        ('Taalaibek', 'Aizhan', '1B'), ('Nicole', 'Nkeiruka', '1B'), ('Martine', 'Hansen', '1B'),
        ('Seyed', 'Hassan', '1B'), ('Vegge', 'Marta', '1B'), ('Jasminka', 'Poetlover', '1A'),        
        ('Zorica', 'Sutevska', '1B'), ('Petros', 'Huskovic', '1A'), ('Nnamdi', 'Azikiwe', '1A'),
        ('Johnson', 'Ironsi', '1A'), ('Goran', 'Petrovski', '1C'), ('Ayub', 'Lodhi', '1B'),
        ('Goodluck', 'Mohammed', '1C'), ('Olusegun', 'Obasanjo', '1C'), ('Lizeth', 'Tapia', '1A'),
        ('Shehu', 'Shagari', '1C'), ('Leleti', 'Khumalo', '1C'), ('Zou-Poo', '(张)', '1B'),
        ('Ibrahim', 'Babangida', '1C'), ('Ernest', 'Shonekan', '1C'), ('Håvard', 'Tho', '1B'),
        ('Moses', 'Cleo', '1B'), ('Sani', 'Abacha', '1C'), ('Chung-lee', '(刘)', '1B'),
        ('Zoe', 'Abubakar', '1C'), ('Umaru', 'Yar-Adua', '1C'), ('Marija', 'Slavkovik', '1A'),
        ('Joseph', 'Bheki', '1C'), ('Chen-Lee', '(陈)', '1B'),
        ('Muhammadu', 'Buhari', '1B'), ('kaguta', 'Museveni', '1A'), ('Quarantine', 'Hansen', '1C'),
        ('Li-chen', '(李)', '1A'), ('Patricia', 'Kiso', '1B'),  ('Yang-Poo', '(杨)', '1B'),
        ('Huang-Huang', '(黄)', '1A'), ('Poske', 'Larsen', '1C'), ('Yakubu', 'Gowon', '1C'),
        ('Zhao-Mao', '(赵)', '1A'), ('Angellphina', 'Kiso', '1A'), ('Masana', 'Kiso', '1C'),
         ('William', 'Salasia', '1C'), ('Amina', 'Nalubega', '1C'),
         ('Daniel-Arap', 'Moi', '1B'), ('Shoni', 'Leo', '1A'), ('Wang-Poo', '(王)', '1A');
    '''

    #SECTION 3 : EXECUTING 
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
 


    #EXECUTE ALL THE SQL STATEMENTS  FOR CREATING TABLES
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    dbcursor.execute(class_sql)
    dbcursor.execute(learner_sql)
    dbcursor.execute(course_preference_sql)
    dbcursor.execute(course_sql)    
    dbcursor.execute(social_preference_sql)
    dbcursor.execute(a_preferences_sql)
    dbcursor.execute(b_preferences_sql)
    dbcursor.execute(c_preferences_sql)
   
    #EXECUTE ALL THE SQL STATEMENTS  FOR INSERTING SAMPLE DATA IN THE TABLES
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
    dbcursor.execute(data_class)
    dbcursor.execute(data_course)
    dbcursor.execute(data_learner)
    dbcursor.execute(data_social_preference)    


 

    #COMMIT THE TRANSACTIONS
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
    db.commit()
    print("Database successfully Created")

except Exception as e:
    print(f'An {e} Error occured while creating the Database')
    print('Can not create another Database with the Same Name survey.db')
    print('If the database already Exists, delete it then rerun this command')

finally: 
    dbcursor.close()
    db.close()
