#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 2023

@author: iluzioDev

This script implements a generator for GPS-L1C/A Codes.
"""
import re

LEFT_REGEX = '^1(( )*\+( )*x([0-9]+)?)+$'
RIGHT_REGEX = '^((x([0-9]+)?)( )*\+( )*)*1$'

def binary_to_polynomial(binary):
  """Converts a given binary to a polynomial.

  Args:
      binary (str): Binary to be converted.
      
  Returns:
      list | None: List of type and pows of polynomial in success, None in failure.
  """
  if type(binary) is not str:
    return None
  
  result = []
  for i, bit in enumerate(binary):
    if bit == '1' and i != len(binary) - 1:
      result.append('x' + str(len(binary) - i - 1))
    elif bit == '1':
      result.append('1')
  return result

def extract_exponents(polynomial):
  """Extracts the exponents of a given polynomial in a list.
  
  Args:
      polynomial (list): Polynomial to be checked.
      
  Returns:
      list | None: List of pows of polynomial in success, None in failure.
  """
  if type(polynomial) is not list:
    return None

  for i, pow in enumerate(polynomial):
    if i == 0:
      continue
    polynomial[i] = polynomial[i].replace('x', '')
  return polynomial

def format_polynomial(polynomial, left = True):
  """Formats a given polynomial to be used in the LFSR operation.

  Args:
      polynomial (re.Match): Polynomial to be checked.
      left (bool, optional): Indicates if polynomial is in left or right form. Defaults to True.

  Returns:
      list: List of type and pows of polynomial in success, None in failure.
  """
  if type(polynomial) is not re.Match and type(left) is not bool:
    return None
  
  polynomial = polynomial.string.replace(' ', '').split('+')
  if left:
    polynomial[0] = left
  else:
    polynomial.pop()
    polynomial.insert(0, left)
  
  polynomial = extract_exponents(polynomial)
  
  return polynomial  

def str_to_polynomial(polynomial):
  """Receives a polynomial in string format and converts it to a list.
  
  Args:
      polynomial (str): Polynomial to be checked.
      
  Returns:
      list | None: List of type and pows of polynomial in success, None in failure.
  """
  if type(polynomial) is not str:
    return None

  if re.search(LEFT_REGEX, polynomial) != None:
    polynomial = format_polynomial(re.search(LEFT_REGEX, polynomial))
  elif re.search(RIGHT_REGEX, polynomial) != None:
    polynomial = format_polynomial(re.search(RIGHT_REGEX, polynomial), False)
  else:
    return None

  return polynomial

def polynomial_to_str(polynomial):
  """Receives a polynomial in list format and converts it to a string.
  
  Args:
      polynomial (list): Polynomial to be checked.
      
  Returns:
      str | None: String of type and pows of polynomial in success, None in failure.
  """
  if type(polynomial) is not list:
    return None

  if polynomial[0]:
    str_pol = '1'
    for i in range(1, len(polynomial)):
      str_pol += ' + x' + polynomial[i]
  else:
    str_pol = ''
    for i in range(1, len(polynomial)):
      str_pol += 'x' + polynomial[i] + ' + '
    str_pol += '1'

  return str_pol

def xor(binary1, binary2):
  """Makes a XOR operation between two binary numbers.

  Args:
      binary1 (str): First binary to be used.
      binary2 (str): Second binary to be used.
      
  Returns:
      str | None: XOR result in success, None in failure.
  """
  if type(binary1) is not str or type(binary2) is not str:
    return None

  length = len(binary1) if len(binary1) > len(binary2) else len(binary2)
  binary1 = binary1.zfill(length)
  binary2 = binary2.zfill(length)

  result = ''
  for i in range(length):
    if binary1[i] == binary2[i]:
      result += '0'
    else:
      result += '1'
  return result

def calculate_feedback(sequence, polynomial):
  """Calculates the feedback of a given sequence and polynomial in a LFSR operation.

  Args:
      sequence (str): Sequence to be checked.
      polynomial (list): Primative polynomial to be used in the operation.
      
  Returns:
      str | None: Feedback of sequence in success, None in failure.
  """
  if type(sequence) is not str or type(polynomial) is not list:
    return None
  
  feedback = 0
  for i in polynomial[1:]:
    if (polynomial[0]):
      feedback ^= int(sequence[int(i) - 1], 2)
    else:
      feedback ^= int(sequence[len(sequence) - int(i)], 2)
  return bin(feedback)[-1]

def shift(sequence, polynomial):
  """Makes a Linear Feedback Shift Register (LFSR) operation in a given sequence.
     It supports both left and right shift.

  Args:
      sequence (str): Sequence to be shifted.
      polynomial (list): Primative polynomial to be used in the operation.

  Returns:
      str | None: Shifted sequence in success, None in failure.
  """
  if type(sequence) is not str or type(polynomial) is not list:
    return None

  feedback = calculate_feedback(sequence, polynomial)
  if (polynomial[0]):
    sequence = feedback + sequence[:-1]
  else:
    sequence = sequence[1:] + feedback

  return sequence, feedback