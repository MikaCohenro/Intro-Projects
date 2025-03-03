import game_parameters
from game_display import GameDisplay
from snake import Snake
from apple import Apple
from bomb import Bomb

# checking if the head hitting a diff object on board
def wheres_the_head(apples_list, head_location, bomb, snake, gd):
    if head_location == bomb.get_location(): #bomb
        return False
    for cell in range(1, len(snake.get_body())): #hitting itself
        if snake.get_body()[cell] == head_location:
            return False
    for apple in apples_list: # ate an apple and creates a new one
        if apple.get_location() == head_location:
            snake.update_score(apple.get_score())
            gd.show_score(snake.get_score())
            apples_list.remove(apple)
            new_apple = Apple("green")
            while apples_on_snake(snake, new_apple):
                new_apple = Apple("green")
            apples_list.append(new_apple)
            snake.set_body_counter(3)

def move_by_click(snake, key_clicked, old_direction):
    if key_clicked == 'Left' and old_direction != "Right":
        snake.move_snake("Left")
    if key_clicked == 'Right' and old_direction != "Left":
        snake.move_snake("Right")
    if key_clicked == 'Up' and old_direction != "Down":
        snake.move_snake("Up")
    if key_clicked == 'Down' and old_direction != "Up":
        snake.move_snake("Down")
    if key_clicked is None:
        snake.move_snake(old_direction)

def illegal(direction, key_clicked):
    if key_clicked == 'Left' and direction == "Right":
        return True
    if key_clicked == 'Right' and direction == "Left":
        return True
    if key_clicked == 'Up' and direction == "Down":
        return True
    if key_clicked == 'Down' and direction == "Up":
        return True

def did_i_burn_u(place, snake, apples):
    for cell in snake.get_body():
        if cell == place:
            if cell == snake.get_body()[0]:
                return True
            return False
    for apple in apples:
        if apple.get_location() == place:
            apples.remove(apple)
            apples.append(Apple("green"))

def making_snake_bigger(snake, direction):
    if snake.get_body_counter() != 0:
        snake.set_body_counter(snake.get_body_counter() - 1)
        snake.add_body_part(direction)

def full_screen(snake):
    length = len(snake.get_body())
    screen_size = game_parameters.HEIGHT * game_parameters.WIDTH
    if screen_size - 4 == length:
        return True

def is_bomb_on_snake(snake, bomb):
    for cell in snake.get_body():
        if bomb.get_location() == cell:
            return True

def apples_on_snake(snake, apple):
    for cell in snake.get_body():
        if cell == apple.get_location():
            return True

def main_loop(gd: GameDisplay) -> None:
    # start set up
    direction = "Up"
    apples_list = []
    die = False
    head_explosion = False
    body_explosion = False
    gd.show_score(0)
    snake = Snake()
    bomb = Bomb()
    while is_bomb_on_snake(snake, bomb):
        bomb = Bomb()

    #create first 3 apples
    for i in range(3): #TODO change to constant
        apple = Apple("green")
        while apples_on_snake(snake, apple):
            apple = Apple("green")
        apples_list.append(apple)

    bomb.set_time()

    # drawing snake on board
    for elem in snake.get_body():
        gd.draw_cell(elem[0], elem[1], "black")

    # drawing bomb on board
    x_bomb, y_bomb = bomb.get_location()[0], bomb.get_location()[1]
    if bomb.get_time() > 0:
        gd.draw_cell(x_bomb, y_bomb, 'Red')

    # drawing apples on board
    for apple in apples_list:
        row, col = apple.get_location()[0], apple.get_location()[1]
        gd.draw_cell(col, row, "green")
    gd.end_round() #todo why is this here tehila?
    # end set up

    while True:
        if die or head_explosion or body_explosion:
            break

        key_clicked = gd.get_key_clicked()
        if illegal(direction, key_clicked):
            continue

        #moving snake
        move_by_click(snake, key_clicked, direction)
        x_head, y_head = snake.get_body()[0]

        if 0 > x_head or 0 > y_head or x_head >= game_parameters.WIDTH or \
                y_head >= game_parameters.HEIGHT:  # moving limits
            break

        # updating our direction if key was changed and valid
        if key_clicked is not None and not illegal(direction, key_clicked):
            direction = key_clicked

        # checking if bomb exploded
        bomb.set_time()
        orange_cell_list = bomb.explosion(gd)

        # while explosion checking if touched one of the items in the game
        if orange_cell_list is not False:
            for place in orange_cell_list:
                location_explosion = did_i_burn_u(place, snake, apples_list)
                if location_explosion:
                    head_explosion = True #head touched explosion
                if location_explosion is False:
                    gd.draw_cell(place[0], place[1], "orange")
                    body_explosion = True #body touched explosion
                    body_loc = (place[0], place[1])
        else:
            #ended wave need new bomb
            bomb = Bomb()
            while is_bomb_on_snake(snake, bomb):
                bomb = Bomb()

        # making snake bigger if ate an apple
        making_snake_bigger(snake, direction)

        # check if snake hit himself \ bomb \ ate an apple #todo fix red head when touches ITSELF
        if wheres_the_head(apples_list, snake.get_body()[0],bomb, snake,
                           gd) is False:
            die = True


        # drawing snake on board
        for elem in snake.get_body():
            gd.draw_cell(elem[0], elem[1], "black")
            if die:
                gd.draw_cell(snake.get_body()[0][0], snake.get_body()[0][1],
                             "red")
            if head_explosion:
                gd.draw_cell(snake.get_body()[0][0], snake.get_body()[0][1],
                             "orange")
            if body_explosion:
                gd.draw_cell(body_loc[0], body_loc[1], "orange")

        # drawing bomb on board
        x_bomb, y_bomb = bomb.get_location()[0], bomb.get_location()[1]
        if bomb.get_time()>0:
            gd.draw_cell(x_bomb, y_bomb, 'Red')
        if full_screen(snake):
            break

        # drawing apples on board
        for apple in apples_list:
            row, col = apple.get_location()[0], apple.get_location()[1]
            gd.draw_cell(row, col, "green")
        gd.end_round()
