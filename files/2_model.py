import sqlite3
import datetime
import zlib
import signal
import subprocess
import os.path as os


try:
    from dateutil import parser
except:
    input(" Please install 'dateutil', more details on 'README.txt'")
    quit()

# Handle exit signal
stop_program = False
def handler(signum, frame):
    global stop_program

    res = input("Ctrl-c was pressed. Do you really want to exit? (y/n) ")
    if res.lower() == 'y':
        stop_program = True
        # exit(1)

signal.signal(signal.SIGINT, handler)

file_dir = os.abspath(os.dirname(__file__))

# Create database
conn = sqlite3.connect(os.join(file_dir, "model_db.sqlite"))
cur = conn.cursor()

cur.executescript("""CREATE TABLE IF NOT EXISTS Messages (
                  id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                  date TEXT,
                  sender_id INTEGER,
                  subject_id INTEGER,
                  header BLOB,
                  body BLOB
                  );

                  CREATE TABLE IF NOT EXISTS Senders (
                  id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                  sender TEXT UNIQUE
                  );

                  CREATE TABLE IF NOT EXISTS Subjects (
                  id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                  subject TEXT UNIQUE
                  );
""")

# Check last entry
cur.execute("SELECT max(id) FROM Messages")
try:
    start_cur_1_id = cur.fetchone()[0]
except:
    start_cur_1_id = 1
if start_cur_1_id is None: start_cur_1_id = 1

# Cleaning data
def check_if_none(entry: str):
    if len(entry) < 1 or entry is None: return None
    else: return str(entry.decode()).strip()

conn_1 = sqlite3.connect("file:" + os.join(file_dir, "spider.sqlite") + "?mode=ro", uri=True)
cur_1 = conn_1.cursor()

cur_1.execute("SELECT * FROM Messages")

cur_1_id = 1
i = 0
for entry in cur_1:
    if stop_program: break
    if start_cur_1_id != 1 and cur_1_id <= start_cur_1_id:
        print(f"Entry {cur_1_id} already on database...")
        cur_1_id += 1
        continue

    # Email
    email = check_if_none(entry[1])
    if email is not None: email = email.lower().replace(" ", "")

    # Date
    date = check_if_none(entry[2])
    if date is not None:
        try:
            date = parser.parse(date)
            date = date.isoformat()
        except:
            date = None

    # Subject, Header and Body
    subject = check_if_none(entry[3])
    header = check_if_none(entry[4])
    body = check_if_none(entry[5])

    # Insert clean data into database
    cur.execute("INSERT OR IGNORE INTO Senders (sender) VALUES (?)", (email,))
    cur.execute("SELECT id FROM Senders WHERE sender = ? LIMIT 1", (email,))
    try:
        sender_id = cur.fetchone()[0]
    except:
        print(f"Could not retrieve sender_id on entry {cur_1_id}.")
        break

    cur.execute("INSERT OR IGNORE INTO Subjects (subject) VALUES (?)", (subject,))
    cur.execute("SELECT id FROM Subjects WHERE subject = ? LIMIT 1", (subject,))
    try:
        subject_id = cur.fetchone()[0]
    except:
        print(f"Could not retrieve subject_id on entry {cur_1_id}.")
        break

    cur.execute("INSERT INTO Messages (date, sender_id, subject_id, header, body) VALUES (datetime(?), ?, ?, ?, ?)", 
                (date, sender_id, subject_id, zlib.compress(header.encode()), zlib.compress(body.encode())))
    
    print(f"Entry {cur_1_id} succesfully loaded.")

    cur_1_id += 1
    i += 1
    if i % 50 == 0: 
        conn.commit()
        print("Commited 50 entries")

cur_1.close()
conn_1.close()

conn.commit()
cur.close()
conn.close()
print(f"\r\n A total of {i} entries were added succesfully into database.")

while True:
    question = input("\r\n Do you want to run the data visualization (3_visualization.py)? (y/n): ")
    if question.lower() == 'y':
        subprocess.run(['python', os.join(file_dir, '3_visualization.py')])
        break
    elif question.lower() == 'n': break
    else: continue