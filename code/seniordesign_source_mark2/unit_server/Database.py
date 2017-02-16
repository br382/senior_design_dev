"""
@Author Brett
"""
from Storage import Storage, timestamp
import json
import socket
from socketExchange import scanServers, socketExchangeDict

class Database(Storage):
    def __init__(self, port=12345):
        Storage.__init__(self)
        self.port = port
        self.servers = scanServers(port=self.port)
    def findServers(self):
        self.servers = scanServers(port=self.port,r=3)
        self.servers[(socket.gethostbyname(socket.gethostname()), self.port)] = 'localhost'
    def socketExchangeAuto(self, msg, buf=1024, timeout=1.0, DEBUG=False):
        ret = socketExchangeDict(msg, server_dict=self.servers, buf=buf, timeout=timeout, DEBUG=DEBUG)
        if len(server_dict)<=0:
            if DEBUG: print 'Searching For More Servers...'
            self.findServers()
            if DEBUG: print 'Found ', len(self.servers), ' servers during scan.'
        return ret
    def serverWork(self, in_str_json, DEBUG=False):
        if DEBUG: print timestamp(), 'Starting work...'
        self._getJSONin(in_str_json)
        self._handleJSON()
        temp = self._getJSONout()
        if DEBUG: print timestamp(), 'Done work...'
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
