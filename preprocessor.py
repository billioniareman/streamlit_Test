import re

import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APMapm]{2}\s-\s'
    #pattern = '(?:[01]\d|2[0123]):(?:[012345]\d):(?:[012345]\d)'
    dates=re.findall(pattern, data)
    dates = [date.replace('\u202F', '') for date in dates]
    message=re.split(pattern, data)[1:]
    df=pd.DataFrame({'user_message':message,'date':dates})
    df['date']=pd.to_datetime(df['date'], format="%d/%m/%y, %I:%M%p - ",dayfirst=True,errors='coerce')
    user=[]
    msg=[]
    for message in df['user_message']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            user.append(entry[1])
            msg.append(" ".join(entry[2:]))
        else:
            user.append("Group Notification")
            msg.append(entry[0])
    df['user']=user
    df['message']=msg
    df.drop(columns=['user_message'],inplace=True)
    df["year"]=df['date'].dt.year
    df["month"]=df['date'].dt.month_name()
    df['month_num']=df['date'].dt.month
    df["day"]=df['date'].dt.day
    df["hour"]=df['date'].dt.strftime('%I %p')
    df["minute"]=df['date'].dt.minute
    df['only_date']=df['date'].dt.date
    df['day_name']=df['date'].dt.day_name()
    df.drop(columns='date',inplace=True)
    
    period=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour=="11 PM":
            period.append(str(hour)+"-"+str("12 AM"))
        elif hour=="11 AM":
           period.append(str(hour)+"-"+str("12 PM"))
        else:
            period.append(str(hour) + "-" + str(int(hour.split()[0]) + 1) + " " + hour.split()[1])
    df['period']=period
    return df.reset_index() 
