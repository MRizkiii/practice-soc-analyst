"""
SSH Auth Log Analyzer - Main Module

Provides CLI interface and report generation for SSH log analysis.
"""

from parsing import log, is_valid_login_line, parsing
from analysis import (
    count_stats, 
    urutan, 
    brute_force_detected, 
    loginSuccess, 
    corelation,
    calculate_severity,
    get_targeted_users,
    BRUTE_FORCE_WINDOW_SECONDS,
)


def load_log_file(filepath: str = "auth.log") -> list:
    """
    Load and parse auth.log file.
    
    Args:
        filepath: Path to auth.log file
        
    Returns:
        List of parsed log entries
    """
    entries = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if log(line) and is_valid_login_line(line):
                entries.append(parsing(line))
    return entries


def categorize_logs(entries: list) -> dict:
    """
    Categorize log entries by authentication status.
    
    Returns:
        Dictionary with keys 'accepted', 'failed', 'invalid_user'
    """
    accepted = []
    failed = []
    invalid_user = []
    
    for entry in entries:
        status = entry["status"]
        if status == "Accepted password":
            accepted.append(entry)
        elif status == "Failed Password":
            failed.append(entry)
        elif status == "Invalid User":
            invalid_user.append(entry)
    
    return {
        "accepted": accepted,
        "failed": failed,
        "invalid_user": invalid_user,
    }


def generate_report(fullData: list) -> dict:
    """
    Generate comprehensive security report from log entries.
    
    Args:
        fullData: List of parsed log entries
        
    Returns:
        Dictionary containing:
        - ipsort: Top attacking IPs
        - usersort: Top attacked usernames
        - jamsort: Attack frequency by hour
        - alarms: Brute force alerts
        - correlations: IPs that succeeded after failures
        - summary: Quick stats overview
    """
    categories = categorize_logs(fullData)
    
    acceptedLog = categories["accepted"]
    failedLog = categories["failed"]
    invalidUserLog = categories["invalid_user"]
    
    # Calculate statistics
    counterIP = count_stats(failedLog, 'ip')
    invalidUser = count_stats(invalidUserLog, 'user')
    jamRawan = count_stats(failedLog, 'jam')

    ipsort = urutan(counterIP)
    usersort = urutan(invalidUser)
    jamsort = urutan(jamRawan)

    # Track successful logins
    acc = {}
    for entry in acceptedLog:
        loginSuccess(entry, acc)

    # Detect brute force attacks
    sementara = {}
    blacklist = []
    alarms = []

    for entry in failedLog:
        is_brute, total = brute_force_detected(entry, sementara)
        if is_brute and entry["ip"] not in blacklist:
            alarms.append({
                "ip": entry["ip"],
                "total": total,
                "severity": calculate_severity(total),
                "targeted_users": get_targeted_users(sementara, entry["ip"]),
            })
            blacklist.append(entry["ip"])

    # Find correlations (success after failure)
    correlations = {}
    corelation(acc, sementara, correlations)
    
    # Build correlation alerts
    correlation_alerts = []
    for ip, logins in correlations.items():
        failed_count = len(sementara.get(ip, []))
        correlation_alerts.append({
            "ip": ip,
            "successful_logins": len(logins),
            "failed_attempts": failed_count,
            "severity": calculate_severity(failed_count),
            "users": list(set(user for _, user in logins)),
        })
    
    # Sort by failed attempts
    correlation_alerts.sort(key=lambda x: x["failed_attempts"], reverse=True)

    # Summary statistics
    summary = {
        "total_entries": len(fullData),
        "successful_logins": len(acceptedLog),
        "failed_attempts": len(failedLog),
        "invalid_users": len(invalidUserLog),
        "unique_attacker_ips": len(counterIP),
        "brute_force_alerts": len(alarms),
        "potential_compromises": len(correlations),
    }

    return {
        "ipsort": ipsort,
        "usersort": usersort,
        "jamsort": jamsort,
        "alarms": alarms,
        "correlations": correlation_alerts,
        "summary": summary,
        "sementara": sementara,
        "blacklist": blacklist,
    }


def printHasil(IP, USER, JAM):
    """Print formatted statistics to console."""
    print("\n[TOP ATTACKER IPs]")
    print("-" * 45)
    for ip, count in IP[:10]:
        severity = calculate_severity(count)
        indicator = {"critical": "[!!]", "high": "[!]", "medium": "[*]", "low": "[-]"}
        print(f"  {indicator[severity]} {ip:<18} | {count} serangan")

    print("\n[TOP ATTACKED USERS]")
    print("-" * 45)
    for user, count in USER[:10]:
        print(f"  {user:<20} | {count} serangan")

    print("\n[JAM PALING RAWAN SERANGAN]")
    print("-" * 45)
    for hour, count in JAM[:10]:
        bar = "#" * min(count // 5, 30)
        print(f"  {hour}:00 | {bar} ({count})")


def print_report(report: dict) -> None:
    """Print comprehensive formatted report to console."""
    
    print("\n" + "=" * 60)
    print("  SSH LOG SECURITY ANALYSIS REPORT")
    print("=" * 60)
    
    # Summary
    summary = report["summary"]
    print(f"\n[SUMMARY]")
    print(f"  Total log entries     : {summary['total_entries']}")
    print(f"  Successful logins     : {summary['successful_logins']}")
    print(f"  Failed attempts       : {summary['failed_attempts']}")
    print(f"  Invalid user attempts : {summary['invalid_users']}")
    print(f"  Unique attacker IPs   : {summary['unique_attacker_ips']}")
    print(f"  Brute force alerts    : {summary['brute_force_alerts']}")
    print(f"  Potential compromises : {summary['potential_compromises']}")
    
    # Statistics
    printHasil(
        report["ipsort"],
        report["usersort"],
        report["jamsort"]
    )
    
    # Brute Force Alerts
    if report["alarms"]:
        print(f"\n[!!! BRUTE FORCE ALERTS !!!]")
        print("-" * 45)
        for alarm in report["alarms"]:
            severity = alarm.get("severity", "high")
            indicator = {"critical": "[!!]", "high": "[!]", "medium": "[*]", "low": "[-]"}
            print(f"  {indicator[severity]} IP: {alarm['ip']}")
            print(f"      {alarm['total']} attempts dalam {BRUTE_FORCE_WINDOW_SECONDS}s")
            if alarm.get("targeted_users"):
                users = ", ".join(alarm["targeted_users"][:5])
                print(f"      Target users: {users}")
    
    # Correlation Alerts (Success after failure)
    if report["correlations"]:
        print(f"\n[!! POTENTIAL COMPROMISES !!]")
        print("-" * 45)
        for corr in report["correlations"][:10]:
            print(f"  [!!] IP: {corr['ip']}")
            print(f"       Failed {corr['failed_attempts']}x, lalu berhasil login {corr['successful_logins']}x")
            if corr.get("users"):
                users = ", ".join(corr["users"][:3])
                print(f"       Users: {users}")
    
    # Blacklist summary
    if report["blacklist"]:
        print(f"\n[BLACKLIST SUMMARY]")
        print(f"{'IP ADDRESS':<22} | {'TOTAL ATTEMPTS':<15}")
        print("-" * 45)
        for ip in report["blacklist"][:15]:
            total = len(report["sementara"].get(ip, []))
            print(f"  {ip:<20} | {total} kali")
    
    print("\n" + "=" * 60)


def main():
    """Main CLI entry point."""
    fullData = load_log_file()
    report = generate_report(fullData)
    print_report(report)


if __name__ == "__main__":
    main()
