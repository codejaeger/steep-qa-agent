# -*- coding: utf-8 -*-
# Citation: Box Of Hats (https://github.com/Box-Of-Hats )

import win32api as wapi
import win32con as wcon
import time

keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'£$/\\":
    keyList.append(char)


def key_check():
    time.sleep(0.2)
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    if wapi.GetAsyncKeyState(wcon.VK_UP):
        keys.append('up')
    if wapi.GetAsyncKeyState(wcon.VK_DOWN):
        keys.append('down')
    if wapi.GetAsyncKeyState(wcon.VK_RIGHT):
        keys.append('right')
    if wapi.GetAsyncKeyState(wcon.VK_LEFT):
        keys.append('left')
    if wapi.GetAsyncKeyState(wcon.VK_SPACE):
        keys.append('space')

    return keys

# print(key_check())