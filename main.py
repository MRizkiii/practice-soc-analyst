with open("auth.log", "r") as f:
    logs = f.readlines()
sshLog = []
for x in logs:
    x = x.strip()
    if "sshd" in x:
        sshLog.append(x)

#INTI
berhasil = []
gagal = []
invalid = []

#MENGELOMPOKAN
for x in sshLog:
    if "Accepted password" in x:
        berhasil.append(x)
    if "Failed password for" in x:
        if "invalid" not in x:
            gagal.append(x)
    if "Failed password for invalid" in x:
        invalid.append(x)


#USER_DATA
def data(bulan, tanggal, jam, user, ip, port):
    return{
        "bulan" : bulan,
        "tanggal" : tanggal,
        "jam" : jam,
        "user" : user,
        "ip" : ip,
        "port" : port
    }

#DATA LOGIN
dataBerhasilLog = []
for line in berhasil:
    x = line.split()
    dataBerhasilLog.append(data(x[0], x[1], x[2], x[8], x[10], x[12]))

# print(dataBerhasilLog)
# for x in dataBerhasilLog:
#     x = x["user"]
#     print(x)

#USER LOGIN
userLogin = []
userLoginTotal = {}
for x in dataBerhasilLog:
    x = x["user"]
    userLogin.append(x)
for x in userLogin:
    userLoginTotal[x] = userLoginTotal.get(x, 0) + 1


#GAGAL DATA
dataGagalLog = []
for x in gagal:
    x = x.split()
    if x[8] != 'times:':
        dataGagalLog.append(data(x[0], x[1], x[2], x[8], x[10], x[12]))


# for x in dataGagalLog:
#      x = x['user']
#      print(x)

#USER GAGAL
userGagal = []
userGagalTotal = {}
for x in dataGagalLog:
    userGagal.append(x["user"])
for x in userGagal:
    userGagalTotal[x] = userGagalTotal.get(x, 0) + 1

#INVALID DATA


# print(invalid)

newInvalid = []
for y in range(len(invalid)):
    newInvalid.append(list(filter(None, invalid[y].split())))

# print(newInvalid)


botInvalid = []
realInvalid = []
for x in newInvalid:
    if x[11] != "from":
        botInvalid.append(x)
    else:
        realInvalid.append(x)

# print(realInvalid)

dataInvalidLog = []
for x in realInvalid:
    # print(x[10])
    dataInvalidLog.append(data(x[0], x[1], x[2], x[10], x[12], x[14]))

# print(dataInvalidLog)

# USER INVALID
userInvalid = []
userInvalidTotal = {}
for x in dataInvalidLog:
    x = x["user"]
    userInvalid.append(x)

for x in userInvalid:
    userInvalidTotal[x] = userInvalidTotal.get(x, 0) + 1

print(userLoginTotal)
print("////////////////////////////////////////")
print(userGagalTotal)
print("////////////////////////////////////////")
print(userInvalidTotal)







