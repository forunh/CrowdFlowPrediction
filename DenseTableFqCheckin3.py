import DensePrediction
import json
import datetime
import csv

allPeriod = 288
dayUseToPredict = 14

predictDayStr = "2017-02-05"
predictDate = datetime.datetime.strptime(predictDayStr, "%Y-%m-%d")

table = []
prediction = {}
prediction['predict'] = []
csvPredict = []
csvDate = []

havePredictDay = 0

def roundToTime(len):
    if(len>0):
        time = datetime.datetime(2000, 1, 1, 0, 0, 0)
        len = (len-1)*5
        
        time = time + datetime.timedelta(minutes=len)
        return time.strftime('%H:%M')
    return None

filename ="fqCheckinFile_5FEB_CentralWorld.1"

with open(filename+'.json') as json_data:
    checkinJSON = json.load(json_data)
    CheckinList = checkinJSON['checkin']
    CheckinList.sort(key=lambda item:item['date'],reverse=True)
    #init table for predict
    for dayGet in CheckinList:  
        dayGetDate = datetime.datetime.strptime(dayGet['date'], "%Y-%m-%d")       
        if dayGetDate <= predictDate:
            dayList = dayGet['dense']
            table.insert(0, dayList)
            if dayGetDate == predictDate:
                havePredictDay = 1
            if len(table) == dayUseToPredict+havePredictDay:
                break
    #prediction
    if len(table) > 0+havePredictDay:           
        predict = DensePrediction.findNextDense(table)
        allPeriod = 288
        last_length = len(table[-1])
        if last_length == allPeriod:
            table.append([predict])
        else:
            table[-1].append(predict)
    else:
        print("have not enough data to predict")

    predictTime = roundToTime(len(table[-1]))
    prediction['predict'].append({"date":predictDayStr,"time":predictTime,"dense":predict}) 

    #output prediction
    with open('predict_'+filename+'.json', 'w') as outfile:
        json.dump(prediction, outfile)
    
    with open('predict_'+filename+'.csv', 'w', newline='') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(("",predictDayStr))
        a.writerow((str(predictTime),str(predict)))
    # print(csvRow)
