'''
Created on 13 Jun 2015
The Grubs Squirmed and Writhed
@author: NoNotCar
'''
import Img
import pygame
from random import choice
class Entity(object):
    #Anything that can move
    solid=False
    value=0
    name="Entity"
    types=[]
    hidden=False
    xoff=0
    yoff=0
    x=0
    y=0
    speed=4
    moving=False
    img=Img.blank32
    dangerous=True
    def __init__(self,x,y):
        self.place(x,y)
    def get_img(self,world):
        return self.img
    def update(self,world,events):
        pass
    def mupdate(self,world):
        if self.xoff>0:
            self.xoff-=self.speed
        elif self.xoff<0:
            self.xoff+=self.speed
        if self.yoff>0:
            self.yoff-=self.speed
        elif self.yoff<0:
            self.yoff+=self.speed
        if abs(self.xoff)<self.speed and abs(self.yoff)<self.speed and self.moving:
            self.xoff=0
            self.yoff=0
            self.moving=False
    def move(self,dx,dy,world):
        tx=self.x+dx
        ty=self.y+dy
        if world.is_clear(tx,ty,self):
            world.move(self,tx,ty)
            self.moving=True
            self.xoff= -dx*32
            self.yoff= -dy*32
            return True
        return False
    def place(self,x,y):
        self.x=x
        self.y=y
    def in_air(self,world):
        return world.is_clear(self.x,self.y+1,self)
    def squish(self,player,world):
        pass
    def bash(self,world):
        pass