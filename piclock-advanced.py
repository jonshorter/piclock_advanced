#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygame , sys , math, time, os
import RPi.GPIO as GPIO
from pygame.locals import *
os.environ['SDL_VIDEODRIVER']="fbcon"

# Setting up the GPIO and inputs with pull up
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, GPIO.PUD_UP)

pygame.init()
bg = pygame.display.set_mode()
mictimer = 0
pygame.mouse.set_visible(False)

# Change colour to preference (R,G,B) 255 max value
bgcolour       = (0,   0,   0  )
clockcolour    = (255, 0,   0  )
ind1colour     = (255, 0,   0  )
ind2colour     = (255, 0,   0  )
ind3colour     = (0,   255, 0  )
ind4colour     = (0,   255, 255)
offcolour      = (16,  16,  16 )
timercolour    = (210, 210, 210)
txtcolour      = (210, 210, 210)

# Scaling to the right size for the display
digiclocksize  = int(bg.get_height()/8)
digiclocksizesec  = int(bg.get_height()/14)
digiclockspace = int(bg.get_height()/6)
dotsize        = int(bg.get_height()/110)
hradius        = bg.get_height()/3
secradius      = hradius - (bg.get_height()/26)
indtxtsize     = int(bg.get_height()/7)
txtsize        = int(bg.get_height()/9)
indboxy        = int(bg.get_height()/6)
indboxx        = int(bg.get_width()/4)

# Coords of items on display
xclockpos      = int(bg.get_width()*0.5)
ycenter        = int(bg.get_height()/2)
xtxtpos        = int(bg.get_width()*0.85)
xtxtpos_left   = int(bg.get_width()*0.14)     
xindboxpos     = int(xtxtpos-(indboxx/2))
xindboxpos_left= int(xtxtpos_left-(indboxx/2))
ind1y          = int((ycenter*0.4)-(indboxy/2))  #onair     
ind2y          = int((ycenter*0.8)-(indboxy/2))  #mic
ind3y          = int((ycenter*0.8)-(indboxy/2))  #tel 
ind4y          = int((ycenter*1.2)-(indboxy/2))  #tür
txthmy         = int(ycenter)
txtsecy        = int(ycenter+digiclockspace)
studioposx     = int(bg.get_width()*0.5)
studioposy     = int(bg.get_height()*0.07)

# Fonts  
clockfont     = pygame.font.Font("font/SUBWT.ttf",digiclocksize)
clockfontsec  = pygame.font.Font("font/SUBWT.ttf",digiclocksizesec)
indfont       = pygame.font.Font(None,indtxtsize)
txtfont       = pygame.font.Font(None,txtsize)

# Indicator text - edit text in quotes to desired i.e. "MIC" will show MIC on display
doortext = u"TÜR" # umwandlung in utf-8 wegen Umlaut
ind1txt       = indfont.render("ON AIR",True,bgcolour)
ind2txt       = indfont.render("MIC",True,bgcolour)
ind3txt       = indfont.render("TEL",True,bgcolour)
ind4txt       = indfont.render(doortext,True,bgcolour)
timer         = indfont.render("00:00",True,timercolour)
studio        = txtfont.render("Studio 1",True,txtcolour)

# Indicator positions
txtposind1 = ind1txt.get_rect(centerx=xtxtpos,centery=ycenter*0.4)
txtposind2 = ind2txt.get_rect(centerx=xtxtpos_left,centery=ycenter*0.8)
txtposind3 = ind3txt.get_rect(centerx=xtxtpos,centery=ycenter*0.8)
txtposind4 = ind4txt.get_rect(centerx=xtxtpos,centery=ycenter*1.2)
timerpos   = timer.get_rect(centerx=xtxtpos_left,centery=ycenter*1.2)
studiopos  = studio.get_rect(centerx=studioposx,centery=studioposy)

# Parametric Equations of a Circle to get the markers
# 90 Degree ofset to start at 0 seconds marker
# Equation for second markers
def paraeqsmx(smx):
    return xclockpos-(int(secradius*(math.cos(math.radians((smx)+90)))))

