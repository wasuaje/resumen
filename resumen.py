# -*- coding: utf-8 -*-
import gtk
from gtk import glade
from rsm import *

class Resumen:
    def __init__(self):
	self.xml = glade.XML("resumen.glade", None, None)
       # self.xml.signal_connect("on_fahr_value_changed", self.on_spin_change)
        self.xml.signal_connect("on_btnclick",self.btnclick)       
    	self.xml.signal_connect("window1_destroy_cb", lambda w: gtk.main_quit())
    	self.xml.signal_connect("on_combobox1_changed",self.cmb1_click)
       # self.spin = self.xml.get_widget("fahr")
       # self.result = self.xml.get_widget("celsius")
	self.text1 = self.xml.get_widget("entry1")
	self.btn1  = self.xml.get_widget("button1")
	self.textview1  = self.xml.get_widget("textview1")
	self.combo1  = self.xml.get_widget("combobox1")
	#self.combo2  = self.xml.get_widget("combobox2")
    	for srv in servers:
	    	self.combo1.append_text(srv)	
	self.combo1.set_active(1)


    def cmb1_click(self,w):
	self.combo2.get_model().clear()
    	var1=self.combo1.get_active_text()
    	print var1
    	serv2=cmd_srv[var1] #comando especifico a ejecutaar
    	for srv1 in serv2:
    		self.combo2.append_text(srv1[0])
	self.combo2.set_active(0)

	
    def btnclick(self, w):
	textbuffer =gtk.TextBuffer(None)
        self.textview1.get_buffer().set_text("")		#blanqueo el textbox
    	srv=self.combo1.get_active_text()			#en que server estoy trabajando
    	cmd_name=self.combo2.get_active_text()			#nombre del comando que deseo
 	for key in cmds.keys():
 		a=cmds[key]
     		for cmd2 in a:
	    		if cmd2==cmd_name:
    				texto=main(srv,key)   			

	if texto!=None:
	        self.textview1.get_buffer().insert_at_cursor(texto+'  \n')        
   
if __name__ == "__main__":
    resumen = Resumen()
    gtk.main()
    
    
    
    
   
