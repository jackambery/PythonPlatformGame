# Basic arcade program using objects
# Displays a white window with a blue circle in the middle

# Imports
import arcade
import random
import time

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Desert Escape"
PLAYER_SCALING = 0.08
CROW_SCALING = 0.25

# Classes

class FlyingSprite(arcade.Sprite):
    """ Base class for all flying sprites, this includes
        enemies and crows.
    """
    
    def update(self):
        """ Updates position of sprite, when it moves off screen,
            remove it.
        """
        
        #move the sprite
        super().update()

        #remove if off screen
        if self.right < 0:
            self.remove_from_sprite_lists()


class DesertEscape(arcade.Window):
    """ Desert Escape is side scroller game
    Player starts on the left, enemies appear on the right
    Player can move anywhere, but not off screen
    Enemies fly to the left at variable speed
    Collisions end the game
    """

    def __init__(self, width, height, title):
        """ Initialize the game
        """
        super().__init__(width, height, title)

        self.enemies_list = arcade.SpriteList()
        self.crows_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()
        self.ground_list = None
        self.back1_list = None
        self.back2_list = None
        self.back3_list = None
        self.back4_list = None


        self.setup()
        
    def setup(self):
        """ Get the game ready to play
        """
        my_map = arcade.tilemap.read_tmx("desertMap.tmx")

        self.ground_list = arcade.tilemap.process_layer(my_map, "ground", 1)
        self.back1_list = arcade.tilemap.process_layer(my_map, "back1", 1)
        self.back2_list = arcade.tilemap.process_layer(my_map, "back2", 1)
        self.back3_list = arcade.tilemap.process_layer(my_map, "back3", 1)
        self.back4_list = arcade.tilemap.process_layer(my_map, "back4", 1)

        #background
        arcade.set_background_color(arcade.color.TAN)

        #player
        self.player = arcade.Sprite("images/player.png", PLAYER_SCALING)
        self.player.center_y = self.height / 2
        self.player.left = 100
        self.all_sprites.append(self.player)

        #spawn cactus
        arcade.schedule(self.add_enemy, 0.25)

        #spawn crow
        arcade.schedule(self.add_crow, 1.0)

        #sounds
        self.collision_sound = arcade.load_sound("sounds/collision.wav")
        self.background_music = arcade.load_sound("sounds/music.wav")
        self.background_music.play()

        #play background music
        #self.play_sound(self.background_music)

    def on_draw(self):
        """ Draw all game objects 
        """
        arcade.start_render()

        #draw backgrounds in order then ground
        self.back4_list.draw()
        self.back3_list.draw()
        self.back2_list.draw()      
        self.back1_list.draw()
        self.ground_list.draw()

        #draw all sprites
        self.all_sprites.draw()

    def on_update(self, delta_time: float):
        """ Update the positions and statuses of all game objects
            If paused, do nothing
            
            Arguements:
                delta_time {float} -- Time since the last update
        """
        # #if paused, don't update
        # if self.paused:
        #     return

        #did you hit anything? if so, end the game
        if (self.player.collides_with_list(self.enemies_list)) or (self.player.collides_with_list(self.crows_list)):
            self.collision_sound.play()
            time.sleep(1)
            arcade.close_window()

        #update everything
        self.all_sprites.update()

        #keep player on screen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_key_press(self, symbol, modifiers):
        """" Handle user keyboard input 
            Q: Quit the game
            P: Pause/Unpause the game
            W,A,S,D: Move up, left, down, right
            
            Arguements:
                symbol {int} -- which key is pressed
                modifiers {int} -- which modifiers were pressed
        """
        if symbol == arcade.key.Q:
            #Quit immediately
            arcade.close_window()
        
        # if symbol == arcade.key.P:
        #     self.paused = not self.paused

        if symbol == arcade.key.W:
            self.player.change_y = 5

        if symbol == arcade.key.S:
            self.player.change_y = -5

        if symbol == arcade.key.A:
            self.player.change_x = -5

        if symbol == arcade.key.D:
            self.player.change_x = 5

    def on_key_release(self, symbol: int, modifiers: int):
        """ Undo movement vectors when movement keys are released 
        
            Arguments:
                symbol {int} -- which key was pressed
                modifier {int} -- which modifiers were pressed 
        """
        if (
            symbol == arcade.key.W
            or symbol == arcade.key.S
        ):
            self.player.change_y = 0

        if (
            symbol == arcade.key.A
            or symbol == arcade.key.D
        ):
            self.player.change_x = 0

    def add_enemy(self, delta_time: float):
        """ Adds a new enemy to the screen

            Arguments:
                delta_time {float} -- how much time has passed since tha last call 
        """
        #create sprite 
        enemy = FlyingSprite("images/cactus.png", PLAYER_SCALING)
        enemy.left = random.randint(self.width, self.width + 80)
        enemy.top = random.randint(10, self.height - 10)

        #set velocity
        enemy.velocity = (random.randint(-5, -1), random.randint(-5, 5))

        #add to enemy list
        self.enemies_list.append(enemy)
        self.all_sprites.append(enemy)

    def add_crow(self, delta_time: float):
        """ Adds a new crow to the screen
        Arguments:
            delta_time {float} -- how much time has passed since the last call
        """

        #create sprite
        crow = FlyingSprite("images/crow.gif", CROW_SCALING)
        crow.left = random.randint(self.width, self.width + 80)
        crow.top = random.randint(10, self.height - 10)

        #set velocity
        crow.velocity = (random.randint(-5, -2), random.randint(-5, 5))

        #add to enemy list
        self.crows_list.append(crow)
        self.all_sprites.append(crow)

# Main code entry point
if __name__ == "__main__":
    app = DesertEscape(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    #app.setup()
    arcade.run()