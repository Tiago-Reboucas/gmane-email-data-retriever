import sqlite3
import subprocess
import os.path as os


file_dir = os.abspath(os.dirname(__file__))

conn = sqlite3.connect("file:" + os.join(file_dir, "model_db.sqlite") + "?mode=ro", uri=True)
cur = conn.cursor()

# Handle input
print("========== Line - Month ==========")
while True:
    n = input(" Chose the top 'n' organizations: ")
    try:
        n = int(n)
        if n < 1: continue
        else: break
    except:
        print("\r\nEnter a valid number.")

cur.execute("SELECT sender, date FROM Messages JOIN Senders\
            ON Messages.sender_id = Senders.id")

# Join organizations and month
orgs = dict()
org_month = list()
for entry in cur:
    parts = str(entry[0]).split("@")
    if len(parts) != 2: continue
    orgs[parts[1]] = orgs.get(parts[1], 0) + 1

    org_month.append((parts[1], str(entry[1][:7])))

orgs_sorted = sorted(orgs, key=orgs.get, reverse=True)
orgs_sorted = orgs_sorted[:n]

# Count top organizations per month
months = list()
org_month_count = dict()
for entry in org_month:
    if entry[0] not in orgs_sorted: continue
    if entry[1] not in months:
        months.append(entry[1])

    key = (entry[0], entry[1])
    org_month_count[key] = org_month_count.get(key, 0) + 1

months.sort()

# Write in .js file
file_h = open(os.join(file_dir, 'gline.js'),'w')
file_h.write("gline = [['Month'")
for org in orgs_sorted:
    file_h.write(",'"+org+"'")
file_h.write("]")

for month in months:
    file_h.write(",\n['"+month+"'")
    for org in orgs_sorted:
        key = (org, month)
        value = org_month_count.get(key,0)
        file_h.write(","+str(value))
    file_h.write("]")

file_h.write("\n];\n")
file_h.close()

print("\r\n Data written on gline.js")
print(" Open gline.htm to visualize in a browser.\r\n")

cur.close()
conn.close()

while True:
    visualize = input(" Want to visualize on your default browser now? (y/n): ").lower()
    if visualize == 'y':
        subprocess.run(os.join(file_dir, 'gline.htm'), shell=True)
        break
    elif visualize == 'n': break
    else: 
        print("\r\nPlease enter a valid answer.")
        continue
print("")