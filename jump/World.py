'''
Created on 22 Sep 2014

@author: NoNotCar
'''
from Img import img2
import Img
from random import randint,choice
import pygame
import Player
import Terrain
import Enemies
import Object
import Entity
import sys
e=enumerate
keyconv=[[pygame.K_w,(0,-1)],[pygame.K_a,(-1,0)],[pygame.K_s,(0,1)],[pygame.K_d,(1,0)]]
editorobjs=[Object.GoalBlock,Object.GunBlock]
editorents=[Player.Player,Enemies.SquishyThing]
EDITORLIST = Terrain.terrlist[1:] + editorobjs + editorents
class Scroller(object):
    solid=False
    hidden=False
    img=img2("Mouse")
    def __init__(self):
        self.x=0
        self.y=0
        self.ex=0
        self.xoff=0
        self.yoff=0
        self.speed=2
        self.excool=0
        self.moving=False
    def get_img(self):
        return self.img
    def mupdate(self):
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
    def update(self,world):
        if not self.moving:
            dx=0
            dy=0
            keys=pygame.key.get_pressed()
            if keys[pygame.K_s] and pygame.key.get_mods()&pygame.KMOD_LCTRL:
                world.save()
                sys.exit()
            if not self.moving and keys[pygame.K_SPACE]:
                if not world.eworld[self.x][self.y]:
                    world.eworld[self.x][self.y]=self.ex+1
            elif not self.moving and keys[pygame.K_LSHIFT]:
                world.edestroy(self.x,self.y)
            for k,d in keyconv:
                if keys[k]:
                    dx+=d[0]
                    dy+=d[1]
            if self.excool:
                self.excool-=1
            else:
                if keys[pygame.K_LEFT]:
                    self.ex=(self.ex-1)%len(EDITORLIST)
                    self.excool=10
                if keys[pygame.K_RIGHT]:
                    self.ex=(self.ex+1)%len(EDITORLIST)
                    self.excool=10
            if dx or dy:
                if world.inworld(self.x+dx,self.y+dy):
                    self.x+=dx
                    self.y+=dy
                    self.xoff=-dx*32
                    self.yoff=-dy*32
                    self.moving=True
