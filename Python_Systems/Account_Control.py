
import psycopg2
import psycopg2.extras

conn = psycopg2.connect(
        dbname="database",
        user="username",
        password="secret",
        host="postgres_database",
        port="5432",
    )
conn.autocommit = True
print("Connected")

def change_password(conn, EMAIL, PASSWORD):
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
    
def delete_account(conn, EMAIL, PASSWORD):
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
    

def write_account(conn, EMAIL, PASSWORD):

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


def check_login(conn, EMAIL, PASSWORD):
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
    
    