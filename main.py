from parsing import log, is_valid_login_line, parsing
from analysis import count_stats, urutan, brute_force_detected

def printHasil(IP, USER, JAM):
    print("=== TOP ATTACKER IPs ===")
    for ip, count in IP[:10]:
        print(f"IP: {ip} | Total Serangan: {count}")

    print("=== TOP ATTACKED USER ===")
    for user, count in USER[:10]:
        print(f"User: {user} | Total Serangan: {count}")

    print("=== JAM PALING RAWAN SERANGAN ===")
    for x, y in JAM[:10]:
        print(f" JAM {x} di serang {y}x")
 
def main():
    fullData = []
    with open("auth.log", "r") as f:
        for x in f:
            if log(x) and is_valid_login_line(x):
                data = parsing(x)
                fullData.append(data)

    acceptedLog = []
    failedLog = []
    invalidUserLog = []

    for x in fullData:
        if x["status"] == "Accepted password":
            acceptedLog.append(x)
        if x["status"] == "Failed Password":
            failedLog.append(x)
        if x["status"] == "Invalid User":
            invalidUserLog.append(x)

    counterIP = count_stats(failedLog, 'ip')
    invalidUser = count_stats(invalidUserLog, 'user')
    jamRawan = count_stats(failedLog, 'jam')

    ipAcc = {x["ip"] for x in acceptedLog}

    for x, y in counterIP.items():
        if x in ipAcc:
            print(f"{x} berhasil setelah gagal sebanyak, {y}x")

    ipsort = urutan(counterIP)
    usersort = urutan(invalidUser)
    jamsort = urutan(jamRawan)

    printHasil(ipsort, usersort, jamsort)
    sementara = {}
    blacklist = []
    for x in failedLog:
        is_brute, total = brute_force_detected(x, sementara)
        if is_brute and x["ip"] not in blacklist:
            print(f"ALARM: IP {x['ip']} Terdeteksi Brute Force! (Total: {total} kali dalam 60 detik)")
            blacklist.append(x["ip"])

    sementara = {}
    blacklist = []

    for x in failedLog:
        ip_sekarang = x["ip"]
        is_brute, total = brute_force_detected(x, sementara)
        
        if is_brute and ip_sekarang not in blacklist:
            blacklist.append(ip_sekarang)

    print(f"{'IP ADDRESS':<20} | {'TOTAL SERANGAN':<15}")
    print("-" * 40)

    for ip in blacklist:

        total_akhir = len(sementara[ip])
        print(f"{ip:<20} | {total_akhir:<15} kali")

if __name__ == "__main__":
    main()
