import tkinter as tk
import timer
import ex12_utils

TITLE = "Welcome to boggle BH its not moogle"
FONT = "PT Mono"
BUTTON_HOVER_COLOR = 'gray'
REGULAR_COLOR = 'lightyellow'
BUTTON_ACTIVE_COLOR = "slateblue"
BUTTON_STYLE = {"font": ("PT Mono", 20), "borderwidth": 1, "relief":
tk.GROOVE, "bg": REGULAR_COLOR, "activebackground": BUTTON_ACTIVE_COLOR}
TIMER = timer.CountdownLabel
TIME = 180
WORDS = ex12_utils.load_words_dict(ex12_utils.file_path("boggle_dict.txt"))
WRONG_PATH = "Try again"
NEW_WORD = "GREAT JOB! Enter new word"
NO_WORD = "word doesnt exist"
DEFAULT = "HERE WE GO!LET'S PLAY"