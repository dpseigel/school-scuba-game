import pgzrun
# import random
from pgzhelper import *
import pygame.math
import characters
import stations
import game_var


world_scale = 8

#Game Screen dimensions
WIDTH=800
HEIGHT=600

#All the actors are added so that they call the update and draw function
actors = []
#All the actors sprites are added to this list they are classes that have sprites in them
actor_sprites = []
#All the upgrade stations are added to here for collision detection
upgrade_stations = []

current_station_in_use = None

#All Upgrade station are instantiated here
test_upgrade_station = stations.HiringStation('upgrade_station', world_scale, 200, 300)
upgrade_stations.append(test_upgrade_station)

test_water_station = stations.SwimmingStartStation('upgrade_station', world_scale, 400, 300)
upgrade_stations.append(test_water_station)

#add all stations to actors
for up_station in upgrade_stations:
    actors.append(up_station)

#Create Player - player is added (Not added to actors so that it is rendered on top)
building_player = characters.BuildingPlayer(10, world_scale, 400, 300)

#Create Player - player is added (Not added to actors so that it is rendered on top)
swimming_player = characters.SwimmingPlayer(10, world_scale, 4, 400, 300)

#Where all the sprites are added to the actor sprites list
for actor in actors:
    actor_sprites.append(actor.sprite)
                
#Getting keyboard and phidget input
def input():
    x_pos, y_pos = 0, 0
    if keyboard.left:
        x_pos -= 1
    if keyboard.right:
        x_pos += 1
    if keyboard.up:
        y_pos -= 1
    if keyboard.down:
        y_pos += 1
    
    #Moving Player with input
    building_player.move(pygame.Vector2(x_pos, y_pos))
    swimming_player.move(pygame.Vector2(x_pos, y_pos))

#Main Looping Function
def update():
    input()
    check_upgrade_station_collision(False)
    #Running update function on player and all sprites
    building_player.update()
    swimming_player.update()
    for actor in actors:
        actor.update()

#Rendering everything to screen
def draw():
    screen.clear()
    if game_var.game_state == 1:
        draw_building()
        for up_station in upgrade_stations:
            up_station.show()
    else:
        draw_swimming()
        for up_station in upgrade_stations:
            up_station.hide()
    draw_hud()

def draw_building():
    for up_station in upgrade_stations:
        up_station.sprite.draw()
    #Player is rendered after so that it is rendered on top
    building_player.sprite.draw()

def draw_hud():
    if game_var.game_state == 1:
        for up_station in upgrade_stations:
            if up_station.menu:
                up_station.menu.draw(screen)
    else:
        pass

def draw_swimming():
    #Player is rendered after so that it is rendered on top
    swimming_player.sprite.draw()

def check_upgrade_station_collision(using):
    global current_station_in_use
    #Check if it hit something
    hit = building_player.sprite.collidelist(actor_sprites)
    if hit != -1:
        #Checking if they hit an upgrade station
        for up_station in upgrade_stations:
            if up_station.sprite == actor_sprites[hit]:
                station = up_station
                if using:
                    station.use()
                    current_station_in_use = station
    elif not current_station_in_use == None:
        station.menu = None
        station.menu_on = False
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