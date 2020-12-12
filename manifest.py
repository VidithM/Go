import math

class Manifest():
    def __init__(self, keywords, url):
        self.url = url 
        self.keywords = keywords 
    
    #Returns sigmoid(# of query matches)
    def rank(self, query):
        match = 0
        for elem in self.keywords:
            if(elem == query):
                match += 1
        
        return (4 / (1 + math.exp(-match/5))) - 2
    
