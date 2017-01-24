import sys
import json
from datetime import datetime
from sklearn.cluster import KMeans
from geopy.geocoders import Nominatim
import location_history_json_converter

# TODO
# 1. GUI
# 2. locaion visualitor
# 3. finding new places
# 4.
CLUSTERS_NUM = 1000

CURRENT_LAT = 31.865013
CURRENT_LONG = 34.985318
NEXT_HOURS = 1


# CURRENT_LAT = 31.780201
# CURRENT_LONG = 35.199995
PATH = '/cs/usr/merzbach/locations/TakeoutYair/Location/'
FILE_NAME = 'LocationHistory.json'
PARSED_NAME =  'LocationHistoryParsed.json'

def main():
    location_history_json_converter.convert_json_and_save(PATH+FILE_NAME);
    with open(PATH+PARSED_NAME) as data_file:
        jsonData = json.load(data_file)
    locations = []
    days = []
    samples = []
    for item in jsonData['data']['items']:
        entry = [convertTimestampToDate(item['timestampMs']),convertTimestampToHour(item['timestampMs']), preparePoint(item['latitude']), preparePoint(item['longitude'])];
        samples.append(entry)
    model = learnSamples(samples);
    #showCentersAddress(model.cluster_centers_)
    currentEntry = generateEntry();
    predictEntry(currentEntry,model);


def preparePoint(point):
    newPoint = (point - 30)*100
    return newPoint;


def ExtractPoint(point):
    newPoint = (point/100) + 30

    return newPoint;


def showCentersAddress(centers):
    for entry in centers:
        print getAddress(entry[2],entry[3]);

def convertTimestampToHour(ms):
        return datetime.fromtimestamp(ms / 1000.0).hour


def convertTimestampToDate(ms):
    return datetime.fromtimestamp(ms/1000.0).date().weekday()


def generateEntry():
    #prediction for the next hour
    entry = [datetime.today().weekday(),datetime.today().hour + NEXT_HOURS,preparePoint(CURRENT_LAT), preparePoint(CURRENT_LONG)]
    print "current entry:"
    print entry
    return entry;


def learnSamples(X):
    kmeans = KMeans(n_clusters=CLUSTERS_NUM, random_state=0).fit(X);
    kmeans.transform(X);
    return kmeans;


def predictEntry(entry, model):
    clusterLabel = (model.predict(entry));
    print "this is the label data - center"
    print (model.cluster_centers_[clusterLabel])
    lat = ExtractPoint(model.cluster_centers_[clusterLabel][0][2])
    long = ExtractPoint(model.cluster_centers_[clusterLabel][0][3])
    print (lat,long)
    print getAddress(lat,long)




def getAddress(lat,long):
    geolocator = Nominatim();
    LocStr = "";
    LocStr = str(lat) + ", " + str(long);
  #  print LocStr
    location = geolocator.reverse(LocStr);
   # print(location.address);
    return location.address;

def getlatLongFromAddress(string):
    geolocator = Nominatim();
    location = geolocator.geocode("175 5th Avenue NYC")
    print(location.address)
    print (location.latitude, location.longitude)
    return(location.latitude, location.longitude)



if __name__ == "__main__":
    sys.exit(main())