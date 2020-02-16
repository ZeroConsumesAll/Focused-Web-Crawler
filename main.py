from bs4 import BeautifulSoup
from collections import deque
from nltk.stem import SnowballStemmer
from queue import PriorityQueue
import queue
import requests

blacklist = [
    'document',
	'noscript',
	'header',
	'html',
	'meta',
	'head',
    'script', 
	'input',
    'type', 
    'style']

stopwords = [
    "a", "about", "above", "after", "again", "against", "ain", "all", "am", "an", "and", "any", "are", "aren", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can", "couldn", "couldn't", "d", "did", "didn", "didn't", "do", "does", "doesn", "doesn't", "doing", "don", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn", "hadn't", "has", "hasn", "hasn't", "have", "haven", "haven't", "having", "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is", "isn", "isn't", "it", "it's", "its", "itself", "just", "ll", "m", "ma", "me", "mightn", "mightn't", "more", "most", "mustn", "mustn't", "my", "myself", "needn", "needn't", "no", "nor", "not", "now", "o", "of", "off", "on", "once", "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "re", "s", "same", "shan", "shan't", "she", "she's", "should", "should've", "shouldn", "shouldn't", "so", "some", "such", "t", "than", "that", "that'll", "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those", "through", "to", "too", "under", "until", "up", "ve", "very", "was", "wasn", "wasn't", "we", "were", "weren", "weren't", "what", "when", "where", "which", "while", "who", "whom", "why", "will", "with", "won", "won't", "wouldn", "wouldn't", "y", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves", "could", "he'd", "he'll", "he's", "here's", "how's", "i'd", "i'll", "i'm", "i've", "let's", "ought", "she'd", "she'll", "that's", "there's", "they'd", "they'll", "they're", "they've", "we'd", "we'll", "we're", "we've", "what's", "when's", "where's", "who's", "why's", "would"]

specialCharacters  = [
    '.', '@', '#', '$', '%', '^', '&', '*', '(', ')', '{', '}', '[', ']', "/", '!', ';', ':', '|', '`', '~', ',', '?', '-', '>', '<']

stemmer = SnowballStemmer('english')


countWords = set()
childLinks = set()
queueLinks = queue.Queue()
pqueue = PriorityQueue()


def linksToSetandQueue(seed):
    res = requests.get(seed)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    for link in soup.find_all('a'):
        hyperlink = link.get("href")
        #add links to set and queue
        childLinks.add(hyperlink)
        queueLinks.put((hyperlink, 1))

def getText(seed):
    res = requests.get(seed)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text = True)
    
    for k in text:
        if k.parent.name not in blacklist and k not in stopwords and k not in specialCharacters:
            cannonForm = stemmer.stem(k)
            countWords.add(cannonForm)


        
# find priority of each link in queue
def priority():
    linkOverlap = 0
    leftmost = queueLinks.get()
    url = leftmost[0]
    depth = leftmost[1]
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')

    for link in soup.find_all('a'):
        hyperlink = link.get("href")
        queueLinks.add((hyperlink, back[1] + 1))
        if(hyperlink in childLinks):
                linkOverlap += 1
    
    jaccardIndex = linkOverlap/(len(childLinks) + len(compareLinks) - linkOverlap)       
    text = soup.find_all(text = True)

    for t in text:
        if stemmer.stem(t) in countWords:
            textOverlap += 1

    priority = jaccardIndex * .5 + textOverlap * .3 + depth * .2
    pqueue.put((-priority, url))

def printLinks():
    while not pqueue.empty():
        url = pqueue.get()
        print(url[1])


def main(): 
    seed = input("Plese enter a url, surrounded by quotes")
    linksToSetandQueue(seed)
    getText(seed)

    while not queueLinks.empty():
        priority()
    printLinks()

if __name__ == "__main__":
    main()







