'''
Created on 26 Aug 2015

@author: Thomas
'''
import Entity
import Img
sqsnd=Img.sndget("squish")
class SquishyThing(Entity.Entity):
    dire="L"
    img=Img.img2("Squishy")
    fimg=Img.hflip(img)
    solid=True
    s="Sq"
    def get_img(self):
        return self.img if self.dire=="L" else self.fimg
    def update(self, world, events):
        if not self.move(0, 1, world):
            dx=1 if self.dire=="R" else -1
            if not self.move(dx, 0, world):
                self.dire="L" if self.dire=="R" else "R"
    def squish(self, player, world):
        world.dest_tent(self)
        sqsnd.play()
class Laser(Entity.Entity):
    img=Img.img2("Laser")
    def __init__(self,x,y,d):
        self.place(x,y)
        self.d=d
    def update(self,world,events):
        if not self.move(self.d,0,world):
            world.dest_tent(self)
class FireBall(Entity.Entity):
    dx=1
    dy=-1
    img=Img.img2("Fireball")
    imgs=Img.imgrot(img)
    solid=True
    s="FB"
    dconv=[(1,-1),(1,1),(-1,1),(-1,-1)]
    def get_img(self):
        return self.imgs[self.dconv.index((self.dx,self.dy))]
    def update(self, world, events):
        tx=self.x+self.dx
        ty=self.y+self.dy
        if not world.is_clear(tx,self.y,self):
            self.dx*=-1
        if not world.is_clear(self.x,ty,self):
            self.dy*=-1
        self.move(self.dx,self.dy,world)
    def squish(self, player, world):
        world.dest_tent(self)
        sqsnd.play()