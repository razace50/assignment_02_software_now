def encrypt_char(ch, shift1, shift2):
    # lowercase letters
    if 'a' <= ch <= 'm':
        return chr((ord(ch) - ord('a') + shift1 * shift2) % 26 + ord('a'))
    elif 'n' <= ch <= 'z':
        return chr((ord(ch) - ord('a') - (shift1 + shift2)) % 26 + ord('a'))

    # uppercase letters
    elif 'A' <= ch <= 'M':
        return chr((ord(ch) - ord('A') - shift1) % 26 + ord('A'))
    elif 'N' <= ch <= 'Z':
        return chr((ord(ch) - ord('A') + shift2 ** 2) % 26 + ord('A'))

    # other characters remain unchanged
    return ch


def decrypt_char(ch, shift1, shift2):
    # reverse lowercase letters
    if 'a' <= ch <= 'm':
        return chr((ord(ch) - ord('a') - shift1 * shift2) % 26 + ord('a'))
    elif 'n' <= ch <= 'z':
        return chr((ord(ch) - ord('a') + (shift1 + shift2)) % 26 + ord('a'))

    # reverse uppercase letters
    elif 'A' <= ch <= 'M':
        return chr((ord(ch) - ord('A') + shift1) % 26 + ord('A'))
    elif 'N' <= ch <= 'Z':
        return chr((ord(ch) - ord('A') - shift2 ** 2) % 26 + ord('A'))

    return ch


def encrypt_file(shift1, shift2):
    with open("raw_text.txt", "r") as file:
        text = file.read()

    encrypted_text = "".join(encrypt_char(ch, shift1, shift2) for ch in text)

    with open("encrypted_text.txt", "w") as file:
        file.write(encrypted_text)

    print("Encryption complete → encrypted_text.txt")


def decrypt_file(shift1, shift2):
    with open("encrypted_text.txt", "r") as file:
        text = file.read()

    decrypted_text = "".join(decrypt_char(ch, shift1, shift2) for ch in text)

    with open("decrypted_text.txt", "w") as file:
        file.write(decrypted_text)

    print("Decryption complete → decrypted_text.txt")


def verify_files():
    with open("raw_text.txt", "r") as file1:
        original = file1.read()

    with open("decrypted_text.txt", "r") as file2:
        decrypted = file2.read()

    if original == decrypted:
        print("✅ Verification successful: Decryption matches original")
    else:
        print("❌ Verification failed: Files do not match")


# Main program
def main():
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    encrypt_file(shift1, shift2)
    decrypt_file(shift1, shift2)
    verify_files()


main()