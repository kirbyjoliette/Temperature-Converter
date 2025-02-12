from tkinter import *
import all_constants as c
import conversion_rounding as cr


class Converter:
    """"
    Temperature conversion tool (°C to °F or °F to °C)
     """

    def __init__(self):
        """
        Temperature converter GUI
         """
        
        self.all_calculations_list= []

        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        self.temp_heading = Label(self.temp_frame,
                                  text="Temperature Convertor",
                                  font=("Arial", "16", "bold")
                                  )
        self.temp_heading.grid(row=0)

        instructions = ("Please enter a temperature below and then press"
                        " one of the buttons to convert it from "
                        "Celsius to Fahrenheit or vice versa")
        self.temp_instructions = Label(self.temp_frame,
                                       text=instructions,
                                       wraplength=250, width=40,
                                       justify="left")
        self.temp_instructions.grid(row=1)

        self.temp_entry = Entry(self.temp_frame, font=("Arial", "14"))
        self.temp_entry.grid(row=2, padx=10, pady=10)

        # Error Label
        error = "Please enter a number"
        self.temp_error = Label(self.temp_frame, text=error,
                                fg="#9C0000", font=("Arial", "14", "bold"))
        self.temp_error.grid(row=3)

        # Conversion, help and history / export buttons
        self.button_frame = Frame(self.temp_frame)
        self.button_frame.grid(row=4)

        # button list (button text | bg colour | command | row | column)
        button_details_list = [
            ["To Celsius", "#9c0000", lambda: self.check_temp(c.ABS_ZERO_FAHRENHEIT), 0, 0],
            ["To Fahrenheit", "#009c87", lambda: self.check_temp(c.ABS_ZERO_CELSIUS), 0, 1],
            ["Help / Info", "#CC6600", "", 1, 0],
            ["History / Export", "#17009c", "", 1, 1]
        ]

        # Liat to hold buttons once they have been made
        self.button_ref_list = []

        for item in button_details_list:
            self.make_button = Button(self.button_frame,
                                      text=item[0], bg=item[1],
                                      fg="#FFFFFF", font=("Arial", "12", "bold"),
                                      width=12, command=item[2])
            self.make_button.grid(row=item[3], column=item[4], padx=5, pady=5)

            self.button_ref_list.append(self.make_button)

        # retrieve 'history / export' button and disable it at the start
        self.to_history_button = self.button_ref_list[3]
        self.to_history_button.config(state=DISABLED)

    def check_temp(self, min_temp):
        """
        Validates the input temperture and converts if vaild
        """
        print("Min Temp: ", min_temp)

        # Retrieve temperature to be converted
        to_convert = self.temp_entry.get()

        # Rest label and entry box (if we had an error)
        self.temp_error.config(fg="004C99", font=("Arial", "13", "bold"))
        self.temp_entry.config(bg="#FFFFFF")

        error = f"Enter a number more than / equal to {min_temp}"
        has_errors = "no"

        # checks that amount to be converted is a number above absolute zero
        try:
            to_convert = float(to_convert)
            if to_convert >= min_temp:
                error = ""
                self.convert(min_temp, to_convert)
            else:
                error= "Too Low"

        except ValueError:
            error ="Please enter a number"

        # display the error if necesary
        if error != "":
            self.answer_error.config(text= error, fg="#9C0000")
            self.temp_entry.config(bg="#F4CCCC") # Highlight the error
            self.temp_entry.delete(0, END) #clears invaild input

    def convert(self, min_temp, to_convert):
        """
        Converts temperatures and updates answer label. Also stars 
        calcualtions for Export / History feature
        """

        if to_convert >= c.ABS_ZERO_CELSIUS:
            answer = cr.to_fahrenheit(to_convert)
            answer_statement = f"{to_convert}°C is {answer}°F"
        else:
            answer = cr.to_celsius(to_convert)
            answer_statement = f"{to_convert}°F is {answer}°C"

        # enable history export button as soon as we have a vaild calculation
        self.to_history_button.config(state=NORMAL)
        self.temp_error.config(text=answer_statement, fg="black")

        self.answer_error.config(text=answer_statement)
        self.all_calculations_list.append(answer_statement)
        print(self.all_calculations_list)

# main routine
if __name__ == '__main__':
    root = Tk()
    root.title("Temperature converter")
    Converter()
    root.mainloop()
