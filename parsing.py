def log(file):
    return "sshd" in file
    
def is_valid_login_line(line):
    return "for " in line and "from " in line and "port " in line

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

