
## Hello, welcome to the simple and light Colson project. I created this interesting social network 
# for coding practice and published it, and I tried to add comment to a large extent so that my codes 
# are very understandable, if there were any errors in the codes or If you have a suggestion, you can 
# email me. Thank you for listening to me:) Reza Heidary    mywebsite: rezaheidary.ir  mail:rezadev82@gmail.com
# colson project , https://github.com/rezaheidary82/colson  ###colson version 0.1 ###



from os import mkdir


num=input('Please send your phone number(091...): \n')  #Getting the user's phone number

yes=['y','Y','Yes','yes','YES','YEs'] #yes list for the email request section
no=['n','N','no','No','No'] #no list for the email request section

def con_sql():  #Function to connect to the main database
    import sqlite3
    from os import makedirs
    makedirs('data',exist_ok=True)  # Create the required folders if they do not exist
    makedirs('data/users',exist_ok=True)# Create the required folders if they do not exist
    makedirs('data/chats',exist_ok=True)# Create the required folders if they do not exist
    con=sqlite3.connect('data/database.db') # Connecting to the database and if it does not exist, creating the database and its location
    cur=con.cursor() #Creating a pointer to perform an operation on the database
    cur.execute('''CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY , fname TEXT , lname TEXT , number TEXT , mail TEXT , time TEXT , date TEXT);''') #Creating a table to store data according to our needs
    return con , cur #Return two variables for use in other functions

def olduser(num):  #If the user is old
    con , cur = con_sql()
    uid = cur.execute('''SELECT id FROM users WHERE number='%s' '''%num)
    uid= uid.fetchone()
    uid= uid[0]
    name = cur.execute('''SELECT fname FROM users WHERE id=%i '''%uid)
    name= name.fetchone()
    name= name[0]
    print('\n Hey %s , What do you want to do?(send it num)\n' %name)
    tar = input('1-contacts   2-chats  \n :')
    if tar=='1':
        from lib.contacts import contacts
        s = contacts(uid)
        if s=='exit':
            olduser(num)
    elif tar=='2':
        from lib.chats import chats
        s = chats(uid)
        if s=='exit':
            olduser(num)
    else:
        print('wrong! \n')
        olduser(num)

    
def newuser(num): #If the user is a new member, an account will be created for her
    import sqlite3 #Import required libraries
    from os import makedirs #Import required libraries
    from random import randint #Import required libraries
    from datetime import datetime #Import required libraries
    
    con , cur = con_sql() #connect to the main database
    uid = randint(11111111,99999999) #Creating a unique user ID for the user
    fname=input('send your first name: ') #Getting the firstname from the user
    lname=input('send your last name: ') #Getting the lastname from the user
    mail=input('do you want set mail: y/n: ') #Would you like to use email?
    if mail in yes : #If you want to receive the code by email
        mail=input('send your mail for me: ') #Getting email from the user
        cur.execute('''INSERT INTO users(id , fname , lname , number , mail , time , date) VALUES(%i,'%s','%s','%s','%s','%s','%s');''' % (uid , fname , lname, num , mail , datetime.now().strftime('%X') ,datetime.now().strftime('%x') )) #Adding user information to the main database
        con.commit() #Record changes
        con.close() #Close the database
        
        makedirs('data/users/%i'%uid) # Creating a special folder with the name of the user's unique numeric ID
        con=sqlite3.connect('data/users/%i/data.db'%uid) # Creating a dedicated database for the user in her dedicated folder
        cur=con.cursor() #Creating a pointer to perform an operation on the database
        cur.execute('''CREATE TABLE IF NOT EXISTS personaldata (id INT PRIMARY KEY , fname TEXT , lname TEXT , number TEXT ,mail TEXT, time TEXT, date TEXT);''') #Creating a table to store user account information in her own database
        cur.execute('''INSERT INTO personaldata(id , fname , lname , number , mail , time , date) VALUES(%i,'%s','%s','%s','%s','%s','%s');''' % (uid , fname , lname, num , mail , datetime.now().strftime('%X') ,datetime.now().strftime('%x') )) #Entering basic account information in the user's own database
        con.commit() #Record changes
        con.close() #Close the database
        olduser(num) #Now it is considered an old user, so call the old user function
        
    elif mail in no : #If you don't want to receive the code by email
        cur.execute('''INSERT INTO users(id , fname , lname , number , time , date) VALUES(%i,'%s','%s','%s','%s','%s')''' % (uid , fname , lname, num , datetime.now().strftime('%X') ,datetime.now().strftime('%x') ))
        con.commit()
        con.close()
        makedirs('data/users/%i'%uid)
        con=sqlite3.connect('data/users/%i/data.db'%uid)
        cur=con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS personaldata (id INT PRIMARY KEY , fname TEXT , lname TEXT , number TEXT , time TEXT, date TEXT);''')
        cur.execute('''INSERT INTO personaldata(id , fname , lname , number , time , date) VALUES(%i,'%s','%s','%s','%s','%s');''' % (uid , fname , lname, num , datetime.now().strftime('%X') ,datetime.now().strftime('%x') ))
        con.commit()
        con.close()
        olduser(num)
        
    else: #In case of wrong entry, call the new user function again
        print('wrong!!!')
        newuser(num)    
            
    
    
    

def login():  #The first function that is executed for the user to enter the social network
    from lib.sendcode import send #The first function that is executed for the user to enter the social network
    con , cur = con_sql() #Connect to the main database
    exist=cur.execute('''SELECT number FROM users WHERE number='%s' '''%num) #Getting the user number from the database if any
    
    if exist.fetchone() is None : # If the user number was not in the database, then she is a new user
        s=send(num) #Send a verification code to the user
        if s=='verify': #If the user passes the verification code step successfully
            newuser(num) 
            con.close()
    else: #If there is a user number in the database, then she is an old user
        s=send(num) #Send a verification code to the user
        if s=='verify': #If the user passes the verification code step successfully
            olduser(num)
            con.close()
            
            
login()




#colson version 0.1 #
