
import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import os

FLASHCARD_FOLDER = r"D:\01_Project\01_Coding\PY\flashcard"

BG_COLOR = "#0f172a"
CARD_COLOR = "#1e293b"
TEXT_COLOR = "#f8fafc"
ACCENT = "#3b82f6"

cards = []
current_card = None
showing_answer = False
deck = []
deck_index = 0


def get_json_files():
    if not os.path.exists(FLASHCARD_FOLDER):
        return []
    files = [f for f in os.listdir(FLASHCARD_FOLDER) if f.lower().endswith(".json")]
    files.sort()
    return files


def load_cards():
    file_path = os.path.join(FLASHCARD_FOLDER, selected_file.get())

    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return []


def save_cards(data):
    file_path = os.path.join(FLASHCARD_FOLDER, selected_file.get())
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_font_size(text):
    l = len(text)
    if l <= 2:
        return 180
    elif l <= 4:
        return 150
    elif l <= 8:
        return 120
    elif l <= 12:
        return 90
    elif l <= 20:
        return 70
    elif l <= 30:
        return 55
    elif l <= 50:
        return 45
    return 35


def create_new_deck():
    global deck, deck_index
    deck = cards.copy()
    random.shuffle(deck)
    deck_index = 0


def next_card():
    global current_card, showing_answer, deck_index

    if not deck:
        create_new_deck()

    if not deck:
        card_label.config(text="Tidak ada data")
        return

    if deck_index >= len(deck):
        messagebox.showinfo("Selesai", "Semua kartu telah ditampilkan.")
        create_new_deck()

    current_card = deck[deck_index]
    deck_index += 1

    mode = quiz_mode.get()

    if mode == "hanzi":
        text = current_card["hanzi"]
        font_name = "SimSun"
    elif mode == "pinyin":
        text = current_card["pinyin"]
        font_name = "Segoe UI"
    else:
        text = current_card["arti"]
        font_name = "Segoe UI"

    card_label.config(
        text=text,
        font=(font_name, get_font_size(text), "bold")
    )

    info_label.config(text=f"Kartu {deck_index}/{len(deck)}")
    showing_answer = False


def toggle_answer(event=None):
    global showing_answer

    if not current_card:
        return

    if showing_answer:
        info_label.config(text=f"Kartu {deck_index}/{len(deck)}")
        showing_answer = False
        return

    mode = quiz_mode.get()

    if mode == "hanzi":
        answer = f"Pinyin : {current_card['pinyin']}\nArti : {current_card['arti']}"
    elif mode == "pinyin":
        answer = f"Hanzi : {current_card['hanzi']}\nArti : {current_card['arti']}"
    else:
        answer = f"Hanzi : {current_card['hanzi']}\nPinyin : {current_card['pinyin']}"

    info_label.config(
        text=answer + f"\n\nKartu {deck_index}/{len(deck)}"
    )

    showing_answer = True


def add_card_window():
    win = tk.Toplevel(root)
    win.title("Tambah Flashcard")
    win.geometry("400x260")
    win.configure(bg=BG_COLOR)

    ttk.Label(win, text="Hanzi").pack(pady=5)
    hanzi = ttk.Entry(win)
    hanzi.pack(fill="x", padx=15)

    ttk.Label(win, text="Pinyin").pack(pady=5)
    pinyin = ttk.Entry(win)
    pinyin.pack(fill="x", padx=15)

    ttk.Label(win, text="Arti").pack(pady=5)
    arti = ttk.Entry(win)
    arti.pack(fill="x", padx=15)

    def save_new():
        h = hanzi.get().strip()

        if not h:
            messagebox.showerror("Error", "Hanzi kosong")
            return

        cards.append({
            "hanzi": h,
            "pinyin": pinyin.get().strip(),
            "arti": arti.get().strip()
        })

        save_cards(cards)
        messagebox.showinfo("Sukses", "Kartu ditambahkan")
        win.destroy()

    ttk.Button(win, text="Simpan", command=save_new).pack(pady=15)


