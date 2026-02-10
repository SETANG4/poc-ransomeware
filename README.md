# POC Ransomware - Educational Research

⚠️ **WARNING: FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY**

## Description
Proof-of-Concept (POC) ransomware developed for academic research in static malware analysis. This project implements modern encryption techniques (AES-256 + RSA-2048) to simulate ransomware behavior in a controlled environment.

## Features
- AES-256-CBC file encryption
- RSA-2048 key management
- File discovery with safety limits
- Ransom note generation
- Complete decryption tool
- Built-in safety features

## Project Structure

poc-ransomware/ ├── modules/ │ ├── key_manager.py # RSA key generation & management │ ├── crypto_engine.py # AES encryption engine │ ├── file_scanner.py # File discovery module │ └── ransom_note.py # Ransom note generator ├── main.py # Main POC ransomware ├── decryptor.py # Decryption tool ├── test_data/ # Test files directory └── keys/ # Generated keys storage
