
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import sys
import os

encrypted = sys.argv[1]

f = open(f"{encrypted}.encrypted", "rb")
encrypted = f.read()
f.close()

with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password = None,
        backend = default_backend()
    )

originalMessage = private_key.decrypt(
    encrypted,
    padding.OAEP(
        mgf = padding.MGF1(algorithm=hashes.SHA256()),
        algorithm = hashes.SHA256(),
        label = None
    )
)

print(originalMessage.decode("UTF-8"))