import csv
import requests
import pandas as pd
import sys
from bs4 import BeautifulSoup
from selenium  import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class Community:

  def __init__(self, url):
    self.url = url

  def google_func(self):
    ''' Extract target data from google mobility file'''
    Google_Mobility = pd.read_csv(self.url)
    Google_Mobility_LA= Google_Mobility[Google_Mobility['sub_region_2']=='Los Angeles County']
    Google_Mobility_LA=Google_Mobility_LA.iloc[:,[7,8,9,10,11,12,13]]
    mask = (Google_Mobility_LA['date'] >= '2020-04-30')
    Google_up_to_date = Google_Mobility_LA.loc[mask]
    return Google_up_to_date

  def apple_func(self):
    '''Extract target data from apple mobility file'''
    CSV_URL = self.url
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
        mask = (Apple_Mobility_LA['date'] >= '2020-04-30')
        Apple_up_to_date = Apple_Mobility_LA.loc[mask]
    return Apple_up_to_date

  def covid_func(self):
    '''Extract confirmed cases'''
    CSV_URL_1 = self.url
    with requests.Session() as s:
        download = s.get(CSV_URL_1)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        title = ['date','county','num','ZIP','confirmed cases']
        tot = []
        for row in my_list:
            if row[1] == 'Los Angeles' and row[0] >= '2020-04-30':
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
                'Hollywood','Hollywood Hills', 'Lynwood', 'Mar Vista', 'Monterey Park', 'North Hollywood', 'Reseda', 'Santa Clarita',
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
    return confirm_up_to_date

  def population_func(self):
    '''Import population and income level information to input file'''
    population = pd.read_csv(self.url)
    population = population.sort_values(by=['place'])
    population = population[['place','population','Population.Density','incomLev']]
    population.columns = ['ZIP','population','Population.Density','incomLev']
    return population

def combine_table(t1,t2,column):
    '''combine table'''
    table = pd.merge(t1,t2, on=column)
    return table

google_data = Community('https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv?cachebust=6ec44f00b5b4f6ad')
google = google_data.google_func()

url = 'https://covid19.apple.com/mobility'
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
soup = BeautifulSoup(driver.page_source,"html.parser")
item = soup.find('body')
div = item.find("div", {"class": "download-button-container"})
link = div.find('a')
link1 = link['href']

apple_data = Community(link1)
apple = apple_data.apple_func()
total_table = combine_table(apple, google,'date')

confirm_data = Community('https://raw.githubusercontent.com/datadesk/california-coronavirus-data/master/latimes-place-totals.csv')
confirm = confirm_data.covid_func()
total_table = combine_table(confirm,total_table,'date')

population_data = Community('population_income.csv')
popul = population_data.population_func()
total_table = combine_table(total_table, popul,'ZIP')

class update:
    '''add new columns to input file'''
    def __init__(self, table):
        self.table = table

    def new_case(self):
        '''add new confirmed cases column'''
        total = self.table
        case_adjust = []
        new_case_adjust = []
        tot = []
        for index in range(total.shape[0]):
            case_num = int(total.iloc[index,2]) / int(total.iloc[index,13])
            new_case_num = int(total.iloc[index,3]) / int(total.iloc[index,13])
            case_adjust.append(case_num)
            new_case_adjust.append(new_case_num)
        tot.append(case_adjust)
        tot.append(new_case_adjust)
        return tot

    def future_case(self):
        ''' add future cases column'''
        total = self.table
        ave_dict = {}
        tot_list = []
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
        tot_list.append(new6)
        tot_list.append(new7)
        tot_list.append(new8)
        return tot_list

case_column = update(total_table)
case_list = case_column.new_case()
case_adjust = case_list[0]
new_case_adjust = case_list[1]
total_table['cases_adjusted_by_pop'] = case_adjust
total_table['new_cases_adjusted_by_pop'] = new_case_adjust

future_list = case_column.future_case()
total_table['ave_new6_9after'] = future_list[0]
total_table['ave_new7_10after'] = future_list[1]
total_table['ave_new8_11after'] = future_list[2]
total_table.to_csv('daily.csv',index=False)






