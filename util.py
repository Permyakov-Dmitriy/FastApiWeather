from random import randint


def genToken():
    out = ''
    for i in range(8):
        out += chr(randint(48, 57)) if randint(0, 1) else chr(randint(65, 90)) if randint(0, 1) else chr(randint(97, 122))
    
    return out