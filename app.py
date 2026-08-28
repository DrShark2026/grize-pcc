cat > app.py << 'PY'
import streamlit as st
import sqlite3, os
from datetime import datetime
import main as engine

st.set_page_config(page_title="Grize PCC V5", layout="wide")
st.title("Grize PCC V5 - version web")

notion = st.sidebar.text_input("Notion", "pavé")

tab1, tab2 = st.tabs(["Construire", "Voir / Graphe"])

with tab1:
    with st.form("form"):
        src = st.text_input(f"Source [{notion}]", notion)
        cible = st.text_input("Cible ex: plage", "plage")
        op = st.selectbox("Opération", ["γ1","ρ3","θ5","R","θ3"], index=1)
        imP = st.text_input("im(P)")
        ok = st.form_submit_button("Ajouter")
        if ok:
            engine.log(notion, op, src, cible, imP)
            st.success(f"Ajouté [{op}] {src} -> {cible}")

with tab2:
    con=sqlite3.connect(engine.DB)
    cur=con.cursor()
    cur.execute("SELECT id FROM notions WHERE nom=?",(notion,))
    r=cur.fetchone()
    if r:
        cur.execute("SELECT op_code, src, cible FROM operations WHERE notion_id=?", (r[0],))
        rows=cur.fetchall()
        st.table([{"op":o,"src":s,"cible":c} for o,s,c in rows])

        if st.button("Générer graphe"):
            import matplotlib.pyplot as plt, networkx as nx
            G=nx.DiGraph()
            for o,s,c in rows: G.add_edge(s,c,label=o)
            pos=nx.spring_layout(G)
            fig, ax = plt.subplots()
            nx.draw(G,pos,with_labels=True,node_color="lightyellow",node_size=2000, ax=ax)
            st.pyplot(fig)
    else:
        st.info("Vide pour cette notion")
PY
