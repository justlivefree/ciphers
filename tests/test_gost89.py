from ciphers.gost89 import GOST89

plaintext = 'The quick brown fox jumps over the lazy dog'
key = 'password' * 4

gost89_cipher = GOST89()
encrypted_text = gost89_cipher.encrypt(plaintext, key)
decrypted_text = gost89_cipher.decrypt(encrypted_text, key)

print(encrypted_text)
print(decrypted_text)
