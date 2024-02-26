import psycopg2
import psycopg2.extras
from flask import Flask, redirect, render_template, request, session, url_for, make_response

app = Flask(__name__)
app.secret_key = "three"


@app.route("/" , )
def home():

    email = "Guest"

    if "email" not in session:
        return redirect(url_for("login"))
    else:
        
        email = session["email"]

        email = email.split('@')[0]

        response = make_response(render_template("index.html", email=email))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        
        return response    





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


def check_table_exists():
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


def give_session():
    print("Giving session")


check_table_exists()

if __name__ == "__main__":
    app.run(debug=True)
