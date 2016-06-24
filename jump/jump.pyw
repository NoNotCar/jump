'''
Created on 26 Aug 2015

@author: NoNotCar
'''
import sys
import pygame
pygame.init()
edit=0
lvlsize=(40,20)
if edit:
    ssize=(480,512)
else:
    ssize=(480,480)
screen=pygame.display.set_mode(ssize)
import Img
import World
import Worlds
import Terrain
clock=pygame.time.Clock()
level=[1,1]
pdf = pygame.font.get_default_font()
tfont=pygame.font.Font(pdf,60)
sfont=pygame.font.Font(pdf,20)
bfont=pygame.font.Font(pdf,32)
pygame.event.pump()
while True:
    if level[1]==8:
        world=Worlds.castle
    else:
        world=Worlds.worlds[level[0]-1]
    back=Img.gradback(*world[1])
    for t in Terrain.terrlist[1:]:
        t.img=world[0][t.tex]
    Img.musplay(world[2])
    try:
        w=World.World(edit,level,lvlsize)
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
        screen.blit(back,(0,0))
        if w.edit:
            w.eup(events)
        else:
            w.update(events)
        w.scrollrender(screen)
        pygame.display.flip()
        clock.tick(60)
    if w.done:
        if level[1]==8:
            level=[level[0]+1,1]
        else:
            level[1]+=1