# -*- coding: utf-8 -*-
from random import randint
#chains - массив в каждом из элементов которого содержится массив состоящий из 4 и более элементов
#первые три элемента это три слова из текста, далее слова, который появлялись в тексте после этих слов
#т.е. если текст : 'a b c d a b c f', то chains для этого текста будет (слова состоят из одной буквы для экономии места):
#[['a', 'b', 'c', 'd', 'f'],
# ['b', 'c', 'd', 'a'],
# ['c', 'd', 'a', 'b'],
# ['d', 'a', 'b', 'b'],
# здесь по идее должен был быть элемент ['a', 'b', 'c', 'f'], но его нет, т.к. последовательность 'a b c' в тексте уже встерчалсь,
# и 'f' отошел первому элементу
# т.к. после 'b c f' ничего нет после них идут первые элементы
# ['b', 'c', 'f', 'a'],
# ['c', 'f', 'a', 'b'],
# ['f', 'a', 'b', 'c']]
#
#После создания chains начинается генерация текста: берется рандомный элемент из chains, вставляется в output строку
#и из него выбирается рандомный элемент с индексом больше 2х т.е. тот, который стоял в исходном тексте после этой последовательности
#для первого элемента chains из первого примера это может быть 'd' либо 'f', потом ищется последовательность из последних 3
#элементов output (наример, если попался 'f', то это будет 'b c f', иначе 'b c d') и цикл повторяется снова
#(начиная со строки 18), пока количество сгенерированных слов не станет достаточным
#(я даже не знаю что менее непонятно: комменты или код)

def chainIndex(c, chains):
  for i in range(len(chains)):
    if c == chains[i][0:3] :
      return i
  return len(chains)

def isPunctuation(s):
  return s == '.' or s == ',' or s ==  '!' or s == '?'


def textToWords(s) :
  sLen = len(s)
  wordStart = 0
  words = []
  for i in range(sLen) :
    if (s[i].lower() == s[i].upper()) :
      if (i - wordStart > 0) :
        words.append(s[wordStart:i])
      wordStart = i+1
    if (isPunctuation(s[i])) :#чтобы сгенерированный текст содержал знаки орфографии, будем считать их за слова
      words.append(s[i])
  return words

def cap(s, b):
  if b :
    return s.capitalize()
  return s

def generate(s, wordsLen):
  s = s.lower()
  words = textToWords(s)
  chains = []
  for i in range(len(words) - 3):
    activeChain = [words[i], words[i + 1], words[i + 2]]
    aCIndex = chainIndex(activeChain, chains)
    if (aCIndex == len(chains)) :
      chains.append(activeChain)
    chains[aCIndex].append(words[i + 3])
  output = ''
  newChain = []
  t1 = randint(0,len(chains)-1)
  t2 = randint(3,len(chains[t1])-1)
  needToCap = True
  newWord = chains[t1][t2]
  for i in range(3):
    output += cap(chains[t1][i], i == 0) + ' '
    newChain.append(chains[t1][i])
    needToCap = newWord == '.' or newWord == '!' or newWord == '?'
  textLen = 3
  while (textLen < wordsLen):
    newWord = chains[t1][t2]
    output += cap(newWord, needToCap) + ' '
    needToCap = False
    if (not isPunctuation(newWord)):
      textLen += 1
    elif (newWord == '.' or newWord == '!' or newWord == '?'):
      needToCap = True
    for i in range(2):
      newChain[i] = newChain[i+1]
    newChain[2] = newWord
    t1 = chainIndex(newChain, chains)
    if t1 == len(chains):
      t1 = randint(0, len(chains)-1)
    t2 = randint(3,len(chains[t1])-1)
  return output + '.'