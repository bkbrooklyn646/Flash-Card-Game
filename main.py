from tkinter import *
import tkinter
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"  # Setting the background color to light green
current_card = {}


class Root(tkinter.Tk):  # Creating the window of the program

    def __init__(self):
        tkinter.Tk.__init__(self)

        self.title("Flash Card")
        self.geometry("850x760")
        self.config(padx=30, pady=30, bg=BACKGROUND_COLOR)
        self._menu = MainMenu(self)  # Setting the "_menu" variable to be the MainMenu class
        self._container = None  # Just to contain the "NONE" parameter
        self.show_welcome()

    def show_welcome(self):
        if self._container is not None:
            self._container.destroy()
        self._container = MainPage(self)

    def start_game(self):
        if self._container is not None:
            self._container.destroy()
        self._container = Canvas(self)
        self._container.add_image()
        self.update()
        self._container.next_card()

    def end_game(self):
        if self._container is not None:
            self._container.destroy()
        self._container = Display(self)
        self._container.show_text("Congratulations\n\nYou Win!", True)
        self.update()

    def show_help(self):
        if self._container is not None:
            self._container.destroy()
        self._container = Display(self)
        self._container.show_text("To play this game you have to click the 'start' button on the menu page.\n\n"
                                  "When the game is started, you will have 3 seconds to answer whether you know "
                                  "the word or not\n\n"
                                  "Otherwise, the card will be flipped and the answer would be on the screen\n\n"
                                  "Once, you have answered all the words, the game will end.")
        self.update()

    def show_contact(self):
        if self._container is not None:
            self._container.destroy()
        self._container = Display(self)
        self._container.show_text("Contact me!\n\n"
                                  "Instagram: booktrp_\n\n"
                                  "Facebook: Book Teerapat\n\n"
                                  "Email: 64011655@kmitl.ac.th")
        self.update()

    def show_about(self):
        if self._container is not None:
            self._container.destroy()
        self._container = Display(self)
        self._container.show_text("Hi!\n\n"
                                  "My name is Teerapat Wattanamanont\n\n"
                                  "I'm majoring in software engineering at KMITL.")
        self.update()


class MainMenu(tkinter.Menu):

    @property  # Decorator to avoid creating new names, avoid accessing or modifying the data directly
    def root(self):
        return self._root

    def __init__(self, root):
        tkinter.Menu.__init__(self, root)
        self._root = root

        window_menu = WindowMenu(self)
        self.add_cascade(label="Menu", menu=window_menu)

        root.config(menu=self)


class WindowMenu(tkinter.Menu):

    def __init__(self, parent, **kwargs):
        tkinter.Menu.__init__(self, parent, **kwargs)

        self.add_command(label="Start", command=parent.root.start_game)
        self.add_command(label="Help", command=parent.root.show_help)
        self.add_command(label="Contact Us", command=parent.root.show_contact)
        self.add_command(label="About Us", command=parent.root.show_about)
        self.add_command(label="Exit", command=parent.root.quit)


class MainPage(tkinter.Frame):
    def __init__(self, root):
        self._root = root

        tkinter.Frame.__init__(self, root)
        self.config(bg=BACKGROUND_COLOR)
        self.pack(expand=True)

        welcome_label = tkinter.Label(self, text="Welcome to Flash Card!",
                                      bg=BACKGROUND_COLOR,
                                      font=("Ariel", 20, "bold"))

        welcome_label.grid(row=0, column=3)

        question_label = tkinter.Label(self, text="SE KMITL 2021", bg=BACKGROUND_COLOR, font=("Ariel", 10))
        question_label.grid(row=5, column=3)

        buttons_frame = tkinter.Frame(self)
        buttons_frame['bg'] = BACKGROUND_COLOR
        buttons_frame.grid(row=1, column=3)

        start_button = tkinter.Button(
            buttons_frame,
            text="Start",
            padx=21, pady=5,
            relief=FLAT,  # The button does not stand out from its background
            command=self.start_click
        )
        start_button.grid(row=2, column=3, pady=10)

        help_button = tkinter.Button(
            buttons_frame,
            text="Help",
            padx=20, pady=5,
            relief=FLAT,
            command=self.help_click
        )
        help_button.grid(row=3, column=3, pady=10)

        contact_button = tkinter.Button(
            buttons_frame,
            text="Contact Me",
            padx=3, pady=5,
            relief=FLAT,
            command=self.contact_click
        )
        contact_button.grid(row=4, column=3, pady=10)

        about_button = tkinter.Button(
            buttons_frame,
            text="About Me",
            padx=8, pady=5,
            relief=FLAT,
            command=self.about_click
        )
        about_button.grid(row=5, column=3, pady=10)

    def start_click(self):
        self._root.start_game()

    def help_click(self):
        self._root.show_help()

    def contact_click(self):
        self._root.show_contact()

    def about_click(self):
        self._root.show_about()


