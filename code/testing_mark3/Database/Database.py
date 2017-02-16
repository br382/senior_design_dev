"""
@Author Brett
"""
from Storage import Storage, timestamp, readtimestamp
import json
import socket
from socketExchange import *
import threading

class Database(Storage):
    def __init__(self, port=12345, DEBUG=True):
        Storage.__init__(self)
        self.port      = port
        self.servers   = {}
        self.scan_lock = threading.Lock()
        self.scan      = False
        self.DEBUG     = DEBUG
        self.findServers(async=True)
    def pickUID(self, last_uid, step=1):
        uid_list = list(sorted(self.users.keys()))
        cur_ind  = 0
        for k in range(len(uid_list)):
            if uid_list[k] == last_uid:
                cur_ind = k
                cur_ind = (cur_ind + step) % len(uid_list)
        try:
            #print 'uid ind/total: ', cur_ind, len(uid_list)
            uid_new = uid_list[cur_ind]
        except:
            return last_uid
            print 'Inside pickUID() except case'
        return uid_new
    def findServers(self, async=True):
        if self.DEBUG: print 'Searching For More Servers...'
        if async == True:
            while(1):
                try:
                    threading.Thread(target=Database._findServers, args=(self,)).start()
                    break
                except:
                    print 'Trying To Spawn Thread'
                    sleep(1)
                    pass
        else:
            self._findServers()
            if self.DEBUG: print 'Found ', len(self.servers), ' during scan.'
        return
    def _findServers(self):
        boot_me = False
        self.scan_lock.acquire()
        if self.scan == True:
            boot_me = True
        else:
            boot_me = False
            self.scan = True
        self.scan_lock.release()
        if boot_me == True:
            if self.DEBUG: print 'Async Searching Denied.'
            return
        if self.DEBUG: print 'Async Scanning Spawned...'
        self.servers = scanServers(port=self.port, r=3)
        if self.DEBUG: print 'Async Scanning Done.'
        self.scan_lock.acquire()
        self.scan = False
        self.scan_lock.release()
    def socketExchangeAuto(self, msg, buf=1024, timeout=1.0):
        ret = socketExchangeDict(msg, server_dict=self.servers, buf=buf, timeout=timeout, DEBUG=self.DEBUG)
        if len(self.servers)<=0:
            self.findServers()
            return None
        return ret
    def serverWork(self, in_str_json):
        if self.DEBUG: print timestamp(), 'Starting serverWork...'
        self._getJSONin(in_str_json)
        self._handleJSON()
        temp = self._getJSONout()
        if self.DEBUG: print timestamp(), 'Done serverWork...'
        return temp
    def _getJSONin(self, in_str_json):
        t = '_getJSONin() :: '
        if self.DEBUG: print 'INPUT STR: `' + in_str_json + '`'
        self.out_json_obj = {}
        try:
            self.in_json_obj = json.loads(in_str_json)
            self.log(t + 'Valid :: `' + in_str_json + '`')
        except:
            self.in_json_obj = {}
            self.log(t + 'Invalid :: `' + in_str_json + '`')
        if self.DEBUG: print 'INPUT JSON OBJ: `' + str(self.in_json_obj) + '`'
        return None
    def _handleJSON(self):
        if self.DEBUG: print timestamp(), 'Inside _handleJSON(), Starting handles...'
        if self.DEBUG: print timestamp(), 'Inside _handleJSON(), calling _hUpdateUser()...'
        self._hUpdateUser()
        if self.DEBUG: print timestamp(), 'Inside _handleJSON(), calling _hUpdateMarker()...'
        self._hUpdateMarker()
        if self.DEBUG: print timestamp(), 'Inside _handleJSON(), calling _hUpdatePos()...'
        self._hUpdatePos()
        if self.DEBUG: print timestamp(), 'Inside _handleJSON(), calling _hGetUser()...'
        self._hGetUser()
        if self.DEBUG: print timestamp(), 'Inside _handleJSON(), calling _hListUsers()...'
        self._hListUsers()
        if self.DEBUG: print timestamp(), 'Inside _handleJSON(), calling _hPing()...' 
        self._hPing()
        return None
    def _getJSONout(self):
        t = '_getJSONout() :: '
        if self.DEBUG: print 'OUTPUT JSON OBJ: `' + str(self.out_json_obj) + '`'
        out_str_json = json.dumps(self.out_json_obj)
        if self.DEBUG: print 'OUTPUT STR: `' + str(out_str_json) + '`'
        self.log(t + 'OUTPUT :: `' + str(self.out_json_obj) + '`')
        return out_str_json
    def _stuff(self):
        #self.out_json_obj['ME'] = 118
        return None
    def _hUpdateUser(self):
        t = '_hUpdateUser() :: '
        k = 'update_user'
        try:
            uid = self.updateUser(self.in_json_obj[k])
            self.log(t + 'Valid :: ' + str(uid) +', '+ str(self.in_json_obj[k]['uid']) +', '+ str(self.in_json_obj[k]['name']) )
        except Exception as e:
            #self.log(t + 'Unable to Perform Operation :: ' + str(e))
            pass
    def _hUpdateMarker(self):
        t = '_hUpdateMarker() :: '
        k = 'update_marker'
        try:
            uid = self.updateMarker(self.in_json_obj[k])
            self.log(t + 'Valid :: ' + str(uid))
        except Exception as e:
            self.log(t + 'Unable to Perform Operation :: ' + str(e))
    def _hUpdatePos(self):
        t = '_hUpdatePos() :: '
        k = 'update_pos'
        try:
            uid = self.updatePos(self.in_json_obj[k])
            self.log(t + 'Valid :: ' + str(uid))
        except Exception as e:
            self.log(t + 'Unable to Perform Operation :: ' + str(e))
    def _hGetUser(self):
        t = '_hSendUser() :: '
        k = 'get_user'
        try:
            uid = self.in_json_obj[k]
            struct = self.getUser(uid)
            self.out_json_obj = struct
            self.log(t + 'Valid :: ' + 'UID ' + str(uid))
        except Exception as e:
            self.log(t + 'Unable to Perform Operation :: ' + str(e))
    def _hListUsers(self):
        t = '_hListUsers() :: '
        k = 'list_users'
        try:
            test = self.in_json_obj[k]
            struct = self.listUsers()
            self.out_json_obj = struct
            self.log(t + 'Valid :: ', struct)
        except Exception as e:
            self.log(t + 'Unable to Perform Operation :: ' + str(e))
    def _ack(self):
        #return (socket.gethostbyname(socket.gethostname()), self.port)
        return timestamp()
    def _hPing(self):
        t = '_hPing() :: '
        k = 'ping'
        try:
            test = self.in_json_obj[k]
            #if (test):
            if (self.DEBUG): print 'Pinged by ' + str(test)
            self.out_json_obj = self._ack()
            self.log(t + 'Valid :: ' + str(self.in_json_obj))
        except Exception as e:
            self.log(t + 'Unable to Perform Operation :: ' + str(e))
