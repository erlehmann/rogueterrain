#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import stdout
from random import choice

from PerlinNoise import PerlinNoise

from colorama import init, Fore, Back, Style
init()

from os import popen
HEIGHT, WIDTH = [int(i) for i in popen('stty size', 'r').read().split()]


def get_noise(scale=32.0):
    noise = PerlinNoise((HEIGHT, WIDTH)).getData(scale=scale)
    return [i-128 for i in noise.astype('uint8')]

temperature_map = [i+(j/8) for i,j in zip(get_noise(128.0), get_noise(16.0))]
elevation_map = [i+(j/8) for i,j in zip(get_noise(32.0), get_noise(4.0))]
humidity_map = [i+(j/8) for i,j in zip(get_noise(64.0), get_noise(8.0))]
river_map = get_noise(128.0)

def terrain(h, w, temperature_map, elevation_map, humidity_map, river_map):
    index = h*WIDTH + w
    temperature = temperature_map[index]
    elevation = elevation_map[index]
    humidity = humidity_map[index]
    river = river_map[index]

    if elevation < -16:
        return Fore.BLUE + Back.BLUE + '~'  # deep water

    elif elevation < 0:
        if temperature < 0:
            return Fore.WHITE + Back.WHITE + Style.DIM + '-'  # ice
        else:
            return Fore.BLUE + Back.BLUE + Style.DIM + '~'  # shallow water

    elif elevation < 16:
        if 0 < river < 4:
            return Fore.BLUE + Back.BLUE + Style.DIM + '≈'  # river
        if humidity < 0:
            if temperature < 0:
                return Fore.BLACK + Back.WHITE + '.'  # cold desert
            else:
                return Fore.YELLOW + Back.YELLOW + Style.DIM + '.'  # hot desert
        elif humidity < 16:
            if temperature < 0:
                if humidity == 12 or humidity == 14:
                    return Fore.WHITE + Back.WHITE + Style.DIM + '⚘'  # icy flower
                else:
                    return Fore.WHITE + Back.WHITE + Style.DIM + ','  # icy grass
            else:
                if humidity == 12 or humidity == 14:
                    return choice([Fore.RED, Fore.YELLOW, Fore.CYAN, \
                        Fore.MAGENTA, Fore.WHITE]) + Back.GREEN + \
                        Style.DIM + '⚘'  # flower
                else:
                    return Fore.GREEN + Back.GREEN + Style.DIM + ','  # grass
        elif humidity < 32:
            if temperature < 0:
                return Fore.BLACK + Back.WHITE + Style.DIM + '♤'  # icy spade tree
            elif temperature < 16:
                return choice([Fore.YELLOW, Fore.RED, Fore.GREEN]) + \
                    Back.GREEN + Style.DIM + '♠'  # spade tree
            elif temperature < 32:
                return choice([Fore.GREEN, Fore.RED]) + Back.GREEN + \
                    Style.DIM + '♠'  # spade tree
            else:
                return Fore.GREEN + Back.GREEN + Style.DIM + '♠'  # spade tree
        else:
            if temperature < 0:
                return choice([Fore.GREEN, Fore.CYAN]) + Back.WHITE + \
                    Style.DIM + choice(['⇈', '⇈', '↑'])  # icy arrow trees
            else:
                return choice([Fore.GREEN, Fore.CYAN]) + Back.GREEN + \
                    Style.DIM + choice(['⇈', '⇈', '↑'])  # arrow trees

    elif elevation < 32:
        if 0 < river < 2:
            return Fore.BLUE + Back.BLUE + Style.DIM + '≈'  # river
        if humidity < 0:
            if temperature < 0:
                if temperature == 64:
                    return Fore.BLACK + Back.WHITE + Style.DIM + \
                        choice(['λ', 'Y'])  # lambda cactulus
                else:
                    return Fore.BLACK + Back.WHITE + '.'  # cold desert
            else:
                if temperature == 64:
                    return Fore.GREEN + Back.YELLOW + Style.DIM + \
                        choice(['λ', 'Y'])  # lambda cactulus
                else:
                    return Fore.BLACK + Back.YELLOW + Style.DIM + '.'  # hot desert
        elif humidity < 16:
            if temperature < 0:
                return Fore.WHITE + Back.WHITE + Style.DIM + ','  # icy grass
            else:
                return Fore.CYAN + Back.GREEN + Style.DIM + ','  # grass
        elif humidity < 32:
            if temperature < 0:
                return Fore.BLACK + Back.WHITE + Style.DIM + \
                    choice(['♧', '♤'])  # icy club or spade tree
            else:
                return choice([Fore.GREEN, Fore.MAGENTA]) + Back.GREEN + \
                    Style.DIM + choice(['♣', '♠'])  # club or spade tree
        else:
            if temperature < 0:
                return choice([Fore.GREEN, Fore.CYAN]) + Back.WHITE + \
                    Style.DIM + choice(['⇈', '↑', '↑'])  # icy arrow tree
            else:
                return choice([Fore.GREEN, Fore.CYAN]) + Back.GREEN + \
                    Style.DIM + choice(['⇈', '↑', '↑'])  # arrow tree

    elif elevation < 64:
        if humidity < 0:
            if temperature < 0:
                return Fore.BLACK + Back.WHITE + '▲'  # cold desert mountain
            else:
                return Fore.BLACK + Back.YELLOW + '▲'  # hot desert mountain
        else:
            if temperature < 0:
                return choice([Fore.GREEN, Fore.GREEN, Fore.CYAN]) + \
                    Back.WHITE + '▲'  # icy mountain
            else:
                return choice([Fore.GREEN, Fore.GREEN, Fore.CYAN]) + \
                    Back.GREEN + Style.DIM + '▲'  # icy mountain

    elif elevation < 96:
        if humidity < 0:
            if temperature < 0:
                return Fore.WHITE + Back.WHITE + Style.DIM + '▲'  # icy cold desert mountain
            else:
                return Fore.WHITE + Back.YELLOW + '▲'  # icy hot desert mountain
        else:
            if temperature < 0:
                return Fore.WHITE + Back.WHITE + Style.DIM + '▲'  # icy mountain
            else:
                return Fore.WHITE + Back.GREEN  # icy mountain

    return '�'

for h in range(HEIGHT):
    for w in range(WIDTH):
        stdout.write(
            terrain(h, w, temperature_map, elevation_map, humidity_map, \
                river_map)
        )
        stdout.write(Style.RESET_ALL)
    stdout.write('\n')

#print [e for e in elevation_map]
