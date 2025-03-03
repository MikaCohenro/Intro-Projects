from game_display import GameDisplay
import game_parameters


class Bomb:
    def __init__(self):
        data = game_parameters.get_random_bomb_data()
        self.__location = (data[0], data[1])
        self.__radius = data[2]
        self.__time = data[3]

    def set_time(self):
        self.__time -= 1

    def get_location(self):
        return self.__location

    def get_time(self):
        return self.__time

    def get_radius(self):
        return self.__radius

    def explosion(self, gd):
        x_bomb, y_bomb = self.__location[0], self.__location[1]
        places = []
        if self.__time > 0:
            return places
        if (self.__radius * -1) <= self.__time <= 0:
            if self.explosion_helper():
                if self.__time == 0:
                    gd.draw_cell(x_bomb, y_bomb, "orange")
                    places.append((x_bomb, y_bomb))
                    return places
                for row in range(x_bomb - abs(self.__time), x_bomb + abs(self.__time)+1):
                    for col in range(y_bomb - abs(self.__time),y_bomb + abs(self.__time)+1):
                        if abs(x_bomb - row) + abs(y_bomb - col) == abs(self.__time):
                            gd.draw_cell(row, col, "orange")
                            places.append((row, col))
                return places
        return False

    def explosion_helper(self):
        x_bomb, y_bomb = self.__location[0], self.__location[1]
        if x_bomb - abs(self.__time) < 0:
            return False
        if y_bomb - abs(self.__time) < 0:
            return False
        if x_bomb + abs(self.__time) > game_parameters.WIDTH-1:
            return False
        if y_bomb + abs(self.__time) > game_parameters.HEIGHT-1:
            return False
        return True
