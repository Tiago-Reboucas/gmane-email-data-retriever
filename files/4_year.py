import sqlite3
import subprocess
import os.path as os


file_dir = os.abspath(os.dirname(__file__))

conn = sqlite3.connect("file:" + os.join(file_dir, "model_db.sqlite") + "?mode=ro", uri=True)
cur = conn.cursor()

# Handle input
print("========== Line - Year ==========")
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

# Join organizations and year
orgs = dict()
org_year = list()
for entry in cur:
    parts = str(entry[0]).split("@")
    if len(parts) != 2: continue
    orgs[parts[1]] = orgs.get(parts[1], 0) + 1

    org_year.append((parts[1], str(entry[1][:4])))

orgs_sorted = sorted(orgs, key=orgs.get, reverse=True)
orgs_sorted = orgs_sorted[:n]

# Count top organizations per year
years = list()
org_year_count = dict()
for entry in org_year:
    if entry[0] not in orgs_sorted: continue
    if entry[1] not in years:
        years.append(entry[1])

    key = (entry[0], entry[1])
    org_year_count[key] = org_year_count.get(key, 0) + 1

    # In case need the total in a year count
    tkey = ('total', entry[1])
    org_year_count[tkey] = org_year_count.get(tkey, 0) + 1

years.sort()

# Write in .js file
file_h = open(os.join(file_dir, 'gline_year.js'),'w')
file_h.write("gline = [['Year'")
for org in orgs_sorted:
    file_h.write(",'"+org+"'")
file_h.write("]")

for year in years:
    file_h.write(",\n['"+year+"'")
    for org in orgs_sorted:
        key = (org, year)
        value = org_year_count.get(key,0)
        file_h.write(","+str(value))
    file_h.write("]")

file_h.write("\n];\n")
file_h.close()

print("\r\n Data written on gline_year.js")
print(" Open gline_year.htm to visualize in a browser.\r\n")

cur.close()
conn.close()

while True:
    visualize = input(" Want to visualize on your default browser now? (y/n) ").lower()
    if visualize == 'y':
        subprocess.run(os.join(file_dir, 'gline_year.htm'), shell=True)
        break
    elif visualize == 'n': break
    else: 
        print("\r\nPlease enter a valid answer.")
        continue