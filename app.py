import streamlit as st

# --- KONFIGURATION: EURE ECHTEN ZAHLEN ---
TIPPS = {
    "Tipp 1": {"zahlen": [1, 12, 22, 27, 34], "euro": [5, 6]},
    "Tipp 2": {"zahlen": [4, 5, 8, 20, 43], "euro": [4, 10]}
}

st.set_page_config(page_title="Eurojackpot Tippgemeinschaft", page_icon="🎰", layout="wide")

st.title("🎰 Eurojackpot: Unsere Daueraufträge")
st.write("Hier werden unsere festen Zahlen automatisch mit der letzten Ziehung abgeglichen.")
st.markdown("---")

# Aktuelle Ziehungsdaten (Beispielhaft für die letzte Ziehung)
# Diese Zahlen kannst du hier immer nach einer Ziehung aktualisieren:
ziehungs_daten = {
    "zahlen": [1, 15, 22, 29, 34], # Beispielzahlen der Ziehung
    "eurozahlen": [5, 11],         # Beispiel-Eurozahlen
    "datum": "Freitag, 27.03.2026",
    "jackpot": "120 Mio. €"
}

# Jackpot-Anzeige oben
st.metric("Aktueller Jackpot", ziehungs_daten["jackpot"])
st.subheader(f"Ergebnisse der Ziehung vom {ziehungs_daten['datum']}")

# Anzeige der gezogenen Zahlen als Buttons (optische Aufwertung)
cols = st.columns(7)
for i, z in enumerate(ziehungs_daten["zahlen"]):
    cols[i].button(f"{z}", key=f" gezogen_{i}", disabled=True)
for i, e in enumerate(ziehungs_daten["eurozahlen"]):
    cols[i+5].button(f"{e}", key=f"euro_gezogen_{i}", type="primary", disabled=True)

st.markdown("---")

# AUSWERTUNG DER BEIDEN TIPPS
col_f1, col_f2 = st.columns(2)

for i, (name, tipp) in enumerate(TIPPS.items()):
    with (col_f1 if i == 0 else col_f2):
        st.header(f"⭐ {name}")
        
        # Treffer berechnen
        treffer_z = set(tipp["zahlen"]).intersection(set(ziehungs_daten["zahlen"]))
        treffer_e = set(tipp["euro"]).intersection(set(ziehungs_daten["eurozahlen"]))
        
        # Anzeige der eigenen Zahlen
        st.write(f"**Deine Zahlen:** {tipp['zahlen']}")
        st.write(f"**Zusatzzahlen:** {tipp['euro']}")
        
        # Metriken für die Trefferquote
        m1, m2 = st.columns(2)
        m1.metric("Richtige Zahlen", f"{len(treffer_z)} von 5", f"{list(treffer_z)}" if treffer_z else None)
        m2.metric("Richtige Euro", f"{len(treffer_e)} von 2", f"{list(treffer_e)}" if treffer_e else None)
        
        # Gewinn-Check (Mindestens 2 Zahlen + 1 Eurozahl oder Ähnliches)
        if (len(treffer_z) >= 2 and len(treffer_e) >= 1) or len(treffer_z) >= 3:
            st.success("💰 GEWINN IN DIESEM FELD!")
            st.balloons()
        else:
            st.info("Kein Gewinn in dieser Gewinnklasse.")

st.sidebar.header("Tipp-Informationen")
st.sidebar.write("**Dauerauftrag:** Aktiv ✅")
st.sidebar.write("**Mitglieder:** Marcel & Co.")
st.sidebar.markdown("---")
st.sidebar.warning("Hinweis: Gewinne werden ab Klasse 12 angezeigt.")
