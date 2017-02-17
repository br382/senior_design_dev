def dummyUsers(users=3):
    from random import randint
    ret = {}
    for k in range(100,100+users):
        ret[k] = {
            "uid"         :k,   #may be str() or int() but must be same as k (key)
            "name"        :"test uid " + str(k),
            "posStruct"   :{
                "lat":str(  39.9566 + float(randint(-10,10))/10000), #in "deg.xxxxx" #north is pos, south is neg
                "long":str(-75.1899 + float(randint(-10,10))/10000), #in "deg.xxxxx" #east is pos, west is neg
                "heading":randint(0,360),                            #in degrees from north as on a compass
                "altitude":randint(-100,100),                        #in distance units above sea level
                "planet":"earth"
            },
            "markerStruct":{
                "paint_level":randint(0,100),      #current units measured of paint
                "tank_pressure":randint(0,3200),   #PSI of tank
#                "tank_pressure":randint(0,100),   #percentage full of tank
                "tank_pressure_full":3200,         #Full PSI of air tank
                "batteries":[4.8, 3.5],                 #list of battery sensors measured as units (volts?/percentage?)
                "batteries_full":[5.1, 5.1]
            }
            #More keys may exist... but these entries above are guaranteed (per user).
        }
    return ret