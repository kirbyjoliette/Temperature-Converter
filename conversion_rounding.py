def round_ans(val):
    """
    Rounds tempertures to nearest degree
    :parm val: Number to be rounded
    :return: Number rounded to nearest degree
    """
    var_rounded = (val * 2 + 1) // 2
    return "{:.0f}".format(var_rounded)


def to_calsius(to_convert):
    """
    Converts from °F to °C
    :param to_convert: Temperature to be converted in °F
    :return: Converted temprature in °C
    """

    anwer = (to_convert - 32) * 5 / 9
    return round_ans(anwer)

def to_fahrenheit(to_convert):
        """
        Converts from °F to °C
        :param to_convert: Temperature to be converted in °F
        :return: Converted temprature in °C
        """
        anwer = to_convert * 1.8 + 32
        return round_ans(anwer)


# Main Routine / Testing starts here
