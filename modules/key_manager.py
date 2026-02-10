"""
Key Manager Module
Fungsi: Generate RSA key pair untuk enkripsi symmetric key
"""

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os

class KeyManager:
    def __init__(self, key_size=2048):
        """
        Initialize key manager
        key_size: RSA key size (default 2048 bit)
        """
        self.key_size = key_size
        self.private_key = None
        self.public_key = None
        
    def generate_keys(self):
        """
        Generate RSA key pair
        Returns: (private_key, public_key)
        """
        print(f"[*] Generating RSA-{self.key_size} key pair...")
        
        # Generate private key
        key = RSA.generate(self.key_size)
        self.private_key = key
        
        # Extract public key
        self.public_key = key.publickey()
        
        print("[+] Key pair generated successfully!")
        return self.private_key, self.public_key
    
    def save_keys(self, private_path="keys/private.pem", public_path="keys/public.pem"):
        """
        Save keys to file
        """
        # Create keys directory if not exists
        os.makedirs("keys", exist_ok=True)
        
        # Save private key
        with open(private_path, "wb") as f:
            f.write(self.private_key.export_key())
        print(f"[+] Private key saved to: {private_path}")
        
        # Save public key
        with open(public_path, "wb") as f:
            f.write(self.public_key.export_key())
        print(f"[+] Public key saved to: {public_path}")
    
    def load_public_key(self, public_path="keys/public.pem"):
        """
        Load public key from file (for encryption)
        """
        with open(public_path, "rb") as f:
            self.public_key = RSA.import_key(f.read())
        return self.public_key
    
    def load_private_key(self, private_path="keys/private.pem"):
        """
        Load private key from file (for decryption)
        """
        with open(private_path, "rb") as f:
            self.private_key = RSA.import_key(f.read())
        return self.private_key
    
    def encrypt_key(self, symmetric_key):
        """
        Encrypt symmetric key dengan RSA public key
        """
        cipher = PKCS1_OAEP.new(self.public_key)
        encrypted_key = cipher.encrypt(symmetric_key)
        return encrypted_key
    
    def decrypt_key(self, encrypted_key):
        """
        Decrypt symmetric key dengan RSA private key
        """
        cipher = PKCS1_OAEP.new(self.private_key)
        decrypted_key = cipher.decrypt(encrypted_key)
        return decrypted_key


# Testing code
if __name__ == "__main__":
    km = KeyManager()
    km.generate_keys()
    km.save_keys()
    
    # Test encryption/decryption
    test_data = b"This is a symmetric key"
    encrypted = km.encrypt_key(test_data)
    decrypted = km.decrypt_key(encrypted)
    
    print(f"\nOriginal: {test_data}")
    print(f"Encrypted: {encrypted[:50]}...")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {test_data == decrypted}")