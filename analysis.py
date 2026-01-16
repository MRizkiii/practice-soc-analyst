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