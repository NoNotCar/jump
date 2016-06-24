__author__ = 'NoNotCar'
import pygame
import os

np = os.path.normpath
loc = os.getcwd() + "/Assets/"
pygame.mixer.init()

def img(fil):
    return pygame.image.load(np(loc + fil + ".png"))
def img2(fil):
    return pygame.transform.scale2x(pygame.image.load(np(loc + fil + ".png"))).convert_alpha()


def img32(fil):
    return pygame.transform.scale(pygame.image.load(np(loc + fil + ".png")), (32, 32)).convert_alpha()


def imgsz(fil, sz):
    return pygame.transform.scale(pygame.image.load(np(loc + fil + ".png")), sz).convert_alpha()


def imgstrip2(fil):
    img = pygame.image.load(np(loc + fil + ".png"))
    imgs = []
    h=img.get_height()
    for n in range(img.get_width() // h):
        imgs.append(pygame.transform.scale2x(img.subsurface(pygame.Rect(n * h, 0, h, h))).convert_alpha())
    return imgs


def imgstrip(fil):
    img = pygame.image.load(np(loc + fil + ".png"))
    imgs = []
    h=img.get_height()
    for n in range(img.get_width() // h):
        imgs.append(pygame.transform.scale(img.subsurface(pygame.Rect(n * h, 0, h, h)), (h*2, h*2)).convert_alpha())
    return imgs
def imgrot(i):
    imgs=[i]
    for n in range(3):
        imgs.append(pygame.transform.rotate(i,-90*n-90))
    return imgs


def musplay(fil):
    pygame.mixer.music.load(np(loc+"Music/" + fil+".ogg"))
    pygame.mixer.music.play(-1)


def bcentre(font, text, surface, offset=0, col=(0, 0, 0), xoffset=0):
    render = font.render(str(text), True, col)
    textrect = render.get_rect()
    textrect.centerx = surface.get_rect().centerx + xoffset
    textrect.centery = surface.get_rect().centery + offset
    return surface.blit(render, textrect)

def bcentrex(font, text, surface, y, col=(0, 0, 0)):
    render = font.render(str(text), True, col)
    textrect = render.get_rect()
    textrect.centerx = surface.get_rect().centerx
    textrect.top = y
    return surface.blit(render, textrect)

def sndget(fil):
    return pygame.mixer.Sound(np(loc+"Sounds/"+fil+".wav"))

def hflip(img):
    return pygame.transform.flip(img,1,0)
def gradback(t,b):
    back=pygame.Surface((480,480))
    for n in range(480):
        pygame.draw.line(back,[(t[x]*(480-n)+b[x]*n)//480 for x in range(3)],(0,n),(480,n),1)
    return back

blank32=img2("Blank")