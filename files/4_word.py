import sqlite3
import string
import subprocess
import os.path as os


file_dir = os.abspath(os.dirname(__file__))

conn = sqlite3.connect("file:" + os.join(file_dir, "model_db.sqlite") + "?mode=ro", uri=True)
cur = conn.cursor()

cur.execute("""SELECT subject FROM Messages JOIN Subjects
            ON Messages.subject_id = Subjects.id""")

# Count words larger than 3
words = dict()
for subject in cur:
    text = str(subject[0]).lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = text.translate(str.maketrans("", "", string.digits))
    parts = text.split()
    for p in parts:
        if len(p) > 3:
            words[p] = words.get(p, 0) + 1
    
words_sorted_l = sorted(words, key=words.get, reverse=True)
print("========== Words ==========")
print(f" There are {len(words_sorted_l)} different words in the subjects.")

# Handle Input
while True:
    top_words = input(" Enter how many words to rank: ")
    try: top_words = int(top_words)
    except:
        print("\r\nEnter a valid number.")
        continue
    if top_words > len(words_sorted_l): 
        print(f"\r\nYou entered {top_words} words to rank but there are only {len(words_sorted_l)}, please enter a valid value.")
        continue
    break

# Max and Min count of the top 'n' words
count_max = words[words_sorted_l[0]]
count_min = words[words_sorted_l[top_words-1]]
count_var = count_max - count_min
print("\r\nRange of apearence of the top", top_words, "words:", count_min, "-", count_max)

# Range of words size
size_min = 20
size_max = 80
size_var = size_max - size_min

# Create .js file
file_h = open(os.join(file_dir, 'gword.js'), 'w')
file_h.write("gword = [")

# Write on gwords.js
first = True
for k in words_sorted_l[:top_words]:
    if first is True: first = False
    else: file_h.write(",\n")

    # Calculate size
    v = size_min + (words[k] - count_min) * size_var / count_var
    v = round(v)

    file_h.write("{text: '" + k + "', size: " + str(v) + "}")

file_h.write("\n]\n")
file_h.close()

print("\r\n Data written on gword.js")
print(" Open gword.htm to visualize in a browser.\r\n")

cur.close()
conn.close()

while True:
    visualize = input(" Want to visualize on your default browser now? (y/n): ").lower()
    if visualize == 'y':
        subprocess.run(os.join(file_dir, 'gword.htm'), shell=True)
        break
    elif visualize == 'n': break
    else: 
        print("\r\nPlease enter a valid answer.")
print("")