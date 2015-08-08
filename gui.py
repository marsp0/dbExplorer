import Tkinter as tk
from collections import OrderedDict
from explorer import *

class Gui(tk.Frame):

	def __init__(self,parent=None,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)

		self.master.minsize(width=600,height=400)
		self.master.maxsize(width=600,height=400)
		self.pack()

		'''main'''
		self.main_display = tk.Frame(self)
		

		self.table_display = tk.Frame(self)

		self.db_display = tk.Frame(self)
		

		self.main_options = (
							('DB',(self.packer,(self.main_display,self.db_view))),
							('Table',(self.packer,(self.main_display,self.table_view))),
							('Export',(0,)),
							('Quit',(self.quit,))
							)

		self.db_options = (
							('Show DBs',(self.show_dbs,)),
							('Change DB',(0,)),
							('Delete DB',(0,)),
							('Back',(self.packer,(self.db_display,self.main_view)))
						)

		self.table_options = (
								('Tables',(self.show_tables,)),
								('View',(self.view_table,)),
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

		self.explorer = Explorer('root','0899504274')

		self.table_var = tk.StringVar()

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

	def create_main_labels(self,frame,options):
		row=3
		for name,desc in options:
			tk.Label(frame,text=name,width=15).grid(row=row,column=1)
			tk.Label(frame,text=desc,width=65,wraplength=300).grid(row=row,column=2)
			row+=1

	def create_labels(self,frame,options):
		current = 1
		keys = options.keys()
		width = 80 / len(keys)
		while current != len(keys)+1:
			row=2
			tk.Label(frame,text=keys[current-1],bd=3,relief='raised',width=width,pady=3).grid(row=1,column=current)
			for value in options[keys[current-1]]:
				tk.Label(frame,text=value,bd=1,relief='raised',width=width,pady=3).grid(row=row,column=current)
				row += 1
			current += 1

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
		self.create_main_labels(self.main_expl_display,self.main_explanations)

	def db_view(self):
		self.master.title('DB')
		'''create inside frames and pack them'''
		self.db_buttons_display = tk.Frame(self.db_display)
		self.inner_db_display = tk.Frame(self.db_display,bd=2,relief='raised')
		self.db_display.pack()
		self.db_buttons_display.pack(anchor='n')

		self.create_buttons(self.db_buttons_display,self.db_options)

	def show_dbs(self):
		self.clean_inner_frame(self.inner_db_display)
		to_display = self.explorer.show_dbs()
		self.create_labels(self.inner_db_display,to_display)

	def table_view(self):
		self.master.title('Table')
		'''create inside frames and pack them'''
		self.table_buttons_display = tk.Frame(self.table_display)
		self.inner_parent_display = tk.Frame(self.table_display)
		self.inner_table_display = tk.Frame(self.inner_parent_display,bd=2,relief='raised')
		self.inner_options_display = tk.Frame(self.inner_parent_display)
		self.table_display.pack()
		self.table_buttons_display.pack(anchor='n')
		self.inner_parent_display.pack()
		self.create_buttons(self.table_buttons_display,self.table_options)

	def show_tables(self):
		self.clean_inner_parent()
		self.inner_table_display.pack()
		self.inner_table_display.config(bd=2)
		to_display = self.explorer.show_tables()
		self.create_labels(self.inner_table_display,to_display)

	def view_table(self):
		self.clean_inner_parent()
		self.inner_options_display.pack()
		tables = self.explorer.show_tables()['Name']
		tk.OptionMenu(self.inner_options_display,self.table_var,*tables).grid(row=1,column=1)
		tk.Button(self.inner_options_display,text='Search',command = self.search_table).grid(row=1,column=2)

	def search_table(self):
		self.clean_inner_frame(self.inner_table_display)
		self.inner_table_display.config(bd=2)
		results = self.explorer.show_table(self.table_var.get())
		self.create_labels(self.inner_table_display,results)


	def clean_inner_frame(self,frame):
		for child in frame.winfo_children():
			child.destroy()
		frame.pack()

	def clean_inner_parent(self):
		for child in self.inner_parent_display.winfo_children():
			if isinstance(child,tk.Frame):
				child.configure(bd=0)
				try:
					child.pack_forget()
				except:
					child.grid_forget()
				finally:
					for ch in child.winfo_children():
						ch.destroy()
			else:
				child.destroy()

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