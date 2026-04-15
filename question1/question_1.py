def encrypt_char(ch, shift1, shift2):
    # Lowercase letters
    if 'a' <= ch <= 'm':
        shift = shift1 * shift2
        return chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))

    elif 'n' <= ch <= 'z':
        shift = shift1 + shift2
        return chr((ord(ch) - ord('a') - shift) % 26 + ord('a'))

    # Uppercase letters
    elif 'A' <= ch <= 'M':
        shift = shift1
        return chr((ord(ch) - ord('A') - shift) % 26 + ord('A'))

    elif 'N' <= ch <= 'Z':
        shift = shift2 ** 2
        return chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))

    # Other characters unchanged
    return ch


def decrypt_char(ch, shift1, shift2):
    # Reverse lowercase letters
    if 'a' <= ch <= 'm':
        shift = shift1 * shift2
        return chr((ord(ch) - ord('a') - shift) % 26 + ord('a'))

    elif 'n' <= ch <= 'z':
        shift = shift1 + shift2
        return chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))

    # Reverse uppercase letters
    elif 'A' <= ch <= 'M':
        shift = shift1
        return chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))

    elif 'N' <= ch <= 'Z':
        shift = shift2 ** 2
        return chr((ord(ch) - ord('A') - shift) % 26 + ord('A'))

    return ch


def encrypt_file(shift1, shift2):
    with open("raw_text.txt", "r") as file:
        text = file.read()

    encrypted = ""
    for ch in text:
        encrypted += encrypt_char(ch, shift1, shift2)

    with open("encrypted_text.txt", "w") as file:
        file.write(encrypted)

    print("Encryption completed successfully.")


def decrypt_file(shift1, shift2):
    with open("encrypted_text.txt", "r") as file:
        text = file.read()

    decrypted = ""
    for ch in text:
        decrypted += decrypt_char(ch, shift1, shift2)

    with open("decrypted_text.txt", "w") as file:
        file.write(decrypted)

    print("Decryption completed successfully.")


def verify_decryption():
    with open("raw_text.txt", "r") as file1:
        original = file1.read()

    with open("decrypted_text.txt", "r") as file2:
        decrypted = file2.read()

    if original == decrypted:
        print("Verification successful: Decryption matches original file.")
    else:
        print("Verification failed: Files do not match.")


def main():
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    encrypt_file(shift1, shift2)
    decrypt_file(shift1, shift2)
    verify_decryption()


main()