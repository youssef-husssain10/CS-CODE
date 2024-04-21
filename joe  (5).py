import random  # Importing the random module for generating random numbers.
import math  # Importing the math module for mathematical functions.
import time  # Importing the time module for time-related operations.

def is_prime(n):
    if n <= 1:  # If the number is less than or equal to 1, it's not prime.
        return False
    elif n <= 3:  # If the number is 2 or 3, it's prime.
        return True
    elif n % 2 == 0 or n % 3 == 0:  # If the number is divisible by 2 or 3, it's not prime.
        return False
    i = 5
    while i * i <= n:  # Checking divisibility up to square root of n.
        if n % i == 0 or n % (i + 2) == 0:  # If n is divisible by i or (i+2), it's not prime.
            return False
        i += 6
    return True

def generate_large_prime(bits):
    while True:
        p = random.randint(2**(bits-1), 2**bits)  # Generating a random prime number in the specified range.
        q = random.randint(2**(bits-1), 2**bits)  # Generating another random prime number.
        if is_prime(p) and is_prime(q):  # Checking if both generated numbers are prime.
            return p , q

def gcd(a, b):
    while b != 0:
        a, b = b, a % b  # Finding the greatest common divisor using Euclid's algorithm.
    return a

def extended_gcd(a, b):
    if a == 0:  # Base case: if a is 0, return (b, 0, 1).
        return (b, 0, 1)
    else:
        gcd_val, x, y = extended_gcd(b % a, a)  # Recursive call to find gcd and coefficients.
        return (gcd_val, y - (b // a) * x, x)

def generate_keys(bits):
    p,q = generate_large_prime(bits)  # Generating two large prime numbers.
    n = p * q  # Computing the modulus.
    phi = (p - 1) * (q - 1)  # Computing Euler's totient function.
    while True:
        e = random.randrange(2, n)  # Randomly choosing an encryption exponent.
        if gcd(e, phi) == 1:  # Checking if e and phi(n) are coprime.
            break
    gcd_val, x, y = extended_gcd(e, phi)  # Calculating the decryption exponent.
    d = x
    if d < 0:  # Ensuring d is positive.
        d += phi
    return ((e, n), (d, n))  # Returning public and private keys.

def encrypt(message, public_key):
    e, n = public_key
    encrypted_msg = pow(message, e, n)  # Encrypting the message using modular exponentiation.
    return encrypted_msg

def decrypt(encrypted_msg, private_key):
    d, n = private_key
    decrypted_msg = pow(encrypted_msg, d, n)  # Decrypting the message using modular exponentiation.
    return decrypted_msg

def factorize_modulus(n):
    for i in range(2, int(math.sqrt(n)) + 1):  # Iterating from 2 to square root of n.
        if n % i == 0:  # If n is divisible by i, i is a factor of n.
            return i, n // i  # Returning the factors.

def check(d, public_key, encrypted_message_c):
    e, n = public_key
    decrypted_message = pow(encrypted_message_c, d, n)  # Decrypting message using private exponent.
    return decrypted_message

def brute_force_private_exponent(public_key, encrypted_message_c):
    d = 2
    while True:
        decrypted_message = check(d, public_key, encrypted_message_c)  # Brute force decryption.
        if decrypted_message:  # If decryption is successful.
            return decrypted_message, d  # Return decrypted message and private exponent.
        d += 1

def main():
    print("RSA Encryption and Decryption\n")
    
    bits = int(input("Enter the number of bits for key generation: "))  # Input for key size in bits.

    start_time = time.time()  # Recording start time for key generation.
    public_key, private_key = generate_keys(bits)  # Generating public and private keys.
    end_time = time.time()  # Recording end time for key generation.
    print("\nKey Generation Time: {:.6f} millisec".format(end_time - start_time))  # Printing key generation time.
    print("\nPublic Key (e, n):", public_key)  # Printing public key.
    print("Private Key (d, n):", private_key)  # Printing private key.
    
    plaintext = int(input("\nEnter the Message: "))  # Input for the plaintext message.
    
    start_time = time.time()  # Recording start time for encryption.
    encrypted_msg = encrypt(plaintext, public_key)  # Encrypting the plaintext message.
    end_time = time.time()  # Recording end time for encryption.
    print("\nEncryption Time: {:.6f} millisec".format(end_time - start_time))  # Printing encryption time.
    print("\nEncrypted message:", encrypted_msg)  # Printing encrypted message.
    
    start_time = time.time()  # Recording start time for decryption.
    decrypted_msg = decrypt(encrypted_msg, private_key)  # Decrypting the encrypted message.
    end_time = time.time()  # Recording end time for decryption.
    print("\nDecryption Time: {:.6f} millisec".format(end_time - start_time))  # Printing decryption time.
    print("Decrypted message:", decrypted_msg)  # Printing decrypted message.
    
    n = public_key[1]  # Extracting the modulus from the public key.
    start_time = time.time()  # Recording start time for factorization.
    p, q = factorize_modulus(n)  # Factorizing the modulus.
    end_time = time.time()  # Recording end time for factorization.
    print("\nFactorization Time: {:.6f} millisec".format(end_time - start_time))  # Printing factorization time.
    print("Factorized Modulus (p, q):", (p, q))  # Printing factors of the modulus.
    
    start_time = time.perf_counter()  # Recording start time for brute force attack.
    encrypted_message_c = encrypt(plaintext, public_key)  # Encrypting the plaintext message again.
    private_exponent = brute_force_private_exponent(public_key, encrypted_message_c)  # Performing brute force attack.
    end_time = time.perf_counter()  # Recording end time for brute force attack.
    print("\nBrute Force Time: {:.6f} ms".format((end_time - start_time) * 1000))  # Printing brute force time.
    print("Private exponent d:", private_exponent)  # Printing private exponent.

if __name__ == "__main__":
    main()  # Calling the main function.


