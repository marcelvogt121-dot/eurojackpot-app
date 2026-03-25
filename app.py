import streamlit as st
import requests
from bs4 import BeautifulSoup

# --- DEINE ZAHLEN (FEST) ---
TIPPS = {
    "Tipp 1": {"zahlen": [1, 12, 22, 27, 34], "euro": [5, 6]},
    "Tipp 2": {"zahlen": [4, 5, 8, 20, 43], "euro": [4, 10]}
}

st.set_page_config(page_title="Eurojackpot Check", page_icon="🎰")

# FUNKTION: Versucht die echten Zahlen zu holen
def fetch_lotto_data():
    try:
        url = "https://www.lotto.de/eurojackpot"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Suche nach den Gewinnzahlen im HTML
        # Hinweis: Wenn lotto.de das Design ändert, müssen wir hier nachbessern
        digits = [d.text.strip() for d in soup.find_all('span', class_='yl-digit')]
        
        if len(digits) >= 7:
            return {
                "z": [int(x) for x in digits[:5]],
                "e": [int(x) for x in digits[5:7]],
                "jackpot": soup.find('div', class_='yl-jackpot-value').text.strip(),
                "datum": soup.find('span', class_='yl-draw-date').text.strip()
            }
    except:
        pass
    return None

# Daten abrufen
live_results = fetch_lotto_data()

# --- SEITENLEISTE FÜR MANUELLE KORREKTUR ---
st.sidebar.header("⚙️ Daten-Kontrolle")
st.sidebar.write("Falls die Automatik hakt, hier korrigieren:")

if live_results:
    def_z = ",".join(map(str, live_results["z"]))
    def_e = ",".join(map(str, live_results["e"]))
    def_j = live_results["jackpot"]
else:
    def_z, def_e, def_j = "1,2,3,4,5", "1,2", "10 Mio. €"

input_z = st.sidebar.text_input("Gezogene Zahlen (mit Komma)", def_z)
input_e = st.sidebar.text_input("Gezogene Eurozahlen (mit Komma)", def_e)
input_j = st.sidebar.text_input("Aktueller Jackpot", def_j)

# Umwandeln der Inputs in Listen
final_z = [int(x.strip()) for x in input_z.split(",")]
final_e = [int(x.strip()) for x in input_e.split(",")]

# --- HAUPTBEREICH ---
st.title("🎰 Eurojackpot Live-Check")
st.metric("Aktueller Jackpot", input_j)
st.write(f"Abgleich für unsere 2 Felder")

st.markdown("---")
st.subheader("Gezogene Zahlen dieser Woche:")
c_z = st.columns(7)
for i, val in enumerate(final_z):
    c_z[i].success(f"**{val}**")
for i, val in enumerate(final_e):
    c_z[i+5].warning(f"**{val}**")

st.markdown("---")

# AUSWERTUNG
for name, tipp in TIPPS.items():
    st.subheader(f"⭐ {name}")
    
    t_z = set(tipp["zahlen"]).intersection(set(final_z))
    t_e = set(tipp["euro"]).intersection(set(final_e))
    
    col1, col2, col3 = st.columns([2,1,1])
    col1.write(f"Tipp: {tipp['zahlen']} | Euro: {tipp['euro']}")
    col2.metric("Richtige", f"{len(t_z)}")
    col3.metric("Eurozahlen", f"{len(t_e)}")
    
    if len(t_z) + len(t_e) >= 3:
        st.balloons()
        st.success("💰 GEWINN!")
    st.markdown("---")
