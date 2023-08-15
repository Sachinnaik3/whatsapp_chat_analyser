import re
import pandas as pd


def preprocessor(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APapMm]{2}\s-\s'
    massage = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    def convert_year(date_string):
        parts = date_string.split(', ')
        if len(parts) == 2:
            date_part, time_part = parts
            date_parts = date_part.split('/')
            if len(date_parts) == 3:
                year = date_parts[2]
                if len(year) == 2:
                    year = '20' + year if int(year) > 20 else '20' + year
                    date_parts[2] = year
                    new_date = '/'.join(date_parts) + ', ' + time_part
                    return new_date
        return date_string

    # Convert the list of date strings to pandas datetime format
    converted_dates = [convert_year(date) for date in dates]
    
    # Try both 12-hour and 24-hour formats for parsing the dates
    try:
        df = pd.DataFrame({"user_message": massage, "date": pd.to_datetime(converted_dates, format='%m/%d/%Y, %I:%M %p - ')})
    except ValueError:
        try:
            df = pd.DataFrame({"user_message": massage, "date": pd.to_datetime(converted_dates, format='%m/%d/%Y, %I:%M %p')})
        except ValueError:
            df = pd.DataFrame({"user_message": massage, "date": pd.to_datetime(converted_dates, format='%d/%m/%Y, %H:%M - ')})
            
    user = []
    massage = []
    for message in df["user_message"]:
        entry = re.split("([\w\W]+?):\s", message)
        if entry[1:]:
            user.append(entry[1])
            massage.append(entry[2])
        else:
            user.append("group_notification")
            massage.append(entry[0])
    df["users"] = user
    df["massage"] = massage
    df.drop(columns="user_message", inplace=True)
    df["year"] = df["date"].dt.year
    df["month_name"] = df["date"].dt.month_name()
    df["month_num"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute
    df["day_name"] = df["date"].dt.day_name()
    period = []
    for hour in df[["day_name", "hour"]]["hour"]:
        if hour == 23:
            period.append(str(hour) + "-" + str("00"))
        elif hour == 0:
            period.append(str("00") + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df["period"] = period

    return df
