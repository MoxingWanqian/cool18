import os
import sys

cwd = os.path.dirname(sys.argv[0])

class CMD:

    def __init__(self):
        while True:
            command = input('> ').split(' ')
            if command[0] in ['quit', 'quit()', 'exit', 'exit()']:
                break
            elif command[0] == 'help':
                pass
            elif command[0] == 'setting':
                pass
            elif command[0] == 'search':
                pass
            elif command[0] == 'download':
                pass
            elif command[0] == 'update':
                pass
        
    def help(self, command:list):
        pass

    def search(self, command:list):
        pass

    def download(self, command:list):
        pass

    def update(self, command:list):
        pass

if __name__ == '__main__':
    cmd = CMD()
    