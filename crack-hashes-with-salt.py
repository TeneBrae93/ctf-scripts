# Used on the "sync" machine from vulnlab to crack a hash with a custom salt 
import hashlib

# Known values
salt = "[salt]"  # The salt
username = "[sername]"                         # The username
target_hash = "[hash]"  # The hash to crack
wordlist = "/usr/share/wordlists/rockyou.txt"     # Path to the wordlist

# Open the wordlist and iterate over each password
with open(wordlist, "r", encoding="latin-1") as f:
    for password in f:
        password = password.strip()  # Remove newline characters
        # Generate the hash using the salt, username, and password
        data = f"{salt}|{username}|{password}"
        generated_hash = hashlib.md5(data.encode()).hexdigest()
        # Compare the generated hash with the target hash
        if generated_hash == target_hash:
            print(f"[+] Password found: {password}")
            break
    else:
        print("[-] Password not found.")
