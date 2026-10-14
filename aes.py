Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

InvSbox = tuple(Sbox.index(x) for x in range(256))


def sub_bytes(state, inverse=False):
    if inverse:
        for i, value in enumerate(state):
            state[i] = InvSbox[value]
    else:
        for i, value in enumerate(state):
            state[i] = Sbox[value]


def shift_rows(state, inverse=False):
    orig_state = state[:]
    for row in range(4):
        row_values = [orig_state[4 * column + row] for column in range(4)]
        if inverse:
            row_values = row_values[-row:] + row_values[:-row]
        else:
            row_values = row_values[row:] + row_values[:row]
        for column in range(4):
            state[4 * column + row] = row_values[column]

def galois_mult(l, r):
    result = 0
    for _ in range(8):
        if r & 1:
            result ^= l
        l = ((l << 1) ^ (0x1B if l & 0x80 else 0)) & 0xFF
        r >>= 1
    return result
    

def mix_columns(state, inverse=False):
    coefficients = (14, 11, 13, 9) if inverse else (2, 3, 1, 1)
    for column in range(4):
        offset = 4 * column
        a = state[offset:offset + 4]
        state[offset:offset + 4] = [
            galois_mult(coefficients[0], a[0]) ^ galois_mult(coefficients[1], a[1]) ^ galois_mult(coefficients[2], a[2]) ^ galois_mult(coefficients[3], a[3]),
            galois_mult(coefficients[3], a[0]) ^ galois_mult(coefficients[0], a[1]) ^ galois_mult(coefficients[1], a[2]) ^ galois_mult(coefficients[2], a[3]),
            galois_mult(coefficients[2], a[0]) ^ galois_mult(coefficients[3], a[1]) ^ galois_mult(coefficients[0], a[2]) ^ galois_mult(coefficients[1], a[3]),
            galois_mult(coefficients[1], a[0]) ^ galois_mult(coefficients[2], a[1]) ^ galois_mult(coefficients[3], a[2]) ^ galois_mult(coefficients[0], a[3]),
        ]   


def add_round_key(state, round_key):
    for i, value in enumerate(round_key):
        state[i] ^= value


class AES:
    def __init__(self, key):
        if len(key) not in (16, 24, 32):
            raise ValueError("Key must be 16, 24, or 32 bytes long.")
        self.nk = len(key) // 4
        self.rounds = self.nk + 6
        self.round_keys = self.key_expansion(key)   
    
    def rcon(self, index):
        val = 1
        for _ in range(1, index):
            val = galois_mult(val, 2)
        return val

    def key_expansion(self, key):
        words = [list(key[i:i + 4]) for i in range(0, len(key), 4)]
        needed_words = 4 * (self.rounds + 1)
        for i in range(self.nk, needed_words):
            temp = words[i - 1][:]
            if i % self.nk == 0:
                temp = [Sbox[value] for value in temp[1:] + temp[:1]] 
                temp[0] ^= self.rcon(i // self.nk)
            elif self.nk > 6 and i % self.nk == 4:
                temp = [Sbox[value] for value in temp]
            words.append([words[i - self.nk][j] ^ temp[j] for j in range(4)])
        expanded = bytes(value for word in words for value in word)
        return [expanded[16 * round_number:16 * (round_number + 1)] for round_number in range(self.rounds + 1)]


    def encrypt(self, plaintext):
        if len(plaintext) != 16:
            raise ValueError("Plaintext must be 16 bytes long.")
        state = list(plaintext)
        add_round_key(state, self.round_keys[0])
        for round_number in range(1, self.rounds):
            sub_bytes(state)
            shift_rows(state)
            mix_columns(state)
            add_round_key(state, self.round_keys[round_number])
        sub_bytes(state)
        shift_rows(state)
        add_round_key(state, self.round_keys[self.rounds])
        return bytes(state)

    def decrypt(self, ciphertext):
        if len(ciphertext) != 16:
            raise ValueError("Ciphertext must be 16 bytes long.")
        state = list(ciphertext)
        add_round_key(state, self.round_keys[self.rounds])
        for round_number in range(self.rounds - 1, 0, -1):
            shift_rows(state, inverse = True)
            sub_bytes(state, inverse = True)
            add_round_key(state, self.round_keys[round_number])
            mix_columns(state, inverse = True)
        shift_rows(state, inverse = True)
        sub_bytes(state, inverse = True)
        add_round_key(state, self.round_keys[0])
        return bytes(state)
    
def test_vectors():
    #Appendix C - example vectors for testing.
    plaintext = bytes.fromhex("00112233445566778899aabbccddeeff")
    vectors = (
        ("000102030405060708090a0b0c0d0e0f", "69c4e0d86a7b0430d8cdb78070b4c55a"),
        ("000102030405060708090a0b0c0d0e0f1011121314151617", "dda97ca4864cdfe06eaf70a0ec0d7191"),
        ("000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f", "8ea2b7ca516745bfeafc49904b496089"),
    )
    for key_hex, ciphertext_hex in vectors:
        cipher = AES(bytes.fromhex(key_hex))
        ciphertext = bytes.fromhex(ciphertext_hex)
        assert cipher.encrypt(plaintext) == ciphertext
        assert cipher.decrypt(ciphertext) == plaintext

def main():
    test_vectors()
    print("\nFIPS-197 AES-128, AES-192, and AES-256 tests passed.")

    while True:
        print("\n1. Encrypt a 16-byte message block")
        print("2. Decrypt a 16-byte ciphertext block")
        print("3. Exit")
        choice = input("\nChoose an option: ").strip()

        try:
            if choice == "1":
                plaintext = bytes.fromhex(input("Enter plaintext as 32 hex characters (16 bytes): ").strip())
                if len(plaintext) != 16:
                    print(f"Error: your input is {len(plaintext)} bytes; it must be exactly 16 bytes.")
                    continue

                key_hex = input("Enter AES key in hex (32, 48, or 64 hex characters): ").strip()
                key = bytes.fromhex(key_hex)
                cipher = AES(key)
                ciphertext = cipher.encrypt(plaintext)
                print("Ciphertext (hex):", ciphertext.hex())
                print("\nSave the key and ciphertext to decrypt the message.")
            elif choice == "2":
                key = bytes.fromhex(input("Enter AES key in hex: ").strip())
                ciphertext = bytes.fromhex(input("Enter ciphertext as 32 hex characters (16 bytes): ").strip())
                plaintext = AES(key).decrypt(ciphertext)
                print("Decrypted bytes (hex):", plaintext.hex())
            elif choice == "3":
                print("Exiting.")
                break
            else:
                print("\nPlease choose 1, 2, or 3.")
        except ValueError as error:
            print("Error:", error)

    

if __name__ == "__main__":
    main()

    
    