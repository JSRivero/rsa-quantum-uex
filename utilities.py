from math import gcd, fmod

import numpy as np

def factorization(n:int):
    '''
    Function to factorize number. This is the function to be replaced by Shor's algorithm
    
    Input:
        - n (int): Number to factorize
    
    Output (either one or the other, not both):
        - factor (int): n itself if is prime
        - factors (list of ints): list containing the factors of n
    '''

    factors = []

    def get_factor(n):
        x_fixed = 2
        cycle_size = 2
        x = 2
        factor = 1

        while factor == 1:
            for _ in range(cycle_size):
                if factor > 1: break
                x = (x * x + 1) % n
                factor = gcd(x - x_fixed, n)

            cycle_size *= 2
            x_fixed = x

        return factor

    while n > 1:
        next = get_factor(n)
        factors.append(next)
        n //= next

    return factors


def coprime(a:int, b:int):
    '''
    Function to tell whether a and b are coprime.

    Input:
        - a (int)
        - b (int)
    
    Output:
        - True or False
    '''
    return gcd(a, b) == 1


def obtain_keys(p:int, q:int):

    '''
    Calculates the public and private keys when the two primes are p and q.

    Input:
        - p (int): First prime number of the RSA algorithm
        - q (int): Second prime number of the RSA algorithm
    
    Output:
        - e (int): First part of the public key.
        - d (int): First part of the private key.
        - n (int): Product of p and q. Second part of both private and public key.
    '''

    n = p*q
    phin = (p-1)*(q-1)

    begin = np.random.randint(2, phin)

    list_numbers = list(range(begin, phin)) + list(range(2, begin))

    # Choose the first coprime number with x to find e
    for x in list_numbers:
        if coprime(x, phin):
            e = x
            break
    
    # Choose the modulo phin inverse number of e: d such that d*e = 1 mod phin
    k = 2
    # d = ((k * phin) +1) // e
    for x in range(2, phin):
        if x*e % phin == 1:
            d = x
            break
    
    return e, d, n

###################################################################################
###################################################################################

###### ESTO FUNCIONA PORQUE COGE SIEMPRE EL PRIMER e tal que gcd(e, p*q) = 1 ######

###################################################################################
###################################################################################

def get_public_key(p, q):
    '''
    Gets the public key when the two primes are p and q.

    Input:
        - p (int): First prime number of the RSA algorithm
        - q (int): Second prime number of the RSA algorithm
    
    Output:
        - public_key_e (int): First number of the public key
        - public_key_n (int): Product of p and q, second number of the public key
    '''
    public_key_e, _, public_key_n = obtain_keys(p, q)
    return public_key_e, public_key_n



def get_private_key(p, q):
    '''
    Gets the private key when the two primes are p and q.

    Input:
        - p (int): First prime number of the RSA algorithm
        - q (int): Second prime number of the RSA algorithm
    
    Output:
        - private_key_d (int): First number of the private key
        - private_key_n (int): Product of p and q, second number of the private key
    '''
    _, private_key_d, private_key_n = obtain_keys(p, q)
    return private_key_d, private_key_n


def encrypt_message(message:str, key_e:int, key_n:int, dic_codify=None):
    '''
    Encrypting the message. 

    Input:
        - message (str): message to encrypt.
        - key_e (int): first part of the public key.
        - key_n (int): second part of the public key.
        - dic_codify (dictionary): When a different codification is wanted. DO NOT TOUCH
    
    Ouput:
        - encrypted_message (str): string with numbers separated by spaces with the encrypted message
    '''

    if dic_codify is None:
        transformed_message = [ord(c) for c in message]
    else:
        transformed_message = [dic_codify[c] for c in message.lower()]
    

    encrypted_message = [k**key_e % key_n for k in transformed_message]

    return '-'.join([str(x) for x in encrypted_message])



def decrypt_message(message:str, key_d:int, key_n:int, dic_decodify=None):
    '''
    Decrypting the message. 

    Input:
        - message (str): string with numbers separated by spaces with the encrypted message.
        - key_d (int): first part of the private key.
        - key_n (int): second part of the private key.
        - dic_decodify (dictionary): When a different codification is wanted. DO NOT TOUCH
    
    Ouput:
        - decrypted_message (str): Decripted message.
    '''

    message_numbers = [int(x) for x in message.split('-')]

    decrypted_message = [k**key_d % key_n for k in message_numbers]


    if dic_decodify is None:
        transformed_message = [chr(c) for c in decrypted_message]
    else:
        transformed_message = [dic_decodify[c] for c in decrypted_message]


    return ''.join([str(k) for k in transformed_message])