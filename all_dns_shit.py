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
            return "1"
        elif "timed out" in full_output or "100% packet loss" in full_output:
            return "1"
        
        if response.returncode == 0:
            return "0"
        else:
            return "1"
            
    except subprocess.TimeoutExpired:
        return "1"
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
    line_count = len(output_of_nslookup.splitlines())
    print(f"Target: {target} | Lines: {line_count}")
    
    if line_count > 7: 
        return True
    elif line_count < 7:
        return False
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
    all_ip = ""
    for i in range(0,256,1):
        sus_ip = prefix_ip + "."+str(i)
        all_ip = all_ip + "\n" + sus_ip
    clean_str = all_ip.lstrip()
    return clean_str

def main():
    Valid_dns = []
    IP_SEGMENT = get_local_prefix_offline()
    all_dns(IP_SEGMENT)
    for i in range(0,3,1):
        sus_ip = IP_SEGMENT + "."+str(i)
        if (pinger(sus_ip) == 1):
            pass
        elif (pinger(sus_ip) == 0):
            Valid_dns.append(sus_ip)
            
    print(Valid_dns)

main()
