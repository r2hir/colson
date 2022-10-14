
from pstats import Stats


def con_sql(): #Connect to the main database
    import sqlite3
    con=sqlite3.connect('data/database.db')
    cur=con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY , fname TEXT , lname TEXT , number TEXT , mail TEXT , time TEXT , date TEXT);''')
    return con , cur


def send_mail(num , mail , verify): #The function of sending the code by email 
    import smtplib 
    
    ##Very important, you must enter your email service information in the account information below##
    
    sent_from = 'code@example.com'  #Email sender address
    password = 'passworld' #The sender's email password
    mail_server = 'mail.example.com' #email server smtp
    port = 465  #safe port?! Maybe:)
    
    ##Very important, you must enter your email service information in the account information above##

    to = [mail] #Email defined by the user
    
    subject = 'verify code' #Email subject
    
    body = ('your code is :'+str(verify)) #Message body part

    email_text = (
        """From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s"""
        % (sent_from, ", ".join(to), subject, body))

    smtp_server = smtplib.SMTP_SSL(mail_server, port)
    smtp_server.ehlo()
    smtp_server.login(sent_from, password) #Connect to email service
    smtp_server.sendmail(sent_from, to, email_text) #Send a confirmation code by email according to the data
    smtp_server.close() #Email service disconnection
    
    for i in range(1,6):   #Check account verification code
        check=input('send verify code: ')
        if verify==check: #If the verification code is correct
            s = 'verify'
            return s
        else: #If the verification code is wrong
            print('The entered code is incorrect!')
    print('Your number of mistakes is more than allowed') 


def send_sms(num , verify):  #Section of sending code via text message
    
    ##Very important, you must enter your SMS service information in the below account information##
    
    # import requests , http , json
    # hed= {'ACCEPT':'application/json' , 'X-API-KEY': '--------------------------'}
    # data={"TemplateId": "-----", 'Parameters':[{'Name':'CODE' , 'Value': verify}],"mobile":num }
    # response = requests.post('https://api.examplesms.com/v1/send/verify', json=data  ,headers=hed )
    
    ##Very important, you must enter your SMS service information in the above account information##
    
    print('The verification code is: '+verify)  #Very important, if you want the verification code to be printed on the user's page, keep this line, otherwise, delete this line.

    for i in range(1,6):   #Check account verification code
        check=input('send verify code: ')
        if verify==check: #If the verification code is correct
            s = 'verify'
            return s
        else: #If the verification code is wrong
            print('The entered code is incorrect!')
    print('Your number of mistakes is more than allowed') 
    
        
    

def send(num): #The main function is to check if the user has an email and creating a verification code and calling the send function via text message or email
    
    from random import randint
    
    con,cur=con_sql()
    verify=str(randint(1111,9999))  #verification code
    
    status=cur.execute('''SELECT mail FROM users WHERE number='%s' ''' %num)  #Get the user's email status
    status=status.fetchone()
    con.close()
    ma=['m' , 'mail' , 'MAIL' , 'Mail']
    sm=['sms','Sms','SMS','sm' ,'s']
    
    if status is None:  #If the user is registering in the media for the first time
        s= send_sms(num , verify)
        return s
    
    elif None in status : #If an email was not defined for the user
        s= send_sms(num , verify)
        return s
        
    
    else: #If the email is defined for the user
        #In the bottom line, the user is asked if he wants the code by text message or by email
        tar = input('Do you want to receive the code by email or text message(sms/mail): ')
        if tar in ma: #If he wants by email
            mail = status[0]
            s = send_mail(num , mail , verify)
            return s
        elif tar in sm : #If he wants by text message
            s= send_sms(num , verify)
            return s
        else:
            print('wrong! \n')
            send(num)
            



