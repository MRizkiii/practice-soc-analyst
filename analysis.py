def count_stats(data_list, key):
    tes = {}
    for item in data_list:
        val = item[key]
        if key == "jam":
            val = val.split(":")[0]
            
        tes[val] = tes.get(val, 0) + 1
    return tes
def urutan(isi_dict):
    return sorted(isi_dict.items(), key=lambda x: x[1], reverse=True)

def brute_force_detected(x, data):
    jam = x["jam"]
    ip = x["ip"]
    tgl = x["tanggal"]
    user = x["user"]

    jam = jam.split(":")
    perhari = int(tgl) * 86400
    perjam = int(jam[0]) * 3600
    permenit = int(jam[1]) * 60
    perdetik = int(jam[2]) * 1

    jam_sekarang = perhari + perjam + permenit + perdetik

    value = data.get(ip, [])
    value.append((jam_sekarang, user))

    realValue = []
    for waktu_lama, user_lama in value: # Bongkar paketnya di sini
        if jam_sekarang - waktu_lama <= 60:
            realValue.append((waktu_lama, user_lama)) # Masukin lagi paketnya ke list baru

    data[ip] = realValue

    if len(realValue) >= 5:
        return True, len(realValue)
    return False, 0


def loginSuccess(x, container):
    ip = x["ip"]
    jam = x["jam"]
    user = x["user"]

    value = container.get(ip, [])
    value.append((jam, user))
    container[ip] =  value
    
def corelation(accept, fail, hasil):
    for x in accept:
        if x in fail:
            hasil[x] = accept[x]


# def analyze_threat_level(ip, data_failed, data_success):


    