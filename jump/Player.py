'''
Created on 26 Aug 2015
Play with friends
@author: NoNotCar
'''
import Entity
import pygame
import Img
upsound=Img.sndget("Jump")
dsound=Img.sndget("RJump")
class Player(Entity.Entity):
    img=Img.img2("Peng")
    imgu=Img.img2("Pengu")
    imgd=Img.img2("Pengd")
    fimg,fimgu,fimgd=[pygame.transform.flip(i,1,0) for i in [img,imgu,imgd]]
    jump=0
    dire="R"
    dangerous=False
    air=True
    solid=True
    s="P"
    def update(self, world, events):
        for e in events:
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_s and self.move(0, 1, world):
                    self.jump=0
                    world.pdone=True
                elif e.key in [pygame.K_d,pygame.K_a]:
                    self.jump=0
                    dx=1 if e.key==pygame.K_d else -1
                    self.dire="R" if dx==1 else "L"
                    if self.in_air(world) and world.is_clear(self.x+dx,self.y+1,self):
                        if world.is_clear(self.x+dx,self.y,self):
                            if not self.move(dx, 1, world):
                                self.move(dx, 0, world)
                        else:
                            self.move(0, 1, world)
                        world.pdone=True
                    else:
                        world.pdone=self.move(dx, 0, world)
                elif e.key==pygame.K_w:
                    if self.jump:
                        world.pdone=True
                        self.jump-=1
                        if not self.move(0, -1, world):
                            self.bash(world)
                            self.jump=0
                    elif not self.in_air(world):
                        if self.move(0, -1, world):
                            world.pdone=True
                            self.jump=3
                        else:
                            self.bash(world)
                            self.jump=0
                    else:
                        world.pdone=self.move(0, 1, world)
                        self.jump=0
                elif e.key in [pygame.K_q,pygame.K_e]:
                    dx=1 if e.key==pygame.K_e else -1
                    self.dire="R" if dx==1 else "L"
                    if self.jump and world.is_clear(self.x,self.y-1,self):
                        dy=-1
                        self.jump-=1
                    elif self.in_air(world):
                        dy=1
                    elif world.is_clear(self.x,self.y-1,self):
                        dy=-1
                        self.jump=3
                    else:
                        dy=0
                    if not world.is_clear(self.x,self.y-1,self):
                        self.bash(world)
                        self.jump=0
                    if world.is_clear(self.x+dx,self.y,self):
                        if not self.move(dx, dy, world):
                            self.move(dx, 0, world)
                    else:
                        self.move(0, dy, world)
                    world.pdone=True
        self.air=self.in_air(world)
    def get_img(self):
        if self.dire=="R":
            return self.img if not self.air else self.imgu if self.jump else self.imgd
        return self.fimg if not self.air else self.fimgu if self.jump else self.fimgd
    def bash(self,world):
        if world.get_obj(self.x,self.y-1):
            world.get_obj(self.x,self.y-1).bash(world)
    def move(self, dx, dy, world):
        gents=False
        if 0<dy:
            gents=world.get_ents(self.x+dx,self.y+dy)
            for gent in gents:
                gent.squish(self,world)
        if not gents:
            if dy==1:
                dsound.play()
            elif dy==-1:
                upsound.play()
        return Entity.Entity.move(self, dx, dy, world)
                    
                    