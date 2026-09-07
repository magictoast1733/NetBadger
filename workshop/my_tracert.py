import re
import subprocess

def route(ip):
    # Strict pattern matching to catch the IP immediately following "From" or "from"
    re_router = re.compile(r"[Ff]rom\s+([\d.]+)")


    def get_hop_ip(host, ttl):
        command = ["ping", "-t", str(ttl), "-c", "1", "-W", "1", host]
        result = subprocess.run(command, capture_output=True, text=True)

        # Search line by line for the actual network response line
        for line in result.stdout.splitlines():
            match = re_router.search(line)
            if match:
                return match.group(1)  # Returns just the IP string found after 'from'

        return None


    #ip = ("10.149.100.1")
    t = 1
    final = ""
    final_list = []

    while final != ip:
        final = get_hop_ip(ip, t)

        if final:
            print(f"TTL {t}: {final}")
            final_list.append(final)
        else:
            print(f"TTL {t}: * * *")
            final = ""  # Prevent false positive matches on None

        t += 1

    return final_list