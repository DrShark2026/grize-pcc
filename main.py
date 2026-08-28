# Grize PCC V5 - version simple
import sqlite3, json, os, re, glob
from datetime import datetime

DB="grize.db"
EXPORT_DIR="exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

def init():
    con=sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS notions (id INTEGER PRIMARY KEY, nom TEXT UNIQUE)")
    con.execute("CREATE TABLE IF NOT EXISTS operations (id INTEGER PRIMARY KEY, notion_id INTEGER, op_code TEXT, src TEXT, cible TEXT, imP TEXT, auteur TEXT, date TEXT, phrase TEXT)")
    con.commit(); con.close()
init()

def log(notion, op, src, cible, imP=""):
    con=sqlite3.connect(DB); cur=con.cursor()
    cur.execute("SELECT id FROM notions WHERE nom=?", (notion,))
    r=cur.fetchone()
    if not r:
        cur.execute("INSERT INTO notions (nom) VALUES (?)", (notion,))
        nid=cur.lastrowid
    else: nid=r[0]
    cur.execute("INSERT INTO operations VALUES (NULL,?,?,?,?,?,?,?,?)",(nid,op,src,cible,imP,"A",datetime.now().strftime("%H:%M"),""))
    con.commit(); con.close()

def voir(notion):
    con=sqlite3.connect(DB); cur=con.cursor()
    cur.execute("SELECT id FROM notions WHERE nom=?",(notion,))
    r=cur.fetchone()
    if not r: return []
    cur.execute("SELECT op_code, src, cible FROM operations WHERE notion_id=?", (r[0],))
    return cur.fetchall()

if __name__ == "__main__":
    while True:
        print("\n--- MENU V5 SIMPLE ---")
        print("1.Construire 2.Voir 3.Graphe 4.Quitter")
        c=input("> ")
        if c=="1":
            n=input("Notion ex:pavé > ") or "pavé"
            s=input(f"Source [{n}] > ") or n
            ci=input("Cible ex:plage > ") or "plage"
            op=input("Op γ1/ρ3/θ5/R/θ3 [ρ3] > ") or "ρ3"
            imp=input("im(P)? > ") or ""
            log(n,op,s,ci,imp)
        elif c=="2":
            print(voir(input("Notion? > ")))
        elif c=="4": break
