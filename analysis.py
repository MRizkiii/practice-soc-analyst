"""
SSH Auth Log Analysis Module

Provides statistical analysis, brute force detection, and correlation
for SSH authentication logs.
"""

from typing import Tuple, List, Dict


# Detection thresholds (configurable)
BRUTE_FORCE_THRESHOLD = 5  # Min attempts to trigger alert
BRUTE_FORCE_WINDOW_SECONDS = 60  # Time window for detection


def count_stats(data_list: List[dict], key: str) -> Dict[str, int]:
    """
    Count occurrences of a field value across log entries.
    
    Args:
        data_list: List of parsed log entries
        key: Field to count ('ip', 'user', 'jam', etc.)
        
    Returns:
        Dictionary mapping field values to counts
    """
    counts = {}
    for item in data_list:
        val = item[key]
        
        # For time field, extract just the hour
        if key == "jam":
            val = val.split(":")[0]
            
        counts[val] = counts.get(val, 0) + 1
    return counts


def urutan(stats_dict: Dict[str, int], limit: int = None) -> List[Tuple[str, int]]:
    """
    Sort statistics by count in descending order.
    
    Args:
        stats_dict: Dictionary of value -> count
        limit: Optional limit on results
        
    Returns:
        List of (value, count) tuples sorted by count descending
    """
    sorted_items = sorted(stats_dict.items(), key=lambda x: x[1], reverse=True)
    if limit:
        return sorted_items[:limit]
    return sorted_items


def _timestamp_to_seconds(entry: dict) -> int:
    """
    Convert log entry timestamp to seconds since start of month.
    
    Args:
        entry: Parsed log entry with 'tanggal' and 'jam' fields
        
    Returns:
        Total seconds as integer
    """
    jam_parts = entry["jam"].split(":")
    
    per_hari = int(entry["tanggal"]) * 86400
    per_jam = int(jam_parts[0]) * 3600
    per_menit = int(jam_parts[1]) * 60
    per_detik = int(jam_parts[2])
    
    return per_hari + per_jam + per_menit + per_detik


def brute_force_detected(entry: dict, ip_attempts: dict) -> Tuple[bool, int]:
    """
    Check if an IP has exceeded brute force threshold.
    
    Uses a sliding window approach: tracks attempt timestamps per IP
    and checks if there are >= BRUTE_FORCE_THRESHOLD attempts within
    BRUTE_FORCE_WINDOW_SECONDS.
    
    Args:
        entry: Parsed log entry
        ip_attempts: Dictionary tracking {ip: [(timestamp, user), ...]}
                     Modified in place to update attempt history.
        
    Returns:
        Tuple of (is_brute_force: bool, attempt_count: int)
    """
    ip = entry["ip"]
    user = entry["user"]
    current_time = _timestamp_to_seconds(entry)
    
    # Get existing attempts for this IP
    attempts = ip_attempts.get(ip, [])
    attempts.append((current_time, user))
    
    # Filter to only attempts within the time window
    valid_attempts = [
        (t, u) for t, u in attempts 
        if current_time - t <= BRUTE_FORCE_WINDOW_SECONDS
    ]
    
    # Update the tracking dictionary
    ip_attempts[ip] = valid_attempts
    
    if len(valid_attempts) >= BRUTE_FORCE_THRESHOLD:
        return True, len(valid_attempts)
    
    return False, 0


def loginSuccess(entry: dict, container: dict) -> None:
    """
    Track successful login attempts per IP.
    
    Args:
        entry: Parsed log entry with successful login
        container: Dictionary tracking {ip: [(jam, user), ...]}
    """
    ip = entry["ip"]
    jam = entry["jam"]
    user = entry["user"]
    
    value = container.get(ip, [])
    value.append((jam, user))
    container[ip] = value


def corelation(accepted: dict, failed: dict, result: dict) -> None:
    """
    Find IPs that appear in both accepted and failed logs.
    
    This identifies potential compromises where an attacker
    successfully logged in after brute force attempts.
    
    Args:
        accepted: Dict of {ip: [(jam, user), ...]} for successful logins
        failed: Dict of {ip: [(timestamp, user), ...]} for failed attempts
        result: Output dict to store correlated IPs
    """
    for ip in accepted:
        if ip in failed:
            result[ip] = accepted[ip]


def calculate_severity(attempt_count: int) -> str:
    """
    Calculate severity level based on attempt count.
    
    Args:
        attempt_count: Number of failed attempts
        
    Returns:
        Severity string: 'low', 'medium', 'high', or 'critical'
    """
    if attempt_count >= 50:
        return "critical"
    elif attempt_count >= 20:
        return "high"
    elif attempt_count >= 10:
        return "medium"
    return "low"


def get_targeted_users(ip_attempts: dict, ip: str) -> List[str]:
    """
    Get list of usernames targeted by a specific IP.
    
    Args:
        ip_attempts: Dictionary of {ip: [(timestamp, user), ...]}
        ip: IP address to look up
        
    Returns:
        List of unique usernames targeted
    """
    attempts = ip_attempts.get(ip, [])
    users = list(set(user for _, user in attempts))
    return users
