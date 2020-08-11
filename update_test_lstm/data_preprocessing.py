import csv
import requests
import pandas as pd
import sys


#google
CSV_URL = 'https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv?cachebust=6ec44f00b5b4f6ad'
with requests.Session() as s:
    download = s.get(CSV_URL)

    decoded_content = download.content.decode('utf-8')

    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    tot = []
    for row in my_list:
        if row[3] == 'Los Angeles County':
            row.remove('')
            row.remove('')
            tot.append(row)
    Google_Mobility = pd.DataFrame(tot)
    Google_Mobility_LA = Google_Mobility.iloc[:, [5,6,7, 8, 9, 10, 11]]
    Google_Mobility_LA.columns = ['date','retail_and_recreation_percent_change_from_baseline',
                                  'grocery_and_pharmacy_percent_change_from_baseline',
                                  'parks_percent_change_from_baseline','transit_stations_percent_change_from_baseline',
                                  'workplaces_percent_change_from_baseline','residential_percent_change_from_baseline']
    mask = (Google_Mobility_LA['date'] >= '2020-07-27')
    Google_up_to_date = Google_Mobility_LA.loc[mask]


#apple
CSV_URL = 'https://covid19-static.cdn-apple.com/covid19-mobility-data/2014HotfixDev8/v3/en-us/applemobilitytrends-2020-08-08.csv'
with requests.Session() as s:
    download = s.get(CSV_URL)

    decoded_content = download.content.decode('utf-8')

    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    tot = []
    title = my_list[0][6:]
    for row in my_list:
        if row[1] == 'Los Angeles':
            tot.append(row[6:])
    Apple_Mobility = pd.DataFrame(tot,columns=title)
    Apple_Mobility_LA = Apple_Mobility.transpose()
    Apple_Mobility_LA = Apple_Mobility_LA.reset_index()
    Apple_Mobility_LA.rename(columns={'index':'date',0: 'driving', 1: 'transit', 2: 'walking'}, inplace=True)
    mask = (Apple_Mobility_LA['date'] >= '2020-07-27')
    Apple_up_to_date = Apple_Mobility_LA.loc[mask]

total = pd.merge(Apple_up_to_date, Google_up_to_date, on='date')

#covid19 confirmed cases
CSV_URL = "https://raw.githubusercontent.com/datadesk/california-coronavirus-data/master/latimes-place-totals.csv"
with requests.Session() as s:
    download = s.get(CSV_URL)

    decoded_content = download.content.decode('utf-8')

    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    title = ['date','county','num','ZIP','confirmed cases']
    tot = []
    for row in my_list:
        if row[1] == 'Los Angeles' and row[0] >= '2020-07-27':
            tot.append(row[0:5])
    confirm_num = pd.DataFrame(tot,columns=title)
    confirm_up_to_date = confirm_num[['date','ZIP','confirmed cases']]
    target = ['Alhambra', 'Arcadia', 'Beverly Hills', 'Boyle Heights', 'Carson', 'Diamond Bar', 'Encino', 'Gardena',
              'Glendale', 'Glendora',
              'Granada Hills', 'Inglewood', 'La Mirada', 'Lancaster', 'Manhattan Beach', 'Melrose', 'Northridge',
              'San Dimas', 'San Pedro',
              'Santa Monica', 'Sherman Oaks', 'Silver Lake', 'Tarzana', 'Torrance', 'Venice', 'West Adams',
              'West Hills', 'West Hollywood',
              'West Vernon', 'Westchester', 'Altadena', 'Baldwin Hills', 'Brentwood', 'Culver City', 'Eagle Rock',
              'Hollywood',
              'Hollywood Hills', 'Lynwood', 'Mar Vista', 'Monterey Park', 'North Hollywood', 'Reseda', 'Santa Clarita',
              'Woodland Hills',
              'Sylmar', 'Walnut', 'Beverlywood', 'Burbank', 'Calabasas', 'Castaic', 'Covina', 'Crestview',
              'East Los Angeles', 'Echo Park',
              'Hancock Park', 'Hawthorne', 'Lawndale', 'Lomita', 'Palms', 'Playa Vista', 'South El Monte',
              'Stevenson Ranch', 'Studio City',
              'Tujunga', 'University Park', 'Valley Glen', 'Van Nuys', 'Vermont Knolls', 'Westwood', 'Whittier',
              'Century City', 'El Segundo',
              'Lake Balboa', 'Lakewood', 'Miracle Mile', 'Park La Brea', 'Redondo Beach', 'San Fernando',
              'South Whittier', 'Winnetka',
              'Del Rey', 'La Canada Flintridge', 'La Verne', 'Montebello', 'Sun Valley', 'Sunland', 'Vermont Vista',
              'Vernon Central',
              'West Covina', 'Westlake', 'Bellflower', 'Canoga Park', 'East Hollywood', 'Los Feliz', 'Paramount',
              'Rancho Palos Verdes',
              'South Gate', 'Agoura Hills', 'Duarte', 'Exposition Park', 'Hyde Park', 'Lincoln Heights', 'Palmdale',
              'South Park',
              'Wilshire Center', 'Canyon Country', 'Claremont', 'Downey', 'Harbor Gateway', 'Harvard Heights',
              'Highland Park',
              'La Puente', 'Norwalk', 'Pico Rivera', 'Porter Ranch', 'San Gabriel', 'Wholesale District', 'Willowbrook',
              'Arleta',
              'Bell Gardens', 'Glassell Park', 'Panorama City', 'Pomona', 'Valinda', 'Watts', 'Azusa', 'Bell',
              'Chatsworth',
              'Hacienda Heights', 'Harbor City', 'Leimert Park', 'Maywood', 'Monrovia', 'North Hills', 'Pacoima',
              'Avalon', 'Baldwin Park',
              'Bassett', 'Central', 'El Monte', 'El Sereno', 'Harvard Park', 'Lake Los Angeles', 'Rosemead',
              'Rowland Heights', 'Temple City',
              'Acton', 'Cerritos', 'Cloverdale/Cochran', 'Compton', 'Downtown', 'Huntington Park', 'Koreatown',
              'Mt. Washington', 'Pasadena',
              'South Pasadena', 'Wilmington']

    confirm_up_to_date = confirm_up_to_date[confirm_up_to_date['ZIP'].isin(target)]
    confirm_up_to_date = confirm_up_to_date.sort_values(by=['ZIP','date'])
    place_dict = {}
    for index in range(confirm_up_to_date.shape[0]):
        key = confirm_up_to_date.iloc[index,1]
        if key not in place_dict:
            place_dict[key] = []
            place_dict[key].append(confirm_up_to_date.iloc[index,2])
        else:
            place_dict[key].append(confirm_up_to_date.iloc[index, 2])
    new = []
    for key in place_dict:
        value = place_dict[key]
        count = 0
        for i in value:
            if count ==0:
                new.append(10000)
                count += 1
            else:
                num = int(i) - int(value[count-1])
                new.append(num)
                count += 1
    confirm_up_to_date['new_confirmed_cases'] = new
    mask = (confirm_up_to_date['new_confirmed_cases'] != 10000)
    confirm_up_to_date = confirm_up_to_date.loc[mask]
    confirm_up_to_date = confirm_up_to_date.sort_values(by=['date','ZIP'])
    total = pd.merge(confirm_up_to_date, total, on='date')

