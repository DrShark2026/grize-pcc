import streamlit as st
import sqlite3, os
from datetime import datetime
import matplotlib.pyplot as plt
import networkx as nx
import main as engine

st.set_page_config(page_title="Grize PCC V5", page_icon="🧠", layout="wide")
st.title("🧠 Grize PCC V5")
st.caption("Version web - Jean")

# sidebar
notion = st.sidebar.text_input("Notion", "pavé")
st.sidebar.markdown("---")
st.sidebar.write("DB:", engine.DB)

# construction
st.header(f"Notion: {notion}")

col1, col2 = st.columns([1,2])

with col1:
    st.subheader("Construire")
    with st.form("form", clear_on_submit=True):
        src = st.text_input("Source", notion)
        cible = st.text_input("Cible", "plage")
        op = st.selectbox("Opération", ["γ1","ρ3","θ5","R","θ3"], index=1)
        imP = st.text_input("im(P)", "")
        submitted = st.form_submit_button("➕ Ajouter")
        if submitted:
            engine.log(notion, op, src, cible, imP)
            st.success(f"[{op}] {src} -> {cible}")
            st.rerun()

with col2:
    st.subheader("Opérations")
    con=sqlite3.connect(engine.DB)
    cur=con.cursor()
    cur.execute("SELECT id FROM notions WHERE nom=?",(notion,))
    r=cur.fetchone()
    if r:
        cur.execute("SELECT op_code, src, cible, imP FROM operations WHERE notion_id=? ORDER BY id DESC", (r[0],))
        rows=cur.fetchall()
        if rows:
            st.dataframe([{"op":o,"src":s,"cible":c,"im(P)":i} for o,s,c,i in rows], use_container_width=True)

            if st.button("📈 Générer graphe"):
                G=nx.DiGraph()
                for o,s,c,i in rows: G.add_edge(s,c,label=o)
                pos=nx.spring_layout(G, k=1.5)
                fig, ax = plt.subplots(figsize=(6,4))
                nx.draw(G,pos,with_labels=True,node_color="lightyellow",node_size=2000, ax=ax, font_size=10)
                edge_labels = nx.get_edge_attributes(G,'label')
                nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels, ax=ax)
                st.pyplot(fig)
        else:
            st.info("Aucune opération encore")
    else:
        st.info("Vide pour cette notion, commence à construire!")

con.close()