class World(object):
    done=False
    def __init__(self,edit,level):
        self.guitorun=None
        self.objs=[[None]*15 for n in range(30)]
        self.edit=edit
        self.ents=[]
        if edit:
            self.ents=[Scroller()]
            self.size=(30,15)
            self.player=self.ents[0]
            self.eworld=[[0]*15 for n in range(30)]
            self.terr=[[0]*15 for n in range(30)]
        else:
            savfile=open(Img.np("lvls/%s-%s.sav" % tuple(level)))
            savr = savfile.readlines()
            self.size=(30,15)
            self.fltext = savr[0][:-1]
            self.terr=[[0]*15 for n in range(30)]
            del savr[0]
            for x,row in enumerate(savr):
                for y,n in enumerate(row.split()):
                    try:
                        n=int(n)
                    except ValueError:
                        n=self.symbreconvert(n)
                    if n:
                        obj=EDITORLIST[n-1]
                        if obj in Terrain.terrlist:
                            self.set_terr(x,y,n)
                        elif obj in editorobjs:
                            self.spawn_obj(obj(x,y))
                        else:
                            if obj==Player.Player:
                                self.player=obj(x,y)
                                self.spawn_ent(self.player)
                            else:
                                self.spawn_ent(obj(x,y))
        self.complete=False
        self.pdone=False
    def update(self,events):
        """Update Everything"""
        if not self.pdone:
            self.player.update(self, events)
        elif self.player.moving:
            self.player.mupdate(self, events)
            if not self.player.moving:
                self.check_kill()
                for r in self.objs:
                    for o in r:
                        if o:
                            o.update(self)
                for ent in [e for e in self.ents if e is not self.player]:
                    ent.update(self,events)
        else:
            for ent in [e for e in self.ents if e is not self.player]:
                ent.mupdate(self,events)
            self.pdone=any([ent.moving for ent in self.ents])
            if not self.pdone:
                self.check_kill()
    def eup(self,events):
        self.player.update(self)
        self.player.mupdate()
    def scrollrender(self,screen):
        """Render Everything in scrolling mode"""
        if self.guitorun:
            self.guitorun.run(screen,self.player)
            self.guitorun=None
        ply=self.player
        asx=ply.x*32+int(round(ply.xoff))-224
        asx=0 if asx<0 else asx if asx<self.size[0]*32-480 else self.size[0]*32-480
        asy=ply.y*32+int(round(ply.yoff))-224
        asy=0 if asy<0 else asy if asy<self.size[1]*32-480 else self.size[1]*32-480
        sx=7 if ply.x<7 else ply.x if ply.x<self.size[0]-8 else self.size[0]-8
        sy=7 if ply.y<7 else ply.y if ply.y<self.size[1]-8 else self.size[1]-8
        if self.edit:
            for x,row in e(self.eworld):
                for y,obj in e(row):
                    if obj and abs(x-sx)<9 and abs(y-sy)<9:
                        screen.blit(EDITORLIST[obj-1].img,(x*32-asx,y*32-asy))
        for x,row in e(self.terr):
            for y,tile in e(row):
                if abs(x-sx)<9 and abs(y-sy)<9:
                    screen.blit(Terrain.terrlist[tile].img,(x*32-asx,y*32-asy))
        for y in xrange(self.size[1]):
            for x in xrange(self.size[0]):
                obj = self.get_obj(x, y)
                if obj and abs(x-sx)<9 and abs(y-sy)<9:
                    screen.blit(obj.get_img(self),(x*32-asx,y*32-asy))
        #Entity Rendering
        for ent in [en for en in self.ents if not en.hidden]:
            if abs(ent.x-sx)<9 and abs(ent.y-sy)<9:
                screen.blit(ent.get_img(),(ent.x*32-asx+int(round(ent.xoff)),ent.y*32-asy+int(round(ent.yoff))))
        if self.edit:
            pygame.draw.rect(screen,(200,200,200),pygame.Rect(0,480,480,32))
            for n,x in enumerate(EDITORLIST):
                screen.blit(x.img,(n*32,480))
            screen.blit(self.player.img,(self.player.ex*32,480))
    def get_obj(self,x,y):
        """Get object from coordinates. If the coordinates are not in the world, returns None"""
        if self.inworld(x,y):
            return self.objs[x][y]
        return None
    def get_ent(self,x,y):
        """Get an entity from coordinates. If there are no entities at the location, returns None"""
        for ent in self.ents:
            if (ent.x,ent.y)==(x,y):
                return ent
        return None
    def get_ents(self,x,y):
        """Get all entities at the coordinates"""
        ents=[]
        for ent in self.ents:
            if (ent.x,ent.y)==(x,y):
                ents.append(ent)
        return ents
    def dest_ent(self,x,y):
        """Destroy all entities at the coordinates"""
        for ent in self.ents:
            if (ent.x,ent.y)==(x,y):
                self.ents.remove(ent)
    def dest_tent(self,ent):
        """Destroy this entity"""
        self.ents.remove(ent)
    def get_objname(self,x,y):
        """Get object name from coordinates. If the coordinates are not in the world, returns None"""
        getob=self.get_obj(x, y)
        if getob:
            return getob.name
        return None
    def inworld(self,x,y):
        """Is the coordinate in the world?"""
        return 0<=x<self.size[0] and 0<=y<self.size[1]
    def inworldent(self,x,y):
        """Is the coordinate in the world or off the bottom?"""
        return 0<=x<self.size[0] and 0<=y
    def ranpos(self):
        """return a random coordinate"""
        return randint(0,self.size[0]-1),randint(0,self.size[1]-1)
    def dest_obj(self,x,y):
        """Destroy the object at the coordinates"""
        self.objs[x][y]=None
    def spawn_obj(self,obj):
        """Create an object at its x,y position"""
        self.objs[obj.x][obj.y]=obj
    def spawn_ent(self,ent):
        """Does what it says on the tin"""
        self.ents.append(ent)
    def is_empty(self,x,y):
        """If there are no objects or solid entities at the location"""
        return not self.get_terr(x,y).solid and self.get_obj(x, y)==None and not any([e.solid for e in self.get_ents(x,y)])
    def is_clear(self,x,y,ent):
        """If an entity can enter this location"""
        if not self.inworld(x, y):
            if self.inworldent(x,y):
                return True
            return False
        return not any([self.get_terr(x, y).solid,(self.get_obj(x, y) and self.get_obj(x, y).solid),(self.get_ent(x,y) and self.get_ent(x,y).dangerous==ent.dangerous)])
    def get_terr(self,x,y):
        """Get the terrain object of the location"""
        return Terrain.terrlist[self.get_tid(x, y)]
    def get_tid(self,x,y):
        """Get the terrain id at the location"""
        return self.terr[x][y]
    def set_terr(self,x,y,tid):
        """Set the terrain id at the location"""
        self.terr[x][y]=tid
    def exists(self,obj):
        """Has this object been destroyed?"""
        return self.get_obj(obj.x, obj.y) is obj
    def run_GUI(self,gui):
        """Run a GUI"""
        self.guitorun=gui
    def check_kill(self):
        kents=self.get_ents(self.player.x,self.player.y)
        if any([kent.dangerous for kent in kents]):
            self.complete=True
    def edestroy(self,x,y):
        self.eworld[x][y]=0
    def save(self):
        savfile = open(Img.np("lvls//save.sav"), "w")
        savfile.write("\n")
        for row in self.eworld:
            savfile.write(" ".join([self.symbconvert(o) for o in row]) + "\n")
        savfile.close
    def symbconvert(self,n):
        if n<len(Terrain.terrlist):
            return str(n)
        else:
            return EDITORLIST[n-1].s
    def symbreconvert(self,s):
        for n,e in enumerate(EDITORLIST):
            if n>=len(Terrain.terrlist)-1 and e.s==s:
                return n+1