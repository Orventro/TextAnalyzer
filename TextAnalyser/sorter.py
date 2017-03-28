# -*- coding: utf-8 -*-

def quantity(w) :
  return w[1]

def alphabet(w) :
  return w[0]

def sortBy(vocabulary, b, sByQ) :
  if sByQ:
  	return sorted(vocabulary, key = quantity, reverse = not b)
  return sorted(vocabulary, key = alphabet, reverse = b)