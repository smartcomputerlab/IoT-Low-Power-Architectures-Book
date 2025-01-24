# whisper_filter
import re
import os

def whisper_filter(input_string):
    pattern = bytes.fromhex("201b5b324b0d20").decode('latin1')
    start_index = input_string.rfind(pattern)
    if start_index == -1:
        return ""
    result=input_string[start_index+7:]  # starting after the token
    if result[0:1]!="[" and result[0:1]!="(" and result[0:1]!=">":
        return result
    