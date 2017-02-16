"""
@Author Brett
"""
from DataStruct import *
import json
def t():
    return readtimestamp(timestamp())
class Storage():
    def __init__(self):
        self.log_file     = 'dump.log'
        self.in_json_obj  = {}
        self.out_json_obj = {}
        self.users        = {}
        self.errors       = {}
    def log(self, msg):
        if len(self.errors.keys()) > 10:
            self.errors = {}
        self.errors[t()] = str(msg)
        return
    def isUserExist(self, uid):
        try:
            self.users[uid]
            print 'Exist? ' + str(uid) + ' True'
            return True
        except:
            pass
        print 'Exist? ' + str(uid) + ' False'
        return False
    def addUser(self, uid, name='', safe=True):
        if (uid != None):
            if (not(self.isUserExist(uid)) and safe) or (not(safe) and True):
                self.users[uid]         = userStruct()
                self.users[uid]["uid"]  = uid
                self.users[uid]["name"] = name
                s = readtimestamp(timestamp())
                self.users[uid]["first_modify"] = s
                self.users[uid]["last_modify"]  = s
                return True #added new user
        return False #did not add new user
    def delUser(self, uid):
        try:
            del self.users[uid]
            return True
        except:
            pass
        return False
    def updateUser(self, update_user_obj, uid_old=None):
        uid_new = None
        try:
            uid_new = update_user_obj['uid']
        except:
            uid_new = None
            print 'updateUser() ' + 'Unable to find new_uid/old_uid: ' + str(uid_old) + '/' + str(uid_old)
        msg_h = 'updateUser(' + str(uid_old) + '/' + str(uid_new) + '): '
        if (uid_old != uid_new) and not(uid_old == None):
            if not self.delUser(uid_old): self.log(msg_h + 'Unable to delete uid_old.')
            if not self.addUser(uid_new): self.log(msg_h + 'Unable to create uid_new.')
        else:
            if not self.isUserExist(uid_new):
                if not self.addUser(uid_new):
                    self.log(msg_h + 'Unable to create uid ' + str(uid_new) + '.')
        source = cleanStruct(update_user_obj, userStruct())
        if inttimestamp(source['last_modify']) > inttimestamp(self.users[uid_new]['last_modify']):
            for k in source.keys():
                self.users[uid_new][k] = source[k]
                if k == 'markerStruct': self.users[uid_new][k] = cleanStruct(self.users[uid_new][k], markerStruct())
                if k == 'posStruct':    self.users[uid_new][k] = cleanStruct(self.users[uid_new][k],    posStruct())
                if k == 'posStruct':    self.users[uid_new][k] = cleanStruct(self.users[uid_new][k],   scanStruct())
        return uid_new
    def updateMarker(self, update_marker_obj, uid_old=None):
        uid_new = None
        try:
            uid_new = update_marker_obj['uid']
        except:
            uid_new = None
            print 'updateMarker() ' + 'Unable to find new_uid/old_uid: ' + str(uid_old) + '/' + str(uid_old)
        msg_h = 'updateMarker(' + str(uid_old) + '/' + str(uid_new) + '): '
        if (uid_old != uid_new) and not(uid_old == None):
            if not self.delUser(uid_old): self.log(msg_h + 'Unable to delete uid_old.')
            if not self.addUser(uid_new): self.log(msg_h + 'Unable to create uid_new.')
        else:
            if not self.isUserExist(uid_new):
                if not self.addUser(uid_new):
                    pass
                    #self.log(msg_h + 'Unable to create uid ' + str(uid_new) + '.')
        if (uid_new != None):
            source = cleanStruct(update_marker_obj, markerStruct())
            print 'Cleaned: ' + str(source)
            if inttimestamp(source['last_modify']) > inttimestamp(self.users[uid_new]['markerStruct']['last_modify']):
                for k in source.keys():
                    self.users[uid_new]['markerStruct'][k] = source[k]
        return uid_new
    def updatePos(self, update_pos_obj, uid_old=None):
        uid_new = None
        try:
            uid_new = update_pos_obj['uid']
        except:
            uid_new = None
            print 'updatePos() ' + 'Unable to find new_uid/old_uid: ' + str(uid_old) + '/' + str(uid_old)
        msg_h = 'updatePos(' + str(uid_old) + '/' + str(uid_new) + '): '
        if (uid_old != uid_new) and not(uid_old == None):
            if not self.delUser(uid_old): self.log(msg_h + 'Unable to delete uid_old.')
            if not self.addUser(uid_new): self.log(msg_h + 'Unable to create uid_new.')
        else:
            if not self.isUserExist(uid_new):
                if not self.addUser(uid_new):
                    self.log(msg_h + 'Unable to create uid ' + str(uid_new) + '.')
        if (uid_new != None):
            source = cleanStruct(update_pos_obj, posStruct())
            print 'Cleaned: ' + str(source)
            if inttimestamp(source['last_modify']) > inttimestamp(self.users[uid_new]['posStruct']['last_modify']):
                for k in source.keys():
                    self.users[uid_new]['posStruct'][k] = source[k]
        return uid_new
    def updateScan(self, update_scan_obj, uid_old=None):
        uid_new = None
        try:
            uid_new = update_scan_obj['uid']
        except:
            uid_new = None
            print 'updateScan() ' + 'Unable to find new_uid/old_uid: ' + str(uid_old) + '/' + str(uid_old)
        msg_h = 'updateScan(' + str(uid_old) + '/' + str(uid_new) + '): '
        if (uid_old != uid_new) and not(uid_old == None):
            if not self.delUser(uid_old): self.log(msg_h + 'Unable to delete uid_old.')
            if not self.addUser(uid_new): self.log(msg_h + 'Unable to create uid_new.')
        else:
            if not self.isUserExist(uid_new):
                if not self.addUser(uid_new):
                    self.log(msg_h + 'Unable to create uid ' + str(uid_new) + '.')
        if (uid_new != None):
            source = cleanStruct(update_scan_obj, scanStruct(), skip=[])
            print 'Cleaned: ' + str(source)
            if inttimestamp(source['last_modify']) > inttimestamp(self.users[uid_new]['scanStruct']['last_modify']):
                for k in source.keys():
                    self.users[uid_new]['posStruct'][k] = source[k]
        return uid_new
    def updatePoint(self, update_point_obj, uid_old=None):
        uid_new = None
        try:
            uid_new = update_point_obj['uid']
        except:
            uid_new = None
            print 'updatePoint() ' + 'Unable to find new_uid/old_uid: ' + str(uid_old) + '/' + str(uid_old)
        msg_h = 'updatePoint(' + str(uid_old) + '/' + str(uid_new) + '): '
        if (uid_old != uid_new) and not(uid_old == None):
            if not self.delUser(uid_old): self.log(msg_h + 'Unable to delete uid_old.')
            if not self.addUser(uid_new): self.log(msg_h + 'Unable to create uid_new.')
        else:
            if not self.isUserExist(uid_new):
                if not self.addUser(uid_new):
                    self.log(msg_h + 'Unable to create uid ' + str(uid_new) + '.')
            for k in source:
                self.users[uid_new]['posStruct']['points'] = source[k]
        return uid_new
    def getUser(self, uid):
        return self.users[uid]
    def listUsers(self):
        list = self.users.keys()
        return list
    def dump(self):
        dump_struct = {
            "dump_timestamp"   :readtimestamp(timestamp()),
            "self.in_json_obj" :self.in_json_obj,
            "self.out_json_obj":self.out_json_obj,
            "self.log_file"     :self.log_file,
            "self.users"        :self.users,
            "self.errors"       :self.errors
            }
        print 'Dumping:'
        print str(dump_struct)
        dump_string = json.dumps(dump_struct, indent=4, sort_keys=True)
        with open(self.log_file, 'w') as f:
            f.write(dump_string)
        return None
    def load(self):
        filepath = self.log_file
        dump_struct = {
            "dump_timestamp"   :'',
            "self.in_json_obj" :'',
            "self.out_json_obj":'',
            "self.log_file"    :'',
            "self.users"       :'',
            "self.errors"         :''
            }
        try:
            f = open(filepath)
            json_str  = f.read()
            json_data = json.loads(json_str)
        except:
            json_str  = '{}'
            json_data = {}
        #Showing any JSON exceptions:
        in_keys   = list(sorted(json_data.keys()))
        test_keys = list(sorted(dump_struct.keys()))
        if in_keys == test_keys: #test for len() and equal key contents
            #self.log_file = self.log_file #no change
            #self.log      = self.log      #no change
            self.in_json_obj  = {}         #clear it out
            self.out_json_obj = {}         #clear it out
            self.users        = json_data['self.users']
            return json_data['dump_timestamp'] #successfully loaded
        return None #didn't work
