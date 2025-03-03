from collections import deque

from game_display import GameDisplay


class Snake:

    def __init__(self):
        self.__body = deque('')
        self.__body.append((10, 10))
        self.__body.append((10, 9))
        self.__body.append((10, 8))
        self.__add_body_counter = 0
        self.__score = 0

    def get_body(self):
        return self.__body

    def directions(self, direction):
        x, y = self.__body[0]
        if direction == "Left":
            self.__body.appendleft((x - 1, y))
        if direction == "Right":
            self.__body.appendleft((x + 1, y))
        if direction == "Up":
            self.__body.appendleft((x, y + 1))
        if direction == "Down":
            self.__body.appendleft((x, y - 1))

    def move_snake(self, direction):
        self.__body.pop()
        self.directions(direction)

    def update_score(self, score):
        self.__score += score

    def add_body_part(self, direction):
        x, y = self.__body[len(self.__body)-1]
        if direction == "Left":
            self.__body.append((x, y))
        if direction == "Right":
            self.__body.append((x, y))
        if direction == "Up":
            self.__body.append((x, y))
        if direction == "Down":
            self.__body.append((x, y))


    def get_score(self):
        return self.__score

    def set_body_counter(self, count):
        self.__add_body_counter = count

    def get_body_counter(self):
        return self.__add_body_counter

    def add_to_body(self, place):
        self.__body.append(place)