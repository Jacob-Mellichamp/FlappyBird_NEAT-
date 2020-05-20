import pygame  #Game library
import time     #for time management
import neat     #ML
import os
import random
pygame.font.init()

import Bird
import Ground

WIN_HEIGHT = 800
WIN_WIDTH = 500



PIPE_IMG =     pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))


BG_IMG =     pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
STAT_FONT = pygame.font.SysFont("comisans", 50, bold=False, italic=False)

#Pipe class
class Pipe:
    #GAP between pipes and speed of pipe 
    GAP = 150
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0 
        self.gap = 100

        self.top = 0
        self.bottom = 0 
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.setHeight()


    #Get random heights of gap 
    def setHeight(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP


    #move pipe towards bird
    def move(self):
        self.x -= self.VEL

    #draw pipe onto window
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))


    def collide(self, bird):

        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x , self.top - round(bird.y))
        bottom_offset = (self.x - bird.x , self.bottom - round(bird.y))

        # point of collison
        b_point = bird_mask.overlap(bottom_mask, bottom_offset) 
        t_point = bird_mask.overlap(top_mask, top_offset) 

        if t_point or b_point:
            return True

        return False



def draw_window(win, birds, pipes, base, score):
    win.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)
    

    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()
   
def main(genomes, config):

    nets = []
    ge = []
    score = 0
    birds = []
    
    #set up neural Network
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird.Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Ground.Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()


    run = True

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            #click red x button
            if event.type == pygame.QUIT :
                run = False
                pygame.quit()
                quit()
        base.move()


        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            
            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1

                    #remove from existence
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
        
            
            pipe.move()

        #add pipe if distance good
        if add_pipe:
            score += 1
            #add 5 fitness to remaining birds
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))

        #remove pipes that have been passed
        for r in rem:
            pipes.remove(r)


    
        #if bird hits ground / goes off screen
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        draw_window(win, birds, pipes, base, score)




def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                        neat.DefaultStagnation, config_path)

    #generate population
    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(main,50)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)

    


    

