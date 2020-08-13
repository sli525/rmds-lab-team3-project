# Risk-Score-Team3-UMichZJU

* Team Members: Pushin Huang, Nanbo Li, Shanshan Li
* Project Manager: Yula Guo
* Open source project in collaboration with University of Michigan, ZJU Team. Link to their project found [here](https://grmds.org/node/744).*

## Technical Solutions Description

We built a data modeling pipeline that integrates case count data, mobility data, and social-economic data for forecasting new cases. Next, we converted the data into community level and run a LSTM model, and the detailed modeling process is as follows: 
We first normalized all features and randomly divided the whole dataset into training set, validation set and test set, respectively. The proportions of the training set, validation set and test set is 70%,15%,15%. We use Adam optimizer to train the LSTM network. The initial learning rate is 0.0003, and we used an adaptive learning rate schedule. Specifically, when validation loss doesn’t decrease for seven epochs, we reduced the learning rate. The number of training epoch is set to 1,500. The training process was early stopped when validation loss doesn’t decrease for 24 epochs. 
The regional risk score is defined as predicted new cases divided by the population. After getting the risk score, we sorted the risk score and used the binning technique to transform the score into 4 risk level (0,1,2,3) as our final output.	

## Setup

 We have three steps to get a up-to-date output file

1. Web Scraping and data preprocessing

`python data_preprocessing.py`

2. Train model
- train daily level dataset to generate an updated checkpoint file

`python main.py --mode train --type daily`

- test daily level dataset

`python main.py --mode test --type daily`

3. run output file to get risk level

`python daily_predict_4_day_avg_output.py`

## Input

Data Overview - Key Features

| Feature name  | Description of feature|
| ------------- | ------------- |
| Confirmed cases      		| Cureent number of infections   |
| Income Level         		| Income level from rank 1-3     |
| Population           		| Population for each community  |
| Density_Per_Sq_Mile  		| Population / land area         |
| Driving/Transit/Walking	| a relative walking volumn of directions requests per location |
| Driving/Transit/Walking	| compared to a baseline volumn on Jan 13th, 2020.  |
| workplaces_percent_change_from_baseline  | Mobility trends for places of work |
| Residential_percent_change_from_baselin  | Mobility trends for places of residence |

## Output

Output file: ** [risk_level.csv](https://github.com/sli525/rmds-lab-team3-project/blob/master/output%20file/risk_level.csv)

**Timestamp:**
- Date of newly updated data

**Region:**
- Community region in LA County

**Risk Score:**
- Risk score for each region; calculated by 10,000x number of infectious people predicted by LSTM model and divided by population size for each region.

**Risk Score Level:**
- Risk level categorized as (0,1,2,3) levels according the risk score percentile rank

## Workflow

![workflow](https://github.com/sli525/rmds-lab-team3-project/blob/master/RMDS_Workflow.png)

