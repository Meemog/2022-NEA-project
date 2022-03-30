import pygame, threading
from InputHandler import InputHandler
from Boxes import InputBox, Button
from Text import Text

class Scene:
    def __init__(self, window, resolution, socket = None) -> None:
        self.__listOfBoxObjects = []
        self.__listOfButtonObjects = []
        self.__listOfTextObjects = []

    