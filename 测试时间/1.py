from datetime import datetime, timedelta
time_format = "%m/%d/%Y %I:%M:%S %p"
expire_time="07/26/2013 03:45:00 PM"
print(datetime.strptime(expire_time, time_format) - timedelta(seconds=45))