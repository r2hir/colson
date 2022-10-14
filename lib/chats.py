import sqlite3

def con_sql(uid):#Connecting to the user's own database
    con=sqlite3.connect('data/users/%i/data.db'%uid)
    cur=con.cursor()
    return con , cur

def write(chatid , body , uid , nx): #The function of writing messages in the chat database
    from datetime import datetime
    con=sqlite3.connect('data/chats/%i.db'%chatid) #Open chat database using chat ID
    cur=con.cursor()
    nx+=1 #
    cur.execute('''INSERT INTO conversation VALUES(%i ,'%s','%s','%s',0 , 0);'''%(nx , uid , body, datetime.now().strftime('%X '+'%x')))
    con.commit() 
    con.close()

def read(chatid , uid , mname): #The function of reading new messages
    con=sqlite3.connect('data/chats/%s.db'%chatid)
    cur=con.cursor()
    list = cur.execute('''SELECT * FROM conversation WHERE se%s=0 ;'''%uid) #Receiving messages whose se%s are zero (zero means not seen and when seen, it changes to one)
    list = list.fetchall()
    nx = cur.execute('''SELECT MAX(nx) FROM conversation;''') # Each message has a number to preserve order, this returns the last number for rewriting
    nx = cur.fetchone()
    for i in list : #After receiving new messages, their visit status should change from 0 to 1
        cur.execute('''UPDATE conversation SET se%s=1 ; '''%uid)
        con.commit()
    con.close()
    
    for i in list : # Display new messages to the user
        if i[1] == uid :
            pass
        else:
            print('['+str(mname)+'] '+str(i[2])+'  {'+str(i[3])+'}')
    
    if type(nx[0]) is int: #If the message number is an integer, then it is not the first message and sends the last message number
        return nx[0]
    
    else: # If it is the first message, it sets the SMS number to zero and returns it
        nx = 0 
        return nx
    

def chats(uid): #The main chat function
    con , cur = con_sql(uid)
    list = cur.execute('''SELECT * FROM chats;''') #Getting a list of all user conversations
    list = list.fetchall()
    con.close()
    count= 0
    nlist= [] #An external list to list sorted dialogs
    for i in list: # Arrange conversations
        count+=1
        mname = i[1]
        nlist.append([str(count),i[0],i[1],i[2],i[3]]) #Add conversations to the empty list
        print(str(count)+'-'+''+i[1])#Show conversations
        
    ntar = input('select chats from list  and zero(0) for back to menu \n : ')#Selection of dialogue by the user
    if ntar=='0': #Back To Menu
        return'exit'
    
    for i in nlist:#Login to the chat section
        if ntar in i :
            chatid = i[1]#Get the chat ID of the conversation for when the write function is called
            when = 0
            print('\n If you want to exit the chat mode, just type exit and send.(exit)')
            print('\n Press Enter to refresh the chat and read new messages')
            while when==0:#Chat mode until the user sends an exit. If enter is pressed, the chat will be refreshed and new messages will be displayed
                nx = read(chatid , uid , mname)
                body=input('')
                
                if body=='': #If the user hits enter (refreshing the conversation)
                    nx = read(chatid , uid , mname)
                    
                elif body=='exit': #If the user sent the exit (exit from the chat)
                    chats(uid)
                    break
                
                else: # Otherwise, enter the rest of the user's entries into the database as messages
                    write(chatid,body,uid , nx)
                        
    else:
        chats(uid)
                    
             

    
