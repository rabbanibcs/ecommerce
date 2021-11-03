from datetime import datetime, timedelta
from pytz import timezone
import pytz
print(dir(pytz))
utc = pytz.utc
# print(utc.zone)
eastern = timezone('Asia/Dhaka')
# print(eastern.zone)
print(pytz.country_names)
countries=pytz.country_names
t=[]
print(dir(t))
for v, c in countries.items():
    t.append((v,c))
    print(c,v)

print(t)




























