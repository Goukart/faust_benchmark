#! /usr/bin/python3
  
import os
import re
import sys


def main(args):
    if len(args) > 3:
        print("Too many arguments given")
        quit()
    elif len(args) < 2:
        print("No expression given")
        quit()

    # begin at 1, because first argument is script itself
    try:
        regex = re.compile(args[1])
    except re.error:
        print("Expression not valid")
        exit()
    print(f"Loading all files matching expression [{regex.pattern}]\n")

    filtered = []
    for entry in os.listdir("./"):
        if regex.match(entry):
            filtered.append(entry)
    print("here are the filtered files:")
    print(f"{filtered}\n")

  
if __name__ == '__main__':
    main(sys.argv)
