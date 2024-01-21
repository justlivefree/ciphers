from ciphers.rsa import RSA

plaintext = 'The quick brown fox jumps over the lazy dog'

r = RSA()
encrypted_text = r.encrypt(plaintext)
decrypted_text = r.decrypt(encrypted_text)

print(encrypted_text)
print(decrypted_text)
