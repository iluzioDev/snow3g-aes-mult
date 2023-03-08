#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 2023

@author: iluzioDev

This script implements the multiplication used in the SNOW 3G and AES algorithms.
"""
import lfsr
import functools

ROW = '■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■'

SNOW3G_BYTE = '10101001'
AES_BYTE = '00011011'

def mult(byte1, byte2, algorithm_byte):
  """This function implements the multiplication used in the SNOW 3G and AES algorithms.

  Args:
      byte1 (str): First byte to be multiplied
      

  Returns:
      str: Result of the multiplication.
  """
  if type(byte1) is not str and type(byte2) is not str and type(algorithm_byte) is not str:
    return None
  
  length = len(byte1) if len(byte1) > len(byte2) else len(byte2)
  byte1 = byte1.zfill(length)
  byte2 = byte2.zfill(length)
  
  exponents = lfsr.binary_to_polynomial(byte2)
  
  if len(algorithm_byte) < length:
    algorithm_byte = algorithm_byte.zfill(length)
  
  result = []
  
  for i in exponents:
    if i == '1':
      result.append(byte1)
    else:
      aux = byte1
      for j in range(int(i[1:])):
        overflow = aux[0]
        aux =  aux[1:] + '0'
        if overflow == '1':
          aux = lfsr.xor(aux, algorithm_byte)
      result.append(aux)
      
  if len(result) != 0:
    result = functools.reduce(lfsr.xor, result)
  else:
    result = '0' * length
  return result

def main():
  """Main function of the script.
  """
  while(True):
    print(ROW)
    print('■      WELCOME TO THE SNOW 3G AND AES MULTIPLICATION TOOL      ■')
    print(ROW)
    print('What do you want to do?')
    print('[1] SNOW 3G multiplication.')
    print('[2] AES multiplication.')
    print('[0] Exit.')
    print(ROW)
    option = input('Option  ->  ')
    print(ROW)
  
    if int(option) not in range(3):
      print('Invalid option!')
      continue

    if option == '0':
      print('See you soon!')
      print(ROW)
      break
    
    if option == '1':
      print('SNOW 3G multiplication.')
      print(ROW)
      print('Please, enter the two bytes to be multiplied.')
      byte1 = input('Byte 1  ->  ')
      byte2 = input('Byte 2  ->  ')
      print(ROW)
      print('Result: ' + mult(byte1, byte2, SNOW3G_BYTE))
    
    if option == '2':
      print('AES multiplication.')
      print(ROW)
      print('Please, enter the two bytes to be multiplied.')
      byte1 = input('Byte 1  ->  ')
      byte2 = input('Byte 2  ->  ')
      print(ROW)
      print('Result: ' + mult(byte1, byte2, AES_BYTE))
      
  return

if __name__ == '__main__':
  main()