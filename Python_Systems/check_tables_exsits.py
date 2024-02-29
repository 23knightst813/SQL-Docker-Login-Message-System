
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
                CREATE SEQUENCE messages_message_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 41 CACHE 1;

                CREATE TABLE "public"."messages" (
                    "message_id" integer DEFAULT nextval('messages_message_id_seq') NOT NULL,
                    "receiver_id" integer,
                    "sent_id" integer,
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
    result = cur.fetchone()
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
            ('Admin', 'Admin'),
            ('khumes2g@vk.com', 'rO2!uGjl0/'),
            ('tnorcliff2h@discovery.com', 'yF5\\H9tr>'),
            ('gpennycock2i@xinhuanet.com', 'lI2$Tu8vv#'),
            ('fsliman2k@state.tx.us', 'nE0$*X{<9HzR')
            """
        )
    else:
        print("Table exists")
    print("Data added to the users table")

