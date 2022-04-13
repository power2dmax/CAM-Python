# g_grand_adventure.py

"""

Platformer game built on Arcade

"""
import arcade
import arcade.gui
import os, sys

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
SCREEN_TITLE = "G's Grand Adventure"

# Constants used to scaler the sprites from their orginal size

TILE_SCALING = 0.40 # if the sprite is 128x128 then the sprite will be scaled by the percentage
CHARACTER_SCALING = TILE_SCALING * 2
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Movement speed of player, in pixel per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 18

# Player starting posistion
PLAYER_START_X = SPRITE_PIXEL_SIZE * TILE_SCALING * 2
PLAYER_START_Y = SPRITE_PIXEL_SIZE * TILE_SCALING * 1 + 225

# Constants to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

# Layer Nmaes from the TileMap
LAYER_NAME_MOVING_PLATFORMS = "Moving Platforms"
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_FOREGROUND = "Foreground"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_DONT_TOUCH = "Don't Touch"
LAYER_NAME_LADDERS = "Ladders"
LAYER_NAME_PLAYER = "Player"


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image
    """
    return [arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)]


class PlayerCharacter(arcade.Sprite):
    """ Setting up the player sprite"""
    
    def __init__(self):
        super().__init__()
        
        # Default the character to face-right
        self.character_face_direction = RIGHT_FACING
        
        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING
        
        # Track the state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        
        # Load the textures
        main_path = ":resources:images/animated_characters/female_person/femalePerson"
        
        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}_fall.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for climbing
        self.climbing_textures = []
        texture = arcade.load_texture(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        self.hit_box = self.texture.hit_box_points
        
    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Climbing animation
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return

        # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][
            self.character_face_direction
        ]

class MyGame(arcade.Window, arcade.View):
    """
    Main application class
    """
    
    def __init__(self):
        
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        # Set the path to start with this program
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False
        
        self.scene = None # The lists that keep track of the Sprite. Each Sprite per list
        self.player_sprite = None # Create a seperate variable that holds the player Sprite
        self.physics_engine = None # The physics engine
        self.camera = None # Add a camera for screen scrolling
        self.gui_camera = None # Add a camera that can be used to draw GUI elements in a stationary position
        self.score = 0 # Used to create and track the score
        self.end_of_map = 0 # Used to determine where is the right edge of the map
        self.level = 1 # Setup the levels, starting with level 1
        self.score = 0 # Setup the score tracking
                
        # Load the various sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")
        

        
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        
    def setup(self):
        """ Setup the game here. Call this function to restart the game """
        
        # Set up the cameras
        self.camera = arcade.Camera(self.width, self.height) # Sprite camera
        self.gui_camera = arcade.Camera(self.width, self.height)# GUI camera
        
        # Name of tiled map to use
        map_name = f"level_{self.level}.json"
        
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
                },
            }
        layer_options = {
            LAYER_NAME_COINS: {
                "use_spatial_hash": True,
                },
            }
        LAYER_NAME_LADDERS: {
                "use_spatial_hash": True,
            }
        layer_options = {
            LAYER_NAME_DONT_TOUCH: {
                "use_spatial_hash": True,
                },
            }
        
        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        
        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        
        # Setting up the foreground
        self.scene.add_sprite_list_after("Player", LAYER_NAME_FOREGROUND)
        
        # Setup the player, specificalloy placing at the coordinates
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)
            
        # Calculate the right edge of the map
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE - 128
            
        # Create the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            gravity_constant = GRAVITY,
            ladders = self.scene["Ladders"],
            walls = self.scene[LAYER_NAME_PLATFORMS]
            )
        
    def on_draw(self):
        # Render the screen
        
        self.clear() # Clear the screen to the background color
        self.camera.use() # Activate the camera
        self.scene.draw() # Draw the Sprites
        self.gui_camera.use() # Activate then GUI camera before drawing the GUI elements
        
        # Draw the game title
        game_title = f"G's Grand Adventure"
        arcade.draw_text(game_title, 800, 10, arcade.csscolor.WHITE, 24, bold=True)
        
        # Draw the score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 18,)
        
    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif (
                self.physics_engine.can_jump(y_distance=10)
                and not self.jump_needs_reset
            ):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        # Process up/down when on a ladder and no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0
    
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        self.process_keychange()
            
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
    
    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # Update animations
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

        # Update Animations
        self.scene.update_animation(
            delta_time, [LAYER_NAME_COINS, LAYER_NAME_BACKGROUND, LAYER_NAME_PLAYER]
        )

        # Update walls, used with moving platforms
        self.scene.update([LAYER_NAME_MOVING_PLATFORMS])

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[LAYER_NAME_COINS]
        )

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists() # Remove the coin
            arcade.play_sound(self.collect_coin_sound) # Play a sound
            self.score += 1 # Add on to the score

        # Position the camera
        self.center_camera_to_player()
        
        # Did the player fall off the map?
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            arcade.play_sound(self.game_over)
            
        # Did the player touch something they should not?
        if arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[LAYER_NAME_DONT_TOUCH]
        ):
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y
            self.score = 0

            arcade.play_sound(self.game_over)
        
        # See if the user got to the end of the level
        if self.player_sprite.center_x >= self.end_of_map:
            # Advance to the next level
            self.level += 1
            
            if self.level == 2:
                game_over_text = "Game Over"
                arcade.draw_text(game_over_text, 200, 200, arcade.csscolor.WHITE, 44, bold=True)
                
                arcade.pause(5)
                arcade.close_window()
                
            else:
                # Load the next level
                self.setup()
               
    
def main():
    """ Main function"""
    
    window = MyGame()
    window.setup()
    arcade.run()
    
    
if __name__ == "__main__":
    main()