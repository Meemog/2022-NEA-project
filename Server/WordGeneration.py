from random_word import RandomWords

class WordGenerator:
    def __init__(self):
        self.__wordGenerator = RandomWords()

    #Gets list of random words
    def __GetWords(self):
        listOfWords = self.__wordGenerator.get_random_words()
        x = 0
        #Removes instances with numbers
        while x < len(listOfWords):
            erroneousFound = False
            listOfWords[x] = listOfWords[x].lower()
            for i in range(len(listOfWords[x]) - 1):
                asciiOfLetter = ord(listOfWords[x][i])
                if not (33 <= asciiOfLetter <= 47 or 58 <= asciiOfLetter <= 90 or 97 <= asciiOfLetter <= 122):
                    erroneousFound = True
            x += 1
            if erroneousFound:
                listOfWords.pop(x)
        return listOfWords
    
    #cuts lyrics down to certain length and removes newlines
    def __MakeWordsCorrectLength(self, words, length):
        newWords = []
        while len(words) < length:
            newWords += words
            length -= len(words)

        newWords += words[:length]
        wordsString = " ".join(newWords)
        return wordsString

    #main function that is to generate a number of words to be displayed in the game
    def GetWordsForProgram(self, length):
        return self.__MakeWordsCorrectLength(self.__GetWords(), length)
