import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION
from pygame.transform import scale
import time
from random import choice
"""Whack-a-Mole code for mouse control, no OpenCV"""

class MoleView(object):
    """ Visualizes a whack_a_mole game in a pygame window """
    def __init__(self, model, screen):
        """ Initialize the view with the specified model
            and screen. """
        self.model = model
        self.screen = screen

    def draw(self):
        """ Draw the game state to the screen """
        # draw the black screen
        self.screen.fill(pygame.Color('black'))
        # load images
        img = pygame.image.load('WhackAMole1.jpg')
        img_whacked = pygame.image.load('whacked.jpg')
        # make and display title
        white = (250, 250, 250)
        message = 'WHACK-A-MOLE!'
        font = pygame.font.Font(None, 40)
        text = font.render(message, 1, white)
        screen.blit(text, (192,40))
        # make and display scoreboard
        white = (250, 250, 250)
        message = 'Score: ' + str(model.score) + '                             Failed Whacks: ' + str(model.missed)
        font = pygame.font.Font(None, 40)
        text = font.render(message, 1, white)
        screen.blit(text, (50,450)) 
        # if there are 3 failed whacks, end game
        if self.model.missed == 3:
            text2 = font.render("Game Over!",1, white)
            screen.blit(text2, (230,200))    
            pygame.display.update()
            pygame.time.wait(2000)     
            pygame.quit()
            sys.exit()
        # if mole is whacked, display Pow! image and punch! sound effect
        if self.model.last_modified.whacked:
            self.screen.blit(pygame.transform.scale(img_whacked, (40,40)), (self.model.last_modified.left,self.model.last_modified.top))
            pygame.mixer.music.load ("punch.wav")
            pygame.mixer.music.play(1,0.0)
        # display moving mole
        else:    
            self.screen.blit(pygame.transform.scale(img, (40,40)), (self.model.last_modified.left,self.model.last_modified.top))              
        pygame.display.update()

class MoleHole(object):
    """ Represents a mole hole in our whack-a-mole game """
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = "green"
        self.draw = True
        self.whacked = False

class MoleModel(object):
    """ Stores the game state for our whack-a-mole game """
    def __init__(self):
        self.holes = []
        self.MARGIN = 5
        self.BRICK_WIDTH = 40
        self.BRICK_HEIGHT = 40
        self.score = 0
        self.missed = 0
        self.click = False

        # instantiates a new_hole and appends it to the self.holes list
        new_hole = MoleHole(5, 5, 40, 20)
        self.holes.append(new_hole)
        for left in range(self.MARGIN,
                          640 - self.BRICK_WIDTH - self.MARGIN,
                          self.BRICK_WIDTH + self.MARGIN):
            for top in range(self.MARGIN,
                             980/2,
                             self.BRICK_HEIGHT + self.MARGIN):
                mole_hole = MoleHole(left, top, self.BRICK_WIDTH, self.BRICK_HEIGHT)
                self.holes.append(mole_hole)
        # randomly chooses a new hole and sets it equal to self_last_modified
        self.last_modified = choice(self.holes)

    def update(self):
        """Updates the status of the chosen mole hole"""
        change_color = choice(self.holes)
        change_color.draw = False
        change_color.color = "white"
        if self.last_modified:
            self.last_modified.draw = True
        self.last_modified = change_color
        self.last_modified.whacked = False

    def whack(self):
        """If the click attribute is true, sets the click attribute to false and
        sets last_modified.whacked to true to indicate tha the mole has been
        whacked and the pow! image should appear.
        """
        if self.click:
            self.click = False
            self.last_modified.whacked = True

class MoleMouseController(object):
    """Represents the controller of the mouse position"""
    def __init__(self, model):
        self.model = model

    def get_cursor(self):
        """Determines the position of the mouse cursor when it is being pressed
        and checks if the mouse_position is in the location of the mole. If it is,
        the score is incremeneted, otherwise the number of failed whacks is
        incremented"""
        get_pressed = pygame.mouse.get_pressed()
        if get_pressed[0] == 1 or get_pressed[1] == 1 or get_pressed[2] == 1:
            mouse_position = pygame.mouse.get_pos()
            if mouse_position[0] > self.model.last_modified.left and mouse_position[0] < (self.model.last_modified.left+40):
                if mouse_position[1] > self.model.last_modified.top and mouse_position[1] < (self.model.last_modified.top+40):
                    self.model.click = True
                    self.model.last_modified.color = 'red'
                    self.model.score += 5
            else:
                self.model.missed += 1

if __name__ == '__main__':
    pygame.init()
    size = (640, 480)
    screen = pygame.display.set_mode(size)
    # instantiates an object of MoleModel
    model = MoleModel()
    # instantiates an object MoleView
    view = MoleView(model, screen)
    # instantiates an object of MoleMouseController
    controller = MoleMouseController(model)
    # sets while True loop
    running = True
    while running:
        # gets the current time and sets it equal to the variable ticks
        ticks = pygame.time.get_ticks()
        model.whack()
        # if the remainder of ticks/1000 is less than or equal to 5 
        # (so if around one second has passed), updates
        if ticks%1000 <= 5:
            model.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            # calls the method get_cursor of the object controller
            controller.get_cursor()
        # calls the method draw of the object view    
        view.draw()