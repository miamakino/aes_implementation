# Implementation of the AES algorithm

## How to run the implementation

1. Download the aes.py file
2. Open the terminal in directory containing the aes.py file
3. Run "python3 aes.py"
4. The code with first run the test vectors that were provided in the FIPS document. It will then allow the user to choose to encrypt a 16-byte message, decrypt a ciphertext, or exit. The user will have to save the key and ciphertext on their own to use for decrypting.

## Description of Code

The code was written based on this [FIPS document](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=901427), additionally with the help of [this animation](https://formaestudio.com/rijndaelinspector/archivos/Rijndael_Animation_v4_eng-html5.html). The implementation includes both encryption and decryption and allow for the use of keys of 128, 192, and 256 bits.

Main AES Functions: 
1. sub_bytes: Replaces each byte in the internal state using the S-box. During decryption, the inverse S-box is used to reverse this operation. 

2. shift_rows: Shifts the rows of the internal state by different offsets. During decryption the shifts are performed in the opposite direction. 

3. galois_mult: Transforms the bytes in each column using mathematical operations in a finite field. 

4. mix_columns: Transforms the bytes in each column using mathematical operations in a finite field. 

5. add_round_key: Combines the internal state with a round key using the XOR operation.

6. key_expansion: Generates the round keys required for encryption and decryption from the original secret key. 

Helper functions: 

7. galois_mult: Performs multiplication in the finite Galois field (GF(2^8)). Used in the mix_columns function where the state bytes mustbe multipled by specified constants. 

8. rcon: generates the round constants that are required during key expansion

The operations are then combined in the AES class. The constructor prepares the round keys and the encrypt() and decrypt() methods perform the corresponding AES operations on a single block of data (16 bytes).

The test vectors function checks the results against values in Appendix C for AES-128, AES-192, and AES-256.


## Design choices

- In the FIPS 197 documentation, the forward and inverse functions are described separately (ex. SubBytes() and InvSubBytes()). However, in my implementation I combined each pair into a single function by adding an inverse Boolean parameter. This was done to reduce duplicated code and to keep the code simple. 

- Padding was omitted to keep the implementation simple. Because AES operates on blocks of 16 bytes, the program requires the input to by exactly 16 bytes long. This is something that could be worked on for further improvement of functionality.


