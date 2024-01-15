from ciphers.md5 import MD5

plaintext = 'The quick brown fox jumps over the lazy dog'

md5_hash = MD5()
encrypted_text = md5_hash.encrypt(plaintext)
compare = md5_hash.compare(plaintext, encrypted_text)
