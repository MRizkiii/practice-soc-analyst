def log(file):
    return [x for x in file if "sshd" in x]

def is_valid_login_line(line):
    return "for " in line and "from " in line and "port " in line

def parsing(x):
    x = x.replace("  ", " ")

    Auser = x.find("for ") + 4
    Buser = x.find(" ", Auser)

    Aip = x.find("from ", Buser) + 5
    Bip = x.find(" ", Aip)

    Aport= x.find("port ", Bip) + 5
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
        "bulan" : bulan,
        "tanggal" : tanggal,
        "jam" : jam,
        "user" : user,
        "ip" : x[Aip:Bip],
        "port" : x[Aport:Bport],
        "status" : status
    }

# def FailedLoginIPCount(line):


with open("auth.log", "r") as f:
    logs = f.readlines()
    sshLog = log(logs)

fullData = []
for line in sshLog:
    if not is_valid_login_line(line):
        continue

    data = parsing(line)
    fullData.append(data)


for x in fullData:
    if x["status"] ==  "unknown":
        print(x)

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

CounterIpFailed = []
counterIP = {}

for x in failedLog:
    CounterIpFailed.append(x["ip"])    
for x in CounterIpFailed:
    counterIP[x] = counterIP.get(x, 0)+1
sorted_ip = sorted(counterIP.items(), key=lambda item: item[1], reverse=True)

print("=== TOP ATTACKER IPs ===")
for ip, count in sorted_ip[:10]:
    print(f"IP: {ip} | Total Serangan: {count}")

allInvalidUser = []
countInvUser = {}
for x in invalidUserLog:
    allInvalidUser.append(x["user"])
for x in allInvalidUser:
    countInvUser[x] = countInvUser.get(x, 0) +1
sorted_user = sorted(countInvUser.items(), key=lambda item: item[1], reverse=True)


print("=== TOP ATTACKED USER ===")
for user, count in sorted_user[:10]: 
    print(f"User: {user} | Total Serangan: {count}")

ip_accepted = []
for x in fullData:
    if x["status"] == "Accepted password":
        ip_accepted.append(x["ip"])

ip_accepted = set(ip_accepted)

for ip, total in counterIP.items():
    if ip in ip_accepted:
        print(f"IP : {ip}, pernah gagak {total}x, dan berhasil")

jam_rawan = []

for x in failedLog:
    jam_rawan.append(x["jam"])

jam_rawan_count = {}
for x in jam_rawan:
    x = x.split(":")
    jam = x[0]
    jam_rawan_count[jam] = jam_rawan_count.get(jam , 0) + 1

urut = sorted(jam_rawan_count.items(), key=lambda item: item[1], reverse=True)

print("=== JAM PALING RAWAN SERANGAN ===")
for x, y in urut[:10]:
    print(f" JAM {x} di serang {y}x")

# print(urut)


# print(jam_rawan_count)