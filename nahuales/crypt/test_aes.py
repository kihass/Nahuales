from hashlib import sha256
import pyaes

# A 256 bit (32 byte) key
#key = "12345678901234567890123456789012"
#key = b"12345678901234567890123456789012"
key = sha256(b"Llave")
key = key.digest()
#plaintext = b"Mi mensaje"
plaintext = bytes([x for x in range(256)])

# key must be bytes, so we convert it
#key = key.encode('utf-8')

aes = pyaes.AESModeOfOperationCTR(key)
#ciphertext = aes.encrypt(plaintext.decode('utf-8'))
ciphertext = aes.encrypt(plaintext.decode('latin1'))
#ciphertext = aes.encrypt(plaintext.decode('base64', 'strict'))
#ciphertext = aes.encrypt(plaintext.decode('ascii'))

print('len', len(ciphertext))

# DECRYPTION
# CRT mode decryption requires a new instance be created
aes = pyaes.AESModeOfOperationCTR(key)

# decrypted data is always binary, need to decode to plaintext
#decrypted = aes.decrypt(ciphertext).decode('utf-8')
decrypted = aes.decrypt(ciphertext)

# True
if decrypted == plaintext:
	print("key:", key.hex(), "len", len(key))
	print("plaintext:", plaintext, "len", len(plaintext))
	
	print ("ciphertext:", ciphertext.hex(), "len", len(ciphertext))

	print("decrypted:", decrypted, "len", len(decrypted))

else:
	print('Error')