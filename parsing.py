import codecs
import json

def c_parse(file_name:str):
    ### Инициализация переменных
    dictionary = {}       # Словарь для создания json
    word = ''       # Название объявления
    rooms=''        # Количество комнат
    square=''       # Площадь
    floor=''        # Этаж
    reg = ''        # Регион
    city = ''       # Город
    district = ''   # Район
    metro = ''      # Метро
    street = ''     # Улица
    house = ''      # Дом
    price = ''      # Стоимость
    id = ''         # ID объявления
    
    
    with open (file_name, "r", encoding="utf-8") as file:    
    #lines = [line.rstrip() for line in file]
        for line in file:
            # Заголовок объявления
            if '<span class="">' in line:
                i = line.find('<span class="">') + 15
                word = ''
                for j in range(i, i + 40):
                    if line[j] != '<':
                        word += line[j]
                    else:
                        break
                res = word.split()
                if len(res) > 4:
                    rooms = res[0][0]   # Количество комнат
                    square = res[2]     # Площадь помещения
                    floor = res[4]      # Этаж

                # Стоимость
                p = line.find('₽') - 12
                price_s = []
                for j in range(p, p + 12):
                    if line[j] != '<': price_s.append(line[j])
                    else: break
                
                price = ''
                for s in price_s:
                    if s != '\"' and s != '>':# and s != ' ':
                        price += s

            if "<a data-name=\"GeoLabel\" class=\"_93444fe79c--link--NQlVc\"" in line:
                # Регион
                reg_i = line.find('</a>, <a data-name="GeoLabel"') - 20
                reg = ''
                for u in range(reg_i, reg_i + 30):
                    if line[u] != '<': reg += line[u]
                    else: break

                # Город
                city_i = line.find('</a>, <a data-name="GeoLabel"', reg_i+50) -20
                city_m = ''
                for u in range(city_i, city_i + 20):
                    if line[u] != '<': 
                        if line[u] == '>': city_m += ' '
                        else: city_m += line[u]
                    else: break                    
                city = city_m.split()[1]
                
                # Район
                district_i = line.find('</a>, <a data-name="GeoLabel"', city_i + 50) -20
                district_m = ''
                for u in range(district_i, district_i + 30):
                    if line[u] != '<':
                        if line[u] == '>': district_m += ' '
                        else: district_m += line[u]
                    else: break
                if len(district_m.split()) < 3:
                    district = district_m.split()[0] + ' ' + district_m.split()[1]
                else:  district = district_m.split()[1] + ' ' + district_m.split()[2]
                
                # Метро
                metro_i = line.find('</a>, <a data-name="GeoLabel"', district_i + 50) -20
                metro = ''
                count = 0
                for u in range(metro_i, metro_i + 30):
                    if line[u] != '<':
                        if line[u] == '>': count +=1
                        if count > 0 and line[u] != '>': metro += line[u]                        
                    else: break
                #print(metro_m)
                
                # Улица                
                street_i = line.find('</a>, <a data-name="GeoLabel"', metro_i + 50) -20
                street = ''
                count = 0
                for u in range(street_i, street_i + 30):
                    if line[u] != '<':
                        if line[u] == '>': count +=1
                        if count > 0 and line[u] != '>': street += line[u]                        
                    else: break
                    
                # Дом
                house_i = line.find('</a></div></div><div data-name=\"GeneralInfoSectionRowComponent\"')-5
                house = ''
                count = 0
                for u in range(house_i, house_i + 30):
                    if line[u] != '<':
                        if line[u] == '>': count +=1
                        if count > 0 and line[u] != '>': house += line[u]                        
                    else: break
            
            # ID объявления                
            if 'https://kazan.cian.ru/sale/flat/' in line:
                id_i = line.find('https://kazan.cian.ru/sale/flat/')+32
                id = ''
                for u in range(id_i, id_i +10):
                    if line[u] != '/': id += line[u]
                    else: break
            
            # Номер страницы
            if ';offer_type=flat&amp;p=' in line:
                sheet_i = line.find(';offer_type=flat&amp;p=')+23
                sheet = ''
                for u in range(sheet_i, sheet_i +10):
                    if line[u] != '&': sheet += line[u]
                    else: break
            
            # Запись
            if word != '':  
                # построчная в CSV
                with open('parse_res.csv', 'a', encoding='utf-8') as csv_file:                    
                    csv_file.write(word + ';' + rooms + ';' + square + ';' + floor + ';' + \
                                   reg + ';' + city + ';' + district + ';' + metro + ';' + \
                                   street + ';' + house + ';' + price + ';' + id + ';' + \
                                   sheet + '\n')
                    csv_file.close()
                
                # в словарь
                dictionary[word] = {'rooms': rooms, 'square': square, 'floor': floor,
                                  'reg': reg, 'city': city, 'district': district,
                                  'metro': metro, 'street': street, 'house': house,
                                  'price': int(price.replace(' ', '')),
                                  'id': int(id), 'sheet': int(sheet)}                    
            word = ''
        
        # Запись словаря в json
        with codecs.open('parse_res.json', 'w', encoding='utf-8') as json_file:
            jstr = json.dumps(dictionary, indent=4).replace('%', '\\').encode('utf-8')            
            json_file.write(jstr.decode('unicode-escape'))
            json_file.close()            

# Точка входа
if __name__ == '__main__':
    c_parse('cian_data.html')
    print("Complete!")