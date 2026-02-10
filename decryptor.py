"""
Decryptor Tool
Decrypt files encrypted by POC ransomware
"""

import os
import sys
from modules.crypto_engine import CryptoEngine
from modules.key_manager import KeyManager

class Decryptor:
    def __init__(self):
        self.crypto = CryptoEngine()
        self.key_mgr = KeyManager()
    
    def load_keys(self):
        """
        Load decryption keys
        """
        print("[*] Loading decryption keys...")
        
        # Load RSA private key
        if not os.path.exists("keys/private.pem"):
            print("[!] ERROR: Private key not found!")
            return False
        
        self.key_mgr.load_private_key("keys/private.pem")
        
        # Load symmetric key
        if not os.path.exists("keys/symmetric.key"):
            print("[!] ERROR: Symmetric key not found!")
            return False
        
        with open("keys/symmetric.key", "rb") as f:
            self.symmetric_key = f.read()
        
        print("[+] Keys loaded successfully!")
        return True
    
    def find_encrypted_files(self, directory="test_data"):
        """
        Find all .encrypted files
        """
        encrypted_files = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.encrypted'):
                    encrypted_files.append(os.path.join(root, file))
        
        return encrypted_files
    
    def decrypt_file(self, encrypted_path):
        """
        Decrypt single file
        """
        try:
            # Read encrypted file
            ciphertext, iv = self.crypto.read_encrypted_file(encrypted_path)
            
            # Decrypt
            plaintext = self.crypto.decrypt_file(
                ciphertext,
                self.symmetric_key,
                iv
            )
            
            if plaintext:
                # Write decrypted file
                original_path = encrypted_path.replace('.encrypted', '')
                with open(original_path, 'wb') as f:
                    f.write(plaintext)
                
                # Remove encrypted file
                os.remove(encrypted_path)
                
                print(f"[+] Decrypted: {original_path}")
                return True
            
        except Exception as e:
            print(f"[-] Error decrypting {encrypted_path}: {str(e)}")
            return False
    
    def run(self, directory="test_data"):
        """
        Main decryption process
        """
        print("="*60)
        print("           POC RANSOMWARE DECRYPTOR")
        print("="*60)
        
        # Load keys
        if not self.load_keys():
            return
        
        # Find encrypted files
        print(f"\n[*] Searching for encrypted files in: {directory}")
        encrypted_files = self.find_encrypted_files(directory)
        
        if len(encrypted_files) == 0:
            print("[!] No encrypted files found!")
            return
        
        print(f"[*] Found {len(encrypted_files)} encrypted files")
        
        # Decrypt all files
        print("\n[*] Starting decryption...")
        success_count = 0
        
        for file_path in encrypted_files:
            if self.decrypt_file(file_path):
                success_count += 1
        
        print(f"\n[+] Successfully decrypted {success_count}/{len(encrypted_files)} files!")
        print("="*60)


if __name__ == "__main__":
    decryptor = Decryptor()
    decryptor.run()