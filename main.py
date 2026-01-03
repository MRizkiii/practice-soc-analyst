with open("auth.log", "r") as f:
    logs = f.readlines()

sshLog = []

for x in logs:
    x = x.strip()
    if "sshd" in x:
        sshLog.append(x)
        # print(x)


berhasil = []
gagal = []
invalid = []

for x in sshLog:
    if "Accepted password" in x:
        berhasil.append(x)
    if "Failed password for invalid" in x:
        invalid.append(x)

dataBerhasilLog = []

def data(bulan, tanggal, jam, user, ip, port):
    return{
        "bulan" : bulan,
        "tanggal" : tanggal,
        "jam" : jam,
        "user" : user,
        "ip" : ip,
        "port" : port
    }

for line in berhasil:
    x = line.split()
    dataBerhasilLog.append(data(x[0], x[1], x[2], x[8], x[10], x[12]))

# print(dataBerhasilLog)

userLogin = []

userLoginTotal = {}

for x in dataBerhasilLog:
    x = x["user"]
    userLogin.append(x)


for x in userLogin:
    userLoginTotal[x] = userLoginTotal.get(x, 0) + 1
    
# print(userLoginTotal)

dataGagalLog = []


for x in sshLog:
    if "Failed password for" in x:
        if "invalid" not in x:
            gagal.append(x)    
# print(gagal)


userGagal = []
userGagalTotal = {}

for x in gagal:
    x = x.split()
    dataGagalLog.append(data(x[0], x[1], x[2], x[8], x[10], x[12]))

# print(dataGagalLog)

for x in dataGagalLog:
    userGagal.append(x["user"])

for x in userGagal:
    userGagalTotal[x] = userGagalTotal.get(x, 0) + 1

# print(userGagal)
print(userGagalTotal)