from Adafruit_IO import Client

# import sensitive data from secrets file
try:
    from secrets import secrets
except ImportError:
    print("WiFi and io secrets are kept in secrets.py, please add them there.")

aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]

aio = Client(aio_username, aio_key)

# get feed information
feed = aio.feeds("aac-for-dogs")
print(feed)

# get data from feed
data = aio.data("aac-for-dogs")

# create file to store data from feed
# if file already exists this will erase file
file = open("feedData.txt", "w")
file.close()
file = open("feedData.txt", "a")
for line in data:
    date = line.created_at[0:10]
    time = line.created_at[11:19]
    file.write("{} {} {}".format(date, time, line.value))
file.close()
