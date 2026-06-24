import platform
import subprocess
import socket

def pinger(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    
    try:
        response = subprocess.run(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True,
            timeout=3
        )
        
        full_output = (response.stdout + response.stderr).lower()
        
        if "unreachable" in full_output:
            return False
        elif "timed out" in full_output or "100% packet loss" in full_output:
            return False
        
        if response.returncode == 0:
            return True
        else:
            return False
            
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        return f"Error executing ping: {str(e)}"

def run_nslookup(domain):
    try:
        result = subprocess.run(
            ["nslookup", domain], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout
        
    except subprocess.CalledProcessError as e:
        error_output = e.stdout if e.stdout else e.stderr
        return error_output
    except FileNotFoundError:
        return "Error: 'nslookup' command not found on this system."

def LookupCheck(target):
    output_of_nslookup = run_nslookup(target)
    if not ("Non-existent domain" in output_of_nslookup):
        return True
    else:
        return False

def get_local_prefix_offline():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        if local_ip.startswith("127."):
            local_ip = socket.gethostbyname_ex(hostname)[2][-1]
 
        first_three_bytes = ".".join(local_ip.split(".")[:3])
        return first_three_bytes
        
    except Exception as e:
        return f"Error: {e}"
    
def all_dns(prefix_ip):
    ip_list = []
    for i in range(256):
        ip_list.append(f"{prefix_ip}.{i}")
    return ip_list

def main():
    Valid_dns = []
    IP_SEGMENT = get_local_prefix_offline()
    all_dns_list = all_dns(IP_SEGMENT)
    for i in range(0,3,1):
        sus_ip = all_dns_list[i]
        Is_pingable = pinger(sus_ip)
        if (Is_pingable):
            pass
        elif (not (Is_pingable)):
            Valid_dns.append(sus_ip)
            
    print(Valid_dns)

main()