class Canvas(tkinter.Canvas):
    _images = []
    to_learn = {}
    current_card = None
    flip_timer = None

    def __init__(self, root):
        self._root = root
        tkinter.Canvas.__init__(self, root)
        self.config(width=800, height=545)
        self.pack(fill="both", expand=True)
        self.flip_timer = self.after(3000, func=self.flip_card)
        try:
            self.data = pandas.read_csv("data/thai_words.csv")
        except FileNotFoundError:
            self.original_data = pandas.read_csv("data/thai_words.csv")
            self.to_learn = self.original_data
        else:
            self.to_learn = self.data.to_dict(orient="records")
        self.back_button = Button(self._root, text="Back", padx=20, pady=5, relief=FLAT, command=self.to_show_welcome)
        self.back_button.place(x=0, y=670)

    def add_image(self):
        self.card_front_image = PhotoImage(file="images/card_front.png")
        self.card_back_image = PhotoImage(file="images/card_back.png")
        self.card_background = self.create_image(400, 264, image=self.card_front_image, anchor='center', tags=None)
        self.card_title = self.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
        self.card_word = self.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
        self._images.append(self.card_background)
        self.config(bg=BACKGROUND_COLOR, highlightthickness=0)
        self.grid(row=0, column=0, columnspan=2)
        self.cross_image = PhotoImage(file="images/wrong.png")

        self.unknown_button = Button(image=self.cross_image, highlightthickness=0, command=self.next_card)
        self.unknown_button.grid(row=1, column=0)

        self.check_image = PhotoImage(file="images/right.png")
        self.known_button = Button(image=self.check_image, highlightthickness=0, command=self.is_known)
        self.known_button.grid(row=1, column=1)

    def to_show_welcome(self):
        self.back_button.place_forget()
        self.unknown_button.grid_remove()
        self.known_button.grid_remove()
        root.show_welcome()

    def next_card(self):
        self.after_cancel(self.flip_timer)
        try:
            self.current_card = random.choice(self.to_learn)
            self.itemconfig(self.card_title, text="Thai", fill="black")
            self.itemconfig(self.card_word, text=self.current_card["Thai"], fill="black")
            self.itemconfig(self.card_background, image=self.card_front_image)
            self.flip_timer = self.after(3000, func=self.flip_card)
        except IndexError:
            # This is where the players have answered all the questions correctly
            # Show the END GAME page
            self.back_button.place_forget()
            self.unknown_button.grid_remove()
            self.known_button.grid_remove()
            root.end_game()

    def flip_card(self):
        self.itemconfig(self.card_title, text="English", fill="white")
        self.itemconfig(self.card_word, text=self.current_card["English"], fill="white")  # Getting the English Key
        self.itemconfig(self.card_background, image=self.card_back_image)

    def is_known(self):
        self.to_learn.remove(self.current_card)
        self.next_card()
        pandas.DataFrame(self.to_learn)
        self.data.to_csv("data/words_to_learn.csv")


class Display(tkinter.Frame):
    def __init__(self, root, *args, **kwargs):
        self._root = root

        tkinter.Frame.__init__(self, root, *args, **kwargs)
        self.config(bg=BACKGROUND_COLOR)
        self.pack(expand=True)

    def show_text(self, text, endgame=None):
        if endgame:
            help_label = tkinter.Label(self, text=text, bg=BACKGROUND_COLOR, font=("Ariel", 20, "bold"))
        else:
            help_label = tkinter.Label(self, text=text, bg=BACKGROUND_COLOR, font=25)
        help_label.grid(row=0, column=3)
        self.show_back_button()

    def show_back_button(self):
        self.back_button = Button(self._root, text="Back", padx=20, pady=5, relief=FLAT, command=self.to_show_welcome)
        self.back_button.place(x=0, y=670)

    def to_show_welcome(self):
        self.back_button.place_forget()
        root.show_welcome()


if __name__ == "__main__":
    root = Root()
    root.mainloop()
else:
    print("Program Failed")
