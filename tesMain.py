def log(file):
    ssh_log = []
    for x in file:
        if "sshd" in x:
            ssh_log.append(x)
    return ssh_log



def parsing(x):
    x= x.replace("  ", " ")
    pos = 0
    
    awal = x.find("for ", pos)
    if awal == -1 : return None
    Auser = awal + 4
    Buser = x.find(" ", Auser)
    if Buser == -1 : return None


    Aip = x.find("from ", Buser) + 5
    if Aip == -1 : return None

    Bip = x.find(" ", Aip)
    if Bip == -1 : return None

    Aport = x.find("port ", Bip) + 5
    if Aport == -1 : return None

    Bport = x.find(" ", Aport)
    if Bport == -1 : return None

    pos = Bport


    bulan = x.split()[0]
    tanggal = x.split()[1]
    jam = x.split()[2]

    return {
        "bulan" : bulan,
        "tanggal" : tanggal,
        "jam" : jam,
        "user" : x[Auser:Buser],
        "ip" : x[Aip:Bip],
        "port" : x[Aport:Bport]
    }



with open("auth.log", "r") as f:
    logs = f.readlines()
    sshLog = log(logs)
    print(sshLog)
  
fullData = []

for line in sshLog:
    data = parsing(line)
    fullData.append(data)
    print(fullData)
    

    





# for x in 
#     parsing(x)