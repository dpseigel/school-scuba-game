#State of the game - changing scenes
#1 - Inside building
#2 - In the river
game_state = 1

player_speed_default = 10
player_speed = 10

bottle_spawn_amount = 5
bottle_count = 0

total_old_bottle_count = 0

hired_people = 1
person_rounds = 1
bottle_per_person = 3
money_per_bottle = 5
money_per_person = 3

person_speed = 1

money = 0

highscore = 0

game_timer = 1000
game_timer_reset = 1000

text_colour = 'white'
text_font = 'mainfont'

screen_width = 0
screen_height = 0

def reset_game():
    global player_speed, game_timer
    game_timer = game_timer_reset
    bottle_count = 0
    player_speed = player_speed_default

def reset():
    global game_timer
    game_timer = game_timer_reset
    bottle_count = 0