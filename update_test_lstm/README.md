
 
 
 
 ### Covid-19_Risk_Umich_ZJU
 We have three steps to get a up-to-date output file

1. Web Scraping and data preprocessing
`python data _preprocessing.py`

2. Train model
- train daily level dataset to generate an updated checkpoint file

`python main.py --mode train --type daily`

- test daily level dataset

`python main.py --mode test --type daily`

3. run output file to get risk level

`python daily_predict_4_day_avg_output.py`
