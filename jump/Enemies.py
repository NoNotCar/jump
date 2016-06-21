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
    def update(self,world,events):
        if not self.move(-1,0,world):
            world.dest_tent(self)