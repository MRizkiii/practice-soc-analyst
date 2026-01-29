"""
SSH Auth Log Parser Module

Parses sshd authentication log entries and extracts structured data
for security analysis.
"""

from typing import Optional


def log(line: str) -> bool:
    """Check if log line is from sshd service."""
    return "sshd" in line


def is_valid_login_line(line: str) -> bool:
    """Check if line contains login attempt information."""
    return "for " in line and "from " in line and "port " in line


def _determine_status(line: str) -> str:
    """
    Determine the authentication status from log line.
    
    Returns one of:
    - Accepted publickey
    - Accepted password  
    - Invalid User
    - Failed Publickey
    - Failed Password
    - Message Repeated
    - Session Started (Shell)
    - Error
    - unknown
    """
    if "Accepted" in line:
        return "Accepted publickey" if "publickey" in line else "Accepted password"
    
    if "Failed" in line:
        if "invalid user" in line:
            return "Invalid User"
        if "message repeated" in line:
            return "Message Repeated"
        if "publickey" in line:
            return "Failed Publickey"
        return "Failed Password"
    
    if "Starting session:" in line:
        return "Session Started (Shell)"
    
    if "Invalid user" in line:
        return "Invalid User"
    
    if "error" in line.lower():
        return "Error"
    
    return "unknown"


def parsing(line: str) -> dict:
    """
    Parse a single SSH auth log line into structured data.
    
    Args:
        line: Raw log line string
        
    Returns:
        Dictionary with keys:
        - bulan: Month (e.g., "Mar")
        - tanggal: Day of month
        - jam: Time (HH:MM:SS)
        - fulltime: Combined timestamp
        - user: Target username
        - ip: Source IP address
        - port: Source port
        - status: Authentication status
    """
    # Normalize double spaces
    line = line.replace("  ", " ")
    
    # Extract user field
    user_start = line.find("for ") + 4
    user_end = line.find(" ", user_start)
    
    # Handle "invalid user" prefix
    if line[user_start:user_end] == "invalid":
        user_start = line.find("invalid user ") + 13
        user_end = line.find(" ", user_start)
    
    # Extract IP field
    ip_start = line.find("from ", user_end) + 5
    ip_end = line.find(" ", ip_start)
    
    # Extract port field
    port_start = line.find("port ", ip_end) + 5
    port_end = line.find(" ", port_start)
    if port_end == -1:
        port_end = len(line)
    
    # Extract timestamp parts
    parts = line.split()
    bulan = parts[0]
    tanggal = parts[1]
    jam = parts[2]
    
    # Get user, handling edge cases
    user = line[user_start:user_end]
    if user == "from":
        user = "Bot"
    
    return {
        "bulan": bulan,
        "tanggal": tanggal,
        "jam": jam,
        "fulltime": f"{jam} {tanggal} {bulan} 2025",
        "user": user,
        "ip": line[ip_start:ip_end],
        "port": line[port_start:port_end].strip(),
        "status": _determine_status(line),
    }
