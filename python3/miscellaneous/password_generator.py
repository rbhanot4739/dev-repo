from random import SystemRandom
import os
import string


def generate_password(rand):
    """ function to generate random secure password """
    letters = string.ascii_letters + string.digits + string.punctuation
    count = 0
    while count < 15:
        num = rand.randint(0, 128)
        char = chr(num)
        if char in letters:
            print(char, end='')

            count += 1


if __name__ == '__main__':
    os.system('clear')
    SR = SystemRandom()
    generate_password(SR)
    print('\n')
