from random_word import RandomWords

class WordGenerator:
    def __init__(self):
        self.__wordGenerator = RandomWords()

    def __GetWords(self):
        listOfWords = self.__wordGenerator.get_random_words()
        x = 0
        while x < len(listOfWords):
            numFound = False
            listOfWords[x] = listOfWords[x].lower()
            for i in range(len(listOfWords[x]) - 1):
                try: 
                    int(listOfWords[x][i])
                    numFound = True
                except:
                    pass
            x += 1
            if numFound:
                listOfWords.pop(x)
        return listOfWords
    
    #cuts lyrics down to certain length and removes newlines
    def __MakeWordsCorrectLength(self, words, length):
        newWords = []
        print(words)
        while len(words) < length:
            newWords += words
            length -= len(words)

        newWords += words[:length]
        wordsString = " ".join(newWords)
        return wordsString

    #main function that is to generate a number of words to be displayed in the game
    def GetWordsForProgram(self, length):
        return self.__MakeWordsCorrectLength(self.__GetWords(), length)

wordGenerator = WordGenerator()
print(wordGenerator.GetWordsForProgram(50))
