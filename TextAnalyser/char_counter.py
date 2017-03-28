# -*- coding: utf-8 -*-

def charIndex(c, alphabet):#c - char which we will check
  if (len(alphabet) == 0): return 0
  for i in range(len(alphabet)):
  	#if char is already defined to the aphabet => return it's index 
  	#otherwise return alpabet length (it's future index)
    if (c == alphabet[i][0]): return i 
  return len(alphabet)

def totalChars(alphabet):
  a = 0
  for i in alphabet:
    a += i[1]
  return a

#method will return list of all used chars and it's quantity
def count(s, ignUC): #s - input string
  if ignUC:
    s = s.lower()
  alphabet = []	
  charNum = len(s)
  chars = list(s)
  for i in range(charNum):
    activeChar = charIndex(chars[i], alphabet)
    #if char index == alphabet length char wasn't defined to the alphabet
    if (activeChar == len(alphabet)):
      alphabet.append([chars[i],0])
    alphabet[activeChar][1] += 1
  for i in range(len(alphabet)):
    alphabet[i].append(alphabet[i][1]*1.0/charNum*100.0) #adding percent of each char in text
    if alphabet[i][0] == ' ':
      alphabet[i][0] = '[ ]'
    elif alphabet[i][0] == '\n':
      alphabet[i][0] = '[\\n]'
  return alphabet
  # example of return : {{'a'(char),10(number of using),4(percent from all chars)},{'j',25,10},{'c',75,30}}