import streamlit as st

# --- EURE DAUER-TIPPS ---
TIPPS = {
    "Tipp 1": {"zahlen": [1, 12, 22, 27, 34], "euro": [5, 6]},
    "Tipp 2": {"zahlen": [4, 5, 8, 20, 43], "euro": [4, 10]}
}

st.set_page_config(page_title="Eurojackpot Check", page_icon="🎰", layout="wide")

# --- SEITENLEISTE: MANUELLE KONTROLLE ---
st.sidebar.header("📝 Ziehung aktualisieren")
st.sidebar.write("Trage hier die Zahlen vom Freitag/Dienstag ein:")

# Standardwerte (Echte Zahlen vom 24.03.2026)
zug_z = st.sidebar.text_input("Gezogene Zahlen (mit Komma)", "9,15,23,43,48")
zug_e = st.sidebar.text_input("Gezogene Eurozahlen (mit Komma)", "3,5")
zug_j = st.sidebar.text_input("Jackpot Höhe", "23 Mio. €")
zug_d = st.sidebar.text_input("Datum der Ziehung", "Dienstag, 24.03.2026")

# Umwandlung der Eingabe in Listen für den Vergleich
try:
    final_z = [int(x.strip()) for x in zug_z.split(",")]
    final_e = [int(x.strip()) for x in zug_e.split(",")]
except:
    st.sidebar.error("Bitte Zahlen korrekt mit Komma trennen!")
    final_z, final_e = [0,0,0,0,0], [0,0]

# --- HAUPTBEREICH ---
st.title("🎰 Eurojackpot: Gewinn-Check")
st.metric("Aktueller Jackpot", zug_j)
st.info(f"Ergebnisse für die Ziehung am {zug_d}")

st.markdown("---")

# AUSWERTUNG DER 2 TIPPS (Direkter Vergleich)
st.header("🔍 Abgleich mit unseren Dauer-Tipps")
c1, c2 = st.columns(2)

for i, (name, tipp) in enumerate(TIPPS.items()):
    with (c1 if i == 0 else c2):
        st.subheader(f"⭐ {name}")
        
        # Treffer finden (Schnittmenge)
        t_z = set(tipp["zahlen"]).intersection(set(final_z))
        t_e = set(tipp["euro"]).intersection(set(final_e))
        
        st.write(f"Unser Tipp: `{tipp['zahlen']}` | Euro: `{tipp['euro']}`")
        
        m1, m2 = st.columns(2)
        m1.metric("Richtige Zahlen", f"{len(t_z)}/5", f"+{list(t_z)}" if t_z else None)
        m2.metric("Eurozahlen", f"{len(t_e)}/2", f"+{list(t_e)}" if t_e else None)
        
        # Gewinn-Logik
        if (len(t_z) >= 2 and len(t_e) >= 1) or len(t_z) >= 3:
            st.balloons()
            st.success("💰 GEWINN! Kontostand prüfen!")
        else:
            st.info("Diese Woche leider kein Treffer.")

st.sidebar.markdown("---")
st.sidebar.write("💡 **Info:** Die Gewinnprüfung erfolgt direkt gegen die oben in der Leiste eingetragenen Zahlen.")
