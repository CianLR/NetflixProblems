import string
import random
import sys


class MarkovChain:

    chain = {}

    def __init__(self, corpus):
        prevWord1 = "" #Word that's one back from current
        prevWord2 = "" #Word that's two back from current
        
        for word in corpus.split():

            #Check if we're at the end of a sentence
            isEnd = False
            if word[-1] == '.' or word[-1] == '?' or word[-1] == '!':
                isEnd = True

            #Strip special chars and change to lowercase
            word = word.translate(string.maketrans("",""), string.punctuation).lower()

            self.addWord(prevWord2,prevWord1,word) #Add the word to the chain
            prevWord2 = prevWord1
            prevWord1 = word

            if isEnd:
                #If at the end add the keyword "~ENDISNIGH~" and reset vars
                self.addWord(prevWord2,prevWord1,"~ENDISNIGH~")
                prevWord2 = ""
                prevWord1 = ""

        return
    
    def getNextWord(self,prevWord2,prevWord1):
        random.seed()
        randSelector = random.random() #Generate random float between 0 and 1
        probabilityAccum = 0.0
        nextWord = ""
        
        totalCount = self.chain[prevWord2][prevWord1]["~COUNT~"]

        #For each word add its probability to probabilityAccum unill it passes randSelector
        #and the current word is selected.
        for word in self.chain[prevWord2][prevWord1]:
            if word == "~COUNT~": continue
            
            currentWordCount = self.chain[prevWord2][prevWord1][word]
            probabilityAccum += currentWordCount/float(totalCount)

            if probabilityAccum >= randSelector:
                nextWord = word
                break

        return nextWord
        
    def fixGrammar(self, word):
        if word == "i": return "I"
        if word == "im": return "I'm"
        if word == "id": return "I'd"
        if word == "ive": return "I've"
        if word == "howd": return "how'd"
        if word == "dont": return "don't"
        if word == "cant": return "can't"
        if word == "didnt": return "didn't"
        if word == "youve": return "you've"
        if word == "weve": return "we've"
        if word == "youre": return "you're"
        if word == "youd": return "you'd"
        if word == "wont": return "won't"
        if word == "couldnt": return "couldn't"
        if word == "wouldnt": return "wouldn't"
        if word == "havent": return "haven't"
        return word

    def addWord(self,prevWord2,prevWord1,word):
        #Add the word to the chain if not there.
        #If the word is there then increment its frequency and increment the total number of words.
        if prevWord2 in self.chain:
            if prevWord1 in self.chain[prevWord2]:
                if word in self.chain[prevWord2][prevWord1]:
                    self.chain[prevWord2][prevWord1][word] += 1
                    self.chain[prevWord2][prevWord1]["~COUNT~"] += 1

                else:
                    self.chain[prevWord2][prevWord1][word] = 1
                    self.chain[prevWord2][prevWord1]["~COUNT~"] += 1
                    
            else:
                self.chain[prevWord2][prevWord1] = {"~COUNT~":1,word:1}
        else:
            self.chain[prevWord2] = {prevWord1:{"~COUNT~":1,word:1}}       
        
        return

    def buildSentence(self, maxLen):
        prevWord1 = ""
        prevWord2 = ""
        sentence = ""
        
        while True:
            nextWord = self.getNextWord(prevWord2, prevWord1)

            prevWord2 = prevWord1
            prevWord1 = nextWord
            if nextWord == "~ENDISNIGH~": break #If the end of sentence keyword is reached then finish the sentence
            
            sentence += self.fixGrammar(nextWord) + " "

            if len(sentence) > maxLen:
                #If the sentence overshoots the max then start again
                prevWord1 = ""
                prevWord2 = ""
                sentence = ""

        if len(sentence) > 1:
            sentence = sentence[0].upper() + sentence[1:-1] + "." #Capitalise and add a full stop
        else:
            sentence = self.buildSentence(maxLen) #If the sentence is too short then build a new one
        
        if len(sentence) < maxLen/2 and maxLen > 30: #If the sentence is less than half the max length and the max length isn't too small then append another
            return sentence + " " + self.buildSentence(maxLen - len(sentence))
        else:
            return sentence        
        

#Take in corpus
if len(sys.argv) != 2:
    print "Usage:"
    print "python twitterbot.py [path to corpus]"
    sys.exit()
else:
    corpusPath = sys.argv[1]

corpusFile = open(corpusPath,'r')

print "Building Markov chain..."
print "(This takes about 25s for a 10MB file)"
twitterBot = MarkovChain(corpusFile.read()) #Build MarkovChain object
print "Chain built!"


while True:

    if raw_input("Press enter to print a sentence or 'q' to quit: ") == 'q': sys.exit()
    
    print ""
    print twitterBot.buildSentence(140) #Build a sentence of maxLength 140 chars.
    print ""
        
    
