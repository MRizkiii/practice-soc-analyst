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
    perhari = int(tgl) * 8760
    perjam = int(jam[0]) * 3600
    permenit = int(jam[1]) * 60
    perdetik = int(jam[2]) * 1

    jam = perhari+perjam + permenit + perdetik
    
    kantong = data.get(ip, [])
    kantong_baru = []
    for y in kantong:
        if jam - y <= 60:
            kantong_baru.append(y)

    kantong_baru.append(jam)
    data[ip] = kantong_baru


    
    