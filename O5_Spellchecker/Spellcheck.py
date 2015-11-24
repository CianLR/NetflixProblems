from BKTree import *
from Tkinter import *
from time import sleep
#from multiprocessing import Process
import thread
import string
import cPickle

class Spellcheck:
    def __init__(self, BKFile):
        self.tree = None
        thread.start_new_thread(self.loadTree, (BKFile,))
        
        self.suggestions = {}
                   
        self.top = Tk()

        self.F1 = Frame(self.top)
        self.F1.pack()
        self.F2 = Frame(self.top, width=80, height=50)
        self.F2.pack()

        self.L1 = Label(self.F1, text="Check yourself before you wreck yourself")
        self.L1.pack(side=LEFT)
        self.B1 = Button(self.F1, text="Check words", command=lambda:thread.start_new_thread(self.checkWord,()))
        self.B1.pack(side=RIGHT)
        self.B2 = Button(self.F1, text="Settings", command=self.settingsWindow)
        self.B2.pack(side=RIGHT)
        self.T1 = Text(self.F2, bd=5, width=60)
        self.T1.pack()
        self.T1.focus()    

    def start(self):
        self.top.mainloop()

    def loadTree(self, BKFile):
        f = open(BKFile,'r')
        self.tree = cPickle.load(f)
        f.close()
        
    def settingsWindow(self):
        setWin = Toplevel(self.top)
        setWin.wm_title("Settings")
        l = Label(setWin, text="This is window #")
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)
    
    def contextMenuSuggest(self, event):

        def replaceWordBuilder(tag, word):
            def replaceWord():
                tagRange = self.T1.tag_ranges(tag)
                self.T1.delete(tagRange[0], tagRange[1])
                self.T1.insert(tagRange[0], word)
                self.T1.tag_delete(tag)
            return replaceWord

        def ignoreBuilder(tag):
            def ignore():
                self.T1.tag_delete(tag)
            return ignore
        
        print "Tag Clicked"
        tag = self.T1.tag_names("@{0},{1}".format(event.x, event.y))[0]
        menu = Menu(self.top, tearoff=0)

        suggestions = self.suggestions[tag]

        if suggestions == []:
            menu.add_command(label="No suggestions", state="disabled")
        else:
            for i in range(len(suggestions)):
                if i > 5:
                    break
                menu.add_command(label=suggestions[i], command=replaceWordBuilder(tag, suggestions[i]))

        menu.add_separator()
        menu.add_command(label="Ignore", command=ignoreBuilder(tag))
        menu.post(event.x_root, event.y_root)

    def allAlpha(self, word):
        for char in word:
            if char not in string.ascii_letters:
                return False
        return True

    def checkWord(self):
        #print "WHAT"
        while self.tree == None:
            print "Hoooold..."
            sleep(1)
            #self.treeLoading.join()
        text = self.T1.get(1.0,END)
        currWord = ''
        for tag in self.T1.tag_names():
            self.T1.tag_delete(tag)
            
        for i in range(len(text)):
            if text[i] not in '''\t\n\x0b\x0c\r ",.!?''':
                currWord += text[i]
            elif currWord != '':
                if not self.allAlpha(currWord):
                    currWord = ""
                    continue
                
                print currWord
                startIndex = "1.0 + {0} chars".format(i - len(currWord))
                endIndex = "1.0 + {0} chars".format(i)
                self.T1.tag_add(str(i), startIndex, endIndex)

                if len(currWord) < 4:
                    matches = self.tree.find(currWord, 1)
                else:
                    matches = self.tree.find(currWord, 2)
                print matches, self.tree
                if matches != [] and matches[0].lower() == currWord.lower():
                    currWord = ""
                    continue
                
                if len(matches) < 3:
                    matches = self.tree.find(currWord, 3)
                
                self.suggestions[str(i)] = matches
                self.T1.tag_config(str(i), foreground="red")
                self.T1.tag_bind(str(i), '<3>', self.contextMenuSuggest)
                print currWord
                print matches

                currWord = ""



#testList = ['book','books','cart','cake','boo','cape','boon','cook']
#tree = BKTree(open("large.txt",'r').read().split())
#cPickle.dump(tree,f)

spell = Spellcheck("txt\pickeledL.txt")
#thread.start_new_thread(loadTree,(f,spell))
spell.start()
                   
