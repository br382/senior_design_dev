"""
@Author Brett
"""
import datetime, time
def timestamp():
    #floating point since epoch, timezone usually UTC, but specified by the platform
    return time.time()
def readtimestamp(input, offset= (-5), zone='EUS'): #eus timezone is -5
    #user readable string of the timestamp, offset by timezone shift
    return zone + ' ' + str(datetime.datetime.utcfromtimestamp(input) + datetime.timedelta(hours=offset))

def timeZones():
    s = 'Standard Time'
    d = 'Daylight Time'
    name   = ['Eastern United States '+s, 'Coordinated Universal Time'
              'Atlantic '+s, 'Eastern '+s, 'Eastern '+d, 'Central '+s, 'Central '+d, 'Mountain'+s, 'Mountain '+d,
              'Pacific '+s, 'Pacific '+d, 'Alaska Time', 'Alaska '+s, 'Alaska '+d, 'Hawaii '+s, 'Hawaii-Aleutian '+s, 'Hawaii-Aleutian '+d,
              'Samoa '+s, 'Samoa '+d, 'Chamorro '+s]
    zones  = ['EUS', 'UTC', 'AST', 'EST', 'CST', 'CDT', 'MST', 'MDT', 'PST', 'PDT', 'AKST', 'AKDT', 'HST', 'HAST', 'HADT', 'SST', 'SDT', 'CHST']
    offset = [-5, 0, -4, -5, -4, -6, -5, -7, -6, -8, -7, -9, -8, -10, -10, -9, -11, -10, +10]
    return [name, zones, offset]

def inttimestamp(input):
    #get timestamp() from readtimestamp() str (and truncates decimal point) 
    parts = input.split()
    delta = datetime.timedelta(hours=0)
    if len(parts)==3:
        k = timeZones()
        #name   = k[0]
        zones  = k[1]
        offset = k[2]
        for n in range(len(zones)):
            if zones[n] == parts[0]:
                delta = datetime.timedelta(hours= -1*offset[n])
    if len(parts)==2 or len(parts)==3:
        then = datetime.datetime.strptime(parts[-2]+' '+parts[-1], "%Y-%m-%d %H:%M:%S.%f") + delta
        sinceEpoch = time.mktime(then.timetuple())
        return sinceEpoch
    return None
    
def userStruct(time=readtimestamp(timestamp())):
    ret = {
        "uid"         :000,
        "name"        :"",
        "posStruct"   :posStruct(time),
        "markerStruct":markerStruct(time),
        #"scanStruct"  :scanStruct(time),
        "first_modify":time,
        "last_modify" :time
        }
    return ret
def cleanStruct(parse, ideal, skip=[]):
    new = {}
    from_keys = parse.keys()
    #print from_keys
    for k in ideal.keys():
        #print k
        if not(k in skip) and (k in from_keys):
            new[k] = parse[k]
    return new
def isUserStruct(val):
    val_keys  = list(sorted(val.keys()))
    test_keys = list(sorted(userStruct().keys()))
    if val_keys != test_keys: #tests for length and contents
        return False
    return isPosStruct(val['posStruct']) and isMarkerStruct(val['markerStruct'])
def posStruct(time=readtimestamp(timestamp())):
    ret = {
        "lat":"",         #in "deg:min:sec.xxx"
        "long":"",        #in "deg:min:sec.xxx"
        "heading":000,    #in degrees from north as on a compass
        "altitude":000,   #in distance units above sea level
        "planet":"earth",
        "first_modify":time,
        "last_modify" :time
        }
    return ret
def isPosStruct(val):
    val_keys  = list(sorted(val.keys()))
    test_keys = list(sorted(posStruct().keys()))
    if val_keys != test_keys: #tests for length and contents
        return False
    return True
def markerStruct(time=readtimestamp(timestamp())):
    ret = {
        "paint_level":000,          #current units measured of paint
        "paint_level_full":100,     #units when full
        "tank_pressure":000,        #PSI of tank
        "tank_pressure_full":000,   #PSI of tank
        "batteries":[000],          #list of battery sensors measured as units (volts?/percentage?)
        "batteries_full":[5],       #list of battery sensors full value volts/percentages...
        "mag_heading":000,
        "first_modify":time,
        "last_modify" :time
        }
    return ret
def isMarkerStruct(val):
    val_keys  = list(sorted(val.keys()))
    test_keys = list(sorted(markerStruct().keys()))
    if val_keys != test_keys: #tests for length and contents
        return False
    return True
def pointStruct():
    ret = {
        "x":0.0,
        "y":0.0,
        "deg_N":0.0,
        "dist_m":0.0
        }
    return ret
def scanStruct(time=readtimestamp(timestamp())):
    ret = {
        'pointStruct':{0:pointStruct()},
        "first_modify":time,
        "last_modify" :time
        }
    return ret
def isScanStruct(val):
    val_keys  = list(sorted(val.keys()))
    test_keys = list(sorted(scanStruct().keys()))
    if val_keys != test_keys: #tests for length and contents
        return False
    return True
    
