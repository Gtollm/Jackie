from openai_api import Qtype
class former:
    def __init__(self):
        self.text=""
        tmp=["True/False Question*","Multiple-Choice Question*","Fill-in-the-Blank Question*","Question* with open answer"]
        self.types=[Qtype(tmp[i],0) for i in range(4)]
    def setText(self, text):
        self.text=text
    def appendType(self,type,i):
        self.types[i-1]=type
    def getText(self):
        return self.text
    def getTypes(self):
        return self.types
