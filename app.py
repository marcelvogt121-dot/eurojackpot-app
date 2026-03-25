import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# --- KONFIGURATION: EURE ECHTEN ZAHLEN (FEST HINTERLEGT) ---
TIPPS = {
    "Tipp 1": {"zahlen": [1, 12, 22, 27, 34], "euro": [5, 6]},
    "Tipp 2": {"zahlen": [4, 5, 8, 20, 43], "euro": [4, 10]}
}

st.set_page_config(page_title="Eurojackpot Live-Check", page_icon="🎰", layout="wide")

# FUNKTION: Holt die echten Daten live von einer Lotto-Seite
@st.cache_data(ttl=3600) # Speichert die Daten für 1 Stunde, um die Seite nicht zu überlasten
def get_live_eurojackpot_data():
    try:
        # Wir nutzen eine zuverlässige Quelle für die Gewinnzahlen
        url = "https://www.lotto.de/eurojackpot/gewinnzahlen"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraktion der Zahlen (Logik angepasst an lotto.de Struktur)
        # Hinweis: Scraper sind anfällig für Designänderungen der Webseite.
        numbers = [int(n.text) for n in soup.find_all('span', class_='yl-digit')[:5]]
        euros = [int(e.text) for e in soup.find_all('span', class_='yl-digit')[5:7]]
        
        # Extraktion Jackpot-Höhe
        jackpot_text = soup.find('div', class_='yl-jackpot-value').text.strip()
        datum_text = soup.find('span', class_='yl-draw-date').text.strip()
        
        return {"zahlen": numbers, "eurozahlen": euros, "jackpot": jackpot_text, "datum": datum_text}
    except:
        # Fallback, falls die Seite das Design ändert oder blockiert
        return {
            "zahlen": [1, 2, 3, 4, 5], 
            "eurozahlen": [1, 2], 
            "jackpot": "Daten laden fehlgeschlagen", 
            "datum": "Fehler beim Abruf"
        }

# Daten laden
live_data = get_live_eurojackpot_data()

st.title("🎰 Eurojackpot: Live-Abgleich")
st.write(f"Automatische Prüfung für unseren Dauerauftrag (Stand: {live_data['datum']})")
st.markdown("---")

# Jackpot-Anzeige
st.metric("Aktueller Jackpot", live_data["jackpot"])

# Anzeige der GEZOGENEN Zahlen
st.subheader(f"Gezogene Zahlen vom {live_data['datum']}")
cols = st.columns(7)
for i, z in enumerate(live_data["zahlen"]):
    cols[i].button(f"{z}", key=f" gezogen_{i}", disabled=True)
for i, e in enumerate(live_data["eurozahlen"]):
    cols[i+5].button(f"{e}", key=f"euro_gezogen_{i}", type="primary", disabled=True)

st.markdown("---")

# AUSWERTUNG
col_f1, col_f2 = st.columns(2)

for i, (name, tipp) in enumerate(TIPPS.items()):
    with (col_f1 if i == 0 else col_f2):
        st.header(f"⭐ {name}")
        
        # Treffer berechnen
        treffer_z = set(tipp["zahlen"]).intersection(set(live_data["zahlen"]))
        treffer_e = set(tipp["euro"]).intersection(set(live_data["eurozahlen"]))
        
        st.write(f"**Unsere Zahlen:** {tipp['zahlen']} | **Euro:** {tipp['euro']}")
        
        m1, m2 = st.columns(2)
        m1.metric("Richtige Zahlen", f"{len(treffer_z)}", f"{list(treffer_z)}" if treffer_z else None)
        m2.metric("Richtige Euro", f"{len(treffer_e)}", f"{list(treffer_e)}" if treffer_e else None)
        
        if (len(treffer_z) >= 2 and len(treffer_e) >= 1) or len(treffer_z) >= 3:
            st.success("💰 GEWINN!")
            st.balloons()
        else:
            st.info("Diese Woche leider kein Treffer.")

st.sidebar.info("Die App aktualisiert sich jede Stunde automatisch mit den neuesten Ziehungen.")
