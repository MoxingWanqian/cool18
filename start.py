import os
import sys

print(os.path.dirname(sys.argv[0]))

class CMD:

    def __init__(self):
        while True:
            command = input('> ')
            if command in ['quit', 'quit()', 'exit', 'exit()']:
                break
            elif command.split(' ')[0] == 'search':
                pass

if __name__ == '__main__':
    cmd = CMD()
    