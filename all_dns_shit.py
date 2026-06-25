import platform
import subprocess
import socket

def Run_Ping(host):
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
import subprocess

def get_nslookup_address(domain):
    try:
        result = subprocess.run(
            ["nslookup", domain], 
            capture_output=True, 
            text=True
        )
        
        addresses = []
        for line in result.stdout.splitlines():
            if line.strip().lower().startswith("address:"):
                # Extract the IP address part
                ip = line.split(":", 1)[1].strip()
                addresses.append(ip)
                return line
        
            
        return None
        
    except FileNotFoundError:
        return "Error: 'nslookup' command not found."
    
def Run_nslookup(domain):
    try:
        result = subprocess.run(
            ["nslookup", domain], 
            capture_output=True, 
            text=True,
        )
        combined_output = result.stdout + "\n" + result.stderr
        return combined_output
        
    except FileNotFoundError:
        return "Error: 'nslookup' command not found on this system."

def LookupCheck(target):
    output_of_nslookup = Run_nslookup(target)
    if "Non-existent domain" in output_of_nslookup or "can't find" in output_of_nslookup.lower():
        return False
    else:
        return True

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
    Sus_DNS_List_Names = []
    Sus_ip_List = []
    
    IP_SEGMENT = get_local_prefix_offline()
    all_dns_list = all_dns(IP_SEGMENT)
    for i in range(0,3,1):
        sus_ip = all_dns_list[i]
        Is_pingable = Run_Ping(sus_ip)
        Is_nslookup = LookupCheck(sus_ip)
        if (Is_pingable):
            pass
        elif ((not (Is_pingable)) and Is_nslookup):
            Sus_ip_List.append(sus_ip)
            Sus_DNS_List_Names.append()
            
    print(Sus_DNS_List_Names)

main()import platform
import subprocess
import socket

def Run_Ping(host):
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

def Run_nslookup(domain):
    try:
        result = subprocess.run(
            ["nslookup", domain], 
            capture_output=True, 
            text=True,
        )
        combined_output = result.stdout + "\n" + result.stderr
        return combined_output
        
    except FileNotFoundError:
        return "Error: 'nslookup' command not found on this system."

def LookupCheck(target):
    output_of_nslookup = Run_nslookup(target)
    if "Non-existent domain" in output_of_nslookup or "can't find" in output_of_nslookup.lower():
        return False
    else:
        return True

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
        Is_pingable = Run_Ping(sus_ip)
        Is_nslookup = LookupCheck(sus_ip)
        if (Is_pingable):
            pass
        elif ((not (Is_pingable)) and Is_nslookup):
            Valid_dns.append(sus_ip)
            
    print(Valid_dns)

main()
