

import psycopg2
import psycopg2.extras
from flask import Flask, redirect, render_template, request, session, url_for, make_response, flash


from Account_Control import change_password , delete_account, write_account, check_login
from check_tables_exsits import check_messages_table_exsits , check_users_table_exists
from Message_System import send_message


app = Flask(__name__, template_folder='../templates')

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

        x = change_password(conn, EMAIL, PASSWORD)


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

        x = check_login(conn, EMAIL, PASSWORD)

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

        x = write_account(conn, EMAIL, PASSWORD)


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

        x = delete_account(conn, EMAIL, PASSWORD)


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

            x = send_message(conn, TARGET_EMAIL, TARGET_MESSAGE)


            if x == True:
                return('Message sent successfully!')
            if x == False:
                return('Failed to send message!')

            return ("x is neither true nor false")

        if request.method == "GET":
            print('get')

            return render_template('Message.html')

@app.route('/inbox' , methods=["GET", "POST"])
def inbox():
    print('Inbox')
    if request.method == "GET":
        print('get')

    messages 
    sender 
    messagetext 


    if request.method == "POST":
        print('post')
        return render_template('inbox.html')

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


check_users_table_exists()
check_messages_table_exsits()

if __name__ == "__main__":
    app.run(debug=True)

