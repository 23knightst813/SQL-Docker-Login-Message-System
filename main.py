import psycopg2
import psycopg2.extras
from flask import Flask, redirect, render_template, request, session, url_for, make_response, flash
import datetime

app = Flask(__name__)
app.secret_key = "three"


@app.route("/"  )
def home():

    email = "Guest"
    print("keurfe")

    if "email" not in session:
        return redirect(url_for("login"))
    else:
        
        email = session["email"]

        email = email.split('@')[0]

        response = make_response(render_template("index.html", email=email))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"

        return response    


@app.route("/changepassword", methods=["GET", "POST"])
def chnagepassword():
    print("Change password start")
    if request.method == "POST":
        print("Post")
        EMAIL = request.form["email"]
        PASSWORD = request.form["password"]
        print(EMAIL)
        print(PASSWORD)

        x = change_password(EMAIL, PASSWORD)

        if x == True:
            print("Password changed")

        if x == False:
            print("No account found")

        return redirect(("/"))

    if request.method == "GET":
        return render_template("changepassword.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    print("Login start")
    if request.method == "POST":
        print("Post")
        EMAIL = request.form["email"]
        PASSWORD = request.form["password"]
        print(EMAIL)
        print(PASSWORD)

        # INTEGRATES CHECK_LOGIN FUNCTION

        x = check_login(EMAIL, PASSWORD)

        if x == True:
            session["email"] = EMAIL
            print("Logged in")

        if x == False:
            print("Not logged in")

        return redirect(("/"))
    if request.method == "GET":
        return render_template("login.html")


@app.route("/logout")
def logout():
    print("Logout start")
    session.pop("email", None)
    return redirect(("/"))


@app.route("/register", methods=["GET", "POST"])
def register():
    print("Register start")
    if request.method == "POST":
        print("Post")
        EMAIL = request.form["email"]
        PASSWORD = request.form["password"]
        print(EMAIL)
        print(PASSWORD)

        # Need to add the write_account function here

        x = write_account(EMAIL, PASSWORD)

        if x == True:
            print("Wrote account")

        if x == False:
            print("Account already exists")

        return redirect(("/"))

    if request.method == "GET":
        return render_template("register.html")


@app.route("/deleteaccount", methods=["GET", "POST"])
def deleteaccount():
    print("Delete account start")
    if request.method == "POST":
        print("Post")
        EMAIL = request.form["email"]
        PASSWORD = request.form["password"]
        print(EMAIL)
        print(PASSWORD)

        x = delete_account(EMAIL, PASSWORD)

        if x == True:
            print("Deleted account")

        if x == False:
            print("No account found")

        return redirect(("/"))

    if request.method == "GET":
        return render_template("deleteaccount.html")


@app.route('/Message', methods=["GET", "POST"])
def send_message_page():



        print('SenMessgaeFlask')

        if request.method == "POST":

            print('post')

            TARGET_EMAIL = request.form["email"]
            TARGET_MESSAGE = request.form["Message"]
            print(TARGET_EMAIL)
            print(TARGET_MESSAGE)

            x = send_message(TARGET_EMAIL, TARGET_MESSAGE)

            '''
            if x = True
                print('Message sent successfully!', 'success')
            if x = False
                print('Failed to send message!', 'error')
            '''

            return render_template('Message.html', status = x)


        if request.method == "GET":
            print('post')

            return render_template('Message.html')




try:
    conn = psycopg2.connect(
        dbname="database",
        user="username",
        password="secret",
        host="postgres_database",
        port="5432",
    )
    conn.autocommit = True
    print("Connected")


except:
    print("Not connected")





def check_login(EMAIL, PASSWORD):
    print("Pulling account")
    print(f"Email: {EMAIL}, Password: {PASSWORD}")
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        """
        SELECT * FROM users WHERE Email = %s
        """,
        (EMAIL,),
    )
    row = cur.fetchone()
    print(f"Fetched row: {row}")
    if row is not None and row["password"] == PASSWORD:
        print("Account password matches")
        return True
    else:
        print("Account password or email does not match")
        return False


def write_account(EMAIL, PASSWORD):

    print("Writing account")
    cur = conn.cursor()

    try:

        cur.execute(
            """
            INSERT INTO "users" (Email, Password) VALUES (%s, %s)
            """,
            (EMAIL, PASSWORD),
        )
        print("Account written")
        return True

    except psycopg2.errors.UniqueViolation:

        print("Account already exists")
        return False


