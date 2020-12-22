import math

class Manifest():
    def __init__(self, keywords, url, title):
        self.url = url 
        self.keywords = keywords 
        self.title = title
    
    #Returns sigmoid(# of query matches)
    def rank(self, query):
        match = 0
        for elem in query:
            if(elem.lower() in self.keywords):
                match += 1
        
        return (4 / (1 + math.exp(-match/5))) - 2
    
