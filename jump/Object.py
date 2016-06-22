'''
Created on 26 Aug 2015

@author: NoNotCar
'''
import sys
import Img
import Enemies
class Object(object):
    img=Img.blank32
    solid=True
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def bash(self,world):
        pass
    def get_img(self,world):
        return self.img
    def update(self,world):
        pass
class GoalBlock(Object):
    img=Img.img2("GoalBlock")
    s="GB"
    def bash(self,world):
        world.complete=True
        world.done=True
class GunBlock(Object):
    img=Img.img2("GunBlock")
    fimg=Img.img2("GunBlockFire")
    t=0
    s="GuB"
    d=-1
    def update(self,world):
        if self.t==4:
            self.t=0
            world.spawn_ent(Enemies.Laser(self.x,self.y,self.d))
        else:
            self.t+=1
    def get_img(self,world):
        if self.t==4:
            return self.fimg
        return self.img
class FGunBlock(GunBlock):
    img=Img.hflip(GunBlock.img)
    fimg=Img.hflip(GunBlock.fimg)
    s="GuBF"
    d=1
class SquishySpawner(Object):
    img=Img.img2("SquishySpawner")
    fimg=Img.img2("SquishySpawnerActive")
    t=0
    s="SqS"
    def update(self,world):
        if self.t==4:
            self.t=0
            if world.is_empty(self.x,self.y-1):
                world.spawn_ent(Enemies.SquishyThing(self.x,self.y-1))
        else:
            self.t+=1
    def get_img(self,world):
        if self.t==4:
            return self.fimg
        return self.img
