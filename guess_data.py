from random import randint

data = randint(5,10)

print 'Guess what i think?'
answer = input()
while data != answer:
    if answer > data:
        print 'too big,please guess again:'
        answer = input()

    if answer < data:
        print 'too small,please guess again:'
        answer = input()
print 'BINGO!'
