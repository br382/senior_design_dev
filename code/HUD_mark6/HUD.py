# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 13:59:39 2016

@author: rick

Defines the HUD, which is characterized by data and a canvas (image)
"""
import json
from Database import *
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
    def work(self):
        if self.DEBUG: print timestamp(), 'Starting...'
        send = '{"list_users":1}'
        if self.DEBUG: print timestamp(), 'Requesting list of users...'
        user_list = self.data.socketExchangeAuto(send)
        try:
            user_list = json.loads(user_list)
        except:
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
        self.data.dump()
        self.data.users = dummyUsers() #dummy data
        #self.myUID = list(sorted(self.data.users.keys()))[0] #setting uid from dummy keys
        PICK_NEW_UID = True
        if PICK_NEW_UID:
            self.myUID = self.data.pickUID(self.myUID) #choose new uid, 
            PICK_NEW_UID = False
        if self.DEBUG: print 'Dummy myUID: ', self.myUID
        if self.DEBUG: print 'self.user_data', self.data.users
        #Update display image according to values in user_data
        if self.DEBUG: print timestamp(), 'Drawing scope_canvas...'
        self.scope_canvas.updateDisplay(self.data.users, self.myUID)
        if self.DEBUG: print timestamp(), 'Done'
        if self.DEBUG: print ''
