import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION
import time
from random import choice


class MoleView(object):
    """ Visualizes a brick breaker game in a pygame window """
    def __init__(self, model, screen):
        """ Initialize the view with the specified model
            and screen. """
        self.model = model
        self.screen = screen


    def draw(self):
        """ Draw the game state to the screen """
        self.screen.fill(pygame.Color('black'))
        # draw the bricks to the screen
        for brick in self.model.bricks:
            r = pygame.Rect(brick.left, brick.top, brick.width, brick.height)
            pygame.draw.rect(self.screen, pygame.Color(brick.color), r)
        pygame.display.update()

class MoleHole(object):
    """ Represents a brick in our brick breaker game """
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = "red" # choice(["red", "green", "orange", "blue", "purple"])

class MoleModel(object):
    """ Stores the game state for our brick breaker game """
    def __init__(self):
        self.bricks = []
        self.MARGIN = 5
        self.BRICK_WIDTH = 40
        self.BRICK_HEIGHT = 40


        new_hole = MoleHole(5, 5, 40, 20)
        self.bricks.append(new_hole)
        for left in range(self.MARGIN,
                          640 - self.BRICK_WIDTH - self.MARGIN,
                          self.BRICK_WIDTH + self.MARGIN):
            for top in range(self.MARGIN,
                             980/2,
                             self.BRICK_HEIGHT + self.MARGIN):
                mole_hole = MoleHole(left, top, self.BRICK_WIDTH, self.BRICK_HEIGHT)
                self.bricks.append(mole_hole)

        self.last_modified = choice(self.bricks)
        self.last_modified.color = "blue"

    def update(self):
        print "updating"
        change_color = choice(self.bricks)
        change_color.color = "blue"
        if self.last_modified:
            self.last_modified.color = "red"
        self.last_modified = change_color
        # print self.last_modified.top
        print self.last_modified.left

class MoleMouseController(object):
    def __init__(self, model):
        self.model = model

    def get_cursor(self):
        get_pressed = pygame.mouse.get_pressed()
        print self.model.last_modified.left
        if get_pressed[0] == 1 or get_pressed[1] == 1 or get_pressed[2] == 1:
            mouse_position = pygame.mouse.get_pos()
            print mouse_position
            if mouse_position[0] > self.model.last_modified.left and mouse_position[0] < (self.model.last_modified.left+40):
                if mouse_position[1] > self.model.last_modified.top and mouse_position[1] < (self.model.last_modified.top+40):
                    print "IN BOUNDS"
                    # self.model.update()
                    self.model.last_modified.color = 'red'


    # def handle_event(self, event):
    #     """ Look for mouse movements and respond appropriately """
    #     if event.type != MOUSEMOTION:
    #         return
    #     self.model.paddle.left = event.pos[0]

if __name__ == '__main__':
    pygame.init()
    size = (640, 480)
    screen = pygame.display.set_mode(size)

    model = MoleModel()
    view = MoleView(model, screen)
    # controller = PyGameKeyboardController(model)
    controller = MoleMouseController(model)

    running = True
    while running:
        ticks = pygame.time.get_ticks()
        if ticks%1000 == 0:
            model.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            # controller.handle_event(event)
            controller.get_cursor()
        view.draw()
        # time.sleep(1)
        # pygame.time.wait(1000)
        # print pygame.time.get_ticks()