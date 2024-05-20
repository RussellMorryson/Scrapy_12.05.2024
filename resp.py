import requests

url_1 = 'https://kazan.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p='
url_2 = '&region=4777&room1=1'

for i in range(10):    
    response = requests.get(url_1 + str(i+1) + url_2)
    data = response.text
    with open("cian_data.html", 'a', encoding="utf-8") as f:    
        f.write(data)       
        f.close()
    response.close()
    print("Complete!")