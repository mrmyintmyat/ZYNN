
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_file():
    key = generate_key()
    input_file = input('    \033[32mEnter the path to the file you want to encrypt:\033[0m ')
    output_file = input('    \033[32mEnter the path for the encrypted file:\033[0m ')

    input_file = input_file.strip('"')
    output_file = output_file.strip('"')
    with open(input_file, 'rb') as f:
        data = f.read()

    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted_data)

    with open('tools/keys/keys.txt', 'a') as key_file:
         key_file.write(f"{output_file}'s key = {key.decode('utf-8')}\n")

    print('it is your key:' + key.decode('utf-8'))
    print('You can look in keys/keys.txt')
    print('    \033[32m successfully.\033[0m')

def decrypt_file():
    key = input('    \033[32mEnter your key:\033[0m ')
    input_file = input('    \033[32mEnter the path to the file you want to decrypt:\033[0m ')
    output_file = input('    \033[32mEnter the path for the decrypted file:\033[0m ')

    input_file = input_file.strip('"')
    output_file = output_file.strip('"')
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()

    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)

    with open(output_file, 'wb') as f:
        f.write(decrypted_data)
    print('    \033[32m successfully.\033[0m')
