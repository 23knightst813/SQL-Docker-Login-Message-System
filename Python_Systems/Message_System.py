from flask import session

import psycopg2
import psycopg2.extras

import datetime

conn = psycopg2.connect(
        dbname="database",
        user="username",
        password="secret",
        host="postgres_database",
        port="5432",
    )
conn.autocommit = True
print("Connected")

def send_message(conn , TARGET_EMAIL, TARGET_MESSAGE):
    print('Send Message')

    #find the targets id ( receiver )
    
    receiver_email = TARGET_EMAIL
    
    cur = conn.cursor()
    cur.execute('''

        SELECT id
        FROM users
        WHERE Email = %s

''', (receiver_email,))
    
    receiver_id = cur.fetchone()

    #find your id
    sender_id = get_your_id()

    # Get the message they wanna send
    Message = TARGET_MESSAGE

    Time_Date = datetime.datetime.now()

    #Add to data base
    if receiver_id == None or sender_id == None or Message == None or Message == '':
        print('Error')
        return False
    else:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO "messages" (receiver_id, sent_id, message , time) VALUES (%s, %s, %s , %s)
        ''', (receiver_id, sender_id, Message , Time_Date.strftime("%c")))

        print('Sent')
        return True

def get_your_id():
    #Find your id aka you

    #get the email
    sender_email = session["email"]

    #sql the email to get the id

    cur = conn.cursor()
    cur.execute('''

        SELECT id
        FROM users
        WHERE Email = %s

''', (sender_email,))
    your_id = cur.fetchone()

    return your_id

