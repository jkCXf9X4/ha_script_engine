import datetime
import time

now = datetime.datetime.now()
delta = datetime.timedelta(hours=5, minutes=2)
# delta = datetime.datetime(minute=2)

t = now + delta
t = t.time().strftime("%H:%M")
print(t)


a = time.strptime("13:00", "%H:%M")

b = time.strptime("12:30", "%H:%M")


a = datetime.timedelta(hours=5, minutes=2)
b = datetime.timedelta(hours=6, minutes=2)

print(a-b)