###FILTERING


def log(file):
    return "sshd" in file
    # return [x for x in file if "sshd" in x]
    
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

    parts = x.split()
    bulan = parts[0]
    tanggal = parts[1]
    jam = parts[2]

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
fullData = []
with open("auth.log", "r") as f:
    for x in f:
        if log(x) and is_valid_login_line(x):
            data = parsing(x)
            fullData.append(data)


def FailedLoginIPCount(x):
    tes = {}
    for i in x:
        ip = i["ip"]
        tes[ip] = tes.get(ip, 0) + 1
    return tes

def tes (x):
    tes = {}
    for i in x:
        usr = i["user"]
        tes[usr] = tes.get(usr, 0) + 1
    return tes

def TimeAttack(xx):
    tes = {}
    for x in xx:
        x = x["jam"]
        x = x.split(":")
        jam = x[0]
        tes[jam] = tes.get(jam, 0) + 1
    return tes


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

counterIP = FailedLoginIPCount(failedLog)
invalidUser = tes(invalidUserLog)
jamRawan = TimeAttack(failedLog)


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