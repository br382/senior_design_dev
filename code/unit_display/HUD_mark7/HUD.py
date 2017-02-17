# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 13:59:39 2016

@author: rick

Defines the HUD, which is characterized by data and a canvas (image)
"""
import json
from Database import *
from Storage import posStruct
from ScopeCanvas import ScopeCanvas, dummyUsers
from uidGen import uidGen

class HUD():
    def __init__(self, canvas, DEBUG=True):
        self.data = Database()
        self.data.log_file = 'gui_dump.log'
        self.scope_canvas = ScopeCanvas(canvas)
        self.myUID = uidGen()
        self.DEBUG = DEBUG
        self.my_lat = 0
        self.my_lon = 0
        self.my_heading = 0
        self.USE_DUMMY = True
    def work(self):
        if self.DEBUG: print timestamp(), 'Starting...'            
        try:
            if self.DEBUG: print 'Building position update message...'
            send_data = posStruct()
            send_data['uid'] = str(self.myUID)
            send_data['lat'] = str(self.my_lat)
            send_data['long'] = str(self.my_lon)
            send_data['heading'] = str(self.my_heading)
            update_pos = {'update_pos':send_data}
            send = json.dumps(update_pos)
            self.data.socketExchangeAuto(send)
        except:
            print 'Issue building position update message'
            
        send = '{"list_users":1}'
        if self.DEBUG: print timestamp(), 'Requesting list of users...'
        user_list = self.data.socketExchangeAuto(send)
        try:
            user_list = json.loads(user_list)
        except:
            if self.DEBUG: self.data.users = dummyUsers() #dummy data
            if self.DEBUG: self.data.dump()
            user_list = []
            print 'User List Not Found...'
        try:
            for uid in user_list:
                try:
                    if self.DEBUG: print timestamp(), 'Requesting user...'
                    send = str('{"get_user":' + str(uid) + '}')
                    this_user = self.data.socketExchangeAuto(send)
                    self.data.users[uid] = json.loads(this_user)
                except:
                    if self.DEBUG: print 'No data received for ' + str(uid)
        except:
            if self.DEBUG: print 'user_list cannot be iterated over'
        if self.DEBUG: print 'Original myUID: ', self.myUID
        if self.DEBUG: print 'Dummy myUID: ', self.myUID
        if self.DEBUG: print 'self.user_data', self.data.users
        #Update display image according to values in user_data
        if self.DEBUG: print timestamp(), 'Drawing scope_canvas...'
        self.scope_canvas.updateDisplay(self.data.users, self.myUID)
        if self.DEBUG: print timestamp(), 'Done'
        if self.DEBUG: print ''

    def pickUID(self, keycode, DEBUG=False):
        pass