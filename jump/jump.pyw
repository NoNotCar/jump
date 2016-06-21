'''
Created on 26 Aug 2015

@author: NoNotCar
'''
import sys
import pygame
pygame.init()
edit=0
if edit:
    ssize=(480,512)
else:
    ssize=(480,480)
screen=pygame.display.set_mode(ssize)
import Img
import World
clock=pygame.time.Clock()
level=[1,1]
pdf = pygame.font.get_default_font()
tfont=pygame.font.Font(pdf,60)
sfont=pygame.font.Font(pdf,20)
bfont=pygame.font.Font(pdf,32)
while True:
    try:
        w=World.World(edit,level)
    except IOError:
        screen.fill((255,255,100))
        Img.bcentre(tfont,"YOU WIN",screen)
        pygame.display.flip()
        pygame.time.wait(2000)
        break
    if not edit:
        screen.fill((200,200,255))
        Img.bcentre(tfont,"WORLD %s-%s"%tuple(level),screen)
        Img.bcentre(sfont,w.fltext,screen,50)
        pygame.display.flip()
        pygame.time.wait(2000)
    while not w.complete:
        events=pygame.event.get()
        for event in events:
            if event.type==pygame.QUIT:
                sys.exit()
        screen.fill((200,255,255))
        if w.edit:
            w.eup(events)
        else:
            w.update(events)
        w.scrollrender(screen)
        pygame.display.flip()
        clock.tick(60)
    if w.done:
        level[1]+=1