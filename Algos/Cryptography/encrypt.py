
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import sys

message = sys.argv[1]

with open("public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend = default_backend()
    )

encrypted = public_key.encrypt(
    message.encode('UTF-8'),
    padding.OAEP(
        mgf = padding.MGF1(algorithm=hashes.SHA256()),
        algorithm = hashes.SHA256(),
        label = None
    )
)

print(f"{message} -> {encrypted}\n")
f = open(f'{message}.encrypted', 'wb')
f.write(encrypted)
f.close()