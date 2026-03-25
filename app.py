import streamlit as st
import requests
import pandas as pd

# --- DEINE DATEN (HIER ANPASSEN) ---
UNSERE_ZAHLEN = [5, 12, 20, 35, 48] 
UNSERE_EUROZAHLEN = [7, 9]

st.set_page_config(page_title="Eurojackpot Tippgemeinschaft", page_icon="🎰", layout="centered")

st.title("🎰 Eurojackpot Dauerauftrag")
st.write("Unsere Zahlen werden automatisch mit der letzten Ziehung verglichen.")
st.markdown("---")

# Funktion zum Abrufen der Daten (Simulation der letzten Ziehung)
def get_lotto_results():
    # In einer echten App nutzen wir hier eine API. 
    # Für den Start setzen wir die aktuellen Ziehungsdaten manuell:
    return {
        "zahlen": [5, 14, 21, 35, 49], 
        "eurozahlen": [2, 9],
        "datum": "Freitag, 20.03.2026",
        "jackpot": "120 Mio. €"
    }

data = get_lotto_results()

# Jackpot-Anzeige als Highlight
st.metric("Aktueller Jackpot", data["jackpot"])
st.subheader(f"Ziehung vom {data['datum']}")

# Vergleichs-Logik
treffer = set(UNSERE_ZAHLEN).intersection(set(data["zahlen"]))
euro_treffer = set(UNSERE_EUROZAHLEN).intersection(set(data["eurozahlen"]))

# Visuelle Aufbereitung
c1, c2 = st.columns(2)
with c1:
    st.info(f"**Unsere Zahlen:**\n{UNSERE_ZAHLEN}")
with c2:
    st.success(f"**Gezogene Zahlen:**\n{data['zahlen']}")

st.markdown("---")

# Gewinn-Check
st.header("🔍 Ergebnis")
col_a, col_b = st.columns(2)
col_a.metric("Richtige (5)", f"{len(treffer)}")
col_b.metric("Eurozahlen (2)", f"{len(euro_treffer)}")

if len(treffer) + len(euro_treffer) >= 3:
    st.balloons()
    st.success("💰 GEWINN! Wir haben etwas getroffen!")
else:
    st.warning("Kein Gewinn diesmal. Kopf hoch, der Dauerauftrag läuft weiter! 🍀")

# Seitenleiste für die Gemeinschaft
st.sidebar.header("Tippgemeinschaft")
st.sidebar.write("Mitglieder: 3")
st.sidebar.write("Status: Dauerauftrag AKTIV ✅")
