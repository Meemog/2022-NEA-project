#Object that is used in Scene objects to render pygame surface objects
class Surface():
    #Surface is a pygame surface object 
    #Location is where it is rendered (x,y)
    def __init__(self, surface, location = (0,0)):
        self.surface = surface
        self.location = location

    #Window is pygame surface object to draw on
    def Render(self, window):
        window.blit(self.surface, self.location)