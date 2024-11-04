import pgzrun
import random
from pgzhelper import *
import pygame.math
import characters
import stations
import game_var


#***GAME VARIABLES***

world_scale = 8
text_size = 50

#Game Screen dimensions
WIDTH=800
HEIGHT=600
game_var.screen_height = HEIGHT
game_var.screen_width = WIDTH



#***ENEMY VARIABLES***

#All Enemies are added to this list
enemies = []

enemy_timer_max = 100
enemy_timer = 100

#***BOTTLE VARIABLES***
bottles = []

#***STATION VARIABLES***

#All the upgrade stations are added to here for collision detection
upgrade_stations = []
current_station_in_use = None

#All Upgrade station are instantiated here
test_upgrade_station = stations.HiringStation('upgrade_station', world_scale, 200, 300)
upgrade_stations.append(test_upgrade_station)

test_water_station = stations.SwimmingStartStation('upgrade_station', world_scale, 400, 300)
upgrade_stations.append(test_water_station)


#***PLAYER VARIABLES***

#Create Both Players - player is added 
building_player = characters.BuildingPlayer(10, world_scale, 400, 300)
swimming_player = characters.SwimmingPlayer(world_scale, 4, 400, 300)
                
#Getting keyboard and phidget input

def input():
    x_dir, y_dir = 0, 0
    if keyboard.left:
        x_dir -= 1
    if keyboard.right:
        x_dir += 1
    if keyboard.up:
        y_dir -= 1
    if keyboard.down and game_var.game_state == 1:
        y_dir += 1
    
    #Moving Player with input
    building_player.move(pygame.Vector2(x_dir, y_dir))
    swimming_player.move(pygame.Vector2(x_dir, y_dir))

#***UPDATE FUNCTIONS***

#Main Looping Function
def update():
    input()
    if game_var.game_state == 1:
        #Removing All Enemies From the list
        enemies.clear()
        #Making the Stations Show up
        for up_station in upgrade_stations:
            up_station.show()
        building_update()
    elif game_var.game_state == 2:
        #Hiding them all when game starts
        for up_station in upgrade_stations:
            up_station.hide()
        swimming_update()

def building_update():
    check_upgrade_station_collision(False)
    #Running update function on player and all sprites
    building_player.update()
    #Running updates on each upgrade station
    for up_station in upgrade_stations:
        up_station.update()

def swimming_update():
    spawn_bottles()
    swimming_player.update()
    for bottle in bottles:
        bottle.update()
    for enemy in enemies:
        enemy.update()
    spawn_enemies()
    check_enemy_collision()
    check_enemy_location()
    check_bottle_collision()
    game_var.game_timer -= 1
    if game_var.game_timer <= 0:
        game_var.game_state = 1


#***DRAWING FUNCTIONS8**

#Rendering everything to screen
def draw():
    screen.clear()
    if game_var.game_state == 1:
        draw_building()
    else:
        draw_swimming()
    draw_hud(screen)

#Drawing The Building Scene
def draw_building():
    for up_station in upgrade_stations:
        up_station.sprite.draw()
    #Player is rendered after so that it is rendered on top
    building_player.sprite.draw()

#Drawing the Swimming Scene
def draw_swimming():
    for bottle in bottles:
        bottle.sprite.draw()
    #Player is rendered after so that it is rendered on top
    for enemy in enemies:
        enemy.sprite.draw()
    swimming_player.sprite.draw()

#Drawing the HUD overtop
def draw_hud(screen):
    if game_var.game_state == 1:
        for up_station in upgrade_stations:
            print(up_station.menu)
            if up_station.menu:
                up_station.menu.draw(screen)
    else:
        screen.draw.text(str(game_var.game_timer), (300, 100), color=game_var.text_colour, fontsize=text_size, fontname=game_var.text_font)


#***SWIMMING SCENE***

#ENEMIES
#Spawns enemies in the swimming scene
def spawn_enemies():
    global enemy_timer
    enemy_timer -= 1
    if enemy_timer == 0:
        left = True
        if random.randint(0, 1) == 1:
            left = False
        enemy = None
        if left:
            enemy = characters.Enemy(8, world_scale, 0, random.randint(0, HEIGHT), True)
        else:
            enemy = characters.Enemy(8, world_scale, WIDTH, random.randint(0, HEIGHT), False)
        enemies.append(enemy)
        enemy_timer = enemy_timer_max

def check_enemy_location():
    for enemy in enemies:
        if enemy.pos.x > WIDTH or enemy.pos.x < 0:
            kill_enemy(enemy)

def check_enemy_collision():
    for enemy in enemies:
        if enemy.sprite.colliderect(swimming_player.sprite):
            kill_enemy(enemy)

def kill_enemy(enemy):
    enemies.remove(enemy)

#BOTTLES
def check_bottle_collision():
    for bottle in bottles:
        if bottle.sprite.colliderect(swimming_player.sprite):
            collect_bottle(bottle)

def collect_bottle(bottle):
    game_var.bottle_count += 1
    bottles.remove(bottle)

def spawn_bottles():
    if len(bottles) < game_var.bottle_spawn_amount:
        bottle_instance = characters.Bottle(world_scale, WIDTH, HEIGHT)
        bottles.append(bottle_instance)

#***BUILDING SCENE***

def check_upgrade_station_collision(using):
    global current_station_in_use
    #Check if it hit something

    for up_station in upgrade_stations:
        if building_player.sprite.colliderect(up_station.sprite):
            if using:
                up_station.use()
                current_station_in_use = up_station
            return
    if current_station_in_use:
        current_station_in_use.menu = None
        current_station_in_use = None

def on_key_down(key):
    if key == keys.SPACE:
        check_upgrade_station_collision(True)
    if key == keys.E:
        if game_var.game_state == 1:
            game_var.game_state = 2
        else:
            game_var.game_state = 1


pgzrun.go() # Must be last line