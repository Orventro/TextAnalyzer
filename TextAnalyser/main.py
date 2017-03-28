# -*- coding: utf-8 -*-
import char_counter as cc
import word_counter as wc
from sorter import sortBy
import text_generator as tg
from tkinter import *
from math import *

inputFile = ' '
inputString = ' '
generatedString = ''
generatedTextLen = 1000
revOrder = False # reversed order
sByQ = True # sort by Quantity : if true => sort by quantity, otherwise sort by alphabet
wPN = 0 # active word page number
cPN = 0 # active char page number
ignUC = False # ignore uppercase
infoFormat = 'Information. Total words : {}; Total charachters : {}; Average word length : {}; Longest word : {}, {} chars! '

def changeOrder():
  global revOrder, vocabulary, alphabet
  if revOrder:
    apperOrderBtn['text'] = '▼'
  else:
    apperOrderBtn['text'] = '▲'
  revOrder = not revOrder
  vocabulary.reverse()
  alphabet.reverse()
  displayStatistics()
  unhighlight()

def analyze():
  global alphabet, vocabulary, ignUC
  alphabet = cc.count(inputString, ignUC)
  vocabulary = wc.count(inputString)
  tw = wc.totalWords(vocabulary)
  tc = cc.totalChars(alphabet)
  lw = wc.longestWord(vocabulary)
  infoLbl['text'] = infoFormat.format(tw, tc, tc/tw, lw, len(lw))
  displayStatistics()
  unhighlight()

def setSortingBy(a):
  global sByQ
  sByQ = a
  if a:
    sbyQuant['bg'] = '#ccc'
    sbyAlph['bg'] = '#eee'
  else :
    sbyQuant['bg'] = '#eee'
    sbyAlph['bg'] = '#ccc'
  displayStatistics()
  unhighlight()

def displayStatistics():
  global alphabet,vocabulary, cPN, wPN
  alphabet = sortBy(alphabet, revOrder, sByQ)
  vocabulary = sortBy(vocabulary, revOrder, sByQ)
  for i in range(25):
    if i+cPN*25 < len(alphabet):
      charNameLabel[i+1]['text'] = alphabet[i + cPN * 25][0]
      charQuantityLabel[i+1]['text'] = str(alphabet[i + cPN * 25][1])
      charPercentLabel[i+1]['text'] = str(round(alphabet[i + cPN * 25][2], 2))
    else:
      charNameLabel[i+1]['text'] = ''
      charQuantityLabel[i+1]['text'] = '0'
      charPercentLabel[i+1]['text'] = '0'
    if i+wPN*25 < len(vocabulary):
      wordNameLabel[i+1]['text'] = vocabulary[i + wPN * 25][0]
      wordQuantityLabel[i+1]['text'] = str(vocabulary[i + wPN * 25][1])
      wordPercentLabel[i+1]['text'] = str(round(vocabulary[i + wPN * 25][2], 2))
    else:
      wordNameLabel[i+1]['text'] = ''
      wordQuantityLabel[i+1]['text'] = '0'
      wordPercentLabel[i+1]['text'] = '0'
    charNumLabel[i+1]['text'] = str(i+cPN*25+1)
    wordNumLabel[i+1]['text'] = str(i+wPN*25+1)
  c = navBtns(cPN, ceil(len(alphabet)/25), 7)
  for i in range(7):
    charNav[i].pack_forget()
    if c[i][0]:
      charNav[i]=Button(charFrame[26],padx=3,bg=c[i][2],text=c[i][1],fg='#333',command=lambda a=int(c[i][1]):moveToPage(a-1,True))
      charNav[i].pack(side = LEFT)
    elif i > 0 and c[i - 1][0] and i < 6 and c[i + 1][0]:
      charNav[i] = Label(charFrame[26], bg = '#ccc', text = '...', fg = '#333')
      charNav[i].pack(side = LEFT)
  w = navBtns(wPN, ceil(len(vocabulary)/25), 9)
  for i in range(9):
    wordNav[i].pack_forget()
    if w[i][0]:
      wordNav[i]=Button(wordFrame[26],padx=3,bg=w[i][2],text=w[i][1],fg='#333',command=lambda a=int(w[i][1]):moveToPage(a-1,False))
      wordNav[i].pack(side = LEFT)
    elif i > 0 and w[i - 1][0] and i < 8 and w[i + 1][0]:
      wordNav[i] = Label(wordFrame[26], bg = '#ccc', text = '...', fg = '#333')
      wordNav[i].pack(side = LEFT)
  resizeWords()

def moveToPage(a, b):
  global cPN, wPN
  if b :
    cPN = a
  else : 
    wPN = a
  displayStatistics()
  unhighlight()

def ignoreUppercase():
  global ignUC, ignUCBtn, alphabet
  ignUC = not ignUC
  ignUCBtn['bg'] = '#ccc' if ignUC else '#eee'
  alphabet = cc.count(inputString, ignUC)
  displayStatistics()
  unhighlight()

