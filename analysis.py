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

    jam = jam.split(":")
    perhari = int(tgl) * 86400
    perjam = int(jam[0]) * 3600
    permenit = int(jam[1]) * 60
    perdetik = int(jam[2]) * 1

    jam_sekarang = perhari + perjam + permenit + perdetik

    value = data.get(ip, [])
    value.append(jam_sekarang)

    realValue = []
    for jam_lama in value:
        if jam_sekarang - jam_lama <= 60 :
            realValue.append(jam_lama)

    data[ip] = realValue

    if len(realValue) >= 3:
        return True, len(realValue)
    return False, 0
      