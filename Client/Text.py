#Text object that is stored in an array of objects in scene objects
class Text:
    #Font is the pygame font object that it will be rendered with
    #Colour is the RGB value in the form of a tuple
    #Text is the text that needs to be displayed
    #Location is the location of the top left of the render
    def __init__(self, font, colour = (255,255,255), text = "", location = (0,0)):
        self.font = font
        self.colour = colour
        self.text = text
        self.location = location

        #Pygame surface object that can be drawn on other surface objects
        self.textRender = self.font.render(self.text, True, self.colour)

    #Having this here reduces number of times it needs to be rendered, better performance
    def UpdateRender(self):
        self.textRender = self.font.render(self.text, True, self.colour)

    #Changes the text that needs to be rendered
    def SetText(self, newText):
        self.text = newText
        self.UpdateRender()
        
    #Changes the colour
    def SetColour(self, newColour):
        self.colour = newColour
        self.UpdateRender()

    #Changes the font
    def SetFont(self, newFont):
        self.font = newFont
        self.UpdateRender()
        
    #Renders the text onto the given window
    def Render(self, window):
        window.blit(self.textRender, self.location)