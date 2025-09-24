from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime
import threading
import os

#poo and pee och sånt

app = Flask(__name__) # Skapar Flask appen
DATA_FILE = "guestbook.json" # Fil där alla inlägg sparas
lock = threading.Lock() # Lås så att användare inte skriver till filen samtidigt 

# Funktion för att läsa inlägg från JSON
def load_entries(): 
    if not os.path.exists(DATA_FILE):
        return [] # Returnera tom lista om filen inte finns
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f) # Ladda JSON-data och sånt
        except json.JSONDecodeError:
            return [] # Om filen är tom eller korrupt, returnera tom lista
        
# Funktion för att skriva inlägg till JSON
def save_entries(entries):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)  