def navBtns(p, n, l):
  b = []
  if n < l+1:
    for i in range(l):
      b.append([i<n, str(i+1)])
  else :
    b.append([True, '1'])
    if n - p > (l-5)/2+1:
      if p > (l-5)/2+1:
        b.append([False])
        for i in range(l-4):
          b.append([True, str(p+i-(l-4)//2+1)])
      else:
        for i in range(1,l-2):
          b.append([True, str(i+1)])
      b.append([False])
    else:
      for i in range((l-1)//2-1):
        b.append([True, str(i+2)])
      b.append([False])
      for i in range((l-1)//2-1):
        b.append([True, str(n-(l-1)//2+1+i)])
    b.append([True, str(n)])
  for i in range(l):
    if b[i][0]:
      if p+1 == int(b[i][1]):
        b[i].append('#ccc')
      else:
        b[i].append('#eee')
  return b

def search(a):
  global vocabulary, alphabet, wPN, cPN
  unhighlight()
  b = []
  ci = len(alphabet)
  wi = wc.wordIndex(a, vocabulary)
  if len(a) == 1 or len(a) >= 3 and a[:1] + a[len(a)-1:] == '[]' :
    ci = cc.charIndex(a, alphabet)
  if wi < len(vocabulary):
    wPN = int((wi)/25)
    wordNumLabel[wi%25+1]['bg'] = '#ee7'
    wordNameLabel[wi%25+1]['bg'] = '#ee7'
    wordQuantityLabel[wi%25+1]['bg'] = '#ee7'
    wordPercentLabel[wi%25+1]['bg'] = '#ee7'
  if ci < len(alphabet):
    cPN = int((ci-1)/25)
    charNumLabel[ci%25+1]['bg'] = '#ee7'
    charNameLabel[ci%25+1]['bg'] = '#ee7'
    charQuantityLabel[ci%25+1]['bg'] = '#ee7'
    charPercentLabel[ci%25+1]['bg'] = '#ee7'
  displayStatistics()
    
def unhighlight():
  for i in range(1,26):
    wordNumLabel[i]['bg'] = '#eee'
    wordNameLabel[i]['bg'] = '#eee'
    wordQuantityLabel[i]['bg'] = '#eee'
    wordPercentLabel[i]['bg'] = '#eee'
    charNumLabel[i]['bg'] = '#eee'
    charNameLabel[i]['bg'] = '#eee'
    charQuantityLabel[i]['bg'] = '#eee'
    charPercentLabel[i]['bg'] = '#eee'

def openFileBrowser():
  global inputFile, inputString
  from tkinter.filedialog import askopenfilename
  inputFile = open(askopenfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*") )))
  inputString = inputFile.read()
  inputFile.close()
  inputText.delete(1.0, END)
  inputText.insert(1.0, inputString)

def resizeWords():
  global wordNameLabel, charNameLabel
  a = 15
  for i in wordNameLabel:
    if a < len(i['text']):
      a = len(i['text'])
  for i in range(len(wordNameLabel)):
    wordNameLabel[i]['width'] = a

#def resizeTextFields():
#  global 

def generate():
  global generatedString, generatedTextLen
  generatedTextLen = int(generateEntry.get())
  generatedString = tg.generate(inputString, generatedTextLen)
  generatedText.delete(1.0, END)
  generatedText.insert(1.0, generatedString)



# INTERFACE
root = Tk()
sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (sw, sh))
#Topbar
topbar = Frame(root, bg = '#ccc')
topbar.pack(side = TOP, fill = X)
ignUCBtn = Button(topbar, bg = '#eee', fg = '#333', text = 'Aa', padx = 5, command = ignoreUppercase)
ignUCBtn.pack(side = LEFT, padx = 5)
apperOrderBtn = Button(topbar, bg = '#eee', fg = '#333', text = '▼', padx = 3, command = changeOrder)
apperOrderBtn.pack(side = LEFT, padx = 5)
sbyLabel = Label(topbar, bg = '#ccc', fg = '#333', text = 'sort by:')
sbyLabel.pack(side = LEFT)
sbyFrame = Frame(topbar, bg = '#eee')
sbyFrame.pack(side = LEFT, fill = Y)
sbyAlph = Button(sbyFrame, bg = '#eee', fg = '#333', text = 'Chacters', padx = 0, pady = 0, command = lambda : setSortingBy(False))
sbyAlph.pack(side = TOP)
sbyQuant = Button(sbyFrame, bg = '#ccc', fg = '#333', text = 'Quantity', padx = 0, pady = 0, command = lambda : setSortingBy(True))
sbyQuant.pack(side = BOTTOM)
searchLabel = Label(topbar, bg = '#ccc', fg = '#333', text = 'Search:')
searchLabel.pack(side = LEFT, padx = 5)
searchEntry = Entry(topbar, bg = '#f8f8f8', fg = '#333', width = 12)
searchEntry.pack(side = LEFT)
applySearch = Button(topbar, bg = '#eee', fg = '#333', text = 'OK', command = lambda : search(searchEntry.get()))
applySearch.pack(side = LEFT)
analyzeBtn = Button(topbar, bg = '#eee', fg = '#333', text = 'Analyse text', command = analyze)
analyzeBtn.pack(side = LEFT, padx = 5)
generateBtn = Button(topbar, bg = '#eee', fg = '#333', text = 'Generate text', command = generate)
generateBtn.pack(side = LEFT)
generateLabel = Label(topbar, bg = '#ccc', fg = '#333', text = 'with length of:')
generateLabel.pack(side = LEFT)
generateEntry = Entry(topbar, bg = '#eee', fg = '#333', width = 6)
generateEntry.pack(side = LEFT)
generateEntry.insert(0, '1000')
openFileBtn = Button(topbar, bg = '#eee', fg = '#333', text = 'Open file', command = openFileBrowser)
openFileBtn.pack(side = LEFT, padx = 5)
#Workplace
workplace = Frame(root, bg = '#aaa')
workplace.pack(side = TOP, fill = BOTH)
charListFrame = Frame(workplace, bg = '#333', bd = 2)
charListFrame.pack(side = LEFT, fill = Y)
charFrame = []
charNumLabel = []
charNameLabel = []
charQuantityLabel = []
charPercentLabel = []
for i in range(26):
  charFrame.append(Frame(charListFrame, bg = '#333'))
  charFrame[i].pack(side = TOP, pady = i%2)
  charNumLabel.append(Label(charFrame[i], text = '№', bg = '#eee', fg = '#417', width = 3))
  charNumLabel[i].pack(side = LEFT, fill = Y, padx = 1)
  charNameLabel.append(Label(charFrame[i], text = 'Char', bg = '#eee', fg = '#417', font = 20, width = 4))
  charNameLabel[i].pack(side = LEFT, fill = Y)
  charQuantityLabel.append(Label(charFrame[i], text = 'Quantity', bg = '#eee', fg = '#333', width = 8))
  charQuantityLabel[i].pack(side = LEFT, fill = Y, padx = 1)
  charPercentLabel.append(Label(charFrame[i], text = '%', bg = '#eee', fg = '#181', width = 4))
  charPercentLabel[i].pack(side = LEFT, fill = Y)
charFrame.append(Frame(charListFrame, bg = '#ccc'))
charFrame[26].pack(side = TOP, fill = X)
wordListFrame = Frame(workplace, bg = '#333', bd = 2)
wordListFrame.pack(side = LEFT, fill = Y)
wordFrame = []
wordNumLabel = []
wordNameLabel = []
wordQuantityLabel = []
wordPercentLabel = []
for i in range(26):
  wordFrame.append(Frame(wordListFrame, bg = '#333'))
  wordFrame[i].pack(side = TOP, pady = i%2)
  wordNumLabel.append(Label(wordFrame[i], text = '№', bg = '#eee', fg = '#417', width = 4))
  wordNumLabel[i].pack(side = LEFT, fill = Y, padx = 1)
  wordNameLabel.append(Label(wordFrame[i], text = 'Word', bg = '#eee', fg = '#417', font = 20, width = 15))
  wordNameLabel[i].pack(side = LEFT, fill = Y)
  wordQuantityLabel.append(Label(wordFrame[i], text = 'Quantity', bg = '#eee', fg = '#333', width = 7))
  wordQuantityLabel[i].pack(side = LEFT, fill = Y, padx = 1)
  wordPercentLabel.append(Label(wordFrame[i], text = '%', bg = '#eee', fg = '#181', width = 4))
  wordPercentLabel[i].pack(side = LEFT, fill = Y)
wordFrame.append(Frame(wordListFrame, bg = '#ccc'))
wordFrame[26].pack(side = TOP, fill = X)
inputFrame = Frame(workplace)
inputFrame.pack(side = LEFT, fill = Y)
inputHead = Label(inputFrame, bg = '#eee', fg = '#555', font = 20, text = 'Input text')
inputHead.pack(side = TOP, fill = X)
inputText = Text(inputFrame, bg = '#fff', fg = '#333', wrap = WORD, width = 60)
inputText.pack(side = LEFT, fill = Y)
generatedFrame = Frame(workplace)
generatedFrame.pack(side = LEFT, fill = Y)
generatedHead = Label(generatedFrame, bg = '#eee', fg = '#555', font = 20, text = 'Generated text')
generatedHead.pack(side = TOP, fill = X)
generatedText = Text(generatedFrame, bg = '#fff', fg = '#333', wrap = WORD)
generatedText.pack(side = LEFT, fill = Y)
#Bottombar
bottombar = Frame(root, bg = '#eee')
bottombar.pack(side = TOP, fill = BOTH)
charNav = []
for i in range(7):
  charNav.append(Label(charFrame[26], bg = '#ccc'))
wordNav = []
for i in range(9):
  wordNav.append(Label(wordFrame[26], bg = '#ccc'))
infoLbl = Label(bottombar, bg = '#eee', fg = '#333', text = 'Here will appear some information about text')
infoLbl.pack(side = LEFT)
root.mainloop()