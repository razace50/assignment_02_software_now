
# ================= SHIFT FUNCTION =================
def shift_char(ch, shift, direction, base):
    return chr(((ord(ch) - ord(base) + direction * shift) % 26) + ord(base))


# ================= ENCRYPTION =================
def encrypt_text(text, shift1, shift2):
    result = ""

    for ch in text:

        # -------- lowercase --------
        if 'a' <= ch <= 'z':
            pos = ord(ch) - ord('a')

            if pos < 13:  # a–m
                result += shift_char(ch, shift1 * shift2, +1, 'a')
            else:         # n–z
                result += shift_char(ch, shift1 + shift2, -1, 'a')

        # -------- uppercase --------
        elif 'A' <= ch <= 'Z':
            pos = ord(ch) - ord('A')

            if pos < 13:  # A–M
                result += shift_char(ch, shift1, -1, 'A')
            else:         # N–Z
                result += shift_char(ch, shift2 ** 2, +1, 'A')

        # -------- others --------
        else:
            result += ch

    return result


# ================= DECRYPTION =================
def decrypt_text(text, shift1, shift2):
    result = ""

    for ch in text:

        # -------- lowercase --------
        if 'a' <= ch <= 'z':
            pos = ord(ch) - ord('a')

            if pos < 13:
                result += shift_char(ch, shift1 * shift2, -1, 'a')
            else:
                result += shift_char(ch, shift1 + shift2, +1, 'a')

        # -------- uppercase --------
        elif 'A' <= ch <= 'Z':
            pos = ord(ch) - ord('A')

            if pos < 13:
                result += shift_char(ch, shift1, +1, 'A')
            else:
                result += shift_char(ch, shift2 ** 2, -1, 'A')

        # -------- others --------
        else:
            result += ch

    return result


# ================= FILE OPERATIONS =================
def encrypt_file(s1, s2):
    with open("raw_text.txt", "r", encoding="utf-8") as f:
        text = f.read()

    encrypted = encrypt_text(text, s1, s2)

    with open("encrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(encrypted)

    print("Encryption complete ✔")


def decrypt_file(s1, s2):
    with open("encrypted_text.txt", "r", encoding="utf-8") as f:
        text = f.read()

    decrypted = decrypt_text(text, s1, s2)

    with open("decrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(decrypted)

    print("Decryption complete ✔")


# ================= VERIFICATION =================
def verify():
    with open("raw_text.txt", "r", encoding="utf-8") as f:
        original = f.read()

    with open("decrypted_text.txt", "r", encoding="utf-8") as f:
        decrypted = f.read()

    if original == decrypted:
        print("Verification successful ✔")
    else:
        print("Verification failed ❌")


# ================= MAIN =================
def main():
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    encrypt_file(shift1, shift2)
    decrypt_file(shift1, shift2)
    verify()


main()