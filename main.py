import time

# import flask
import psycopg2

email = "hello@poopoo.con"
password = "gfeiugufieg"
userid = 3


"""
print("Connecting...")
time.sleep(2)
print("Connecting....")
time.sleep(1)
print("Connecting..")
time.sleep(1)
"""

try:

    conn = psycopg2.connect(
        dbname="database",
        user="username",
        password="secret",
        host="postgres_database",
        port="5432",
    )

    print("Connected")

except:

    print("Not connected")


def pull_account():
    print("Pulling account")


def write_account():
    global userid

    print("Writing account")
    cur = conn.cursor()
    cur.execute(
        f"""
    
    INSTERT INTO user (UserId ,Email , Password) VALUES ({userid}, {email}, {password})

  """
    )
    userid = +1
    conn.commit()
    conn.close()
