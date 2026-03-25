import streamlit as st
import requests
from datetime import datetime

# --- KONFIGURATION: EURE ZAHLEN ---
# Hier eure echten Zahlen eintragen!
UNSERE_ZAHLEN = [5, 12, 20, 35, 48] 
UNSERE_EUROZAHLEN = [7, 9]

st.set_page_config(page_title="Eurojackpot Tippgemeinschaft", page_icon="🎰")

st.title("🎰 Eurojackpot Tippgemeinschaft")
st.markdown("---")

# Funktion zum Holen der echten Zahlen (Beispiel-Logik für den Start)
def get_lotto_data():
    # Hinweis: Wir nutzen hier eine einfache Simulation. 
    # Für echte Live-Daten kann man später eine API anbinden.
    return {
        "zahlen": [5, 15, 22, 35, 42], 
        "eurozahlen": [7, 10],
        "datum": "Freitag, 20.03.2026",
        "jackpot": "120 Mio. €"
    }

data = get_lotto_data()

# Jackpot-Anzeige
st.metric("Aktueller Jackpot", data["jackpot"])

st.subheader(f"Ziehung vom {data['datum']}")

# Vergleich der Zahlen
treffer = set(UNSERE_ZAHLEN).intersection(set(data["zahlen"]))
euro_treffer = set(UNSERE_EUROZAHLEN).intersection(set(data["eurozahlen"]))

col1, col2 = st.columns(2)
with col1:
    st.write("Unsere Zahlen:")
    st.info(f"{UNSERE_ZAHLEN}")
with col2:
    st.write("Gezogene Zahlen:")
    st.success(f"{data['zahlen']}")

st.markdown("---")
st.header("🔍 Ergebnis-Check")
c1, c2 = st.columns(2)
c1.metric("Richtige Zahlen", f"{len(treffer)} von 5")
c2.metric("Richtige Eurozahlen", f"{len(euro_treffer)} von 2")

if len(treffer) + len(euro_treffer) >= 3:
    st.balloons()
    st.success("💰 GEWINN! Wir sollten das Konto prüfen!")
else:
    st.info("Nichts gewonnen. Der Dauerauftrag läuft weiter. Viel Glück beim nächsten Mal! 🍀")

st.sidebar.write("Diese App gleicht unseren Dauerauftrag automatisch mit den Ziehungen ab.")
