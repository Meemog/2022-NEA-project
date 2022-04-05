import ctypes, pygame, json
from Game import Game

#Imports settings
file = open("settings.json", "r")
settings = json.load(file)
file.close()

# #Volume value is a percentage
# settings = {
#     "Volume": 100,
#     "Resolution": "Fullscreen"
# }

user32 = ctypes.windll.user32
#Prevents the screen from scaling with windows resolution scale
#System -> Display -> Scale and Layout
user32.SetProcessDPIAware()

if settings["Resolution"] == "Fullscreen":
    window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
else:
    res = settings["Resolution"].split("x")
    window = pygame.display.set_mode((int(res[0]), int(res[1])))

pygame.display.set_caption("SpeedTyper")
pygame.font.init()

game = Game(window, settings)
game.main()

if game.socket is not None:
    game.socket.EndConnection()

pygame.font.quit()
pygame.quit()