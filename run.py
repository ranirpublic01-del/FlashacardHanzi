import tkinter as tk
from tkinter import messagebox
import json
import random
import os

FILE_DATA = r"D:\01_Project\01_Coding\PY\flashcard\subject.json"

# Font
# SimSun Untuk yang di buku basic 
# Gangjian Handwriting untuk tulisan org cina asli
# Microsoft YaHei untuk ketikan di hp

# =====================
# Load Data
# =====================
def load_cards():
    if not os.path.exists(FILE_DATA):
        return []

    with open(FILE_DATA, "r", encoding="utf-8") as f:
        return json.load(f)


def save_cards(cards):
    with open(FILE_DATA, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=4)


cards = load_cards()

if not cards:
    cards = [
        {
            "hanzi": "你好",
            "pinyin": "nǐ hǎo",
            "arti": "Halo"
        }
    ]
    save_cards(cards)

current_card = None
showing_answer = False


# =====================
# Flashcard Functions
# =====================
def next_card_key(event):
    next_card()
    


def next_card():
    global current_card, showing_answer

    current_card = random.choice(cards)

    card_label.config(
        text=current_card["hanzi"]
    )

    info_label.config(text="")

    showing_answer = False


def toggle_answer(event=None):
    global showing_answer

    if not current_card:
        return

    if showing_answer:
        # Sembunyikan jawaban
        info_label.config(text="")
        showing_answer = False
    else:
        # Tampilkan jawaban
        info_label.config(
            text=f"Pinyin : {current_card['pinyin']}\nArti : {current_card['arti']}"
        )
        showing_answer = True


# =====================
# Add Card Window
# =====================
def add_card_window():

    win = tk.Toplevel(root)
    win.title("Tambah Flashcard")
    win.geometry("300x250")

    tk.Label(win, text="Hanzi").pack()
    hanzi_entry = tk.Entry(win, font=("Arial", 16))
    hanzi_entry.pack(fill="x", padx=10)

    tk.Label(win, text="Pinyin").pack()
    pinyin_entry = tk.Entry(win)
    pinyin_entry.pack(fill="x", padx=10)

    tk.Label(win, text="Arti").pack()
    arti_entry = tk.Entry(win)
    arti_entry.pack(fill="x", padx=10)

    def save_new():

        hanzi = hanzi_entry.get().strip()
        pinyin = pinyin_entry.get().strip()
        arti = arti_entry.get().strip()

        if not hanzi:
            messagebox.showerror(
                "Error",
                "Hanzi tidak boleh kosong"
            )
            return

        cards.append({
            "hanzi": hanzi,
            "pinyin": pinyin,
            "arti": arti
        })

        save_cards(cards)

        messagebox.showinfo(
            "Sukses",
            "Flashcard berhasil ditambahkan"
        )

        win.destroy()

    tk.Button(
        win,
        text="Simpan",
        command=save_new
    ).pack(pady=15)


# =====================
# GUI
# =====================
root = tk.Tk()
root.title("Flashcard Hanzi Mandarin")
root.geometry("800x600")

title = tk.Label(
    root,
    text="FLASH CARD HANZI",
    font=("Arial", 20, "bold")
)
title.pack(pady=10)

card_label = tk.Label(
    root,
    text="",
    font=("SimSun", 60),
    anchor="center",
    justify="center"
)

# Area kartu memenuhi ruang kosong
card_label.pack(
    expand=True,
    fill="both"
)

info_label = tk.Label(
    root,
    text="",
    font=("Arial", 16)
)
info_label.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(
    side="bottom",
    pady=20
)

tk.Button(
    btn_frame,
    text="Tampilkan Jawaban",
    command=toggle_answer
).grid(row=0, column=0, padx=5)

tk.Button(
    btn_frame,
    text="Kartu Berikutnya",
    command=next_card
).grid(row=0, column=1, padx=5)

tk.Button(
    btn_frame,
    text="Tambah Kartu",
    command=add_card_window
).grid(row=0, column=2, padx=5)


# =====================
# Auto Resize Font
# =====================
def resize_font(event):
    try:
        width = root.winfo_width()

        # Ukuran font mengikuti lebar window
        hanzi_size = max(60, int(width / 5))
        info_size = max(14, int(width / 50))

        card_label.config(
            font=("SimSun", hanzi_size)
        )

        info_label.config(
            font=("Arial", info_size)
        )

    except:
        pass


root.bind("<Configure>", resize_font)
root.bind("<Return>", lambda event: next_card())
root.bind("<space>", toggle_answer)

next_card()

root.mainloop()