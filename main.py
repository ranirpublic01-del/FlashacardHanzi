import os
import json
import random

from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog

FLASHCARD_FOLDER = "flashcards"

from kivy.core.text import LabelBase

LabelBase.register(
    name="HanziFont",
    fn_regular="fonts/Noto Sans Bold 700.ttf"
)
class FlashcardApp(MDApp):

    current_text = StringProperty("")
    info_text = StringProperty("")
    deck_name = StringProperty("")

    def build(self):

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        self.cards = []
        self.deck = []
        self.deck_index = 0
        self.current_card = None
        self.showing_answer = False
        self.quiz_mode = "hanzi"

        return Builder.load_file("flashcard.kv")

    def on_start(self):

        self.json_files = self.get_json_files()

        if self.json_files:
            self.deck_name = self.json_files[0]
            self.load_deck()

        self.create_menu()

    # =====================
    # JSON
    # =====================
    def get_json_files(self):

        if not os.path.exists(FLASHCARD_FOLDER):
            os.makedirs(FLASHCARD_FOLDER)

        return sorted([
            f for f in os.listdir(FLASHCARD_FOLDER)
            if f.endswith(".json")
        ])

    def load_cards(self):

        path = os.path.join(
            FLASHCARD_FOLDER,
            self.deck_name
        )

        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)

        except:
            return []

    # =====================
    # Menu Deck
    # =====================
    def create_menu(self):

        items = []

        for file in self.json_files:

            items.append({
                "text": file,
                "on_release":
                    lambda x=file: self.select_deck(x)
            })

        self.menu = MDDropdownMenu(
            caller=self.root.ids.deck_btn,
            items=items,
            width_mult=4
        )

    def open_menu(self):
        self.menu.open()

    def select_deck(self, filename):

        self.deck_name = filename

        self.menu.dismiss()

        self.load_deck()

    # =====================
    # Deck
    # =====================
    def load_deck(self):

        self.cards = self.load_cards()

        self.deck = self.cards.copy()

        self.deck_index = 0

        self.next_card()

    def shuffle_deck(self):

        random.shuffle(self.deck)

        self.deck_index = 0

        self.next_card()

    # =====================
    # Font
    # =====================
    def get_font_size(self, text):

        length = len(text)

        if length <= 2:
            return "120sp"

        elif length <= 4:
            return "100sp"

        elif length <= 8:
            return "80sp"

        elif length <= 12:
            return "60sp"

        elif length <= 20:
            return "50sp"

        else:
            return "40sp"

    # =====================
    # Card
    # =====================
    def next_card(self):

        if not self.deck:
            return

        if self.deck_index >= len(self.deck):

            dialog = MDDialog(
                text="Semua kartu selesai"
            )

            dialog.open()

            self.deck_index = 0

        self.current_card = self.deck[self.deck_index]

        self.deck_index += 1

        if self.quiz_mode == "hanzi":
            self.current_text = self.current_card["hanzi"]

        elif self.quiz_mode == "pinyin":
            self.current_text = self.current_card["pinyin"]

        else:
            self.current_text = self.current_card["arti"]

        self.info_text = (
            f"Kartu {self.deck_index}/{len(self.deck)}"
        )

        self.showing_answer = False

    def show_answer(self):

        if not self.current_card:
            return

        if self.showing_answer:

            self.info_text = (
                f"Kartu {self.deck_index}/{len(self.deck)}"
            )

            self.showing_answer = False
            return

        if self.quiz_mode == "hanzi":

            self.info_text = (
                f"Pinyin : {self.current_card['pinyin']}\n"
                f"Arti : {self.current_card['arti']}"
            )

        elif self.quiz_mode == "pinyin":

            self.info_text = (
                f"Hanzi : {self.current_card['hanzi']}\n"
                f"Arti : {self.current_card['arti']}"
            )

        else:

            self.info_text = (
                f"Hanzi : {self.current_card['hanzi']}\n"
                f"Pinyin : {self.current_card['pinyin']}"
            )

        self.showing_answer = True

    # =====================
    # Mode
    # =====================
    def set_hanzi(self):
        self.quiz_mode = "hanzi"
        self.next_card()

    def set_pinyin(self):
        self.quiz_mode = "pinyin"
        self.next_card()

    def set_arti(self):
        self.quiz_mode = "arti"
        self.next_card()


# =====================
# RUN APP
# =====================
if __name__ == "__main__":
    FlashcardApp().run()