#population and income
population = pd.read_csv('econ_level.csv')
population = population.sort_values(by=['place'])
population = population[['place','population','Population.Density','incomLev']]
population.columns = ['ZIP','population','Population.Density','incomLev']
total = pd.merge(total, population, on='ZIP')

case_adjust = []
new_case_adjust = []
for index in range(total.shape[0]):
    case_num = int(total.iloc[index,2]) / int(total.iloc[index,13])
    new_case_num = int(total.iloc[index,3]) / int(total.iloc[index,13])
    case_adjust.append(case_num)
    new_case_adjust.append(new_case_num)
total['cases_adjusted_by_pop'] = case_adjust
total['new_cases_adjusted_by_pop'] = new_case_adjust

#ave_new7_10after,ave_new6_9after,ave_new8_11after column
ave_dict = {}
new6 = []
new7 = []
new8 = []
for index in range(total.shape[0]):
    key = total.iloc[index, 1]
    if key not in ave_dict:
        ave_dict[key] = []
        ave_dict[key].append(total.iloc[index, 3])
    else:
        ave_dict[key].append(total.iloc[index, 3])
for k in ave_dict:
    value = ave_dict[k]
    count = 0
    for i in value:
        if count + 11 <= len(value) - 1:
            num6 = (value[count + 6] + value[count + 7] + value[count + 8] + value[count + 9]) / 4
            new6.append(num6)
            num7 = (value[count + 7] + value[count + 8] + value[count + 9] + value[count + 10]) / 4
            new7.append(num7)
            num8 = (value[count + 8] + value[count + 9] + value[count + 10] + value[count + 11]) / 4
            new8.append(num8)
        elif count + 10 <= len(value) - 1:
            num6 = (value[count + 6] + value[count + 7] + value[count + 8] + value[count + 9]) / 4
            new6.append(num6)
            num7 = (value[count + 7] + value[count + 8] + value[count + 9] + value[count + 10]) / 4
            new7.append(num7)
            new8.append(0)
        elif count + 9 <= len(value) - 1:
            num6 = (value[count + 6] + value[count + 7] + value[count + 8] + value[count + 9]) / 4
            new6.append(num6)
            new7.append(0)
            new8.append(0)
        else:
            new6.append(0)
            new7.append(0)
            new8.append(0)
        count += 1

total['ave_new6_9after'] = new6
total['ave_new7_10after'] = new7
total['ave_new8_11after'] = new8
print(total.head(5))
total = total.sort_values(by='date')
total.to_csv('daily.csv',index=False)