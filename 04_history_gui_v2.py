from tkinter import *
from functools import partial  # To prevent unwanted windows
from datetime import date
import re


class Converter:

    def __init__(self):
        # common format for all buttons
        # Arial size 14 bold, with white text
        self.all_calculations_list = None
        button_font = ("Arial", "12", "bold")
        button_fg = "#FFFFFF"

        # Five item list
        self.all_calculations_list = ['10.0 °F is -12°', '20.0 °F is -7°C',
                                           '30.0 °F is -1°C', '40.0 °F is 4 °C',
                                           '50.0 °F is 10°C', '60.0 °F is 16 °C']

        # Set up GUI Frame
        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        self.button_frame = Frame(padx=30, pady=30)
        self.button_frame.grid(row=0)

        self.to_history_button = Button(self.button_frame,
                                        text="History / Export",
                                        bg="#004C99",
                                        fg=button_fg,
                                        font=button_font, width=12,
                                        state=DISABLED,
                                        command=lambda: self.to_history(self.all_calculations_list))
        self.to_history_button.grid(row=1, column=1, padx=5, pady=5)

        # **** Remove when integrating!! ***
        self.to_history_button.config(state=NORMAL)

    def to_history(self, self.all_calculations_list):


class HistoryExport:

    def __init__(self, partner, calc_list):

        # set maximum number of calculations to 5
        # this can be changed if we want to show fewer /
        # more calculations
        max_calcs = 5
        self.var_max_calcs = IntVar()
        self.var_max_calcs.set(max_calcs)

        # Set variables to hold filename and date
        # for when writing to file
        self.var_filename = StringVar()
        self.var_todays_date = StringVar()
        self.var_calc_list = StringVar()

        # Function converts contents of calculation list
        # into a string.
        calc_string_text = self.get_calc_string(calc_list)

        # setup dialogue box and background colour
        self.history_box = Toplevel()

        # disable help button
        partner.to_history_button.config(state=DISABLED)

        # If users press cross at top, closes help and
        # 'releases' help button
        self.history_box.protocol('WM_DELETE_WINDOW',
                                  partial(self.close_history, partner))

        self.history_frame = Frame(self.history_box, width=300,
                                   height=200
                                   )
        self.history_frame.grid()

        self.history_heading_label = Label(self.history_frame,
                                           text="History / Export",
                                           font=("Arial", "16", "bold"),
                                           width=25)
        self.history_heading_label.grid(row=0)

        # Customise text and background colour for calculation
        # area depending on whether all or only some calculations
        # are shown.
        num_calcs = len(calc_list)

        if num_calcs > max_calcs:
            calc_background = "#FFE6CC"  # peach
            showing_all = "Here are your recent calculations " \
                          "({}/{} calculations shown).  Please export" \
                          " your " \
                          "calculations to see your full calculation " \
                          "history".format(max_calcs, num_calcs)

        else:
            calc_background = "#B4FACB"  # pale green
            showing_all = "Below is your calculation history."

        # History text and label
        hist_text = "{}  \n\nAll calculations are shown to " \
                    "the nearest degree.".format(showing_all)
        self.text_instructions_label = Label(self.history_frame,
                                             text=hist_text,
                                             width=40, justify="left",
                                             wraplength=300,
                                             padx=10, pady=10,
                                             )
        self.text_instructions_label.grid(row=1)

        self.all_calcs_label = Label(self.history_frame,
                                     text=calc_string_text,
                                     padx=10, pady=10, bg=calc_background,
                                     width=40, justify="left")
        self.all_calcs_label.grid(row=2)

        # instructions for saving files
        save_text = "Either choose a custom file name (and push " \
                    "<Export>) or simply push <Export> to save your " \
                    "calculations in a text file.  If the " \
                    "filename already exists, it will be overwritten!"
        self.save_instructions_label = Label(self.history_frame,
                                             text=save_text,
                                             wraplength=300,
                                             justify="left", width=40,
                                             padx=10, pady=10)
        self.save_instructions_label.grid(row=3)

        # Filename entry widget, white background to start
        self.filename_entry = Entry(self.history_frame,
                                    font=("Arial", "14"),
                                    bg="#ffffff", width=25)
        self.filename_entry.grid(row=4, padx=10, pady=10)

        self.filename_feedback_label = Label(self.history_frame,
                                             text="",
                                             fg="#9C0000", wraplength=300,
                                             font=("Arial", "12", "bold"))
        self.filename_feedback_label.grid(row=5)

        self.button_frame = Frame(self.history_frame)
        self.button_frame.grid(row=6)

        self.export_button = Button(self.button_frame,
                                    font=("Arial", "12", "bold"),
                                    text="Export", bg="#004C99",
                                    fg="#FFFFFF", width=12,
                                    command=self.make_file)
        self.export_button.grid(row=0, column=0, padx=10, pady=10)

        self.dismiss_button = Button(self.button_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#666666",
                                     fg="#FFFFFF", width=12,
                                     command=partial(self.close_history,
                                                     partner))
        self.dismiss_button.grid(row=0, column=1, padx=10, pady=10)

    # change calculation list into a string so that it
    # can be outputted as a label.
    def get_calc_string(self, var_calculations):
        # get maximum calculations to display
        # (was set in __init__ function)
        max_calcs = self.var_max_calcs.get()
        calc_string = ""

        # generate string for writing to file
        # (the oldest calculation first)
        oldest_first = ""
        for item in var_calculations:
            oldest_first += item
            oldest_first += "\n"

        self.var_calc_list.set(oldest_first)

        # work out how many times we need to loop
        # to output either the last five calculations
        # or all the calculations
        if len(var_calculations) >= max_calcs:
            stop = max_calcs

        else:
            stop = len(var_calculations)

        # iterate to all but last item,
        # adding item and line break to calculation string
        for item in range(0, stop):
            calc_string += var_calculations[len(var_calculations)
                                            - item - 1]
            calc_string += "\n"

        calc_string = calc_string.strip()
        return calc_string

    def make_file(self):
        # retrieve filename
        filename = self.filename_entry.get()

        filename_ok = ""
        date_part = self.get_date()

        if filename == "":
            # get date and create default filename
            filename = "{}_temperature_calculations".format(date_part)

        else:
            # check that filename is valid
            filename_ok = self.check_filename(filename)

        if filename_ok == "":
            filename += ".txt"
            success = "Your calculations have  " \
                      "been saved (filename: {})".format(filename)
            self.var_filename.set(filename)
            self.filename_feedback_label.config(text=success,
                                                fg="dark green")
            self.filename_entry.config(bg="#FFFFFF")

            # Write content to file!
            self.write_to_file()

        else:
            self.filename_feedback_label.config(text=filename_ok,
                                                fg="dark red")
            self.filename_entry.config(bg="#F8CECC")

    # retrieves date and creates YYYY_MM_DD string
    def get_date(self):
        today = date.today()

        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%Y")

        todays_date = "{}/{}/{}".format(day, month, year)
        self.var_todays_date.set(todays_date)

        return "{}_{}_{}".format(year, month, day)

    # checks filename only has letters, numbers
    # and underscores
    @staticmethod
    def check_filename(filename):
        problem = ""

        # Regular expression to check filname is valid
        valid_char = "[A-Za-z0-9_]"

        # iterates through filename and checks each letter.
        for letter in filename:
            if re.match(valid_char, letter):
                continue

            elif letter == " ":
                problem = "Sorry, no spaces allowed"

            else:
                problem = ("Sorry, no {}'s allowed".format(letter))
            break

        if problem != "":
            problem = "{}.  Use letters / numbers / " \
                      "underscores only.".format(problem)

        return problem

    # write history to text file
    def write_to_file(self):
        # retrieve date, filename and calculation history...
        filename = self.var_filename.get()
        generated_date = self.var_todays_date.get()

        # set up strings to be written to file
        heading = "**** Temperature Calculations ****\n"
        generated = "Generated: {}\n".format(generated_date)
        sub_heading = "Here is your calculation history " \
                      "(oldest to newest)...\n"
        all_calculations = self.var_calc_list.get()

        to_output_list = [heading, generated,
                          sub_heading, all_calculations]

        # write to file
        # write output to file
        text_file = open(filename, "w+")

        for item in to_output_list:
            text_file.write(item)
            text_file.write("\n")

        # close file
        text_file.close()

    # closes history dialogue (used by button and x at top of dialogue)
    def close_history(self, partner):
        # Put help button back to normal...
        partner.to_history_button.config(state=NORMAL)
        self.history_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.mainloop()