def paraeqsmy(smy):
    return ycenter-(int(secradius*(math.sin(math.radians((smy)+90)))))

# Equations for hour markers
def paraeqshx(shx):
    return xclockpos-(int(hradius*(math.cos(math.radians((shx)+90)))))

def paraeqshy(shy):
    return ycenter-(int(hradius*(math.sin(math.radians((shy)+90)))))

def Interrupt_timer(channel):
    global mictimer
	
#Interrupt für Timer
GPIO.add_event_detect(12, GPIO.BOTH, callback = Interrupt_timer, bouncetime = 250)
	
# This is where pygame does its tricks
while True :
    pygame.display.update()

    bg.fill(bgcolour)

    # Retrieve seconds and turn them into integers
    sectime = int(time.strftime("%S",time.localtime(time.time())))

    # To get the dots in sync with the seconds
    secdeg  = (sectime+1)*6

    # Draw second markers
    smx=smy=0
    while smx < secdeg:
        pygame.draw.circle(bg, clockcolour, (paraeqsmx(smx),paraeqsmy(smy)),dotsize)
        smy += 6  # 6 Degrees per second
        smx += 6

    # Draw hour markers
    shx=shy=0
    while shx < 360:
        pygame.draw.circle(bg, clockcolour, (paraeqshx(shx),paraeqshy(shy)),dotsize)
        shy += 30  # 30 Degrees per hour
        shx += 30

    # Retrieve time for digital clock
    retrievehm    = time.strftime("%H:%M",time.localtime(time.time()))
    retrievesec   = time.strftime("%S",time.localtime(time.time()))

    digiclockhm   = clockfont.render(retrievehm,True,clockcolour)
    digiclocksec  = clockfontsec.render(retrievesec,True,clockcolour)

    # Align it
    txtposhm      = digiclockhm.get_rect(centerx=xclockpos,centery=txthmy)
    txtpossec     = digiclocksec.get_rect(centerx=xclockpos,centery=txtsecy)

    # Function for the indicators
    if GPIO.input(11):
        pygame.draw.rect(bg, offcolour,(xindboxpos, ind1y, indboxx, indboxy))
    else:
        pygame.draw.rect(bg, ind1colour,(xindboxpos, ind1y, indboxx, indboxy))

    if GPIO.input(12):
        pygame.draw.rect(bg, offcolour,(xindboxpos_left, ind2y, indboxx, indboxy))
    else:
        pygame.draw.rect(bg, ind2colour,(xindboxpos_left, ind2y, indboxx, indboxy))

    if GPIO.input(13):
        pygame.draw.rect(bg, offcolour,(xindboxpos, ind3y, indboxx, indboxy))
    else:
        pygame.draw.rect(bg, ind3colour,(xindboxpos, ind3y, indboxx, indboxy))

    if GPIO.input(15):
        pygame.draw.rect(bg, offcolour,(xindboxpos, ind4y, indboxx, indboxy))
    else:
        pygame.draw.rect(bg, ind4colour,(xindboxpos, ind4y, indboxx, indboxy))
    
    # Render the text
    bg.blit(digiclockhm, txtposhm)
    bg.blit(digiclocksec, txtpossec)
    bg.blit(ind1txt, txtposind1)
    bg.blit(ind2txt, txtposind2)
    bg.blit(ind3txt, txtposind3)
    bg.blit(ind4txt, txtposind4)
    bg.blit(timer, timerpos)
    bg.blit(studio, studiopos)
    
    time.sleep(0.04)
    pygame.time.Clock().tick(25)
    for event in pygame.event.get() :
        if event.type == QUIT:
            pygame.quit()
            GPIO.cleanup()
            sys.exit()
        # Pressing q+t to exit
        elif event.type == KEYDOWN:
            if event.key == K_q and K_t:
                pygame.quit()
                GPIO.cleanup()
sys.exit()