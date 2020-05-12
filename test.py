import random
from random import choice


# x = 12
# y = 4
x = 9 + 5
y = 3 - 5


leading = 40 - x - 10
inter = x + y

M = ((leading + 5) * 10 + (leading + 10 + x + y + 15) * 30) / 40

block = '█'

def getNumber(size):
    chars = '0123456789'
    return ''.join([choice(chars) for x in range(size)])

def getChars(size):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ .'
    return ''.join([choice(chars) for x in range(size)])

def getString():
    return ' ' * leading + getNumber(10) + ' ' * inter + getChars(30)

out = 80 - len(getString())
print('X={:02},Y={:02},M={:3.1f}'.format(x, y, M))
print('123456789 '*8 )#+ '|')
for i in range(20):
    print(getString() + ' ' * 0 )#+ '|')
