import streamlit as st

# --- EURE ZAHLEN (Dauerauftrag) ---
TIPPS = {
    "Tipp 1": {"zahlen": [1, 12, 22, 27, 34], "euro": [5, 6]},
    "Tipp 2": {"zahlen": [4, 5, 8, 20, 43], "euro": [4, 10]}
}

st.set_page_config(page_title="Eurojackpot Check", page_icon="🎰", layout="wide")

# --- SEITENLEISTE: HIER GIBST DU DIE ECHTEN ZAHLEN EIN ---
st.sidebar.header("📝 Ziehung eingeben")
st.sidebar.write("Trage hier die Zahlen vom Freitag/Dienstag ein:")

# Hier habe ich die echten Zahlen vom 24.03.2026 als Standard gesetzt
zug_z = st.sidebar.text_input("Gezogene Zahlen (mit Komma)", "10,21,31,41,45")
zug_e = st.sidebar.text_input("Gezogene Eurozahlen (mit Komma)", "4,9")
zug_j = st.sidebar.text_input("Jackpot Höhe", "23 Mio. €")
zug_d = st.sidebar.text_input("Datum", "24.03.2026")

# Umwandlung der Eingabe in Listen
try:
    final_z = [int(x.strip()) for x in zug_z.split(",")]
    final_e = [int(x.strip()) for x in zug_e.split(",")]
except:
    st.sidebar.error("Bitte Zahlen korrekt mit Komma trennen!")
    final_z, final_e = [0,0,0,0,0], [0,0]

# --- HAUPTBEREICH ---
st.title("🎰 Eurojackpot Tippgemeinschaft")
st.subheader(f"Ergebnisse für die Ziehung am {zug_d}")
st.metric("Aktueller Jackpot", zug_j)

st.markdown("---")
st.write("### Offizielle Ziehungszahlen:")
cols = st.columns(7)
for i, val in enumerate(final_z):
    cols[i].success(f"**{val}**")
for i, val in enumerate(final_e):
    cols[i+5].warning(f"**{val}**")

st.markdown("---")

# AUSWERTUNG
st.header("🔍 Unser Gewinn-Check")
c1, c2 = st.columns(2)

for i, (name, tipp) in enumerate(TIPPS.items()):
    with (c1 if i == 0 else c2):
        st.subheader(f"⭐ {name}")
        
        # Treffer finden
        t_z = set(tipp["zahlen"]).intersection(set(final_z))
        t_e = set(tipp["euro"]).intersection(set(final_e))
        
        st.write(f"Tipp: `{tipp['zahlen']}` | Euro: `{tipp['euro']}`")
        
        m1, m2 = st.columns(2)
        m1.metric("Richtige", f"{len(t_z)}/5", f"+{list(t_z)}" if t_z else None)
        m2.metric("Eurozahlen", f"{len(t_e)}/2", f"+{list(t_e)}" if t_e else None)
        
        if (len(t_z) >= 2 and len(t_e) >= 1) or len(t_z) >= 3:
            st.balloons()
            st.success("💰 GEWINN!")
        else:
            st.info("Kein Gewinn.")

st.sidebar.markdown("---")
st.sidebar.write("Anleitung: Einfach die Zahlen in der Sidebar ändern, wenn eine neue Ziehung war!")
