from parsing import log, is_valid_login_line, parsing
from analysis import count_stats, urutan   

def ipLolos(x, container):
    container.append(x["ip"])
    container
    # container[ip] = container.get(ip, 0) + 1
    return container

def urutan(isi):
    urut = sorted(isi.items(), key=lambda item: item[1], reverse=True) 
    return urut

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

 
##LOGIC
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

    # Ambil semua IP dari acceptedLog, masukin ke set biar unik
    ipAcc = {x["ip"] for x in acceptedLog}

    for x, y in counterIP.items():
        if x in ipAcc:
            print(f"{x} berhasil setelah gagal sebanyak, {y}x")

    ipsort = urutan(counterIP)
    usersort = urutan(invalidUser)
    jamsort = urutan(jamRawan)

    printHasil(ipsort, usersort, jamsort)


if __name__ == "__main__":
    main()
