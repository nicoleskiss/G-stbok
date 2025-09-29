from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime
import threading
import os

#poo and pee och sånt

app = Flask(__name__) # Skapar Flask appen
DATA_FILE = "guestbook.json" # Fil där alla inlägg sparas
lock = threading.Lock() # Lås så att användare inte skriver till filen samtidigt 

def load_entries(): 
    if not os.path.exists(DATA_FILE):
        return [] # Returnera tom lista om filen inte finns
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f) # Ladda JSON-data och sånt
        except json.JSONDecodeError:
            return [] # Om filen är tom returneras en tom lista
        
def save_entries(entries):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)  

@app.route("/", methods=["GET"])
def index():
    entries = load_entries()
    # sorterar senaste först 
    entries_sorted = sorted(entries, key=lambda e: e.get("time", ""), reverse=True)
    return render_template("index.html", entries=entries_sorted)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip() or "Anonym"
    email = request.form.get("email", "").strip()
    comment = request.form.get("comment", "").strip()

    if len(name) > 60:
        name = name[:60]
    if len(email) > 100:
        email = email[:100]
    if len(comment) > 1000:
        comment = comment[:1000]

    entry = {
        "id": None, 
        "name": name,
        "email": email,
        "comment": comment,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    }

    with lock:
        entries = load_entries()
        max_id = max([e.get("id", 0) for e in entries], default=0)  
        entry["id"] = max_id + 1
        entries.append(entry)
        save_entries(entries)

    # Tillbaka till startsidan
    return redirect(url_for("index"))

# Starta servern
if __name__ == "__main__":
    app.run(debug=True) 
