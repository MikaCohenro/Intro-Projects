import game_parameters


class Apple:
    def __init__(self, color):
        data = game_parameters.get_random_apple_data()
        self.__location = (data[0], data[1])
        self.__score = data[2]
        self.__color = color

    def get_location(self):
        return self.__location

    def get_score(self):
        return self.__score

    def get_color(self):
        return self.__color
