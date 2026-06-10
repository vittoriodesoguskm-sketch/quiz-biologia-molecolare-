import streamlit as st
import random
import os

# -------------------------
# CARICAMENTO QUIZ
# -------------------------
def carica_quiz(file):

    with open(file, "r", encoding="utf-8") as f:
        testo = f.read()

    blocchi = testo.split("===")

    domande = []

    for b in blocchi:

        b = b.strip()

        if not b:
            continue

        righe = [r.strip() for r in b.split("\n") if r.strip()]

        domanda = righe[0]

        opzioni = {}
        corretta = []

        for r in righe[1:]:

            if r.startswith("A)"):
                opzioni["A"] = r[2:].strip()

            elif r.startswith("B)"):
                opzioni["B"] = r[2:].strip()

            elif r.startswith("C)"):
                opzioni["C"] = r[2:].strip()

            elif r.startswith("D)"):
                opzioni["D"] = r[2:].strip()

            elif r.startswith("E)"):
                opzioni["E"] = r[2:].strip()

            elif "CORRETTA:" in r:

                corrette_raw = r.split(":")[1].strip()

                corretta = [
                    x.strip()
                    for x in corrette_raw.split(",")
                ]

        domande.append((domanda, opzioni, corretta))

    return domande


# -------------------------
# FILE QUIZ
# -------------------------
quiz_disponibili = {
    "Biologia Molecolare 1": "biologia molecolare 1.txt",
    "Biologia Molecolare 2": "biologia molecolare 2.txt",
    "Biologia Molecolare 3": "biologia molecolare 3.txt",
}

st.set_page_config(
    page_title="Quiz Universitario",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Quiz Universitario")

# -------------------------
# SESSION STATE
# -------------------------
if "domande" not in st.session_state:
    st.session_state.domande = []
    st.session_state.index = 0
    st.session_state.punteggio = 0
    st.session_state.quiz_avviato = False

# -------------------------
# MENU
# -------------------------
if not st.session_state.quiz_avviato:

    quiz_scelto = st.selectbox(
        "Scegli un quiz",
        list(quiz_disponibili.keys())
    )

    casuale = st.checkbox("🎲 Modalità casuale")

    if st.button("Avvia Quiz"):

        file_quiz = quiz_disponibili[quiz_scelto]

        domande = carica_quiz(file_quiz)

        if casuale:
            random.shuffle(domande)

        st.session_state.domande = domande
        st.session_state.index = 0
        st.session_state.punteggio = 0
        st.session_state.quiz_avviato = True

        st.rerun()

# -------------------------
# QUIZ
# -------------------------
else:

    domande = st.session_state.domande
    index = st.session_state.index

    if index < len(domande):

        domanda, opzioni, corrette = domande[index]

        st.subheader(
            f"Domanda {index + 1}/{len(domande)}"
        )

        st.write(domanda)

        selezionate = []

        for k, testo in opzioni.items():

            if st.checkbox(
                f"{k}) {testo}",
                key=f"{index}_{k}"
            ):
                selezionate.append(k)

        if st.button("Conferma risposta"):

            selezionate.sort()
            corrette.sort()

            if selezionate == corrette:

                st.success("✔ Corretto")
                st.session_state.punteggio += 1

            else:

                st.error(
                    f"✘ Sbagliato - Corrette: {', '.join(corrette)}"
                )

            st.session_state.index += 1

            st.rerun()

    else:

        punteggio = st.session_state.punteggio
        totale = len(domande)

        percentuale = int((punteggio / totale) * 100)

        st.success("🎉 Quiz completato!")

        st.write(f"### Punteggio: {punteggio}/{totale}")
        st.write(f"### Percentuale: {percentuale}%")

        if st.button("Torna al menu"):

            st.session_state.quiz_avviato = False

            st.rerun()
            