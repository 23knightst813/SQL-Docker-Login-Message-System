import psycopg2
import psycopg2.extras

EMAIL = "hello32@poopoo.con"
PASSWORD = "gfetiugufieg"
USERID = 0

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


def check_loging():
    print("Pulling account")
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        """
    
        SELECT * FROM users WHERE Email = %s""",
        (EMAIL,),
    )
    print("Account pulled")
    user_fetch = cur.fetchone()
    print(user_fetch)

    if user_fetch["password"] == PASSWORD:
        print("Account password matches")
        login()

    else:
        print("Account password or email does not match")


def write_account():

    global USERID
    global EMAIL
    global PASSWORD
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

    except psycopg2.errors.UniqueViolation:

        print("Account already exists")


def login():
    print("Logged in")
    # Do something with cookies and sessions


def change_password():
    print("Changing password")
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE users SET password = %s WHERE Email = %s
        """,
        (PASSWORD, EMAIL),
    )
    print("Password changed")


def delete_account():
    print("Deleting account")
    cur = conn.cursor()
    cur.execute(
        """
        DELETE FROM users WHERE Email = %s
        """,
        (EMAIL,),
    )
    print("Account deleted")


def logout():
    print("Logged out")
    # Do something with cookies and sessions


check_loging()
