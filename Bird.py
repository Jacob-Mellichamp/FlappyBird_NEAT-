import pygame #Game library
import time     #for time management
import neat     #ML
import os
import random



def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


BIRD_IMGS = [   pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))) ,
                pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))) ,
                pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))) ]

class Bird:
  


    MAX_ROTATION = 25
    ROT_VELOCITY = 20
    ANIMATION_TIME = 5

    #constructor
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0 
        self.tick_count = 0 
        self.velocity = 0
        self.height = self.y
        self.image_count = 0
        self.img = BIRD_IMGS[0] 

    #How the bird jumps
    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    #move bird every frame
    def move(self):
        self.tick_count += 1

        #gives bird the arc within it's jump
        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count **2

        if displacement >= 16:
            displacement = displacement/displacement * 16

        if displacement < 0:
            displacement -=2

        #change height
        self.y = self.y + displacement

        #tilt angle
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VELOCITY


    def draw(self, win):
        self.image_count += 1

        #Animation of bird flapping
        if self.image_count < self.ANIMATION_TIME:
            self.img = BIRD_IMGS[0]

        elif self.image_count < self.ANIMATION_TIME * 2:
            self.img = BIRD_IMGS[1]

        elif self.image_count < self.ANIMATION_TIME * 3:
            self.img = BIRD_IMGS[2]

        elif self.image_count < self.ANIMATION_TIME * 4:
            self.img = BIRD_IMGS[1]

        elif self.image_count < self.ANIMATION_TIME * 4+1:
            self.image_count = 0


        #if the bird is nosediving toward the ground
        if self.tilt <= -80:
            self.img = BIRD_IMGS[1]
            self.image_count = self.ANIMATION_TIME * 2


        #rotate_image in pygame
        #rotated_image = rot_center(self.img, self.tilt)
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        win.blit(rotated_image, (self.x, self.y))


    def get_mask(self):
        return pygame.mask.from_surface(self.img)



        
