import pgzrun
import random
from pgzhelper import *
import pygame.math
import characters
import stations
import game_var

from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.Devices.DigitalInput import *
from Phidget22.Devices.DigitalOutput import *

#***GAME VARIABLES***

world_scale = 8
text_size = 40

#Game Screen dimensions
WIDTH=800
HEIGHT=600
game_var.screen_height = HEIGHT
game_var.screen_width = WIDTH

phidgets = True

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
hiring_station = stations.HiringStation('upgrade_station', world_scale, WIDTH/4, HEIGHT/2)
upgrade_stations.append(hiring_station)

equipment_station = stations.EquipmentStation('upgrade_station', world_scale, WIDTH/4 * 3, HEIGHT/2)
upgrade_stations.append(equipment_station)

water_cleaning_station = stations.WaterCleaningStation('upgrade_station', world_scale, WIDTH/2, HEIGHT/4 * 3)
upgrade_stations.append(water_cleaning_station)

water_station = stations.SwimmingStartStation('upgrade_station', world_scale, WIDTH/2, HEIGHT/2)
upgrade_stations.append(water_station)

#***PLAYER VARIABLES***

#Create Both Players - player is added 
building_player = characters.BuildingPlayer(10, world_scale, 400, 300)
swimming_player = characters.SwimmingPlayer(world_scale, 4, 400, 300)


redLED = None
vertical = None
horizontal = None

#Getting keyboard and phidget input

def input():
    x_dir, y_dir = 0, 0

    if phidgets:
        x_dir, y_dir = horizontal.getVoltageRatio(), -vertical.getVoltageRatio()
        if x_dir < 0.1 and x_dir > -0.1:
            x_dir = 0
        if y_dir < 0.1 and y_dir > -0.1:
            y_dir = 0
    else:
        #Keyboard input
        if keyboard.left or keyboard.A:
            x_dir -= 1
        if keyboard.right or keyboard.D:
            x_dir += 1
        if keyboard.up or keyboard.W:
            y_dir -= 1
        if keyboard.down or keyboard.S:
            if game_var.game_state == 1:
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
    
    if game_var.bottle_count < 0:
        game_var.bottle_count = 0

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
        end_session()
        game_var.game_state = 1

def end_session():
    #Money calculations - adds money into account per person and per
    game_var.total_old_bottle_count += game_var.bottle_count
    new_bottle_count = 0
    hired_people_count = game_var.hired_people * game_var.person_speed
    while game_var.total_old_bottle_count >= game_var.bottle_per_person and hired_people_count > 0:
        hired_people_count -= 1
        game_var.total_old_bottle_count -= game_var.bottle_per_person
        new_bottle_count += 1
    game_var.money += new_bottle_count * game_var.money_per_bottle
    game_var.bottle_count = 0
    game_var.highscore += new_bottle_count
    game_var.round += 1
    if game_var.money < game_var.hired_people * game_var.money_per_person:
        lose()
    else:
        game_var.money -= game_var.hired_people * game_var.money_per_person
    if game_var.round >= 10:
        win()

def win():
    print("you win score: " + str(game_var.highscore))

def lose():
    print("you lose" + str(game_var.highscore))

#***DRAWING FUNCTIONS**

#Rendering everything to screen
def draw():
    screen.clear()
    if game_var.game_state == 1:
        draw_building()
    elif game_var.game_state == 2:
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
        #Displaying the scores in the building state
        screen.draw.text("ROUND: " + str(game_var.round) + "\nSCORE: " + str(game_var.highscore) + "\nMONEY: " + str(game_var.money) + "\nOLD BOTTLES: " + str(game_var.total_old_bottle_count), (20, 20), color=game_var.text_colour, fontsize=text_size, fontname=game_var.text_font)
        for up_station in upgrade_stations:
            #Showing the menus when using them on the stations
            if up_station.menu:
                up_station.menu.draw(screen)
        #Show stats of current station
        if building_player.menu:
             building_player.menu.draw(screen)
    elif game_var.game_state == 2:
        screen.draw.text(str(game_var.game_timer) + "\n" + str(game_var.bottle_count), (20, 20), color=game_var.text_colour, fontsize=text_size, fontname=game_var.text_font)
    elif game_var.game_state == 3:
        screen.draw.text("YOU LOSE", (20, 20), color=game_var.text_colour, fontsize=text_size, fontname=game_var.text_font)
    else:
        screen.draw.text("YOU WIN", (20, 20), color=game_var.text_colour, fontsize=text_size, fontname=game_var.text_font)

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

#If enemy is off screen remove it
def check_enemy_location():
    for enemy in enemies:
        if enemy.pos.x > WIDTH or enemy.pos.x < 0:
            enemies.remove(enemy)

#Check if it hits player - if so remove enemy
def check_enemy_collision():
    for enemy in enemies:
        if enemy.sprite.colliderect(swimming_player.sprite):
            kill_enemy(enemy)

#Maybe add animation later
def kill_enemy(enemy):
    game_var.bottle_count -= 10
    enemies.remove(enemy)

#BOTTLES
#Check if player is hitting the bottle if so collect it
def check_bottle_collision():
    for bottle in bottles:
        if bottle.sprite.colliderect(swimming_player.sprite):
            collect_bottle(bottle)

#collecting bottle - maybe add animation later
def collect_bottle(bottle):
    game_var.bottle_count += 1
    bottles.remove(bottle)

#Spawn bottles around the game - adds new ones if player collects one
def spawn_bottles():
    if len(bottles) < game_var.bottle_spawn_amount:
        bottle_instance = characters.Bottle(world_scale, WIDTH, HEIGHT)
        bottles.append(bottle_instance)

#***BUILDING SCENE***

def check_upgrade_station_collision(using):
    global current_station_in_use
    #Check if it hit something

    #HIDE PLAYER MENU
    building_player.show_menu(screen, None)
    for up_station in upgrade_stations:
        if building_player.sprite.colliderect(up_station.sprite):
            if up_station:
                building_player.show_menu(screen, up_station.value())
            if using:
                up_station.use()

                current_station_in_use = up_station
                #Show current status of stations above player
            return
    if current_station_in_use:
        current_station_in_use.menu = None
        current_station_in_use = None

def on_key_down(key):
    if key == keys.SPACE:
        buy_button()
    if key == keys.E:
        if game_var.game_state == 1:
            game_var.game_state = 2
        else:
            end_session()
            game_var.game_state = 1

def buy_button():
    check_upgrade_station_collision(True)

def onRedButton_StateChange(self, state):
    redLED.setState(state)
    if(state):
        buy_button()
        
if phidgets:
    #Button
    redButton = DigitalInput()
    redButton.setIsHubPortDevice(True)
    redButton.setHubPort(2)
    redButton.setOnStateChangeHandler(onRedButton_StateChange)
    redButton.openWaitForAttachment(1000)
    #Joystick
    vertical = VoltageRatioInput()
    horizontal = VoltageRatioInput()
    vertical.setChannel(0)
    horizontal.setChannel(1)
    vertical.openWaitForAttachment(1000)
    horizontal.openWaitForAttachment(1000)
    
    #RedLED
    redLED = DigitalOutput()
    redLED.setHubPort(3)
    redLED.setIsHubPortDevice(True)
    redLED.openWaitForAttachment(1000)

pgzrun.go() # Must be last line