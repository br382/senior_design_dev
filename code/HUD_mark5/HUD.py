# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 13:59:39 2016

@author: rick

Defines the HUD, which is characterized by data and a canvas (image)
"""
#import json
from Storage import *
from SendToServer import *
from ScopeCanvas import ScopeCanvas

class HUD():
    def __init__(self, canvas):
        ### -- ###
        SOCKETHOST = socket.gethostname() #'localhost' '192.168.3.92'
        SOCKETPORT = 12345
        self.SOCKET     = (SOCKETHOST, SOCKETPORT)
        self.data = Storage()
        self.data.log_file = 'gui_dump.log'
        ### -- ###
        self.scope_canvas = ScopeCanvas(canvas)
        
        self.myUID = 0 #Hardcoded for now
        
    def work(self):
        ### -- ###
        print timestamp(), 'Starting...'
        send = '{"list_users":1}'
        print timestamp(), 'Requesting list of users...'
        user_list = socketExchange(send, self.SOCKET)
        try:
            user_list = json.loads(user_list)
        except:
            user_list = []
            print 'User List Not Found...'
        #print user_list
            
        #Update self.data with user data structures for each user on server
        try:
            for uid in user_list:
                #print 'itter ', uid
                id = int(uid)
                try:
                    print timestamp(), 'Requesting user...'
                    send = str('{"get_user":' + str(id) + '}')
                    #print send
                    #print 'Sending get_user message to socketExchange()'
                    this_user = socketExchange(send, self.SOCKET)
                    #print this_user
                    self.data.users[id] = json.loads(this_user)
                except:
                    print 'No data received for ' + str(id)
        except:
            print 'user_list cannot be iterated over'
        #self.data.dump()
        ### -- ###
        
#        for uid in user_list:
#            print timestamp(), 'Building user_data...'
#            id = int(uid)
#            print 'Opening UID', id
#            if id == self.myUID:
#                #self.user_data['My Coords'].append(self.data.users[id]['posStruct']['lat'])
#                #self.user_data['My Coords'].append(self.data.users[id]['posStruct']['long'])
#                #self.user_data['My Heading'] = self.data.users[id]['posStruct']['heading']
#                self.user_data['My Coords'].append(self.data.users[118]['posStruct']['lat']) #hardcode uid
#                self.user_data['My Coords'].append(self.data.users[118]['posStruct']['long']) #hardcode uid
#                self.user_data['My Heading'] = self.data.users[118]['posStruct']['heading'] #hardcode uid
#                self.user_data['Paint'] = self.data.users[id]['markerStruct']['paint_level']
#                self.user_data['Air'] = self.data.users[id]['markerStruct']['tank_pressure']
#            else:
#                pass
#                #self.user_data['Users'][id] = [self.data.users[id]['posStruct']['lat'], self.data.users[id]['posStruct']['long'], self.data.users[id]['posStruct']['heading']]            
        
        #--DUMMY DATA--
        from random import randint
        self.user_data = {'My Coords': [37.74972, 135.9825], 
                          'My Heading': 0, 
                          'Paint': randint(0,100), 
                          'Air': randint(0,3200), 
                          'Users':{1018: [37.74944, 135.9822, 210], 
                                   2022: [37.75028, 135.9833, 270]}}
        
        print 'self.user_data', self.user_data
        
        #Update display image according to values in user_data
        print timestamp(), 'Drawing scope_canvas...'
        self.scope_canvas.updateDisplay(self.user_data)
        print timestamp(), 'Done'
        print ''
