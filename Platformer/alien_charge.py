import pygame
import random

# Global constants

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (80, 60, 60)
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700

#pygame.mixer.music.load('sounds/MIT_Fortuna.mp3')
#pygame.mixer.music.play(-1)

 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        
        super().__init__()

        self.image = pygame.image.load('images/Type4a.png')
        self.rect = self.image.get_rect()  # Set a referance to the image rect.

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # List of sprites we can bump against
        self.level = None

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 5
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 5

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -12

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 12

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0


class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
 
        self.image = pygame.image.load('images/star.png')
        self.rect = self.image.get_rect()


class Bullet_Left(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
 
        self.image = pygame.Surface([18, 3])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x -= 35


class Bullet_Right(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
 
        self.image = pygame.Surface([18, 3])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.x += 35


class Platform(pygame.sprite.Sprite):  #Platform the user can jump on
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
 
        self.image = pygame.image.load('images/block.png') 
        self.rect = self.image.get_rect()
 
 
class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
         
        # Background image
        self.background = None
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
        screen.fill(BLUE)  # Draw the background
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 
 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
         
        self.level_limit = -1000
 
        # Array with width, height, x, and y of platform
        level = [
                [210, 25, 0, 680],
                [210, 25, 180, 680],
                [210, 25, 360, 680],
                [210, 25, 540, 680],
                [210, 25, 720, 680],
                [210, 25, 900, 680],
                [210, 70, 900, 430],
                [210, 70, 600, 560],
                [210, 70, 285, 460],
                [210, 70, 560, 340],
                [210, 70, 65, 330],
                [210, 70, 270, 200]
                ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    score = 0
    frame_count = 0
    frame_rate = 60
    font = pygame.font.SysFont(None, 28)

    pygame.display.set_caption("Alien Charge")
    click_sound = pygame.mixer.Sound('sounds/laser5.ogg')
    clouds = pygame.image.load('images/cloud.png')
    ground = pygame.image.load('images/ground.png')
    bullet_list = pygame.sprite.Group()

    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
    
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height - 55
    active_sprite_list.add(player)

    # List of each block in the game
    block_list = pygame.sprite.Group()

    for i in range(25):
        # This represents a block
        block = Block()

        # Set a random location for the block
        block.rect.x = random.randrange(SCREEN_WIDTH)
        block.rect.y = random.randrange(650)

        # Add the block to the list of objects
        block_list.add(block)
        active_sprite_list.add(block)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_a:
                    click_sound.play()
                    bullet_left = Bullet_Left()
                    # Set the bullet so it is where the player is
                    bullet_left.rect.x = player.rect.x + 30
                    bullet_left.rect.y = player.rect.y + 23
                    # Add the bullet to the lists
                    active_sprite_list.add(bullet_left)
                    bullet_list.add(bullet_left)
                if event.key == pygame.K_d:
                    click_sound.play()
                    bullet_right = Bullet_Right()
                    # Set the bullet so it is where the player is
                    bullet_right.rect.x = player.rect.x + 15
                    bullet_right.rect.y = player.rect.y + 23
                    # Add the bullet to the lists
                    active_sprite_list.add(bullet_right)
                    bullet_list.add(bullet_right)
                if event.key == pygame.K_ESCAPE:
                    done = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        active_sprite_list.update()
        current_level.update()

        for bullet in bullet_list:
            # See if it hit a block
            block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)
            # For each block hit, remove the bullet and add to the score
            for block in block_hit_list:
                bullet_list.remove(bullet)
                active_sprite_list.remove(bullet)
                score += 1

            # Remove the bullet if it flies up off the screen
            if bullet.rect.x > SCREEN_WIDTH:
                bullet_list.remove(bullet)
                active_sprite_list.remove(bullet)

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0

        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        screen.blit(clouds, (60,35))
        screen.blit(clouds, (100,15))
        screen.blit(clouds, (400,35))
        screen.blit(clouds, (900,35))
        
        screen.blit(ground, (0, 680))
        screen.blit(ground, (210, 680))
        screen.blit(ground, (420, 680))
        screen.blit(ground, (630, 680))
        screen.blit(ground, (840, 680))
        screen.blit(ground, (1050, 680))

        pygame.draw.rect(screen, GRAY, [970, 0, 120, 35])
        screen.blit(font.render('Score: ', True, WHITE), [980, 7])
        screen.blit(font.render(str(score), True, WHITE), [1050, 7])

        # --- Timer going up ---
        total_seconds = frame_count // frame_rate  # Calculate total seconds

        # Divide by 60 to get total minutes
        minutes = total_seconds // 60

        # Use modulus (remainder) to get seconds
        seconds = total_seconds % 60

        # Use python string formatting to format in leading zeros
        output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)

        # Blit to the screen
        pygame.draw.rect(screen, GRAY, [10, 0, 135, 35])
        text = font.render(output_string, True, WHITE)
        screen.blit(text, [25, 7])
        
        frame_count += 1

        active_sprite_list.draw(screen)

        clock.tick(frame_rate)
        clock.tick(60)
        
        pygame.display.flip()

    pygame.quit()
 
if __name__ == "__main__":
    main()