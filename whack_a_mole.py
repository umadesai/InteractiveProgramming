import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION
from pygame.transform import scale
import time
from random import choice
from multiprocessing import Process, Pipe
from WhackAMoleOpenCV import color_tracking
"""Guac-a-Mole code that connects with WhackAMoleOpenCV"""
class MoleView(object):
    """ Visualizes a guac_a_mole game in a pygame window """
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
        img = pygame.image.load('avocado.jpeg')
        img_whacked = pygame.image.load('Guac.png')
        img_knife = pygame.image.load('knife.png')
        # make and display title
        white = (250, 250, 250)
        message = 'GUAC-A-MOLE!'
        font = pygame.font.Font(None, 40)
        text = font.render(message, 1, white)
        screen.blit(text, (202,40))
        # make and display a countdown timer
        white = (250, 250, 250)
        message = str(model.time_left)
        font = pygame.font.Font(None, 40)
        text = font.render(message, 1, white)
        screen.blit(text, (600,10))
        # make and display scoreboard
        white = (250, 250, 250)
        message = 'Bowls of Guac: ' + str(model.score)
        font = pygame.font.Font(None, 40)
        text = font.render(message, 1, white)
        screen.blit(text, (400,450))
        # draw the knife cursor
        r = pygame.Rect(self.model.hand[0], self.model.hand[1], 10, 10)
        pygame.draw.rect(self.screen, pygame.Color('black'), r) 
        self.screen.blit(pygame.transform.scale(img_knife, (40,40)), (self.model.hand[0],self.model.hand[1]))
        # if avocado is sliced, display guacamole image
        if self.model.last_modified.whacked:
            self.screen.blit(pygame.transform.scale(img_whacked, (40,40)), (self.model.last_modified.left,self.model.last_modified.top))
        # display moving avocado
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
        self.hand = [0,0]
        self.time_left = 10

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
        """Updates the status of the chosen mole hole and the timer, and ends the game if the countdown 
        has run out of time"""
        change_color = choice(self.holes)
        change_color.draw = False
        if self.last_modified:
            self.last_modified.draw = True
        self.last_modified = change_color
        self.last_modified.whacked = False
        self.time_left -= 1
        if self.time_left == -1:
            font = pygame.font.Font(None, 40)
            white = (250, 250, 250)
            text2 = font.render("Game Over! Enjoy the guac!",1, white)
            screen.blit(text2, (140,200))    
            pygame.display.update()
            pygame.time.wait(2000)     
            pygame.quit()
            sys.exit()

    def whack(self):
        """If the click attribute is true, sets the click attribute to false and
        sets last_modified.whacked to true to indicate that the avocado has been
        sliced and the guacamole image should appear.
        """
        if self.click:
            self.click = False
            self.last_modified.whacked = True
        
class MoleMouseController(object):
    """Represents the controller of the mouse position"""
    def __init__(self, model):
        self.model = model

    def get_cursor(self):
        """Sets model.hand (the output of WhackAMoleOpenCV) equal to mouse_position, 
    horizontally flips the mouse_position, and checks if the mouse_position is 
    in the location of the avocado."""
        mouse_position = self.model.hand
        mouse_position[0] = 640 - self.model.hand[0]
        if mouse_position[0] > self.model.last_modified.left and mouse_position[0] < (self.model.last_modified.left+40):
            if mouse_position[1] > self.model.last_modified.top and mouse_position[1] < (self.model.last_modified.top+40):
                self.model.click = True
                self.model.last_modified.color = 'red'
                self.model.score += 5

def whack_mole(parent):
    """The function that contains the while loop of the parent"""
    running = True
    # default value of 0 for time of the last update
    previous_update = 0
    # while True statement
    while running:
        # sets ticks equal to current timing
        ticks = pygame.time.get_ticks()
        model.whack()
        # sets model.hand equal to the output of WhackAMoleOpenCV.py
        model.hand = parent.recv()
        # calls the method get_cursor of the object controller
        controller.get_cursor()
        # checks if the difference between the past update and current time is
        # greater than 1 second and updates if it is
        if ticks - previous_update > 1000:
            previous_update = ticks
            model.update()
        # calls the method draw of the object view
        view.draw()

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

    # plays the background music
    pygame.mixer.music.load ("GuacSong.mp3")
    pygame.mixer.music.play(-1,0.0)

    # creates a connection between the parent and child
    parent, child = Pipe()

    # allows for multiprocessing of both the while loops of whack_mole
    # and color_tracking from WhackAMoleOpenCV
    p1 = Process(target=whack_mole, args=(parent,))
    p2 = Process(target=color_tracking, args=(child,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()