def resize_font(event=None):
    try:
        card_label.config(wraplength=root.winfo_width() - 120)
    except:
        pass


def change_deck(event=None):
    global cards
    cards = load_cards()
    create_new_deck()
    next_card()


root = tk.Tk()
root.title("Mandarin Flashcard Pro")
root.geometry("1200x800")
root.minsize(900, 600)
root.configure(bg=BG_COLOR)

style = ttk.Style()
style.theme_use("clam")

style.configure("TFrame", background=BG_COLOR)
style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=("Segoe UI", 10))
style.configure("TRadiobutton", background=BG_COLOR, foreground=TEXT_COLOR)
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)

json_files = get_json_files()

selected_file = tk.StringVar()
selected_file.set(json_files[0] if json_files else "")

quiz_mode = tk.StringVar(value="hanzi")

title = tk.Label(
    root,
    text="📚 Mandarin Flashcard Pro",
    bg=BG_COLOR,
    fg="white",
    font=("Segoe UI", 24, "bold")
)
title.pack(pady=15)

top_frame = tk.Frame(root, bg=BG_COLOR)
top_frame.pack()

ttk.Label(top_frame, text="Deck").pack(side="left", padx=5)

deck_combo = ttk.Combobox(
    top_frame,
    textvariable=selected_file,
    values=json_files,
    width=40,
    state="readonly"
)
deck_combo.pack(side="left")
deck_combo.bind("<<ComboboxSelected>>", change_deck)

mode_frame = tk.Frame(root, bg=BG_COLOR)
mode_frame.pack(pady=10)

for text, value in [
    ("Hanzi", "hanzi"),
    ("Pinyin", "pinyin"),
    ("Arti", "arti")
]:
    ttk.Radiobutton(
        mode_frame,
        text=text,
        variable=quiz_mode,
        value=value,
        command=next_card
    ).pack(side="left", padx=10)

card_frame = tk.Frame(
    root,
    bg=CARD_COLOR,
    relief="flat",
    bd=0
)
card_frame.pack(expand=True, fill="both", padx=40, pady=20)

card_label = tk.Label(
    card_frame,
    text="",
    bg=CARD_COLOR,
    fg="white",
    font=("SimSun", 120, "bold"),
    justify="center"
)
card_label.pack(expand=True)

info_label = tk.Label(
    root,
    text="",
    bg=BG_COLOR,
    fg="#cbd5e1",
    font=("Segoe UI", 12)
)
info_label.pack(pady=10)

btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=10)

ttk.Button(
    btn_frame,
    text="👁 Jawaban",
    command=toggle_answer
).grid(row=0, column=0, padx=5)

ttk.Button(
    btn_frame,
    text="➡ Berikutnya",
    command=next_card
).grid(row=0, column=1, padx=5)

ttk.Button(
    btn_frame,
    text="🔀 Acak",
    command=lambda: (create_new_deck(), next_card())
).grid(row=0, column=2, padx=5)

ttk.Button(
    btn_frame,
    text="➕ Tambah",
    command=add_card_window
).grid(row=0, column=3, padx=5)

status = tk.Label(
    root,
    text="SPACE = Jawaban | ENTER = Next | 1-2-3 = Mode",
    bg="#020617",
    fg="#94a3b8",
    font=("Segoe UI", 9)
)
status.pack(side="bottom", fill="x")

root.bind("<space>", toggle_answer)
root.bind("<Return>", lambda e: next_card())
root.bind("1", lambda e: (quiz_mode.set("hanzi"), next_card()))
root.bind("2", lambda e: (quiz_mode.set("pinyin"), next_card()))
root.bind("3", lambda e: (quiz_mode.set("arti"), next_card()))
root.bind("<Configure>", resize_font)

cards = load_cards()
create_new_deck()
next_card()

root.mainloop()
