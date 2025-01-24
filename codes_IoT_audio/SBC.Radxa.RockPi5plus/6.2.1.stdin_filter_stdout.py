#!/usr/bin/python3
import re
from whisper_filter import *

def main():
    try:
        while True:
            user_input = input("")
            result = whisper_filter(user_input)
            if result!=None:
                print(result)
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
    