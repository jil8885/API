#stop : Hanyang Univ - 216000719, Start - 217000282, Suwon - 202000106
# route : 707-1 : 216000070
stop = {"Ansan" : 217000282, "Hanyang" : 216000719, "Suwon" : 202000106}
route = 216000070
import os, requests, pickle
from datetime import datetime
from bs4 import BeautifulSoup
weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
result = {}
busauth = os.getenv('busauth')
log = open('log.txt', 'a')
# 데이터 로드
try:
    with open('data', 'rb') as f:
        data = pickle.load(f)
except:
    data = {"suwon" : '', "ansan": '', "hanyang": ''}
# 수원역 출발 시간
stop_id = stop["Suwon"]
url = f"http://openapi.gbis.go.kr/ws/rest/busarrivalservice?serviceKey={busauth}&stationId={stop_id}&routeId={route}"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml-xml')
if soup.find('plateNo1') != None:
    plateno1 = soup.find('plateNo1').text
else:
    plateno1 = ''
now = datetime.now()
if data["suwon"] != plateno1:
    print("통과 : {}-{}-{}".format(weekdays[now.weekday()], now.hour, now.minute))
    log.write("수원 통과 : {}-{}-{}".format(weekdays[now.weekday()], now.hour, now.minute))
else:
    print("진행중 : {}-{}-{}".format(weekdays[now.weekday()], now.hour, now.minute))
result["suwon"] = plateno1

# 한양대 출발 시간
stop_id = stop["Hanyang"]
url = f"http://openapi.gbis.go.kr/ws/rest/busarrivalservice?serviceKey={busauth}&stationId={stop_id}&routeId={route}"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml-xml')
if soup.find('plateNo1') != None:
    plateno1 = soup.find('plateNo1').text
else:
    plateno1 = ''
if data["hanyang"] != plateno1:
    print("통과 : {}-{}-{}".format(weekdays[now.weekday()], now.hour, now.minute))
    log.write("한양대 통과 : {}-{}-{}".format(weekdays[now.weekday()], now.hour, now.minute))
else:
    print("진행중 : {}-{}-{}".format(weekdays[now.weekday()], now.hour, now.minute))
result["hanyang"] = plateno1

# 신안산대 출발시간
stop_id = stop["Ansan"]
url = f"http://openapi.gbis.go.kr/ws/rest/busarrivalservice?serviceKey={busauth}&stationId={stop_id}&routeId={route}"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml-xml')
if soup.find('plateNo1') != None:
    plateno1 = soup.find('plateNo1').text
else:
    plateno1 = ''

if data["ansan"] != plateno1:
    print("통과 : {}-{}-{}".format(weekdays[now.weekday()], now.hour, now.minute))
    log.write("안산 통과 : {}-{}-{}".format(weekdays[now.weekday()], now.hour, now.minute))
else:
    print("진행중 : {}-{}-{}".format(weekdays[now.weekday()], now.hour, now.minute))

result["ansan"] = plateno1

with open('data', 'wb') as f:
    pickle.dump(result, f)

log.close()