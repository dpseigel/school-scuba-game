#State of the game - changing scenes
#1 - Inside building
#2 - In the river
game_state = 1

player_speed_default = 10
player_speed = 10

bottle_spawn_amount = 5
bottle_count = 0

game_timer = 1000
game_timer_reset = 1000

text_colour = 'white'
text_font = 'mainfont'

screen_width = 0
screen_height = 0

def reset():
    global player_speed, game_timer
    player_speed = player_speed_default
    game_timer = game_timer_reset