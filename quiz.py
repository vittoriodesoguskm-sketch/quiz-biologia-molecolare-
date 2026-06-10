import tkinter as tk
import os
import sys
import random


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

        if len(righe) < 2:
            continue

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

        if domanda and opzioni and corretta:
            domande.append((domanda, opzioni, corretta))

    return domande


# -------------------------
# APP
# -------------------------
class QuizApp:

    def __init__(self, root):

        self.root = root

        self.root.title("Quiz App")

        self.root.geometry("900x700")

        self.schermata_iniziale()

    # -------------------------
    # MENU INIZIALE
    # -------------------------
    def schermata_iniziale(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        titolo = tk.Label(
            self.root,
            text="Scegli un quiz",
            font=("Arial", 24)
        )

        titolo.pack(pady=30)

        # -------------------------
        # PATH CORRETTO
        # -------------------------
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        # -------------------------
        # QUIZ DISPONIBILI
        # -------------------------
        quiz_disponibili = {
            "Biologia Molecolare 1": os.path.join(base_path, "biologia molecolare 1.txt"),
            "Biologia Molecolare 2": os.path.join(base_path, "biologia molecolare 2.txt"),
            "Biologia Molecolare 3": os.path.join(base_path, "biologia molecolare 3.txt"),
        }

        for nome, file in quiz_disponibili.items():

            frame = tk.Frame(self.root)
            frame.pack(pady=10)

            # Bottone normale
            btn_normale = tk.Button(
                frame,
                text=nome,
                width=25,
                height=2,
                font=("Arial", 12),
                command=lambda f=file: self.avvia_quiz(f, casuale=False)
            )

            btn_normale.pack(side="left", padx=5)

            # Bottone casuale
            btn_random = tk.Button(
                frame,
                text="🎲 Casuale",
                width=15,
                height=2,
                font=("Arial", 12),
                command=lambda f=file: self.avvia_quiz(f, casuale=True)
            )

            btn_random.pack(side="left", padx=5)

    # -------------------------
    # AVVIO QUIZ
    # -------------------------
    def avvia_quiz(self, file_quiz, casuale=False):

        self.domande = carica_quiz(file_quiz)

        if casuale:
            random.shuffle(self.domande)

        self.index = 0

        self.punteggio = 0

        for widget in self.root.winfo_children():
            widget.destroy()

        self.label_domanda = tk.Label(
            self.root,
            text="",
            wraplength=800,
            font=("Arial", 16),
            justify="left"
        )

        self.label_domanda.pack(pady=20)

        self.vars = {}

        self.checks = {}

        for opt in ["A", "B", "C", "D", "E"]:

            var = tk.IntVar()

            chk = tk.Checkbutton(
                self.root,
                text="",
                variable=var,
                font=("Arial", 13),
                wraplength=700,
                justify="left",
                anchor="w"
            )

            chk.pack(anchor="w", padx=40, pady=5)

            self.vars[opt] = var

            self.checks[opt] = chk

        self.confirm_btn = tk.Button(
            self.root,
            text="Conferma risposta",
            font=("Arial", 14),
            command=self.check
        )

        self.confirm_btn.pack(pady=20)

        self.feedback = tk.Label(
            self.root,
            text="",
            font=("Arial", 14)
        )

        self.feedback.pack(pady=10)

        self.restart_btn = tk.Button(
            self.root,
            text="Torna al menu",
            font=("Arial", 12),
            command=self.schermata_iniziale
        )

        self.carica_domanda()

    # -------------------------
    # CARICA DOMANDA
    # -------------------------
    def carica_domanda(self):

        if self.index >= len(self.domande):

            self.fine()

            return

        domanda, opzioni, _ = self.domande[self.index]

        self.label_domanda.config(
            text=f"Domanda {self.index + 1}/{len(self.domande)}\n\n{domanda}"
        )

        self.feedback.config(text="")

        for k in self.vars:
            self.vars[k].set(0)

        for k in self.checks:

            if k in opzioni:

                self.checks[k].config(
                    text=f"{k}) {opzioni[k]}",
                    state="normal"
                )

            else:

                self.checks[k].config(
                    text="",
                    state="disabled"
                )

    # -------------------------
    # CONTROLLO RISPOSTA
    # -------------------------
    def check(self):

        _, _, corrette = self.domande[self.index]

        selezionate = []

        for k, var in self.vars.items():

            if var.get() == 1:
                selezionate.append(k)

        selezionate.sort()

        corrette.sort()

        if selezionate == corrette:

            self.punteggio += 1

            self.feedback.config(
                text="✔ Corretto",
                fg="green"
            )

        else:

            self.feedback.config(
                text=f"✘ Sbagliato - Corrette: {', '.join(corrette)}",
                fg="red"
            )

        self.index += 1

        self.root.after(1500, self.carica_domanda)

    # -------------------------
    # FINE QUIZ
    # -------------------------
    def fine(self):

        for chk in self.checks.values():
            chk.config(state="disabled")

        self.confirm_btn.config(state="disabled")

        percentuale = int((self.punteggio / len(self.domande)) * 100)

        self.label_domanda.config(
            text=(
                f"Quiz completato!\n\n"
                f"Punteggio: {self.punteggio}/{len(self.domande)}\n"
                f"Percentuale: {percentuale}%"
            )
        )

        self.feedback.config(text="")

        self.restart_btn.pack(pady=20)


# -------------------------
# AVVIO APP
# -------------------------
root = tk.Tk()

app = QuizApp(root)

root.mainloop()