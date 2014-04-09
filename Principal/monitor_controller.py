# -*- coding: utf-8 *-*
'''
Created on 10/02/2014

@author: Admin
'''
import sys
sys.path.append("..")
from Clases.procesos import Procesos
#import Clases.procesos
import time

class MonitorController:
    def __init__(self):
        self.procesos=Procesos()
        self.CicloForever()
        
    def CicloForever(self):    
        while True:
            time.sleep(1)
            self.procesos.Finalizar_Proceso()
#Ejecutamos en un ciclo infinito en espera de un Evento
#app = wx.App()
MonitorController()
#app.MainLoop()            