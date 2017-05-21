# -*- coding: utf-8 -*-

def wordIndex(s, voc) :
  if (len(voc) == 0): return 0
  for i in range(len(voc)):
    #if word is already defined to the vocabulary => return it's index 
    #otherwise return vocabulary length (it's future index)
    if (s == voc[i][0]): return i 
  return len(voc)

#transforms text(string) to list of words(array)
def textToWords(s) :
  sLen = len(s)
  wordStart = 0
  words = []
  for i in range(sLen) :
    if (s[i].lower() == s[i].upper()) :
      if (i - wordStart > 0) :
        words.append(s[wordStart:i])
      wordStart = i+1
  return words

#finds longest word in vocabulary
def longestWord(vocabulary):
  b = ''
  a = 0
  for i in vocabulary:
    if a < len(i[0]):
      b = i[0]
      a = len(i[0])
  return b

#count number of words in vocabulary
def totalWords(vocabulary):
  a = 0
  for i in vocabulary:
    a += i[1]
  return a

#gets string and transforms it to vocabulary
def count(s) :
  vocabulary = []
  s = s.lower() #Lowercases all letters in string. If not do this 'Cat' and 'cat' will count as different words
  #transform string to list of words
  words = textToWords(s)
  wordNum = len(words)
  #creating a vocabulary 
  #vocabulary is a list with structure:
  # [[word, quantity of this word in text, percent of usage], [another word, it's quantity, and percent of usage], [and, so, on]]
  for i in range(wordNum) :
    activeWord = wordIndex(words[i], vocabulary)
    if (activeWord == len(vocabulary)) :
      vocabulary.append([words[i], 0])
    vocabulary[activeWord][1] += 1
  for i in range(len(vocabulary)):
    vocabulary[i].append(vocabulary[i][1]*100.0/wordNum) #adding percent of each word in text
  return vocabulary
