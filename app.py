import streamlit as st
import requests

# --- EURE ZAHLEN ---
TIPPS = {
    "Tipp 1": {"zahlen": [1, 12, 22, 27, 34], "euro": [5, 6]},
    "Tipp 2": {"zahlen": [4, 5, 8, 20, 43], "euro": [4, 10]}
}

st.set_page_config(page_title="Eurojackpot Live-Check", page_icon="🎰", layout="wide")

# FUNKTION: Holt Daten von einer stabilen API-Schnittstelle
@st.cache_data(ttl=600)
def get_lotto_api():
    try:
        # Wir nutzen eine API, die direkt saubere Daten liefert (Beispiel-Schnittstelle)
        url = "https://www.lotto.de/api/stats/eurojackpot"
        data = requests.get(url, timeout=5).json()
        
        # Wir extrahieren die echten Daten aus der Antwort
        last = data.get('lastDraw', {})
        return {
            "z": last.get('numbers', [1, 2, 3, 4, 5]),
            "e": last.get('euroNumbers', [1, 2]),
            "jackpot": f"{data.get('jackpot', '??')} Mio. €",
            "datum": last.get('date', 'Unbekannt')
        }
    except:
        return None

# Daten abrufen
api_data = get_lotto_api()

# --- SEITENLEISTE: DIE MASTER-KONTROLLE ---
st.sidebar.header("🛠️ Gewinnzahlen-Kontrolle")
st.sidebar.write("Falls die Automatik die falschen Zahlen lädt, trage hier die echten ein:")

# Standardwerte setzen (entweder von API oder Platzhalter)
if api_data:
    default_z = ",".join(map(str, api_data["z"]))
    default_e = ",".join(map(str, api_data["e"]))
    default_j = api_data["jackpot"]
    default_d = api_data["datum"]
else:
    default_z, default_e, default_j, default_d = "1,15,22,29,34", "5,11", "120 Mio. €", "Letzte Ziehung"

# Eingabefelder in der Sidebar
input_z = st.sidebar.text_input("Gezogene Zahlen (mit Komma)", default_z)
input_e = st.sidebar.text_input("Gezogene Eurozahlen (mit Komma)", default_e)
input_j = st.sidebar.text_input("Aktueller Jackpot", default_j)
input_d = st.sidebar.text_input("Datum der Ziehung", default_d)

# Umwandeln der Texteingabe in Zahlen-Listen
try:
    final_z = [int(x.strip()) for x in input_z.split(",")]
    final_e = [int(x.strip()) for x in input_e.split(",")]
except:
    st.error("Bitte Zahlen im Format 1,2,3... eingeben!")
    final_z, final_e = [0,0,0,0,0], [0,0]

# --- HAUPTBEREICH ---
st.title("🎰 Eurojackpot Live-Check")
st.metric("Aktueller Jackpot", input_j)
st.write(f"Stand der Ziehung: **{input_d}**")

st.markdown("---")
st.subheader("Offizielle Ziehungszahlen:")

# Anzeige der gezogenen Zahlen in Kreisen
cols = st.columns(7)
for i, val in enumerate(final_z):
    cols[i].markdown(f"<div style='text-align:center; padding:15px; border-radius:50%; background-color:#FFD700; color:black; font-weight:bold; font-size:20px;'>{val}</div>", unsafe_allow_html=True)
for i, val in enumerate(final_e):
    cols[i+5].markdown(f"<div style='text-align:center; padding:15px; border-radius:50%; background-color:#1E90FF; color:white; font-weight:bold; font-size:20px;'>{val}</div>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# AUSWERTUNG DER TIPPS
st.header("🔍 Abgleich mit unseren Tipps")
c1, c2 = st.columns(2)

for i, (name, tipp) in enumerate(TIPPS.items()):
    with (c1 if i == 0 else c2):
        st.subheader(f"⭐ {name}")
        
        # Treffer berechnen
        t_z = set(tipp["zahlen"]).intersection(set(final_z))
        t_e = set(tipp["euro"]).intersection(set(final_e))
        
        st.write(f"Unsere Zahlen: `{tipp['zahlen']}` | Euro: `{tipp['euro']}`")
        
        m1, m2 = st.columns(2)
        m1.metric("Richtige (5)", f"{len(t_z)}", f"+{list(t_z)}" if t_z else None)
        m2.metric("Euro (2)", f"{len(t_e)}", f"+{list(t_e)}" if t_e else None)
        
        if len(t_z) + len(t_e) >= 3:
            st.balloons()
            st.success("💰 GEWINN!")
        else:
            st.info("Leider kein Gewinn in diesem Feld.")

st.sidebar.markdown("---")
if st.sidebar.button("🔄 App neu laden"):
    st.cache_data.clear()
    st.rerun()
