import urllib.request, urllib.parse, urllib.error
import ssl
import sqlite3
import time
import signal
import subprocess
import os.path as os


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

# Create/Connect database
conn = sqlite3.connect(os.join(file_dir, "spider.sqlite"))
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS Messages (
            id INTEGER UNIQUE,
            email TEXT,
            date TEXT,
            subject TEXT,
            header TEXT,
            body TEXT)""")

# Igonre SSL Certificate erros
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Check start
cur.execute("SELECT max(id) FROM Messages")
try:
    row = cur.fetchone()
    start_id = row[0]
except:
    start_id = 0
if start_id == None: start_id = 0

n = curr_id = start_id + 1

# Input
while True:
    messages = input(" How many messages to read: ")
    try:
        messages = int(messages)
        if messages < 1:
            print("Enter a valid number.\r\n")
            continue
        break
    except:
        print("Enter a valid number.\r\n")


email_escape = (" ", "<", ">", "(", ")", "\n", "\r\n")
date_escape = ("<", ">", "(", ")", "_", ".", ",", "\n", "\r\n")
service_url = "https://mbox.dr-chuck.net/sakai.devel/"

fail = 0
i = 0
while True:
    url = service_url + f"{n}/" + str(n+1)

    try:
        data = urllib.request.urlopen(url, timeout=30, context=ctx)
        if data.getcode() != 200:
            print("Code error:", data.getcode(), url)
            break

    except:
        print("Couldn't retrieve page.")
        fail += 1
        if fail > 5: break
        n += 1
        continue

    data = str(data.read().decode())

    if not data.startswith("From "):
        print("Doesn't start with 'From '")
        fail += 1
        if fail > 5: break
        n += 1
        continue

    # Pull "email address"
    pos_data = data.find("From: ")
    pos = data.find("@", pos_data)

    if pos == -1 or pos > data.find("Subject:"):
        print("Fail to retrieve 'email'\r\n")
        fail += 1
        if fail > 5: break
        n += 1
        continue

    j = 1
    while True:
        if data[pos+j:pos+j+1] in email_escape:
            pos_f = pos + j
            break
        j += 1
    j = 1
    while True:
        if data[pos-j:(pos+1)-j] in email_escape:
            pos_i = (pos + 1) - j
            break
        j += 1

    email = data[pos_i:pos_f].strip()

    # Pull "subject"
    pos_data = data.find("Subject: ")

    if pos_data == -1:
        print("Fail to retrieve 'subject'")
        fail += 1
        if fail > 5: break
        n += 1
        continue

    pos = data.find("\n", pos_data)
    subject = data[pos_data+9:pos]

    # Pull "date"
    pos_data = data.find("Date: ")

    if pos_data == -1:
        print("Fail to retrieve 'date'")
        fail += 1
        if fail > 5: break
        n += 1
        continue

    pos_i = data.find(",", pos_data) + 2

    j = 1
    while True:
        if data[pos_i+j:pos_i+j+1] in date_escape:
            pos_f = pos_i + j
            break
        j += 1

    date = data[pos_i:pos_f].strip()
    if date.startswith("0"): date = date[1:]

    # print(email, subject, date)

    # Pull "header" and "body"
    pos_f = data.find("\n\n")
    header = data[:pos_f]
    body = data[pos_f+2:]

    # Save into database
    def memory(text: str):
        return memoryview(text.encode())


    cur.execute("""INSERT INTO Messages (id, email, date, subject, header, body) 
                VALUES (?, ?, ?, ?, ?, ?)""", (curr_id, memory(email), memory(date), memory(subject), memory(header), memory(body)))

    print(f"Message id = {curr_id} was insert into commiting pool...")

    if i % 50 == 0 and i != 0: 
        conn.commit()
        print("\r\nLast 50 items on the pool were commited.\r\n")
    if i % 100 == 0: time.sleep(1)

    i += 1
    n += 1
    curr_id += 1
    if i == messages: break
    if stop_program: break

conn.commit()
cur.close()
conn.close()
print(f"\r\n {i} data entries commited.")

while True:
    question = input("\r\n Do you want to run the database model (2_model.py)? (y/n): ")
    if question.lower() == 'y':
        subprocess.run(['python', os.join(file_dir, '2_model.py')])
        break
    elif question.lower() == 'n': break
    else: continue