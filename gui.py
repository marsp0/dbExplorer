import Tkinter as tk
from collections import OrderedDict

class Gui(tk.Frame):

	def __init__(self,parent=None,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)

		self.master.minsize(width=600,height=400)
		self.master.maxsize(width=600,height=400)
		self.pack()

		'''main'''
		self.main_display = tk.Frame(self)
		

		self.db_display = tk.Frame(self)
		self.table_display = tk.Frame(self)

		self.main_options = (
							('DB',(self.packer,(self.main_display,self.db_view))),
							('Table',(self.packer,(self.main_display,self.table_view))),
							('Export',(0,)),
							('Quit',(self.quit,))
							)

		self.db_options = (
							('Show DB',(0,)),
							('Change DB',(0,)),
							('Delete DB',(0,)),
							('Back',(self.packer,(self.db_display,self.main_view)))
						)

		self.table_options = (
								('Info',(0,)),
								('View',(0,)),
								('Create',(0,)),
								('Alter',(0,)),
								('Delete',(0,)),
								('Insert',(0,)),
								('Update',(0,)),
								('Select',(0,)),
								('Back',(self.packer,(self.table_display,self.main_view))),
							)
		self.main_explanations = (('Relational DB -' , 'collection of information stored in a tabular format. The data can be easily stored and retrieved.'),
									('Table -','structure inside the database that contains rows and columns. Example : Person'),
									('Column -',' defines the different qualities of the table. Example : Name, Age etc.'),
									('Row -',' contains the different records. Example : Ron, 34 , etc.'))

		self.main_view()

	def create_buttons(self,frame,options):
		column = 1
		for key,value in options:
			if len(value) > 1:
				function = value[0]
				args = value[1]
				tk.Button(frame,text = key,command = lambda args = args: function(*args) ).grid(row=0,column=column)
			else:
				tk.Button(frame,text=key,command = value[0]).grid(row=0,column=column)
			column += 1

	def create_labels(self,frame,options):
		row=3
		for name,desc in options:
			tk.Label(frame,text=name,width=15).grid(row=row,column=1)
			tk.Label(frame,text=desc,width=65,wraplength=300).grid(row=row,column=2)
			row+=1

	def main_view(self):
		self.master.title('DB Explorer')
		'''create inside frames and pack them'''
		self.main_buttons_display = tk.Frame(self.main_display)
		self.main_expl_display = tk.Frame(self.main_display,bd=2,relief='raised')
		self.main_display.pack()
		self.main_buttons_display.pack(anchor='n')
		self.main_expl_display.pack()

		self.create_buttons(self.main_buttons_display,self.main_options)

		tk.Label(self.main_expl_display,text='Welcome to DB Explorer',width=20).grid(row=1,column=1,columnspan=2)
		tk.Label(self.main_expl_display,text='').grid(row=2,column=1)
		self.create_labels(self.main_expl_display,self.main_explanations)

	def db_view(self):
		self.master.title('DB')
		'''create inside frames and pack them'''
		self.db_buttons_display = tk.Frame(self.db_display)
		self.db_expl_display = tk.Frame(self.db_display)
		self.db_display.pack()
		self.db_buttons_display.pack(anchor='n')
		self.db_expl_display.pack()


		self.create_buttons(self.db_buttons_display,self.db_options)

	def table_view(self):
		self.master.title('Table')
		'''create inside frames and pack them'''
		self.table_buttons_display = tk.Frame(self.table_display)
		self.table_expl_display = tk.Frame(self.table_display)
		self.table_display.pack()
		self.table_buttons_display.pack(anchor='n')
		self.table_expl_display.pack()


		self.create_buttons(self.table_buttons_display,self.table_options)

	def packer(self,to_unpack,to_pack):
		for child in to_unpack.winfo_children():
			child.destroy()
		to_unpack.pack_forget()
		to_pack()

	def quit(self):
		self.master.quit()

if __name__=='__main__':
	p = Gui()
	p.mainloop()