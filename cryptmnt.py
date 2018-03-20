#!/usr/bin/env python

import os
def mountDevice():
    d = str(input("What block device do you wish to mount?: "))
    m = str(input("Where do you want it mounted? (Default $HOME/malygos): "))
    if m is "":
        m = "$HOME/malygos"
    elif m is " ":
        m = "$HOME/malygos"
    elif m is "/":
        print("You're either insane, or you want to mount to your root directory. Please do this manually.")
        m = "$HOME/malygos"
    decryptDevice(d, m)

def startDeluged():
    s = str(input('Start deluge daemon? (Y/n): '))
    if s.lower() in ['y', 'ye', 'ya', 'yes']:
        os.system('deluged &> /dev/null')
        print("Deluged started!")
    else:
        print("Deluged not started!")
        return

def decryptDevice(d, m):
    os.system('/usr/bin/sudo cryptsetup luksOpen ' + d + ' cryptmnt')
    os.system('/usr/bin/sudo mount /dev/mapper/cryptmnt ' + m)
    startDeluged()

mountDevice()
