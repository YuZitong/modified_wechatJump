# -*- coding: utf-8 -*-
'''
 * @Author: Yu Zitong
 * @Date: 2018-01-03 22:09:10
 * @Last Modified by:   Yu Zitong
 * @Last Modified time: 2018-01-11 02:29:15
'''
# pylint: disable=invalid-name

import time
import wda
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image

# press_time = distance * time_coefficient
# just for iphone5s. Modify it when your device is different
time_coefficient = 0.0023

phone = wda.Client()
phone_s = phone.session()

def pull_screenshot():
    phone.screenshot('catch.png')

def jump(distance):
    press_time = distance * time_coefficient
    press_time = press_time
    print('press_time = ', press_time)
    phone_s.tap_hold(200, 200, press_time)

fig = plt.figure()
pull_screenshot()
img = np.array(Image.open('catch.png'))

update = True
click_count = 0
cor = []

def update_data():
    return np.array(Image.open('catch.png'))

im = plt.imshow(img, animated=True)

def updatefig(*args):
    global update
    if update:
        time.sleep(1)
        pull_screenshot()
        im.set_array(update_data())
        update = False
    return im,

def onClick(event):
    global update
    global ix, iy
    global click_count
    global cor

    # next screenshot
    ix, iy = event.xdata, event.ydata
    coords = []
    coords.append((ix, iy))
    print('now = ', coords)
    cor.append(coords)

    click_count += 1
    if click_count > 1:
        click_count = 0

        cor1 = cor.pop()
        cor2 = cor.pop()

        distance = (cor1[0][0] - cor2[0][0])**2 + (cor1[0][1] - cor2[0][1])**2
        distance = distance ** 0.5
        print('distance = ', distance)
        jump(distance)
        update = True

fig.canvas.mpl_connect('button_press_event', onClick)

ani = animation.FuncAnimation(fig, updatefig, interval=50, blit=True)
plt.show()
