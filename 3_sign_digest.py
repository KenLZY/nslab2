# Signed Message Digest
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import traceback
from termcolor import colored

# Generate 1024 bit asymmetric keys
# TODO: Task 3-1
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=1024,
)

# Extract the RSAPublicKey instance
# TODO: Task 3-2
public_key = private_key.public_key()


def enc_digest(filename):
    # Open and read the file to encrypt as bytes
    with open(filename, "rb") as fp:
        file_data = fp.read()

    print("=============================================================")
    print(f"\nThis test is for {filename}\n")

    # Create a Hash instance
    # TODO: Task 3-3
    hash_function = hashes.Hash(hashes.SHA256())
    hash_function.update(file_data)

    # Hash the file data to produce the message digest
    # TODO: Task 3-4
    message_digest_bytes = hash_function.finalize()

    print(f"This is the hashed file data (bytes):\n{message_digest_bytes}\n")
    # print(f"hash_bytes:\n{message_digest_bytes}\n")

    # Encrypt the message digest
    # TODO: Task 3-5
    encrypted_message_digest_bytes = public_key.encrypt(
        message_digest_bytes,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # Decrypt the message digest back
    # TODO: Task 3-6
    decrypted_message_digest_bytes = private_key.decrypt(
        encrypted_message_digest_bytes,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    try:
        print(
            "Original hash bytes:\n"
            + base64.b64encode(message_digest_bytes).decode("utf8")
            + "\n"
            + f"Length: {len(message_digest_bytes)}\n"
        )
        print(
            "Encrypted hash bytes:\n"
            + base64.b64encode(encrypted_message_digest_bytes).decode("utf8")
            + "\n"
            + f"Length: {len(encrypted_message_digest_bytes)}\n"
        )
        print(
            "Decrypted hash bytes:\n"
            + base64.b64encode(decrypted_message_digest_bytes).decode("utf8")
            + "\n"
            + f"Length: {len(decrypted_message_digest_bytes)}\n"
        )
    except:
        print("Task 3-1 to 3-6 not implemented")


def sign_digest(filename):
    # Open and read the file to sign as bytes
    with open(filename, "rb") as fp:
        file_data = fp.read()

    # Sign the message digest to produce a signature
    # TODO: Task 3-7
    signature = private_key.sign(
        file_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )

    try:
        print(f"Original data bytes length: {len(file_data)} bytes")
        print(f"Signed message digest length: {len(signature)} bytes")
        print("Signed bytes: " + base64.b64encode(signature).decode("utf8"))
    except:
        print("Task 3-7 not implemented")

    try:
        # Verify the authenticity of the signed digest using the public_key
        # TODO: Task 3-8
        public_key.verify(
            signature,
            file_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        # raise Exception("Task 3-8 not implemented")
        print(colored("======= SIGNATURE VERIFIED =======", "yellow"))
    except Exception as e:
        traceback.print_exc()
        print(colored("======= INVALID SIGNATURE =======", "red"))


if __name__ == "__main__":
    # enc_digest("original_files/shorttext.txt")
    # enc_digest("original_files/longtext.txt")
    sign_digest("original_files/shorttext.txt")
    sign_digest("original_files/longtext.txt")