def change_password(EMAIL, PASSWORD):
    print("Changing password")
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE users SET password = %s WHERE Email = %s
        """,
        (PASSWORD, EMAIL),
    )
    if cur.rowcount == 0:
        print("No user found with the provided email")
        return False
    else:
        print("Password changed")
        return True


def delete_account(EMAIL, PASSWORD):
    print("Deleting account")
    print(f"Email: {EMAIL}, Password: {PASSWORD}")
    print("Session Email", session["email"])
    cur = conn.cursor()
    cur.execute(
        """
        DELETE FROM users WHERE Email = %s AND Password = %s
        """,
        (session["email"], PASSWORD),
    )
    print(cur.rowcount)
    if cur.rowcount == 0:
        print("No user found with the provided email")
        return False
    else:
        print("Deleted account")
        return True


def check_users_table_exists():
    print("Checking if table exists")
    cur = conn.cursor()
    cur.execute(
        """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = 'users'
        )
        """
    )
    result = cur.fetchone()[0]
    print(result)

    if result is False:
        print("Table does not exist")
        cur.execute(
            """
            CREATE TABLE users (
                ID SERIAL PRIMARY KEY,
                Email VARCHAR(255) UNIQUE NOT NULL,
                Password VARCHAR(255) NOT NULL
            )
            """
        )
        cur.execute(
            """
            INSERT INTO users (Email, Password)
            VALUES 
            ('khumes2g@vk.com', 'rO2!uGjl0/'),
            ('tnorcliff2h@discovery.com', 'yF5\\H9tr>'),
            ('gpennycock2i@xinhuanet.com', 'lI2$Tu8vv#'),
            ('fsliman2k@state.tx.us', 'nE0$*X{<9HzR')
            """
        )
    else:
        print("Table exists")
    print("Data added to the users table")


def check_messages_table_exsits():
    print('checking if messages table is present')
    cur = conn.cursor()
    cur.execute(
        """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = 'messages'
        )
        """
    )

    result = cur.fetchone()[0]
    print(result)

    if result is False:
        print("Table does not exist")
        cur.execute(
            """
                CREATE SEQUENCE messages_message_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 18 CACHE 1;

                CREATE TABLE "public"."messages" (
                    "message_id" integer DEFAULT nextval('messages_message_id_seq') NOT NULL,
                    "receiver_id" integer NOT NULL,
                    "sent_id" integer NOT NULL,
                    "message" text NOT NULL,
                    "time" timestamp,
                    CONSTRAINT "messages_pkey" PRIMARY KEY ("message_id")
                ) WITH (oids = false);

                COMMENT ON COLUMN "public"."messages"."message_id" IS 'The mail id ';

                COMMENT ON COLUMN "public"."messages"."receiver_id" IS 'The id of the person who got the message';

                COMMENT ON COLUMN "public"."messages"."sent_id" IS 'Hold the guy who sent it';

                COMMENT ON COLUMN "public"."messages"."message" IS 'Hold the messgae';

                COMMENT ON COLUMN "public"."messages"."time" IS 'the time';


                ALTER TABLE ONLY "public"."messages" ADD CONSTRAINT "messages_receiver_id_fkey" FOREIGN KEY (receiver_id) REFERENCES users(id) NOT DEFERRABLE;
                ALTER TABLE ONLY "public"."messages" ADD CONSTRAINT "messages_sent_id_fkey" FOREIGN KEY (sent_id) REFERENCES users(id) NOT DEFERRABLE;
            
            """
        )

    else:
        print("Table exists")



def send_message(TARGET_EMAIL, TARGET_MESSAGE):
    print('Send Message')

    # Get the sender id

    #get the email
    sender_email = session["email"]

    #sql the email to get the id

    cur = conn.cursor()
    cur.execute('''

        SELECT id
        FROM users
        WHERE Email = %s

''', (sender_email,))
    sender_id = cur.fetchone()

    #find the targets id ( receiver )

    receiver_email = TARGET_EMAIL

    cur = conn.cursor()
    cur.execute('''

            SELECT id
            FROM users
            WHERE Email = %s

''', (receiver_email,))

    receiver_id = cur.fetchone()


    # Get the message they wanna send

    Message = TARGET_MESSAGE

    Time_Date = datetime.datetime.now()


    #Add to data base

    if receiver_id or sender_id or Message == None or '':

        print('Error')
        return 'False'

    else:

        cur.execute('''
            INSERT INTO "messages" (receiver_id, sent_id, message , time) VALUES (%s, %s, %s , %s)
        ''', (receiver_id, sender_id, Message , Time_Date.strftime("%c")))

        print('Sent')

        return 'True'





check_users_table_exists()
check_messages_table_exsits()

if __name__ == "__main__":
    app.run(debug=True)
