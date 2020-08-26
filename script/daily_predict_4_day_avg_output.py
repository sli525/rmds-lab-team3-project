import torch
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

day_input = 6
timelagging = 6
average_num = 4
feature_num = 16+2*(day_input-1)

class process_data:
    '''Process input file '''
    def __init__(self, input):
        self.input = input

    def input_table(self):
        filename = self.input
        zipcode_daily = pd.read_csv(filename, encoding="ISO-8859-1", dtype={'ZIP': str, 'date': str})
        zip = zipcode_daily['ZIP']
        date = zipcode_daily['date']  # we have to preserve the date
        del zipcode_daily['ZIP']
        del zipcode_daily['date']
        zipcode_daily = pd.DataFrame(zipcode_daily, dtype=float)  # change the type from 'int' to 'float'
        zipcode_daily['ZIP'] = zip
        zipcode_daily['date'] = date  # add date back
        del zipcode_daily['ave_new6_9after']
        del zipcode_daily['ave_new8_11after']
        return zipcode_daily

    def model_dist(self):
        zipcode = []  # save 'zip code' correlating to input point
        date = []     # save 'date' correlating to input point
        data_x = []  # input
        tot = []
        for key, values in data_dict.items():
            l = len(values)
            input_num = l - timelagging - average_num
            feature = []
            for i in range(input_num):
                first = True
                for j in range(day_input):
                    if first:
                        zipcode.append(values[i][-2])   # save 'zip code' correlating to ont input point
                        date.append(values[i][-1])      # save 'date' correlating to ont input point
                        # because we add 'date' back, the last feature is values[i][:-5] not values[i][:-4]
                        for k in values[i][:-3]:
                            feature.append(k)
                        first = False
                    else:
                        feature.append(values[i + j][0])
                        feature.append(values[i + j][1])
                tmp = []
                tmp.append(feature)
                data_x.append(tmp)  # one input point
                feature = []
        tot.append(zipcode)
        tot.append(date)
        tot.append(data_x)
        return tot

input_file = process_data('daily.csv')
zipcode_daily = input_file.input_table()
data_dict = {}  # key: 'zip', value: feature that belong to the key
for i, zipcode in enumerate(zipcode_daily[:]['ZIP']):
    if zipcode not in data_dict:
        data_dict[zipcode] = []
    feature = []
    for f in zipcode_daily.iloc[i]:
        feature.append(f)
    data_dict[zipcode].append(feature)

total_list = input_file.model_dist()
zipcode = total_list[0]
date = total_list[1]
data_x = total_list[2]
data_x_ls = []
for j in data_x:
    for i in j:
        data_x_ls.append(i)
data_x_df = pd.DataFrame(data_x_ls)
data_x_mean = data_x_df.mean()  # train dataset mean
data_x_std = data_x_df.std()    # train dataset std

for i in range(len(data_x)):    # using train_x mean and train_x std to normalize
    for j in range(len(data_x[i])):
        for k in range(len(data_x[i][j])):
            data_x[i][j][k] = (data_x[i][j][k] - data_x_mean[k]) / data_x_std[k]

data_x = torch.tensor(data_x)

# scale the output value back to its original size and cal the loss
def upscale(predict):
    x = predict[:]
    for i in range(len(predict)):
        x[i][0] = x[i][0] * torch.tensor(data_x_std[1]) + torch.tensor(data_x_mean[1])
    return x


"""     define LSTM model   """
class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # if batch_first=True, then input shape = (batch, seq, shape)
        self.lstm = torch.nn.LSTM(input_size=feature_num, hidden_size=64, num_layers=1, batch_first=True)
        self.linear = torch.nn.Linear(64 * 1, 32)
        self.linear1 = torch.nn.Linear(32, 1)

    def forward(self, x):
        # print(x.shape)
        x, _ = self.lstm(x)
        x = x.reshape(-1, 64 * 1)
        x = self.linear(x)
        x = self.linear1(x)
        return x


model = Net()
path = 'checkpoint_new.tar'
# load from file
checkpoint = torch.load(path)
model.load_state_dict(checkpoint['net'])
model.eval()
predict = np.array(model(data_x.float()).data)  # output
predict_upscale = upscale(predict)      # original scale output

date_list = []
for i in range(1,32):
    if i <=9:
        date_list.append('2020-03-' + str(0) +str(i))
    else:
        date_list.append('2020-03-' +str(i))
for i in range(1,31):
    if i <=9:
        date_list.append('2020-04-' + str(0) +str(i))
    else:
        date_list.append('2020-04-' +str(i))
for i in range(1,32):
    if i <=9:
        date_list.append('2020-05-' + str(0) +str(i))
    else:
        date_list.append('2020-05-' +str(i))
for i in range(1,31):
    if i <=9:
        date_list.append('2020-06-' + str(0) +str(i))
    else:
        date_list.append('2020-06-' +str(i))
for i in range(1,32):
    if i <=9:
        date_list.append('2020-07-' + str(0) +str(i))
    else:
        date_list.append('2020-07-' +str(i))
for i in range(1,32):
    if i <=9:
        date_list.append('2020-08-' + str(0) +str(i))
    else:
        date_list.append('2020-08-' +str(i))
for i in range(1,31):
    if i <=9:
        date_list.append('2020-09-' + str(0) +str(i))
    else:
        date_list.append('2020-09-' +str(i))
for i in range(1,32):
    if i <=9:
        date_list.append('2020-10-' + str(0) +str(i))
    else:
        date_list.append('2020-10-' +str(i))
for i in range(1,31):
    if i <=9:
        date_list.append('2020-11-' + str(0) +str(i))
    else:
        date_list.append('2020-11-' +str(i))
for i in range(1,32):
    if i <=9:
        date_list.append('2020-12-' + str(0) +str(i))
    else:
        date_list.append('2020-12-' +str(i))

date_list_new = []
for date_ in date:
    date_start = date_list[date_list.index(date_)+6]
    date_end = date_list[date_list.index(date_)+9]
    date_list_new.append(date_start)

out = pd.DataFrame()                            # generate table
out['ZIP'] = zipcode                            # zip code column
out['date'] = date_list_new    # date column
out['Predicted new cases'] = predict_upscale     # predicted new cases columns
pop = pd.read_csv('population.csv', index_col = False)  # population data
for i in range(out.shape[0]):
  for j in range(pop.shape[0]):
    if (out.at[i,'ZIP'] == pop.at[j,'ZIP']):
      out.at[i,'cases/population'] = 10000 * out.at[i,'Predicted new cases'] / pop.at[j,'population']
#get percentail for predicted risk score
min_score = min(out['cases/population'])
percent_25 = out['cases/population'].quantile(0.25)
percent_50 = out['cases/population'].quantile(0.5)
percent_75 = out['cases/population'].quantile(0.75)
risk_level = []

#define risk level
for i in range(out.shape[0]):
    score = out.iloc[i,-1]
    if score >= min_score and score < percent_25:
        level = '0'
    elif score >= percent_25 and score < percent_50:
        level = '1'
    elif score >= percent_50 and score < percent_75:
        level = '2'
    else:
        level = '3'
    risk_level.append(level)
out['risk_level'] = risk_level # add risk_level column to output file
output = out[['date','ZIP','cases/population','risk_level']]
output.columns = ['Timestamp','Region','Risk Score','Risk Level'] #rename the columns of table
output = output.sort_values(by=['Timestamp','Region'])
output.to_csv('daily_predict_4_day_avg_risk.csv',index=False)


