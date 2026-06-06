import tkinter as tk
from tkinter import messagebox
import json
import random
import os

FLASHCARD_FOLDER = r"D:\01_Project\01_Coding\PY\flashcard"

def get_json_files():
    files = []

    for file in os.listdir(FLASHCARD_FOLDER):
        if file.lower().endswith(".json"):
            files.append(file)

    files.sort()
    return files



# =====================
# Load Data
# =====================
def load_cards():

    file_path = os.path.join(
        FLASHCARD_FOLDER,
        selected_file.get()
    )

    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:

        messagebox.showerror(
            "JSON Error",
            f"File tidak valid:\n{file_path}"
        )

        return []
    



def save_cards(cards):

    file_path = os.path.join(
        FLASHCARD_FOLDER,
        selected_file.get()
    )

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=4)


cards = []

current_card = None
showing_answer = False

deck = []
deck_index = 0


# =====================
# Auto Font Size
# =====================
def get_font_size(text):

    length = len(text)

    if length <= 2:
        return 180
    elif length <= 4:
        return 150
    elif length <= 8:
        return 120
    elif length <= 12:
        return 90
    elif length <= 20:
        return 70
    elif length <= 30:
        return 55
    elif length <= 50:
        return 45
    else:
        return 35


def create_new_deck():
    global deck, deck_index

    deck = cards.copy()
    random.shuffle(deck)

    deck_index = 0

# =====================
# Flashcard Functions
# =====================
def next_card():

    global current_card
    global showing_answer
    global deck_index

    if len(deck) == 0:
        create_new_deck()

    if deck_index >= len(deck):

        messagebox.showinfo(
            "Sesi Selesai",
            "Semua kartu telah ditampilkan.\nMengacak ulang deck..."
        )

        create_new_deck()

    current_card = deck[deck_index]
    deck_index += 1

    mode = quiz_mode.get()

    if mode == "hanzi":
        display_text = current_card["hanzi"]
        font_name = "SimSun"

    elif mode == "pinyin":
        display_text = current_card["pinyin"]
        font_name = "Arial"

    else:
        display_text = current_card["arti"]
        font_name = "Arial"

    font_size = get_font_size(display_text)

    card_label.config(
        text=display_text,
        font=(font_name, font_size)
    )

    info_label.config(
        text=f"Kartu {deck_index}/{len(deck)}"
    )

    showing_answer = False


def toggle_answer(event=None):

    global showing_answer

    if not current_card:
        return

    mode = quiz_mode.get()

    if showing_answer:
        info_label.config(
    text=f"Kartu {deck_index}/{len(deck)}"
)
        showing_answer = False
        return

    if mode == "hanzi":

        answer = (
            f"Pinyin : {current_card['pinyin']}\n"
            f"Arti   : {current_card['arti']}"
        )

    elif mode == "pinyin":

        answer = (
            f"Hanzi : {current_card['hanzi']}\n"
            f"Arti  : {current_card['arti']}"
        )

    else:

        answer = (
            f"Hanzi  : {current_card['hanzi']}\n"
            f"Pinyin : {current_card['pinyin']}"
        )

    info_label.config(
    text=(
        answer +
        f"\n\nKartu {deck_index}/{len(deck)}"
    )
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

    hanzi_entry = tk.Entry(
        win,
        font=("Arial", 16)
    )
    hanzi_entry.pack(
        fill="x",
        padx=10
    )

    tk.Label(win, text="Pinyin").pack()

    pinyin_entry = tk.Entry(win)
    pinyin_entry.pack(
        fill="x",
        padx=10
    )

    tk.Label(win, text="Arti").pack()

    arti_entry = tk.Entry(win)
    arti_entry.pack(
        fill="x",
        padx=10
    )

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
# Resize Window
# =====================
def resize_font(event):

    try:

        card_label.config(
            wraplength=root.winfo_width() - 80
        )

        info_label.config(
            font=(
                "Arial",
                max(14, int(root.winfo_width() / 50))
            )
        )

    except:
        pass

def change_deck(event=None):

    global cards

    cards = load_cards()

    create_new_deck()
    next_card()


# =====================
# GUI
# =====================
root = tk.Tk()
    

root.title("Flashcard Hanzi Mandarin")
root.geometry("1000x700")

json_files = get_json_files()

selected_file = tk.StringVar()

if json_files:
    selected_file.set(json_files[0])
else:
    selected_file.set("")

quiz_mode = tk.StringVar(value="hanzi")

title = tk.Label(
    root,
    text="FLASH CARD HANZI",
    font=("Arial", 20, "bold")
)
title.pack(pady=10)

deck_frame = tk.Frame(root)
deck_frame.pack(pady=5)

tk.Label(
    deck_frame,
    text="Deck:"
).pack(side="left")

deck_menu = tk.OptionMenu(
    deck_frame,
    selected_file,
    *json_files,
    command=lambda _: change_deck()
)

deck_menu.pack(
    side="left",
    padx=10
)


# =====================
# Mode Selection
# =====================
mode_frame = tk.Frame(root)
mode_frame.pack(pady=5)

tk.Radiobutton(
    mode_frame,
    text="Hanzi",
    variable=quiz_mode,
    value="hanzi",
    command=next_card
).pack(side="left", padx=10)

tk.Radiobutton(
    mode_frame,
    text="Pinyin",
    variable=quiz_mode,
    value="pinyin",
    command=next_card
).pack(side="left", padx=10)

tk.Radiobutton(
    mode_frame,
    text="Arti",
    variable=quiz_mode,
    value="arti",
    command=next_card
).pack(side="left", padx=10)

# =====================
# Card Area
# =====================
card_label = tk.Label(
    root,
    text="",
    font=("SimSun", 120),
    justify="center",
    anchor="center",
    wraplength=900
)

card_label.pack(
    expand=True,
    fill="both",
    padx=20,
    pady=20
)

info_label = tk.Label(
    root,
    text="",
    font=("Arial", 16),
    justify="center"
)

info_label.pack(pady=10)

# =====================
# Buttons
# =====================
btn_frame = tk.Frame(root)

btn_frame.pack(
    side="bottom",
    pady=20
)

tk.Button(
    btn_frame,
    text="Acak Ulang",
    command=lambda: (
        create_new_deck(),
        next_card()
    )
).grid(
    row=0,
    column=3,
    padx=5
)

tk.Button(
    btn_frame,
    text="Tampilkan Jawaban",
    command=toggle_answer
).grid(
    row=0,
    column=0,
    padx=5
)

tk.Button(
    btn_frame,
    text="Kartu Berikutnya",
    command=next_card
).grid(
    row=0,
    column=1,
    padx=5
)

tk.Button(
    btn_frame,
    text="Tambah Kartu",
    command=add_card_window
).grid(
    row=0,
    column=2,
    padx=5
)

# =====================
# Mode Shortcuts
# =====================
def set_mode_hanzi(event=None):
    quiz_mode.set("hanzi")
    next_card()

def set_mode_pinyin(event=None):
    quiz_mode.set("pinyin")
    next_card()

def set_mode_arti(event=None):
    quiz_mode.set("arti")
    next_card()


# =====================
# Keyboard Shortcuts
# =====================
root.bind("<Return>", lambda event: next_card())
root.bind("<space>", toggle_answer)

root.bind("1", set_mode_hanzi)
root.bind("2", set_mode_pinyin)
root.bind("3", set_mode_arti)

root.bind("<Configure>", resize_font)

# =====================
# Start
# =====================
cards = load_cards()

create_new_deck()
next_card()

root.mainloop()