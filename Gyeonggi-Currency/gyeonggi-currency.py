import csv, json, sqlite3


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

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
kind = []
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
                category = y[0].strip()
                if not hasNumbers(category) and "." not in category and category != '':
                    if category in ['여행', '숙박업']:
                        data['category'] = 'trip'
                        data['outputcat'] = '숙박업'
                    elif category in ['한식', '치킨', '떡류'] or '음식' in category or '식품' in category or category == '인삼':
                        data['category'] = 'food'
                        data['outputcat'] = '식품/음료'
                    elif category in ['학원', '서적문구', '교육서비스업', '교육서비스']:
                        data['category'] = 'edu'
                        data['outputcat'] = '교육'
                    elif category in ['병원', '약국', '의원', '보건위생', '기타의료기관', '보건업', '보건업 및 사회복지서비스업']:
                        data['category'] = 'med'
                        data['outputcat'] = '의료'
                    elif '유통' in category or category in ['편의점']:
                        data['category'] = 'shop'
                        data['outputcat'] = '마트/편의점'
                    elif '자동차' in category or '연료' in category or '수리' in category:
                        data['category'] = 'car'
                        data['outputcat'] = '자동차 정비/주유'
                    elif category in ['미용', '화장품']:
                        data['category'] = 'beauty'
                        data['outputcat'] = '미용/화장품'
                    elif '도매' in category or '소매' in category:
                        data['category'] = 'othershop'
                        data['outputcat'] = '기타판매'
                    else:
                        data['category'] = 'other'
                        data['outputcat'] = category
        result[regionKeys[storeItem[0]]].append(data)         
f.close()

conn = sqlite3.connect('store.db')
cur = conn.cursor()
with open("all.json", "w") as f:
    f.write(json.dumps(result, ensure_ascii=False))
for x in regionKeys.values():
    with open(x + ".json", "w") as f:
        data = {"region" : x, "data" : result[x]}
        f.write(json.dumps(data, ensure_ascii=False))
    cur.execute("DROP TABLE IF EXISTS " + x)
    cur.execute("create table " + x + "(name TEXT NOT NULL, phone TEXT, lat TEXT , lng TEXT, category text not null, outputcat text)")
    conn.commit()
    sql = 'insert into ' + x + ' values (?, ?, ? ,?, ? ,?)'
    for store in result[x]:
        if 'category' not in store.keys() or 'outputcat' not in store.keys():
            store['category'] = 'other'
            store['outputcat'] = '기타'
        if 'latitude' not in store.keys() or 'longitude' not in store.keys():
            store['latitude'] = None
            store['longitude'] = None
        if 'telephone' not in store.keys():
            store['telephone'] = None
        cur.execute(sql, (store['name'], store['telephone'], store['latitude'], store['longitude'], store['category'], store['outputcat']))

conn.commit()
cur.close()
conn.close()
