###FILTERING


def log(file):
    return [x for x in file if "sshd" in x]
def is_valid_login_line(line):
    return "for " in line and "from " in line and "port " in line

##PARSING

def parsing(x):
    x = x.replace("  ", " ")

    Auser = x.find("for ") + 4
    Buser = x.find(" ", Auser)

    Aip = x.find("from ", Buser) + 5
    Bip = x.find(" ", Aip)

    Aport = x.find("port ", Bip) + 5
    Bport = x.find(" ", Aport)

    if x[Auser:Buser] == "invalid":
        Auser = x.find("invalid user ") + 13
        Buser = x.find(" ", Auser)

    bulan = x.split()[0]
    tanggal = x.split()[1]
    jam = x.split()[2]

    status = "unknown"
    if "Accepted" in x:
        status = "Accepted publickey" if "publickey" in x else "Accepted password"
    elif "Failed" in x:
        if "invalid user" in x:
            status = "Invalid User"
        elif "message repeated" in x:
            status = "Message Repeated"
        elif "publickey" in x:
            status = "Failed Publickey"
        else:
            status = "Failed Password"
    elif "Starting session:" in x:
        status = "Session Started (Shell)"
    elif "Invalid user" in x:
        status = "Invalid User"
    elif "error" in x:
        status = "Error"

    user = x[Auser:Buser]
    if user == "from":
        user = "Bot"

    return {
        "bulan": bulan,
        "tanggal": tanggal,
        "jam": jam,
        "user": user,
        "ip": x[Aip:Bip],
        "port": x[Aport:Bport],
        "status": status,
    }


def FailedLoginIPCount(x, coontainer):
    ip = x["ip"]
    coontainer[ip] = coontainer.get(ip, 0) + 1
    return coontainer


def InvalidUserCount(x, container):
    usr = x["user"]
    container[usr] = container.get(usr, 0) + 1
    return container


def TimeAttack(x, container):
    x = x["jam"]
    x = x.split(":")
    jam = x[0]
    container[jam] = container.get(jam, 0) + 1
    return container


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
with open("auth.log", "r") as f:
    logs = f.readlines()
    sshLog = log(logs)

fullData = []
for line in sshLog:
    if not is_valid_login_line(line):
        continue

    data = parsing(line)
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

# print(failedLog)

counterIP = {}
for x in failedLog:
    hasil = FailedLoginIPCount(x, counterIP)

invalidUser = {}
for x in invalidUserLog:
    hasil = InvalidUserCount(x, invalidUser)

jamRawan = {}
for x in failedLog:
    TimeAttack(x, jamRawan)

ipAcc = []
for x in acceptedLog:
    ipLolos(x, ipAcc)
ipAcc = set(ipAcc)


for x, y in counterIP.items():
    if x in ipAcc:
        print(f"{x} berhasil setelah gagal sebanyak, {y}x")

ipsort = urutan(counterIP)
usersort = urutan(invalidUser)
jamsort = urutan(jamRawan)

printHasil(ipsort, usersort, jamsort)