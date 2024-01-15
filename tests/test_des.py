from ciphers.des import DESCipher

plaintext = 'The quick brown fox jumps over the lazy dog'
key = 'password'

des_cipher = DESCipher()
encrypted_text = des_cipher.encrypt(plaintext, key)
decrypted_text = des_cipher.decrypt(encrypted_text, key)
