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
editorobjs=[Object.GoalBlock,Object.GunBlock,Object.FGunBlock,Object.SquishySpawner]
editorents=[Player.Player,Enemies.SquishyThing,Enemies.FireBall,Enemies.SquishyClever]
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
                if pygame.key.get_mods()&pygame.KMOD_LCTRL:
                    if not world.eworld[self.x][self.y]:
                        poss=[(self.x,self.y)]
                        while poss:
                            p=poss.pop(0)
                            if not world.eworld[p[0]][p[1]]:
                                world.eworld[p[0]][p[1]]=self.ex+1
                                for dx,dy in [[0,1],[1,0],[0,-1],[-1,0]]:
                                    if world.inworld(p[0]+dx,p[1]+dy):
                                        poss.append((p[0]+dx,p[1]+dy))

                else:
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
    def __init__(self,edit,level,lvlsize):
        self.guitorun=None
        self.edit=edit
        self.olist=[]
        if edit:
            self.size=lvlsize
            s=self.size
            self.eworld=[[0]*s[1] for n in range(s[0])]
            self.terr=[[0]*s[1] for n in range(s[0])]
            self.objs=[[None]*(s[1]+1) for n in range(s[0])]
            self.oconvert()
            self.objs[0][0]=[Scroller(0,0)]
            self.player=self.objs[0][0][0]
        else:
            savfile=open(Img.np("lvls/%s-%s.sav" % tuple(level)))
            savr = savfile.readlines()
            self.size=(len(savr)-1,len(savr[1].split()))
            s=self.size
            self.fltext = savr[0][:-1]
            self.terr=[[0]*s[1] for n in range(s[0])]
            self.objs=[[None]*(s[1]+1) for n in range(s[0])]
            self.oconvert()
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
                            self.spawn(obj(x,y))
                        else:
                            if obj==Player.Player:
                                self.player=obj(x,y)
                                self.spawn(self.player)
                            else:
                                self.spawn(obj(x,y))
        self.complete=False
        self.pdone=False
    def oconvert(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]+1):
                self.objs[x][y]=[]
    def update(self,events):
        """Update Everything"""
        if not self.pdone:
            self.player.update(self, events)
        elif self.player.moving:
            self.player.mupdate(self)
            if not self.player.moving:
                self.check_kill()
                for o in [o for o in self.olist if o is not self.player]:
                    o.update(self,events)
        else:
            for o in [o for o in self.olist if o is not self.player]:
                o.mupdate(self)
            self.pdone=any([o.moving for o in self.olist])
            if not self.pdone:
                self.check_kill()
                for o in self.olist:
                    if o.y==self.size[1]:
                        self.dest_obj(o)
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
        for y in xrange(self.size[1]+1):
            for x in xrange(self.size[0]):
                objs = self.get_objs(x, y)
                if abs(x-sx)<9 and abs(y-sy)<9:
                    for o in objs:
                        screen.blit(o.get_img(self),(x*32-asx+int(round(o.xoff)),y*32-asy+int(round(o.yoff))))
        if self.edit:
            pygame.draw.rect(screen,(200,200,200),pygame.Rect(0,480,480,32))
            for n,x in enumerate(EDITORLIST):
                screen.blit(x.img,(n*32,480))
            screen.blit(self.player.img,(self.player.ex*32,480))
    def get_objs(self,x,y):
        """Get objects from coordinates. If the coordinates are not in the world, returns None"""
        if self.inworldv(x,y):
            return self.objs[x][y]
        return None
    def dest_objs(self,x,y):
        """Destroy all objects at the coordinates"""
        self.objs[x][y]=[]
    def dest_obj(self,obj,poverride=False):
        """Destroy this entity"""
        self.objs[obj.x][obj.y].remove(obj)
        self.olist.remove(obj)
        if obj is self.player and not poverride:
            self.complete=True
    def inworld(self,x,y):
        """Is the coordinate in the world?"""
        return 0<=x<self.size[0] and 0<=y<self.size[1]
    def inworldv(self,x,y):
        """Is the coordinate in the world or off the bottom?"""
        return 0<=x<self.size[0] and 0<=y
    def ranpos(self):
        """return a random coordinate"""
        return randint(0,self.size[0]-1),randint(0,self.size[1]-1)
    def spawn(self,obj):
        """Create an object at its x,y position"""
        self.objs[obj.x][obj.y].append(obj)
        self.olist.append(obj)
    def is_empty(self,x,y):
        """If there is nothing at the location"""
        return not self.get_terr(x,y).solid and self.get_objs(x, y)==[]
    def is_clear(self,x,y,obj):
        """If an object can enter this location"""
        if not self.inworld(x, y):
            if self.inworldv(x,y):
                return True
            return False
        for o in self.get_objs(x,y):
            if o.solid==2 or (o.solid and o.dangerous==obj.dangerous):
                return False
        return not self.get_terr(x, y).solid
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
        return obj in self.get_objs(obj.x, obj.y)
    def run_GUI(self,gui):
        """Run a GUI"""
        self.guitorun=gui
    def check_kill(self):
        kents=self.get_objs(self.player.x,self.player.y)
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
    def move(self,obj,tx,ty):
        self.dest_obj(obj,True)
        obj.x=tx
        obj.y=ty
        self.spawn(obj)
    def set_front(self,obj):
        os=self.get_objs(obj.x,obj.y)
        os.remove(obj)
        os.append(obj)