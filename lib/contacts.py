from optparse import check_choice
from pstats import Stats
import sqlite3
from random import randint
def con_sql(uid): #Connecting to the user's own database
    con=sqlite3.connect('data/users/%i/data.db'%uid) 
    cur=con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS contacts (id INT PRIMARY KEY , fname TEXT , lname TEXT , number TEXT);''') #Create a table to hold the user's contacts if they don't exist
    cur.execute('''CREATE TABLE IF NOT EXISTS chats (chatid INT PRIMARY KEY , name TEXT , number TEXT , muid INT );''') #Create a table to hold the user's chat profile if it doesn't exist
    return con , cur

def check_exists_chat(uid , muid): #The function of checking the existence of dialogue
    con , cur = con_sql(uid) #Connecting to the user's own database
    sta = cur.execute('''SELECT muid FROM chats WHERE muid=%i; '''%muid) #Searching for the user's unique numerical ID in the conversation details section in the chats table
    sta = sta.fetchall()
    con.close()
    if sta==[]: #If there was no dialogue
        sta='not exist'
    else: #If there was a conversation
        sta='exist'
    return sta #Return the dialog presence or absence status
        
    
    

def contacts(uid): #The main function for managing the contacts section
    
    tar = input('\n Please select \n 1-addcontat  2-mycontacts \n 3-Back to MENU \n : ') #Which section does the user go to? Add a contact to the contact list
    if tar=='1': #If the user selects the add contact section
        con=sqlite3.connect('data/database.db')
        cur=con.cursor()
        number=input('send contact number: ') #Getting the number of the desired contact
        status=cur.execute('''SELECT id from users WHERE number='%s' '''%number) #Obtaining the unique numerical ID of the target audience, if any
        status=status.fetchone()
        con.close()
        if status is None: #If the user was not a member of our social network
            print('\n your conteacts not exists \n')
            contacts(uid)
        else: #If the user was a member of our social network
            fname=input('\n send first name : ') #Define a firstname for the audience
            lname=input('\n send last name : ') #Define a lastsname for the audience
            con , cur = con_sql(uid) #Connecting to the user's own database
            cur.execute('''INSERT INTO contacts(id , fname , lname , number) VALUES(%i ,'%s','%s','%s')'''%(status[0],fname,lname,number)) #Entering information in the contacts section in the user's own database
            con.commit()
            con.close()  
            contacts(uid) #After finishing adding, call the contacts section again to get the new target
                  
    elif tar=='2': #If the user chooses to see contacts
        con,cur = con_sql(uid) # Connecting to the user's own database
        list = cur.execute('''SELECT id,fname,lname,number FROM contacts;''') # Get all user contacts from a user specific database
        list = list.fetchall()
        con.close()
        nlist=[] #An empty list to add sorted contacts
        count=0
        
        for i in list: # Sorting contacts based on a number so that they can send messages to them, such as 1, 2,... and also display them.
            from datetime import datetime 
            count+=1
            nlist.append([str(count),i[0],i[1],i[2],i[3]]) #Add the sorted contact to the list defined above
            print(str(count)+'-'+'firstname: '+i[1]+'   lastname: '+i[2]+'   number: '+i[3]) #Display the contact to the user
        
        ntar = input('\n Please select \n 1-send message 2-check profile \n : ') #Getting the goal from the user for what they want to do with the audience
        if ntar=='1': #If the user wants to send a message to the contact (create a private chat)
            mokhtab = input('\n send number list contacts: ') #Which contact based on the number from the list of contacts sent to the user
            for i in nlist:
                if mokhtab in i:
                    sta=check_exists_chat(uid , i[1]) 
                    if sta=='exist': #If there is a conversation
                        print('\n This conversation exists, refer to the chats section \n')
                        contacts(uid)
                    else: #If there is no dialog (create a new dialog)
                        chatid=randint(1111111111111111,9999999999999999) #Creating a unique digital ID for conversation
                        con,cur = con_sql(uid)
                        cur.execute('''INSERT INTO chats(chatid , name , number, muid) VALUES(%i,'%s','%s',%i);'''%(chatid , i[2]+' '+i[3] , i[4] , i[1])) #Writing chat details for the chat section's user-specific database so that all chats can be easily found in the future
                        con.commit()
                        con.close()
                        con,cur = con_sql(i[1])
                        rlist = cur.execute('''SELECT id FROM contacts;''') #Obtaining the unique numerical ID of the target audience
                        rlist = rlist.fetchone()
                        
                        org=sqlite3.connect('data/database.db') 
                        corg=org.cursor()
                        mfl=corg.execute('''SELECT fname , lname , number FROM users WHERE id=%i'''%uid)
                        mfl=mfl.fetchall()
                        org.close()
                        
                        num = mfl[0][2]
                        mfl=mfl[0][0]+' '+mfl[0][1]
                        cur.execute('''INSERT INTO chats(chatid , name , number , muid) VALUES(%i,'%s','%s',%i);'''%(chatid , mfl , num , uid )) #Writing conversation information in the specific database of the target audience in their chats section
                        con.commit()
                        con.close()
                        
                        chatorg=sqlite3.connect('data/chats/%i.db'%chatid) #Creating a database to store chats in the chat folder The name of the chat ID is defined 
                        curorg=chatorg.cursor()
                        curorg.execute('''CREATE TABLE IF NOT EXISTS data (chatid INT PRIMARY KEY , person1 INT , person2 INT , timec TEXT , datec TEXT);''') # Create a table to hold the main conversation information except messages
                        curorg.execute('''CREATE TABLE IF NOT EXISTS conversation (nx INT ,fromuser INT , body TEXT , time TEXT , se%s TEXT , se%s TEXT );'''%(uid , i[1])) # Create a table to hold messages
                        curorg.execute('''INSERT INTO data(chatid , person1 , person2 , timec , datec) VALUES(%i,%i,%i,'%s','%s')'''%(chatid , int(uid),i[1] , datetime.now().strftime('%X') ,datetime.now().strftime('%x') )) #Enter the main information of the dialogue in the table
                        chatorg.commit()
                        chatorg.close()
                        print('\n your chat created  :) \n ') 
                        contacts(uid)

                    
                    
                else:
                    pass
        
        elif ntar=='2':
            print('\n This section will be added in the next update \n')
            contacts(uid)
    
    elif tar=='3' :  #Return to the previous menu
        return 'exit'    
                        
            
            
    else: #If the input was wrong, call the contact function again
        print('wrong! \n')
        contacts(uid)    
    
    

