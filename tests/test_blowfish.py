from ciphers.blowfish import Blowfish

plaintext = 'The quick brown fox jumps over the lazy dog'
key = 'password'

blow_fish = Blowfish()
encrypted_text = blow_fish.encrypt(plaintext, key)
decrypted_text = blow_fish.decrypt(encrypted_text, key)

