import tkinter as tk
from typing import Callable, Dict, List
import boggle_board_randomizer
from timer import *
import ex12_utils
from constats import *
from PIL import ImageTk,Image

class GameGui:
    buttons: Dict[str, tk.Button] = {}

    def __init__(self, current_time) -> None:
        root = tk.Tk()
        root.title("Welcome to boggle BH its not moogle")
        self.path = []
        self.letters = boggle_board_randomizer.randomize_board()
        self.__main_window = root
        self.time = time
        self.current_time = current_time
        self.timer_on = False


    def create_board(self):
        self.__upper_frame = tk.Frame(self.__main_window)
        self.__upper_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.__exit_button = tk.Button(self.__upper_frame, text="Exit",
                                       font=("PT Mono", 15), bg="burlywood2",
                                       height=2, width=4,
                                       relief="groove", command=exit)
        self.__exit_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.__boggle_lable = tk.Label(self.__upper_frame, text="BOGGLE",
                                       font=("PT Mono", 50), bg="burlywood1",
                                       height=2, width=32,
                                       relief="groove")
        self.__boggle_lable.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.__right_frame = tk.Frame(self.__main_window, width=5)
        self.__right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.__gusses_label = tk.Label(self.__right_frame, text="WORD'S LIST",
                                       width=15, height=2,
                                       font=("Bradley Hand", 28),
                                       bg=REGULAR_COLOR,
                                       relief="groove")
        self.__gusses_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.__list_label = tk.Label(self.__right_frame, text="",
                                     font=("Bradley Hand", 20), height=20,
                                     bg=REGULAR_COLOR, relief="groove")
        self.__list_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.__left_frame = tk.Frame(self.__main_window, width=12)
        self.__left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.__tempword_lable = tk.Label(self.__left_frame,
                                         text="HERE WE GO!LET'S PLAY",
                                         height=2, font=("Bradley Hand", 28),
                                         bg="lightblue1", relief="ridge")
        self.__tempword_lable.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.__time_label = tk.Label(self.__right_frame, text="TIME",
                                     font=("PT Mono", 30), height=2,
                                     bg="burlywood1", relief="groove")
        self.__time_label.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.__leftlow_frame = tk.Frame(self.__left_frame, width=15)
        self.__leftlow_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.__score_label = tk.Label(self.__leftlow_frame, text="SCORE: 0",
                                      font=("PT Mono", 30), bg="burlywood1",
                                      height=2, width=8, relief="groove")
        self.__score_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.__enter_button = tk.Button(self.__leftlow_frame,
                                        font=("PT Mono", 30), bg="burlywood1",
                                        height=2, width=7, text="START",
                                        relief="groove", command=lambda
                char="START": self.pressed_button(char))
        self.__enter_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.__letter_frame = tk.Frame(self.__left_frame, height=14, width=15)
        self.__letter_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # creating the letters buttons
    def create_letter_grid(self):
        for i in range(4):
            tk.Grid.columnconfigure(self.__letter_frame, i, weight=1)

        for i in range(4):
            tk.Grid.rowconfigure(self.__letter_frame, i, weight=1)

        img = Image.open("photo-12.jpg")
        photo = ImageTk.PhotoImage(img)
        self.__img_label = tk.Label(self.__letter_frame, image=photo)
        self.__img_label.photo = photo
        self.__img_label.grid(row=0, column=0, rowspan = 4, columnspan=4)

    def set_display(self, display_text: str):
        self.__score_label["text"] = display_text

    def set_button_command(self, button_name, cmd: Callable[[], None]):
        self.buttons[button_name].configure(command=cmd)

    def get_button_chars(self) -> List[str]:
        return list(self.buttons.keys())

    #get button location on grid
    def get_button_place(self, button_name):
        row = self.buttons[button_name].grid_info()["row"]
        col = self.buttons[button_name].grid_info()["column"]
        return (row, col)

    def start_button_command(self):
        self.__enter_button.destroy()
        self.__enter_button = tk.Button(self.__leftlow_frame,
            font=("PT Mono", 30), bg="burlywood1",height=2, width=7,
            text="ENTER", relief="ridge",command=lambda char="ENTER":
                self.pressed_button(char))
        self.__enter_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        for i in range(len(self.letters)):
            for j in range(len(self.letters[0])):
                self.make_button(self.letters[i][j], i, j)
        self._start_countdown()


    def enter_button_command(self, temp_word):
        if ex12_utils.is_valid_path(self.letters, self.path,WORDS) and \
                temp_word not in self.__list_label.cget("text"):  #
            # valid path
            if temp_word in WORDS:
                add_score = len(self.path)
                last_score = self.__score_label.cget("text").split(":")[1]
                new_score = int(last_score) + add_score
                self.__score_label.config(text="SCORE:" + str(new_score))
                self.path = []
                self.__list_label.config(
                    text=self.__list_label.cget("text") + "\n" + temp_word)
                self.__tempword_lable.config(text=NEW_WORD)
            if temp_word not in WORDS:
                self.path = []
                self.__tempword_lable.config(text=NO_WORD)
        else:
            self.path = []
            self.__tempword_lable.config(text=WRONG_PATH)

    # A function that will construct the word in to a given label using the
    # letters the player  chooses and tells him if he was wrong or not
    def try_build_word(self, temp_word, button,x,y):
        self.path.append((x, y))
        if temp_word in [WRONG_PATH, NEW_WORD, NO_WORD,
                         DEFAULT]:  # new word
            self.__tempword_lable.config(text="")
        b = self.__tempword_lable.cget("text")
        self.__tempword_lable.config(text=b + button)

    # A function that collects all the actions of the buttons and performs
    # actions according to the button that is pressed
    def pressed_button(self, button, x=None, y=None):
        temp_word = self.__tempword_lable.cget("text")
        if button == "START":
            self.start_button_command()
        if self.__time_label["text"] != "GAME OVER":
            if button != "ENTER" and button != "START":
                self.try_build_word(temp_word, button,x,y)
            if button == "ENTER":
                self.enter_button_command(temp_word)

    # create button
    def make_button(self, button_char, row, col, rowspan=1, columnspan=1):
        button = tk.Button(self.__letter_frame, text=button_char, height=10,
          width=2, **BUTTON_STYLE, command=lambda char=button_char,
          x=row,y=col: self.pressed_button(char, x, y))
        button.grid(row=row, column=col, rowspan=rowspan,columnspan=columnspan, sticky=tk.NSEW)
        self.buttons[button_char] = button

        #what happens when a letter pressed
        def on_enter(event):
            button["background"] = BUTTON_HOVER_COLOR
            button["relief"] = "sunken"

        # what happens when a letter released
        def on_leave(event):
            button["background"] = "lightblue1"

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        # button.bind("<button-1>", really_enter)
        return button

    def countdown(self):
        self.__time_label.config(text= self.convert_seconds_left_to_time())
        if self.current_time:
            self.current_time -= 1
            self.timer_on = self.__main_window.after(1000, self.countdown)
        else:
            self.__time_label["text"] = "GAME OVER"
            self._game_over()


    def _start_countdown(self):
        self._stop_countdown()
        self.countdown()

    def _stop_countdown(self):
        if self.timer_on:
            self.__main_window.after_cancel(self.timer_on)
            self.__timer_on = False

    def convert_seconds_left_to_time(self):
        return dt.timedelta(seconds=self.current_time)

    def _game_over(self):
        root = tk.Tk()
        new_game_frame = tk.Frame(root, height=10, width=100)
        new_game_frame.pack(side= tk.TOP, fill=tk.BOTH, expand=True)
        new_game_label= tk.Label(new_game_frame, text= "Would you like to "
                                                       "play again? if not "
                                                       "your a LOSER", font=("PT Mono", 15), bg="burlywood2",
                                       height=10, width=100 )
        new_game_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        yes_button = tk.Button(new_game_frame, text="yup",
                                       font=("PT Mono", 15), bg="burlywood2",
                                       height=2, width=10,
                                       relief="groove", command = lambda:
            self.create_new_game(root))
        yes_button.pack(side= tk.RIGHT, fill=tk.BOTH, expand=True)
        no_button = tk.Button(new_game_frame, text="nope",
                               font=("PT Mono", 15), bg="burlywood2",
                               height=2, width=10,
                               relief="groove", command=exit)
        no_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def create_new_game(self, root):
        self.__main_window.destroy()
        gamegui = GameGui(TIME)
        root.destroy()
        gamegui.run()

    def run(self):
        self.create_board()
        self.create_letter_grid()
        self.__main_window.mainloop()







