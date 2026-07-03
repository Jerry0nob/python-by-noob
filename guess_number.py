import random

def random_value():
    return random.randint(1,1000)

guess = random_value()

tries = [1, 2, 3]

while len(tries) > 0:
    print('You have ' + str(tries) + ' tries left')
    guessCorrect = int(input('Guess the number: '))
    if guessCorrect == guess:
        print('Correct, you win!')
        print(tries)
        break
    elif guessCorrect > guess:
        print('You guessed too high!')
        tries.remove(tries[-1])
        print(tries)
    elif guessCorrect < guess:
        print('You guessed too low!')
        tries.remove(tries[-1])
        print(tries)
if len(tries) > 0:
    print(tries)
else:
    print('Game over!')










