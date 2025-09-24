import subprocess
import requests
import ctypes
import uuid
import platform
import winreg
import os

def is_user_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False

def get_user_name():
    try:
        result = subprocess.run(['whoami'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving user name: {e}")
        return "Unknown User"
    
def get_hwid():
    """Get HWID using multiple methods"""
    # Method 1: Try wmic with full path
    try:
        wmic_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'System32', 'wbem', 'wmic.exe')
        if os.path.exists(wmic_path):
            result = subprocess.run([wmic_path, 'csproduct', 'get', 'UUID'], 
                                  capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and 'UUID' not in line:
                    return line
    except Exception as e:
        print(f"WMIC method failed: {e}")
    
    # Method 2: Try PowerShell
    try:
        ps_command = "(Get-WmiObject -Class Win32_ComputerSystemProduct).UUID"
        result = subprocess.run(['powershell', '-Command', ps_command], 
                              capture_output=True, text=True)
        hwid = result.stdout.strip()
        if hwid and hwid != "":
            return hwid
    except Exception as e:
        print(f"PowerShell method failed: {e}")
    
    # Method 3: Try registry
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                           r"SOFTWARE\Microsoft\Cryptography") as key:
            machine_guid, _ = winreg.QueryValueEx(key, "MachineGuid")
            return machine_guid
    except Exception as e:
        print(f"Registry method failed: {e}")
    
    # Method 4: Fallback to node UUID
    try:
        return str(uuid.uuid1())
    except Exception as e:
        print(f"UUID fallback failed: {e}")
    
    return None

def get_cpu_name():
    """Get CPU name using multiple methods"""
    # Method 1: Try wmic with full path
    try:
        wmic_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'System32', 'wbem', 'wmic.exe')
        if os.path.exists(wmic_path):
            result = subprocess.run([wmic_path, 'cpu', 'get', 'name'], 
                                  capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and 'Name' not in line:
                    return line
    except Exception as e:
        print(f"WMIC CPU name failed: {e}")
    
    # Method 2: Try PowerShell
    try:
        ps_command = "(Get-WmiObject -Class Win32_Processor).Name"
        result = subprocess.run(['powershell', '-Command', ps_command], 
                              capture_output=True, text=True)
        cpu_name = result.stdout.strip()
        if cpu_name and cpu_name != "":
            return cpu_name
    except Exception as e:
        print(f"PowerShell CPU name failed: {e}")
    
    # Method 3: Try registry
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                           r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as key:
            cpu_name, _ = winreg.QueryValueEx(key, "ProcessorNameString")
            return cpu_name.strip()
    except Exception as e:
        print(f"Registry CPU name failed: {e}")
    
    # Method 4: Fallback to platform
    try:
        return platform.processor()
    except Exception as e:
        print(f"Platform CPU name failed: {e}")
    
    return None

def get_cpu_id():
    """Get CPU ID using multiple methods"""
    # Method 1: Try wmic with full path
    try:
        wmic_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'System32', 'wbem', 'wmic.exe')
        if os.path.exists(wmic_path):
            result = subprocess.run([wmic_path, 'cpu', 'get', 'ProcessorId'], 
                                  capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and 'ProcessorId' not in line:
                    return line
    except Exception as e:
        print(f"WMIC CPU ID failed: {e}")
    
    # Method 2: Try PowerShell
    try:
        ps_command = "(Get-WmiObject -Class Win32_Processor).ProcessorId"
        result = subprocess.run(['powershell', '-Command', ps_command], 
                              capture_output=True, text=True)
        cpu_id = result.stdout.strip()
        if cpu_id and cpu_id != "":
            return cpu_id
    except Exception as e:
        print(f"PowerShell CPU ID failed: {e}")
    
    # Method 3: Try registry
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                           r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as key:
            cpu_id, _ = winreg.QueryValueEx(key, "Identifier")
            return cpu_id.strip()
    except Exception as e:
        print(f"Registry CPU ID failed: {e}")
    
    return None

def get_IPV4():
    try:
        response = requests.get('https://api.ipify.org?format=text')
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error retrieving IPv4 address: {e}")
        return "Unknown IP"
    
def get_location():
    """Get device location from most accurate to least accurate method"""
    
    # Method 1: Windows Location Service with auto-enable attempt
    try:
        # First check if we have admin rights
        if is_user_admin():
            # Try to enable location service via registry
            try:
                import winreg
                # Enable location service
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                  r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location",
                                  0, winreg.KEY_SET_VALUE) as key:
                    winreg.SetValueEx(key, "Value", 0, winreg.REG_SZ, "Allow")
                
                # Enable for current user
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                  r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location",
                                  0, winreg.KEY_SET_VALUE) as key:
                    winreg.SetValueEx(key, "Value", 0, winreg.REG_SZ, "Allow")
                    
                # Enable location service in system
                subprocess.run(['powershell', '-Command', 
                              'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\PolicyManager\\default\\System\\AllowLocation" -Name "value" -Value 1'], 
                              capture_output=True, text=True)
            except:
                pass  # Registry changes failed, continue anyway
        
        # Try to get GPS location
        ps_command = """
        Add-Type -AssemblyName System.Device
        $GeoWatcher = New-Object System.Device.Location.GeoCoordinateWatcher
        $GeoWatcher.Start()
        Start-Sleep -Seconds 3
        $Location = $GeoWatcher.Position.Location
        if (-not $Location.IsUnknown) {
            Write-Output "$($Location.Latitude),$($Location.Longitude)"
        }
        $GeoWatcher.Stop()
        """
        result = subprocess.run(['powershell', '-Command', ps_command], 
                              capture_output=True, text=True, timeout=15)
        output = result.stdout.strip()
        if ',' in output and 'IsUnknown' not in output and len(output) > 5:
            lat, lon = output.split(',')
            return f"GPS: {float(lat):.6f}, {float(lon):.6f}"
    except:
        pass
    
    # Method 2: IP Geolocation (most reliable fallback)
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        data = response.json()
        if data['status'] == 'success':
            return f"{data['city']}, {data['regionName']}, {data['country']}"
    except:
        pass
    
    # Method 3: Alternative IP service
    try:
        response = requests.get('https://ipapi.co/json/', timeout=5)
        data = response.json()
        if 'city' in data and data['city']:
            return f"{data['city']}, {data['region']}, {data['country_name']}"
    except:
        pass
    
    # Method 4: Timezone-based approximation
    try:
        ps_command = "(Get-TimeZone).Id"
        result = subprocess.run(['powershell', '-Command', ps_command], 
                              capture_output=True, text=True, timeout=5)
        timezone = result.stdout.strip()
        if timezone:
            return f"Timezone: {timezone}"
    except:
        pass
    
    return "Location unavailable"