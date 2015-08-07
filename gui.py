import Tkinter as tk
from collections import OrderedDict

class Gui(tk.Frame):

	def __init__(self,parent=None,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)

		self.master.minsize(width=600,height=400)
		self.master.maxsize(width=600,height=400)
		self.pack()

		self.main_options = OrderedDict({
									'DB':(self.show_add,'db'),
									'Table':(0,),
									'Export':(0,),
									'Quit':(self.quit,)})

		self.db_options = OrderedDict({'Show DB':(0,),
							'Change DB':(0,),
							'Delete DB':(0,),
							'Hide':(0,)})

		self.table_options = OrderedDict({'View Info':(0,),
								'View Table':(0,),
								'Create Table':(0,),
								'Alter Table':(0,),
								'Delete Table':(0,),
								'Insert':(0,),
								'Update':(0,),
								'Select':(0,),
								'Hide':(0,)
								})

		self.main_display = tk.Frame(self)
		self.main_view()

	def create_buttons(self,frame,options):
		row=1
		for key,value in options.items():
			if len(value) > 1:
				function = value[0]
				args = value[1]
				tk.Button(frame,text = key,command = lambda : function(args) ).grid(row=row,column=1)
			else:
				tk.Button(frame,text=key,command = value[0]).grid(row=row,column=1)
			row += 1

	def main_view(self):
		self.buttons_display = tk.Frame(self.main_display)
		self.add_display = tk.Frame(self.main_display)
		self.search_display = tk.Frame(self.main_display)
		self.main_display.pack()
		self.buttons_display.grid(row=1,column=1)
		self.search_display.grid(row=1,column=3)

		self.create_buttons(self.buttons_display,self.main_options)

	def show_add(self,option):
		self.add_display.grid(row=1,column=2)
		if option =='db':
			self.create_buttons(self.add_display,self.db_options)
		else:
			self.create_buttons(self.add_display,self.table_options)

	def quit(self):
		self.master.quit()

if __name__=='__main__':
	p = Gui()
	p.mainloop()