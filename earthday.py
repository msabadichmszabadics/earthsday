import pygame
import requests
import os
from PIL import Image
from io import BytesIO
import math

WIDTH = 900
HEIGHT = 700

TEXTURE_URL = "https://eoimages.gsfc.nasa.gov/images/imagerecords/74000/74192/world.topo.bathy.200412.3x5400x2700.jpg"
TEXTURE_FILE = "earth.jpg"

if not os.path.exists(TEXTURE_FILE):
    print("Föld textúra letöltése...")
    r = requests.get(TEXTURE_URL)
    with open(TEXTURE_FILE, "wb") as f:
        f.write(r.content)

img = Image.open(TEXTURE_FILE)
img = img.resize((1024,512))
texture = img.load()

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Earth Light Switch")

font = pygame.font.SysFont("Arial",28)

earth_radius = 220

earth_surface_on = pygame.Surface((earth_radius*2,earth_radius*2))
earth_surface_off = pygame.Surface((earth_radius*2,earth_radius*2))

for y in range(earth_radius*2):
    for x in range(earth_radius*2):

        dx = x-earth_radius
        dy = y-earth_radius

        if dx*dx+dy*dy <= earth_radius*earth_radius:

            nx = dx/earth_radius
            ny = dy/earth_radius
            nz = math.sqrt(max(0,1-nx*nx-ny*ny))

            lon = math.atan2(nx,nz)
            lat = math.asin(-ny)

            u = int((lon/(2*math.pi)+0.5)*1023)
            v = int((lat/math.pi+0.5)*511)

            r,g,b = texture[u,v][:3]

            light = max(0.15,nz)

            earth_surface_on.set_at((x,y),
                (int(r*light),int(g*light),int(b*light)))

            earth_surface_off.set_at((x,y),
                (int(r*0.08),int(g*0.08),int(b*0.08)))

        else:
            earth_surface_on.set_at((x,y),(0,0,0,0))
            earth_surface_off.set_at((x,y),(0,0,0,0))

light_on = True

running=True

while running:

    for e in pygame.event.get():

        if e.type==pygame.QUIT:
            running=False

        if e.type==pygame.MOUSEBUTTONDOWN:

            mx,my=e.pos

            if 40<mx<110 and 40<my<75:
                light_on = not light_on

    screen.fill((20,20,30))

    pygame.draw.rect(screen,(220,220,220),(40,40,70,35),border_radius=15)

    if light_on:
        pygame.draw.circle(screen,(0,220,0),(93,57),15)
        txt="ON"
    else:
        pygame.draw.circle(screen,(80,80,80),(57,57),15)
        txt="OFF"

    screen.blit(font.render(txt,True,(255,255,255)),(130,43))

    if light_on:
        screen.blit(earth_surface_on,(WIDTH//2-earth_radius,HEIGHT//2-earth_radius))
    else:
        screen.blit(earth_surface_off,(WIDTH//2-earth_radius,HEIGHT//2-earth_radius))

    pygame.display.flip()

pygame.quit()