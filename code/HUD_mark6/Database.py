"""
@Author Brett
"""
from Storage import Storage, timestamp
import json
import socket
from socketExchange import *
import threading

class Database(Storage):
    def __init__(self, port=12345):
        Storage.__init__(self)
        self.port = port
        self.servers = {}
        self.findServers(async=True)
    def pickUID(self, last_uid, step=1, DEBUG=False):
        uid_list = list(sorted(self.users.keys()))
        if DEBUG: print 'UID last: ', last_uid
        if DEBUG: print 'UID list: ', uid_list
        cur_ind = 0
        for k in range(len(uid_list)):
            if uid_list[k] == last_uid:
                cur_ind = k
                if DEBUG: print 'pickUID() k, len(): ', k, ' ', len(uid_list)
                cur_ind = (cur_ind + step) % len(uid_list)
        if len(uid_list)==0:
            if DEBUG: print 'pickUID() No uid inputs to select from.'
            return last_uid
        uid_new = uid_list[cur_ind]
        return uid_new
    def findServers(self, async=True, DEBUG=False):
        if DEBUG: print 'Searching For More Servers...'
        if async:
            #scanServers(ip_start=externLocalIP(), port=12345,r=3, ret_dict={}, DEBUG=False)
            threading.Thread(target=Database._findServers, args=(self, False)).start()
        else:
            self._findServers()
            if DEBUG: print 'Found ', len(self.servers), ' servers during scan.'
    def _findServers(self, DEBUG=False):
        if DEBUG: print 'Searcher Spawned...'
        self.servers = scanServers(port=self.port, r=3)
        if DEBUG: print 'Done Scanning for Servers.'
    def socketExchangeAuto(self, msg, buf=1024, timeout=1.0, DEBUG=False):
        ret = socketExchangeDict(msg, server_dict=self.servers, buf=buf, timeout=timeout, DEBUG=DEBUG)
        if len(self.servers)<=0:
            self.findServers()
            return None
        return ret
    def serverWork(self, in_str_json, DEBUG=False):
        if DEBUG: print timestamp(), 'Starting serverWork...'
        self._getJSONin(in_str_json)
        self._handleJSON()
        temp = self._getJSONout()
        if DEBUG: print timestamp(), 'Done serverWork...'
        return temp
    def _getJSONin(self, in_str_json):
        self.out_json_obj = {}
        try:
            self.in_json_obj = json.loads(in_str_json)
        except:
            self.in_json_obj = {}
        return None
    def _handleJSON(self, DEBUG=False):
        if DEBUG: print 'INPUT: ' + json.dumps(self.in_json_obj)
        if DEBUG: print timestamp(), 'Inside _handleJSON(), Starting handles...'
        #
        if DEBUG: print timestamp(), 'Inside _handleJSON(), calling _hUpdateUser()...'
        self._hUpdateUser()
        if DEBUG: print timestamp(), 'Inside _handleJSON(), calling _hUpdateMarker()...'
        self._hUpdateMarker()
        if DEBUG: print timestamp(), 'Inside _handleJSON(), calling _hUpdatePos()...'
        self._hUpdatePos()
        if DEBUG: print timestamp(), 'Inside _handleJSON(), calling _hGetUser()...'
        self._hGetUser()
        if DEBUG: print timestamp(), 'Inside _handleJSON(), calling _hListUsers()...'
        self._hListUsers()
        if DEBUG: print timestamp(), 'Inside _handleJSON(), calling _hPing()...' 
        self._hPing()
        #
        if DEBUG: print 'OUTPUT: '+ json.dumps(self.out_json_obj)
        return None
    def _getJSONout(self):
        out_str_json = json.dumps(self.out_json_obj)
        return out_str_json
    def _stuff(self):
        #self.out_json_obj['ME'] = 118
        return None
    def _hUpdateUser(self):
        t = '_hUpdateUser: '
        try:
            uid = self.updateUser(self.in_json_obj['update_user'])
            self.log(t + self.in_json_obj['update_user'][uid] + self.in_json_obj['update_user']['name'])
        except:
            self.log(t + 'Unable to Perform Operation')
    def _hUpdateMarker(self):
        t = '_hUpdateMarker() '
        try:
            uid = self.updateMarker(self.in_json_obj['update_marker'])
            self.log('_hUpdateUser: ' + self.in_json_obj['update_user'][uid])
        except:
            self.log(t + 'Unable to Perform Operation')
    def _hUpdatePos(self):
        t = '_hUpdatePos() '
        try:
            uid = self.updatePos(self.in_json_obj['update_pos'])
            self.log('_hUpdateUser: ' + self.in_json_obj['update_user'][uid])
        except:
            self.log(t + 'Unable to Perform Operation')
    def _hGetUser(self):
        t = '_hSendUser()'
        try:
            print self.in_json_obj
            uid = self.in_json_obj['get_user']
            print uid
            struct = self.getUser(uid)
            print struct
            self.out_json_obj = struct
        except:
            pass
    def _hListUsers(self):
        t = '_hListUsers()'
        try:
            test = self.in_json_obj['list_users']
            if (int(test) == 1): print 'Listing Users On Server'
            else: return
            struct = self.listUsers();
            self.out_json_obj = struct
        except:
            pass
    def _ack(self):
        #return (socket.gethostbyname(socket.gethostname()), self.port)
        return timestamp()
    def _hPing(self):
        t = '_hPing()'
        try:
            test = self.in_json_obj['ping']
            #if (test):
            if (True): print 'Pinged by ' + str(test)
            self.out_json_obj = self._ack()
        except:
            pass
