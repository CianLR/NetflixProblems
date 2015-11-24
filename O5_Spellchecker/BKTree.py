class Node:
    def __init__(self, word):
        self.word = word
        self.nodes = {}

    def addNode(self, inNode, distance):
        self.nodes[distance] = inNode

    def getNode(self, distance):
        if distance in self.nodes:
            return self.nodes[distance]
        else:
            return None

    def getWord(self):
        return self.word

class BKTree:
    def KernighanDistance(self, s, t):
        return
    
    def LevenshteinDistance(self, s, t):
        s = s.lower()
        t = t.lower()
        sLen = len(s)
        tLen = len(t)

        if min(sLen,tLen) == 0: return max(sLen, tLen)

        matrix = [[0 for x in range(sLen+1)] for y in range(tLen+1)]
        for x in range(sLen+1):
            matrix[0][x] = x
        for y in range(tLen+1):
            matrix[y][0] = y
        
        for i in xrange(1, sLen+1):
            for j in xrange(1, tLen+1):
                matrix[j][i] = min(matrix[j][i-1] + 1,
                                   matrix[j-1][i] + 1,
                                   matrix[j-1][i-1] + int(not s[i-1]==t[j-1]))
        '''
        for i in range(tLen+1):
            for j in range(sLen+1):
                print str(matrix[i][j]) + ' ',
            print
        '''
        return matrix[tLen][sLen]

    def __init__(self, wordList):
        '''Initialises the BK tree by constructing it out of a list of words'''
        self.root = Node(wordList[0])
        for word in wordList[1:]:
            
            curNode = self.root
            nextNode = self.root
            
            while nextNode != None:
                curNode = nextNode
                curDist = self.LevenshteinDistance(curNode.getWord(),word)
                nextNode = curNode.getNode(curDist)
            
            curNode.addNode(Node(word),curDist)

    def find(self, word, tolerance):
        '''This fucntion calls _find and sorts the return list while removing the distances'''
        return [x[1] for x in sorted(self._find(self.root, word, tolerance))]

    def _find(self, curNode, word, tol):
        '''This is a "private" function that recursively finds words within the tolerance'''
        if curNode == None: return []
        
        curDist = self.LevenshteinDistance(curNode.getWord(),word)
        if curDist <= tol: retList = [[curDist,curNode.getWord()]]
        else: retList = []
        
        for i in xrange(max(curDist - tol,1), curDist + tol):
            retList += self._find(curNode.getNode(i),word,tol)

        return retList
