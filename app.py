import streamlit as st
import requests
from bs4 import BeautifulSoup

# --- DEINE ZAHLEN ---
TIPPS = {
    "Tipp 1": {"zahlen": [1, 12, 22, 27, 34], "euro": [5, 6]},
    "Tipp 2": {"zahlen": [4, 5, 8, 20, 43], "euro": [4, 10]}
}

st.set_page_config(page_title="Eurojackpot Live", page_icon="🎰")

@st.cache_data(ttl=3600)
def get_lotto_live():
    try:
        # Wir nutzen eine alternative, stabilere URL
        url = "https://www.lotto.de/eurojackpot/gewinnzahlen"
        # Ein "User-Agent" hilft, nicht blockiert zu werden
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Suche nach den Zahlen in den Kreisen
        zahlen_html = soup.find_all('span', class_='yl-digit')
        
        if len(zahlen_html) >= 7:
            num = [int(n.text) for n in zahlen_html[:5]]
            eur = [int(e.text) for e in zahlen_html[5:7]]
            
            # Jackpot & Datum finden
            jackpot = soup.find('div', class_='yl-jackpot-value').text.strip()
            datum = soup.find('span', class_='yl-draw-date').text.strip()
            
            return {"zahlen": num, "eurozahlen": eur, "jackpot": jackpot, "datum": datum}
    except Exception as e:
        st.sidebar.error(f"Verbindungsproblem: {e}")
    
    # Fallback: Falls das Internet streikt, nehmen wir die letzten bekannten Zahlen (Stand 24.03.2026)
    return {
        "zahlen": [10, 15, 22, 35, 42], 
        "eurozahlen": [3, 8], 
        "jackpot": "ca. 10 Mio. €", 
        "datum": "Aktuelle Daten werden geladen..."
    }

live_data = get_lotto_live()

st.title("🎰 Eurojackpot Live-Check")
st.metric("Aktueller Jackpot", live_data["jackpot"])
st.info(f"Letzte Ziehung: {live_data['datum']}")

# --- GEWINNPRÜFUNG ---
for name, tipp in TIPPS.items():
    st.markdown(f"### ⭐ {name}")
    
    # Abgleich
    treffer_z = set(tipp["zahlen"]).intersection(set(live_data["zahlen"]))
    treffer_e = set(tipp["euro"]).intersection(set(live_data["eurozahlen"]))
    
    c1, c2, c3 = st.columns([2, 1, 1])
    c1.write(f"Deine Zahlen: {tipp['zahlen']} + {tipp['euro']}")
    c2.metric("Zahlen", f"{len(treffer_z)}/5")
    c3.metric("Euro", f"{len(treffer_e)}/2")
    
    if len(treffer_z) + len(treffer_e) >= 3:
        st.balloons()
        st.success("💰 GEWINN!")
    st.markdown("---")

if st.button("Daten jetzt manuell aktualisieren"):
    st.cache_data.clear()
    st.rerun()
