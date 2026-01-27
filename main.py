from parsing import log, is_valid_login_line, parsing
from analysis import count_stats, urutan, brute_force_detected, loginSuccess, corelation

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

def generate_report(fullData):
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

    ipsort = urutan(counterIP)
    usersort = urutan(invalidUser)
    jamsort = urutan(jamRawan)

    sementara = {}
    blacklist = []
    alarms = []
    acc = {}

    for x in acceptedLog:
        loginSuccess(x, acc)


    for x in failedLog:
        is_brute, total = brute_force_detected(x, sementara)
        if is_brute and x["ip"] not in blacklist:
            alarms.append({
                "ip": x["ip"],
                "total": total
            })
            blacklist.append(x["ip"])

    sc = {}
    corelation(acc, sementara, sc)
    for x in sc:
        totalBerhasil = len(sc[x])
        print(f"IP: {x} | total Login : {totalBerhasil}, setelah melakukan bruteforce sebanyak ")

    return {
        "ipsort": ipsort,
        "usersort": usersort,
        "jamsort": jamsort,
        "alarms": alarms,
        "sementara": sementara,
        "blacklist": blacklist
    }


def main():
    fullData = []
    with open("auth.log", "r") as f:
        for x in f:
            if log(x) and is_valid_login_line(x):
                data = parsing(x)
                fullData.append(data)

    report = generate_report(fullData)

    printHasil(
        report["ipsort"],
        report["usersort"],
        report["jamsort"]
    )

    for alarm in report["alarms"]:
        print(
            f"ALARM: IP {alarm['ip']} "
            f"Terdeteksi Brute Force! "
            f"(Total: {alarm['total']} kali dalam 60 detik)"
        )

    print(f"{'IP ADDRESS':<20} | {'TOTAL SERANGAN':<15}")
    print("-" * 40)

    for ip in report["blacklist"]:
        total_akhir = len(report["sementara"][ip])
        print(f"{ip:<20} | {total_akhir:<15} kali")

if __name__ == "__main__":
    main()
