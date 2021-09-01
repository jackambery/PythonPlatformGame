# Basic arcade program using objects
# Displays a white window with a blue circle in the middle

# Imports
import arcade
import random

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Desert Escape"
SCALING = 0.1

# Classes

class FlyingSprite(arcade.Sprite):
    """ Base class for all flying sprites, this includes
        enemies and clouds. """
    
    def update(self):
        """ Updates position of sprite, when it moves off screen,
            remove it. """
        
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
    Collisions end the game """

    def __init__(self, width, height, title):
        """ Initialize the game """
        super().__init__(width, height, title)

        self.enemies_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()
        
    def setup(self):
        """ Get the game ready to play """

        #background
        arcade.set_background_color(arcade.color.TAN)

        #player
        self.player = arcade.Sprite("images/player.png", SCALING)
        self.player.center_y = self.height / 2
        self.player.left = 100
        self.all_sprites.append(self.player)

        #spawn cactus
        arcade.schedule(self.add_enemy, 0.25)

        #spawn cloud
        arcade.schedule(self.add_cloud, 1.0)

    def on_draw(self):
        """ Draw all game objects """

        arcade.start_render()
        self.all_sprites.draw()

    #def update(s

    def add_enemy(self, delta_time: float):
        """ Adds a new enemy to the screen
        Arguments:
            delta_time {float} -- how much time has passed since tha last call 
        """
        #create sprite 
        enemy = FlyingSprite("images/cactus.png", SCALING)
        enemy.left = random.randint(self.width, self.width + 80)
        enemy.top = random.randint(10, self.height - 10)

        #set velocity
        enemy.velocity = (random.randint(-20, -5), 0)

        #add to enemy list
        self.enemies_list.append(enemy)
        self.all_sprites.append(enemy)

    def add_cloud(self, delta_time: float):
        """ Adds a new cloud to the screen
        Arguments:
            delta_time {float} -- how much time has passed since the last call
        """

        #create sprite
        cloud = FlyingSprite("images/crow.gif", SCALING)
        cloud.left = random.randint(self.width, self.width + 80)
        cloud.top = random.randint(10, self.height - 10)

        #set velocity
        cloud.velocity = (random.randint(-5, -2), 0)

        #add to enemy list
        self.clouds_list.append(cloud)
        self.all_sprites.append(cloud)

# Main code entry point
if __name__ == "__main__":
    app = DesertEscape(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    app.setup()
    arcade.run()