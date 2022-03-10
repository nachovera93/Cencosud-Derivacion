from datetime import date, timedelta
 
today_date = date.today()
 
print("CURRENT DAY : ", today_date)
 
td = timedelta(3)

def month_converter(i):
    global month
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    print(month[0])
    return month[i]


print("AFTER 5 DAYS DATE WILL BE : ", (today_date + td).day)
print("AFTER 5 DAYS DATE WILL BE : ", month_converter(11))
