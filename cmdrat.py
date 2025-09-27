import subprocess
import threading
import time

active_shells = {}

def start_shell(user_id, shell_type, initial_command=None):
    try:
        if shell_type.lower() == "diskpart":
            process = subprocess.Popen(['diskpart'], 
                                     stdin=subprocess.PIPE, 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.STDOUT, 
                                     text=True, bufsize=1,
                                     creationflags=subprocess.CREATE_NO_WINDOW)
        elif shell_type.lower() == "cmd":
            process = subprocess.Popen(['cmd', '/k'], 
                                     stdin=subprocess.PIPE, 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.STDOUT, 
                                     text=True, bufsize=0, 
                                     creationflags=subprocess.CREATE_NO_WINDOW)
        elif shell_type.lower() == "powershell":
            process = subprocess.Popen(['powershell', '-NoLogo', '-NoExit'], 
                                     stdin=subprocess.PIPE, 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.STDOUT, 
                                     text=True, bufsize=0,
                                     creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            return f"Unsupported shell type: {shell_type}"
        
        active_shells[user_id] = process
        
        if initial_command:
            process.stdin.write(initial_command + '\n')
            process.stdin.flush()
        
        if shell_type.lower() == "diskpart":
            time.sleep(4)
        else:
            time.sleep(2)
        
        output = read_output(process, shell_type.lower())
        return output if output.strip() else f"{shell_type} started (no initial output)"
        
    except Exception as e:
        return f"Error starting {shell_type}: {e}"

def send_command(user_id, command):
    if user_id not in active_shells:
        return "No active shell session"
    
    try:
        process = active_shells[user_id]
        
        if process.poll() is not None:
            del active_shells[user_id]
            return "Shell session ended unexpectedly"
        
        process.stdin.write(command + '\n')
        process.stdin.flush()
        
        time.sleep(1)
        
        output = read_output(process)
        
        if not output.strip():
            if process.poll() is None:
                return f"Command '{command}' executed (waiting for output...)"
            else:
                return "Command executed (no output)"
        
        return output
        
    except Exception as e:
        if user_id in active_shells:
            del active_shells[user_id]
        return f"Error executing command: {e}"

def end_shell(user_id):
    if user_id not in active_shells:
        return "No active shell session"
    
    try:
        active_shells[user_id].terminate()
        del active_shells[user_id]
        return "Shell session ended"
    except Exception as e:
        if user_id in active_shells:
            del active_shells[user_id]
        return f"Error ending shell: {e}"

def read_output(process):
    import time
    import threading
    import queue
    import select
    import sys
    
    output_queue = queue.Queue()
    
    def read_lines():
        try:
            while True:
                line = process.stdout.readline()
                if line:
                    output_queue.put(line)
                else:
                    time.sleep(0.01)
        except:
            pass
    
    thread = threading.Thread(target=read_lines)
    thread.daemon = True
    thread.start()
    
    output = ""
    start_time = time.time()
    last_output_time = start_time
    
    while time.time() - start_time < 5:
        try:
            line = output_queue.get(timeout=0.1)
            output += line
            last_output_time = time.time()
            if len(output) > 1800:
                break
        except queue.Empty:
            if time.time() - last_output_time > 1.5:
                break
            continue
        except:
            break
    
    return output

def has_active_shell(user_id):
    return user_id in active_shells

def get_shell_status(user_id):
    """Get status of current shell session"""
    if user_id not in active_shells:
        return "No active shell session"
    
    try:
        process = active_shells[user_id]
        if process.poll() is None:
            return "Shell session is active and running"
        else:
            del active_shells[user_id]
            return "Shell session has ended"
    except:
        if user_id in active_shells:
            del active_shells[user_id]
        return "Shell session error"