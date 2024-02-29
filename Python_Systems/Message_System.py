from email import message
from flask import session
from Account_Control import get_your_id
import psycopg2
import psycopg2.extras
import numpy as np
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



def delete_user_messages():
    print('')

    userId = get_your_id()

    cur = conn.cursor()


    cur.execute(
        """
        DELETE FROM messages WHERE receiver_id = %s
        """,
        (userId,),
    )

    return True


def inbox_info_get():
    print('inbox')

    # Find how many messages

    your_id = get_your_id()

    cur = conn.cursor()

    #fetch current row
    cur.execute("""
                SELECT * FROM messages
                INNER JOIN users ON users.id = messages.sent_id
                WHERE receiver_id = %s
                ORDER BY time DESC;
                """, (your_id,))

    data = cur.fetchall()

    print(data)

    messagesinfo = []  # Initialize as empty list
    message = None
    sender_name = None
    time = None  # Initialize variables separately

    for row in data:
        message = row["message"]
        sender_name = row['email'] 
        time = row['time']
        messagesinfo.append({'message': message, 'email': sender_name, 'time': time})

    return messagesinfo
