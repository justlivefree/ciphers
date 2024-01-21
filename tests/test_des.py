from ciphers.des import DES

plaintext = 'The quick brown fox jumps over the lazy dog'
key = 'password'

des_cipher = DES()
encrypted_text = des_cipher.encrypt(plaintext, key)
decrypted_text = des_cipher.decrypt(encrypted_text, key)

print(encrypted_text)
print(decrypted_text)
