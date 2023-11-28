import sqlite3
import os.path as os


file_dir = os.abspath(os.dirname(__file__))

conn = sqlite3.connect("file:" + os.join(file_dir, "model_db.sqlite") + "?mode=ro", uri=True)
cur = conn.cursor()

print("========== Basic ==========")

# Handle input
while True:
    n = input(" Chose the top 'n' senders/organizations: ")
    try:
        n = int(n)
        if n < 1: continue
        else: break
    except:
        print("\r\nEnter a valid number.")

cur.execute("SELECT sender FROM Messages JOIN Senders\
            ON Messages.sender_id = Senders.id")

# Split senders and organizations
senders = dict()
orgs = dict()
for email in cur:
    parts = str(email[0]).split("@")
    senders[parts[0]] = senders.get(parts[0], 0) + 1
    orgs[parts[1]] = orgs.get(parts[1], 0) + 1

senders_sorted = sorted(senders, key=senders.get, reverse=True)
orgs_sorted = sorted(orgs, key=orgs.get, reverse=True)

# Print senders and orgs
print(f"\r\nThe top {n} senders are:")
for k in senders_sorted[:n]:
    print("  ", k, senders[k])

print(f"\r\nThe top {n} organizations are:")
for k in orgs_sorted[:n]:
    print("  ", k, orgs[k])

cur.close()
conn.close()

input("\r\nPress 'Enter'.")
print("")