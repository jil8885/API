import csv, json


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


f = open('ggcurrency.csv', 'r', encoding='cp949')
reader = csv.reader(f)
result = {}
regionKeys = {
    "가평군" : "gapyeong",
    "고양시" : "goyang",
    "과천시" : "gwacheon",
    "광명시" : "gwangmyeong",
    "광주시" : "gwangju",
    "구리시" : "guri",
    "군포시" : "gunpo",
    "김포시" : "gimpo",
    "남양주시" : "namyangju",
    "동두천시" : "dongdoocheon",
    "부천시" : "bucheon",
    "성남시" : "seongnam",
    "수원시" : "suwon",
    "시흥시" : "siheung",
    "안산시" : "ansan",
    "안성시" : "anseong",
    "안양시" : "anyang",
    "양주시" : "yangju",
    "양평군" : "yangpyeong",
    "여주시" : "yeoju",
    "연천군" : "yeoncheon",
    "오산시" : "osan",
    "용인시" : "yongin",
    "의왕시" : "uiwang",
    "의정부시" : "uijeongbu",
    "이천시" : "icheon",
    "파주시" : "paju",
    "평택시" : "pyeongtack",
    "포천시" : "pocheon",
    "하남시" : "hanam",
    "화성시" : "hwaseong"
}
result = {}
for line in reader:
    storeItem = list(line)
    if storeItem[0] in regionKeys.keys():
        if regionKeys[storeItem[0]] not in result.keys():
            result[regionKeys[storeItem[0]]] = []
        data = {}
        data["name"] = storeItem[1]
        for x in storeItem[2:]:
            if x.startswith("경기도"):
                pass
            elif x.startswith("031-") or x.startswith("02-") or x.startswith("070-") or x.startswith("010-"):
                data["telephone"] = x
            elif x.isdigit() or isfloat(x):
                if float(x) < 100:
                    data["latitude"] = x
                elif float(x) > 100:
                    data["longitude"] = x
                else:
                    pass
            elif len(x.split("-")) == 3 and x.split("-")[0].isdigit() and x.split("-")[1].isdigit() and x.split("-")[2].isdigit():
                pass

            elif "-" in x or "," in x:
                if "-" in x:
                    y = x.split("-")
                else:
                    y = x.split(",")
                data["bigCategory"] = y[0].strip()
        result[regionKeys[storeItem[0]]].append(data)         
f.close()

with open("all.json", "w") as f:
    f.write(json.dumps(result, ensure_ascii=False))
for x in regionKeys.values():
    with open(x + ".json", "w") as f:
        data = {"region" : x, "data" : result[x]}
        f.write(json.dumps(data, ensure_ascii=False))

