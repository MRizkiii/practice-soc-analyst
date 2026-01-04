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

sample = []
newBulanAcc = []
newTanggalAcc = []
newJamAcc = []

newBulanFai = []
newTanggalFai = []
newJamFai = []

newJamInv = []
newBulanInv = []
newTanggalInv = []


def time(inti, bulan, tanggal, jam):
    for y in range(len(inti)):
        sample.append(list(filter(None, inti[y].split())))
    for x in sample:
        bulan.append(x[0])
        tanggal.append(x[1])
        jam.append(x[2])

    return bulan, tanggal, jam

time(berhasil, newBulanAcc, newTanggalAcc, newJamAcc)
time(gagal, newBulanFai, newTanggalFai, newJamFai)
time(invalid, newBulanInv, newTanggalInv, newJamInv )

def dataData(inti,newUserList, newIpList, newPortList):
    for x in inti:
        pos = 0
        while True:
            user = x.find('for ', pos)
            ip = x.find('from ', pos)
            port = x.find('port ', pos)

            if user == -1:
                break
        

            awalID = user + 4
            akhirID = x.find(' ', awalID)

            awalIP = ip + 5
            akhirIP = x.find(' ', awalIP)

            awalPort = port + 5
            akhirPort = x.find(" ", awalPort)

        
            if akhirID == -1:
                break
            
            newUserList.append(x[awalID:akhirID])
            newIpList.append(x[awalIP:akhirIP])
            newPortList.append(x[awalPort:akhirPort])
            pos = akhirID + 1

    return user, ip, port


newUserAcc = []
newIPAcc = []
newPortAcc = []

newUserFai = []
newIPFai = []
newPortFai = []

newUserInv = []
newIPInv = []
newPortInv = []

dataData(berhasil, newUserAcc, newIPAcc, newPortAcc )
dataData(gagal, newUserFai, newIPFai, newPortFai)
dataData(invalid, newUserInv, newIPInv, newPortInv)


dataBerhasilLog = []
dataGagalLog = []
dataInvalidLog = []

def fullData(container, Len, bulan, tanggal, jam, user, ip, port):
    for i in range(len(Len)):
        container.append(data(bulan[i], tanggal[i], jam[i], user[i], ip[i], port[i]))
        
    return bulan, tanggal, jam, user, ip, port

fullData(dataBerhasilLog, newUserAcc, newBulanAcc, newTanggalAcc, newJamAcc, newUserAcc, newIPAcc, newPortAcc)
fullData(dataGagalLog, newUserFai, newBulanFai, newTanggalFai, newJamFai, newUserFai, newIPFai, newPortFai)
fullData(dataInvalidLog, newUserInv, newBulanInv, newTanggalInv, newJamInv, newUserInv, newIPInv, newPortInv)


userLogin = []
userLoginTotal = {}
for x in dataBerhasilLog:
    x = x["user"]
    userLogin.append(x)
# for x in userLogin:
    # userLoginTotal[x] = userLoginTotal.get(x, 0) + 1


#GAGAL DATA
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


# InvalidLog)

# USER INVALID
userInvalid = []
userInvalidTotal = {}
for x in dataInvalidLog:
    x = x["user"]
    userInvalid.append(x)

for x in userInvalid:
    userInvalidTotal[x] = userInvalidTotal.get(x, 0) + 1

# print(userLoginTotal)
# print("////////////////////////////////////////")
# print(userGagalTotal)
# print("////////////////////////////////////////")
# print(userInvalidTotal)







