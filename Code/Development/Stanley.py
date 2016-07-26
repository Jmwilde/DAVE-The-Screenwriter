import random, time
from HAL import sentGenerator as gen

class director(object):
    """
    The director Stanley decides what to print out next.

    Param:
        head : list of header strings
        char : list of character strings
        paren : list of parenthetical strings
        trans : list of transition strings
        act : sentGenerator for action 
        dia : sentGenerator for dialogue
    """
    def __init__(self, headers, characters, parentheticals,
                 transitions, actions, dialogue, outfile):

        self.head = headers
        self.char = characters
        self.paren = parentheticals
        self.trans = transitions
        self.act = actions
        self.dia = dialogue
        self.out = outfile
    
    def __call__(self):
        self.__write_script(120, self.out)

    def __write_script(self, length, outfile):
        start_time = time.time()
        needHeader = True
        needAction = False
        needCharacter = False
        needDialog = False
        needTransition = False
        needParanthetical = False

        for i in range(length):
            actlen = 1.8 * len(self.char)
            dialen = 2.2 * len(self.char)

            if (needCharacter and needTransition and needAction and needHeader):
                rand = random.random() * (len(self.head) + actlen +
                                          len(self.char) + len(self.trans))     
                if (rand < len(self.head) and len(self.head) > 0):
                    currentScene = self.__randomPop(self.head)
                    outfile.write(currentScene)
                    needHeader = False
                    needAction = True

                elif (rand < actlen + len(self.head) and actlen > 0):
                    nextAction = self.act(3)
                    outfile.write('\n')
                    outfile.write('Action:')
                    outfile.write(nextAction)
                    needCharacter = True
                    needTransition = True
                    needHeader = True

                elif (rand < len(self.char) + actlen + len(self.head) 
                        and len(self.char) > 0):
                    nextChar = self.__randomPop(self.char)
                    outfile.write('\n')
                    outfile.write('Character:')
                    outfile.write(nextChar)
                    needDialog = True
                    needParanthetical = True

                elif (rand < len(self.trans) + actlen + len(self.char) 
                           + len(self.head) and len(self.trans) > 0):       
                    nexttrans = self.__randomPop(self.trans)
                    outfile.write('\n')
                    outfile.write('Transition:')
                    outfile.write(nexttrans)
                    needHeader = True
                    needTransition = False

            if needDialog:
                rand = random.random() * (dialen + actlen + len(self.paren))

                if (needParanthetical and rand < len(self.paren) 
                                      and len(self.paren) > 0):
                    nextPara = self.__randomPop(self.paren)
                    outfile.write('\n')
                    outfile.write('Parenthetical:')
                    outfile.write(nextPara)
                    needParanthetical = False

                for i in range(random.randint(1, 10)):
                    nextPhrase = self.dia()
                    outfile.write('\n')
                    outfile.write('Dialogue:')
                    outfile.write(nextPhrase)

                needDialog = False
                needHeader = True
                needAction = True
                needTransition = True
                needCharacter = True

            elif needAction and actlen > 0:

                for i in range(random.randint(0, 3)):
                    nextAction = self.act(3)
                    outfile.write('\n')
                    outfile.write('Action:')
                    outfile.write(nextAction)

                needCharacter = True
                needTransition = True
                needHeader = True

            elif (needHeader and len(self.head) > 0):
                    currentScene = self.__randomPop(self.head)
                    outfile.write('\n')
                    outfile.write(currentScene)
                    needHeader = False
                    needAction = True
            else:
                return
        print ('Time elapsed: ', time.time()-start_time)
        return

    def __randomPop(self, lis):
        """
        Pops off a random item from a list.
        """
        rand = int(random.random() * len(lis))
        if (rand == len(lis) and len(lis) > 0):
            rand -= 1
        obj = lis[rand]
        lis.remove(obj)
        return obj