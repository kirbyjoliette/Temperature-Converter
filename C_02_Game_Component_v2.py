import csv
import random
from funtools import partial  # To prevent unwanted windows


# helper functions go here
def get_colours():
    """
    Reterieves colours from csv file 
    :return: list colours which where each list item has the 
    colour name, associated score and farground colour for the text
    """

    file = open("00_colour_list_hex_3.csv", "r")
    all_colors = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row
    all_colors.pop(0)

    return all_colors

def get_round_colours():
    """
   Choose four colours from larger list ensuring that the scores are all different.
   :return: list of colours and score to beat (median of scores)
    """
    all_colour_list = get_colours()

    round_colours = []
    colour_scores = []

    # loop until we have four colours with different scores
    while len(round_colours) < 4:
        potential_colour = random.choice(all_colour_list)

        # colour scores are being read as a string,
        # change them to an integer to compare / when adding to score list.
        if potential_colour[1] not in colour_scores:
            round_colours.append(potential_colour)

            # make score an integer and ass it to the of scores
            colour_scores.append(potential_colour[1])

    # change scores to integers..
    int_scores = [int(x) in colour_scores]

    # Get median score / target score
    int_scores.sort()
    median = (int_scores[1] + int_scores[2]) / 2
    median = round_ans(median)

    return round_colours, median

def round_ans(val):
    """
    Rounds numbers to nearest integer
    :param val: number to be rounded
    :return: Rounded number (on integer)
    """

    var_rounded = (val * 2 + 1)// 2
    raw_rounded = "{:.0f}".format(var_rounded)
    return int(raw_rounded)

class StartGame:
    """"
    Initial Game interface (asks users how many rounds they would like to play)
     """

    def __init__(self):
        # self.play_box = Toplevel()

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Create play button..
        # self.play_button = Button(self.start_frame, font=("Arial", "16", "bold"),
        #                           fg="#FFFFFF", bg="#990000", text="Play", width="10",
        #                           command=self.check_rounds)
        # self.play_button.grid(row=0, column=1)

        # Strings for labels
        intro_string = "In each round you will be invited to choose a colour. Your goal i" \
                       "to beat the target score and win the round (and keep your points)."

        # choosing_string = "Oops - PLease choose a whole number more than zero."
        choose_string = "How many rounds do you want to play?"

        # List of labels to be made (text | font | fg)
        start_label_list = [
            ["Colour Quest", ("Arial", "16", "bold"), None],
            [intro_string, ("Arial", "12"), None],
            [choose_string, ("Arial", "12", "bold"), "#009900"]
        ]

        # create labels and add them to the reference list...

        start_label_ref = []
        for count, item in enumerate(start_label_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2],
                               wraplength=350, justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # extract choice label to that it can be changed to an
        # error message if necessary.
        self.choose_label = start_label_ref[2]

        # Frame so that entry box and button can be in the same row.
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # create play button...
        self.play_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
            Checks users have entered 1 or more rounds
        """

        # Retrieve temperature to be converted
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more than zero."
        has_errors = "no"

        # checks that amount to be converted is a number above absolute zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # Invoke PLay Class (and take across number of rounds)
                Play(rounds_wanted)
                # Hide root window (ie: hide rounds choice window).
                root.withdraw()

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000", font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)


class Play:
    """
    Interface for playing the Colour Quest Game
    """

    def __init__(self, how_many):

        # Integers / String Variables
        self.target_score = InVar()

        # round played - start with zero
        self.rounds_played = InVar()
        self.rounds_played.set(0)

        self.rounds_wanted = InVar()
        self.rounds_wanted.set(how_many)

        # Colour lists and score list
        self.round_colour_list = []
        self.all_scores_list = []
        self.all_medians_list = []

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # body font for most labels...
        body_font = ("Arial", "12")

        # List for label details (text | font | background | row)
        play_labels_list = [
            ["Round # of #", ("Arial", "12", "bold"), None, 0],
            ["Score to beat: #", body_font, "#FFF2CC", 1],
            ["Choose a colour below. Good luck. 🍀", body_font, "#D5E8D4", 2],
            ["You chose, result", body_font, "#D5E8D4", 4]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.game_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(self.make_label)

        # Retrieve Labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.target_label = play_labels_ref[1]
        self.results_label = play_labels_ref[3]

        # set up colour buttons...
        self.colour_frame = Frame(self.game_frame)
        self.colour_frame.grid(row=3)

        self.colour_button_ref = []
        self.button_colours_list = []

        # create four buttons in a 2 x 2 grid
        for item in range(0,4):
            self.colour_button = Button(self.colour_frame, font=("Arial", "12"),
                                        text="Colour Name", width=15)
            self.colour_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)
            
            self.colour_button.ref.append(self.colour_button)

        # Frame to hold this and stats buttons
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        # List for label details (text | font | background | row)
        control_buttons_list = [
            [self.game_frame, "Next Round", "#0057D8", "", 21, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", "", 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#333333", "", 10, 0, 1],
            [self.game_frame, "End", "#990000", self.close_play, 30, 7, None]
        ]

        # create buttons and add to list
        control_ref_list = []
        for item in control_buttons_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", "16", "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        # Once interface has been created, invoke new
        # round function for first round.
        self.new_round()

        def new_round(self):
            """
            Choose four colours, works out median for score to beat. Configures
            buttons with chosen colours
            """

            # retrieve number of rounds played, add one to it and configure heading
            rounds_played = self.rounds_played.get()
            rounds_played += 1
            self.rounds_played.set(rounds_played)

            rounds_wanted = self.rounds_wanted.get()

            # get round colours and median score..
            self.round_colour_list, median = get_round_colours()

            # set target score as median (for later comparison)
            self.traget_score.set(median)

            # Update heading, and score to beat labels, "Hide" results label
            self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
            self.target_label.config(text= f"Target Score: {median}", font=("Arial", "14", "bold"))
            self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

            # configure buttons using fareground and background colours from list
            # enable colour buttons (disabled at the end of the last round)
            for count, item in enumerate(self.colour_button_ref):
                item.config(fg=self.round_colour_list[count][2], 
                            bg=self.round_colour_list[count][0],
                            text=self.round_colour_list[count][0], state=NORMAL)

    def close_play(self):
        # reshow root (ie: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


# main routine
if __name__ == '__main__':
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
