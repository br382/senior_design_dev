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
        self.user_data = dummyUsers()
        self.myUID = list(sorted(self.user_data.keys()))[0] #setting uid from dummy keys
        if self.DEBUG: print 'self.user_data', self.user_data
        #Update display image according to values in user_data
        if self.DEBUG: print timestamp(), 'Drawing scope_canvas...'
        self.scope_canvas.updateDisplay(self.user_data, self.myUID)
        if self.DEBUG: print timestamp(), 'Done'
        if self.DEBUG: print ''
