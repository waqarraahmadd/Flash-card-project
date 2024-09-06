from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT1 = ("Ariel", 40, "italic")
FONT2 = ("Ariel", 60, "bold")
TEXT_COLOR = "#000000"
WHITE_COLOR = "#FFFFFF"

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    french_word = current_card['French']
    canvas.itemconfig(language, text="French", fill=TEXT_COLOR)
    canvas.itemconfig(word, text=french_word,  fill=TEXT_COLOR)
    canvas.itemconfig(image, image=french_card_image)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    translation = current_card['English']
    canvas.itemconfig(language, text="English", fill=WHITE_COLOR)
    canvas.itemconfig(word, text=translation, fill=WHITE_COLOR)
    canvas.itemconfig(image, image=english_card_image)


def is_known():
    to_learn.remove(current_card)
    df = pd.DataFrame(to_learn)
    df.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.config(pady=50, padx=50, background=BACKGROUND_COLOR)
window.title("Flashy")

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526)
french_card_image = PhotoImage(file="images/card_front.png")
english_card_image = PhotoImage(file="images/card_back.png")
image = canvas.create_image(400, 263, image=french_card_image)
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
language = canvas.create_text(400, 150, text="Title", font=FONT1, fill=TEXT_COLOR)
word = canvas.create_text(400, 263, text="word", font=FONT2, fill=TEXT_COLOR)
canvas.grid(row=0, column=0,columnspan=2)

check_image = PhotoImage(file='images/right.png')
button = Button(image=check_image, highlightthickness=0, border=0, command=is_known)
button.grid(row=1, column=1)

cross_image = PhotoImage(file='images/wrong.png')
button = Button(image=cross_image, highlightthickness=0, borderwidth=0, command=next_card)
button.grid(row=1, column=0)

next_card()


window.mainloop()
