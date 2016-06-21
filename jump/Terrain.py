'''
Created on 26 Aug 2015

@author: NoNotCar
'''
import Img
import pygame
class Terrain(object):
    solid=True
    img=Img.blank32
class Air(Terrain):
    solid=False
class Ground(Terrain):
    img=Img.img2("Ice")
terrlist=[Air(),Ground()]