from datetime import datetime
import pytz
# timezone for search
malwaredetect = "searchbar_url"

tz_london = pytz.timezone('Europe/London')
datetime_london = datetime.now(tz_london)
print("London time:", datetime_london.strftime("%H:%M:%S"))

f = open("malware_report.txt", "a")
f.write("\n"+"\n"+"Malicious site detected"+"\n")
f.write(" - - - - - - - "+"\n")
f.write("Malicious site: "+malwaredetect+"\n")
f.write("Time of search request (London time): "+datetime_london.strftime("%H:%M:%S")+"\n")
f.close()

# open and read the file after the appending:
f = open("malware_report.txt", "r")
print(f.read())