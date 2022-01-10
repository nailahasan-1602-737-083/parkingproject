from tkinter import  *              # IMPORTING TKINTER LIBRARY CLASSES AND FUNCTIONS 
from tkinter import messagebox      # IMPORTING TKINTER MESSEGEBOX FOR POP UP WARNINGS AND INFO

import sqlite3                      # IMPORTING SQL LITE LIBRARY FOR 
                                    # FETCHING AND STORING VALUES TO DATABASE

import bcrypt                       # IMPORTING BYCRYPT LIBRARY WHICH USED TO SAVE PASSWORDS SAFELY
import re                           # REGULAR EXPRESSION LIBRARY FOR VALIDATING INPUT DETAILS

class Admin:                        #ADMIN CLASS WHICH IS CALLED IN LOGIN SCRIPT
		


		def __init__(self,main_window):  # CONSTRUCTOR TO INITIALIZE CONNECTION WITH DATABASE 
                                         # AND INTIALIZE VALUES

			self.con = sqlite3.connect('app_data.db')
			self.c= self.con.cursor()	
			self.main_window=main_window # ASSIGNING MAIN WINDOW OBJECT

			self.admin_window()          # INVOKING ADMIN GUI WINDOW

		def save_details(self):          # FUNCTION TO UPDATE COST DETAILS INTO DATABASE

			global park_window

			self.c.execute("""UPDATE cost SET cost_2 = ? ,cost_4 = ?,total_slots = ?""",(self.cost_2.get(),self.cost_4.get(),self.total_slots.get()))

			self.con.commit() # COMMITING CHANGES TO DATABASE
			
			
			self.cost_2.delete(0,END)
			self.cost_4.delete(0,END)
			self.total_slots.delete(0,END)
		
			messagebox.showinfo("Registered", "Details Saved sucessfull",parent=park_window) 
			park_window.destroy()




		def park_details(self):                          # FUNCTION TO FETCH PARKING COST AND SLOTS AVAILABLE
			global a_window
			global park_window

			park_window = Toplevel(a_window)
			park_window.title(" Parking Page ")
			try:
				self.main_window.iconbitmap("main_icon.ico")
			except:
				self.main_window.iconbitmap("@main_icon.xbm")
			park_window.geometry("550x400")

			l1 = Label(park_window, text="PARKING DETAILS", font="Times 20 bold", padx=40, pady=40,bg="blue", fg="black")
			l1.grid(row=0, column=0, columnspan=3, padx=30, pady=30)
			
	 
			self.cost_2 = Entry(park_window,width=30)
			self.cost_2.grid(row=1,column=1,padx=20)


			self.cost_4 = Entry(park_window,width=30)
			self.cost_4.grid(row=3,column=1,padx=20)

			self.total_slots = Entry(park_window,width=30)
			self.total_slots.grid(row=5,column=1,padx=20)


			cost2_label=Label(park_window,text="2-WEELER Cost in Rs\nfor 1 hr or 60 min:")
			cost4_label=Label(park_window,text="4-WHEELER Cost in Rs\nfor 1 hr or 60 min:")
			total_solts_label=Label(park_window,text="Total Slots Available:")
		  
			cost2_label.grid(row=1,column=0,rowspan=2)
			cost4_label.grid(row=3,column=0,rowspan=2)
			total_solts_label.grid(row=5,column=0)

			save_cost_button = Button(park_window, text="SAVE PARKING DETAILS", bg="white", fg="black", padx=40, pady=20,
									 activebackground="red", command=self.save_details)
			save_cost_button.grid(row=6, column=1)



		def display(self):                 # FUNCTION TO DISPLAY EMPLOYEE DETAILS ON SCREEN
			global a_window
			display_window = Toplevel(a_window) # CREATING GUI WINDOW
												# DISPLAY WINDOW ON TOP OF MAIN WINDOW

			display_window.title(" Employee List ") # ASSIGNING WINDOW TITLE
			try:
				self.main_window.iconbitmap("main_icon.ico") # SETTING WINDOW ICON (PREFERRED FOR WINDOWS SYSTEM)
			except:
				self.main_window.iconbitmap("@main_icon.xbm") # SETTING WINDOW ICON (PREFERRED FOR LINUX SYSTEM)

			self.c.execute("SELECT * ,oid FROM employee") # FETCHING EMPLOYEE DETAILS FROM DATABASE
			records=self.c.fetchall()
			total_rows = len(records)
			total_columns = len(records[0])
			for r in range(total_rows):
				i=0
				for c in [-1,0,2,3]:
					dis = Entry(display_window,width=20,fg="blue",font=('Arial',16,'bold'))
					dis.grid(row=r,column=i)
					dis.insert(END,records[r][c])
					i+=1
			self.con.commit()    # COMMITING CHANGES TO DATABAS

		

		def submit(self):                     # FUNCTION TO SAVE EMPLOYEE DETAILS INTO DATABASE
		
			global register_window

			#CRYPTING USER PASSWORD FOR SAFE STORAGE
			
			self.hash_password =bcrypt.hashpw(str(self.password.get()).encode("utf-8"),bcrypt.gensalt())

			#SAVING EMPLOYEE DETAILS INTO DATABASE

			self.c.execute("INSERT INTO employee VALUES ( :full_name, :email, :phone_number, :login_id, :password)",
													  {
													  'full_name':self.f_name.get()+ " " + self.l_name.get(),
													  'email':self.email.get(),
													  'phone_number':self.phone_number.get(),
													  'login_id':self.login_id.get(),
													  'password':self.hash_password

													  })

			self.con.commit() # COMMITING CHANGES TO DATABASE
			
			#CLEARING INPUT FEILDS 
			self.f_name.delete(0,END)
			self.l_name.delete(0,END)
			self.email.delete(0,END)
			self.phone_number.delete(0,END)
			self.login_id.delete(0,END)
			self.password.delete(0,END)
			messagebox.showinfo("Registered", "Employee Registration sucessfull",parent=register_window)
			register_window.destroy()	#CLOSING REGISTER WINDOW AFTER SAVING VALUES
			



		def validate_name(self,name):     # FUNCTION TO VALIDATE USER NAME
			global register_window
			if name.isalpha():
				return True
			elif name == "":
				return True
			else:
				messagebox.showinfo("Validation", "Only Alphabets are allowed for Name",parent=register_window)
				return False

		def validate_number(self,number):  # FUNCTION TO VALIDATE USER NUMBER
			global register_window
			if number.isdigit():
				return True
			elif number == "":
				return True
			else:
				messagebox.showinfo("Validation", "Only Digits are allowed for Phone Number",parent=register_window)
				return False


		def validate_mail(self,mail):    # FUNCTION TO VALIDATE USER EMAIL
			global register_window
			if len(mail) > 7 :
				if re.match("^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[_a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",mail) != None:
					return True
				else :
					messagebox.showinfo("Validation", "This is not a valid email address",parent=register_window)
					return False

			else :
				messagebox.showinfo("Validation", "This is not a valid email address",parent=register_window)
				return False


		def validate_all(self):          # FUNCTION TO VALIDATE VALUES OF USER DETAILS

			global register_window
			if self.f_name.get() == "":
				messagebox.showinfo("Validation", "Please Enter First Name To Proceed",parent=register_window)
			elif self.l_name.get() == "":
				messagebox.showinfo("Validation", "Please Enter Last Name To Proceed",parent=register_window)
			elif self.phone_number.get() == "":
				messagebox.showinfo("Validation", "Please Enter phone Number To Proceed",parent=register_window)
			elif len(self.phone_number.get()) !=10:
				messagebox.showinfo("Validation", "Please Enter 10 Digit phone Number ",parent=register_window)
			elif self.email.get() == "":
				messagebox.showinfo("Validation", "Please Enter Email To Proceed",parent=register_window)
			elif self.login_id.get() == "":
				messagebox.showinfo("Validation", "Please Enter Login Id To Proceed",parent=register_window)
			elif self.password.get() == "" or self.cpassword.get() == "":
				messagebox.showinfo("Validation", "Please Enter Password To Proceed",parent=register_window)
			elif self.password.get() != self.cpassword.get():
				messagebox.showinfo("Validation", "Password Miss Match",parent=register_window)
			
			elif self.email.get() != "":
				status=self.validate_mail(self.email.get()) # VALIDATING USER EMAIL
				if status:
					self.submit()
			else:
				messagebox.showinfo("Registered", "Employee Registration sucessfull",parent=register_window)


						

			
	

		def register(self):                # FUNCTION TO REGISTER  EMPLOYEE DETAILS

			global a_window
			global register_window

			register_window = Toplevel(a_window) # CREATING GUI WINDOW
												 # LOGIN WINDOW ON TOP OF MAIN WINDOW

			register_window.title(" Registration Page ") # ASSIGNING WINDOW TITLE
			try:
				self.main_window.iconbitmap("main_icon.ico")  # SETTING WINDOW ICON (PREFERRED FOR WINDOWS SYSTEM)
			except:
				self.main_window.iconbitmap("@main_icon.xbm") # SETTING WINDOW ICON (PREFERRED FOR LINUX SYSTEM)

			register_window.geometry("550x400") # SETTING GEOMETERY OF WINDOW

			# MAIN HEADING LABEL 
			l1 = Label(register_window, text="EMPLOYEE REGISTRATION", font="Times 20 bold", padx=40, pady=40,bg="blue", fg="black")
			l1.grid(row=0, column=0, columnspan=3, padx=30, pady=30) # DISPLAYING LABEL IN WINDOW

			# SET OF LABELS FOR PROMPTING USER DETAILS
			f_name_label=Label(register_window,text="First Name")
			f_name_label.grid(row=1,column=0)
			l_name_label=Label(register_window,text="Last Name")
			l_name_label.grid(row=2,column=0)
			phone_number_label=Label(register_window,text="Phone Number")
			phone_number_label.grid(row=3,column=0)
			email_label=Label(register_window,text="Email")
			email_label.grid(row=4,column=0)
			login_id_label=Label(register_window,text="Login Id")
			login_id_label.grid(row=5,column=0)
			password_label=Label(register_window,text="Password")
			password_label.grid(row=6,column=0)
			cpassword_label=Label(register_window,text="Confirm Password")
			cpassword_label.grid(row=7,column=0)
			
			# SET OF ENTERY WIDGETS FOR INPUTING USER DETAILS

			self.f_name = Entry(register_window,width=30)
			self.f_name.grid(row=1,column=1,padx=20)
			self.l_name = Entry(register_window,width=30)
			self.l_name.grid(row=2,column=1,padx=20)
			self.phone_number = Entry(register_window,width=30)
			self.phone_number.grid(row=3,column=1,padx=20)
			self.email = Entry(register_window,width=30)
			self.email.grid(row=4,column=1,padx=20)
			self.login_id = Entry(register_window,width=30)
			self.login_id.grid(row=5,column=1,padx=20)
			self.password = Entry(register_window,width=30,show="*")
			self.password.grid(row=6,column=1,padx=20)
			self.cpassword = Entry(register_window,width=30,show="*")
			self.cpassword.grid(row=7,column=1,padx=20)


			#VALIDATING USER INPUT

			valid_name=register_window.register(self.validate_name)
			valid_number=register_window.register(self.validate_number)
			
			#VALIDATING USER INPUT

			self.f_name.config(validate="key",validatecommand=(valid_name,'%P'))
			self.l_name.config(validate="key",validatecommand=(valid_name,'%P'))
			self.phone_number.config(validate="key",validatecommand=(valid_number,'%P'))
		





			# SUBMIT BUTTON 
			# TO SAVE EMPLOYEE DETAILS

			submit_button = Button(register_window, text=" REGISTER EMPLOYEE",font="Times 15 bold" ,bg="white", fg="black",activebackground="green", command=self.validate_all)
			submit_button.grid(row=8,column=1,pady=30,ipadx=50)




		def admin_window(self):                  # FUNCTION TO INVOKE ADMIN GUI WINDOW
			global login_window,a_window
			a_window = Toplevel(self.main_window) # CREATING GUI WINDOW
												  # ADMIN WINDOW ON TOP OF MAIN WINDOW

			a_window.title(" Admin Page ")        # ASSIGNING WINDOW TITLE
			try:
				self.main_window.iconbitmap("main_icon.ico") # SETTING WINDOW ICON (PREFERRED FOR WINDOWS SYSTEM)
			except:
				self.main_window.iconbitmap("@main_icon.xbm") # SETTING WINDOW ICON (PREFERRED FOR LINUX SYSTEM)

			a_window.geometry("550x400")                      # SETTING GEOMETERY OF WINDOW

			# MAIN HEADING LABEL 
			l1 = Label(a_window, text="  WELCOME BACK ADMIN!!!!\n HAVE A GOOD DAY  ", font="Times 20 bold", padx=40, pady=40,bg="blue", fg="black")
			l1.grid(row=0, column=0, columnspan=3, padx=40, pady=30)  # DISPLAYING LABEL IN WINDOW

			# REGISTER BUTTON 
			# TO REGISTER USER DETAILS
			register_button = Button(a_window, text=" REGISTER EMPLOYEE", bg="white", fg="black", padx=40, pady=20,
									 activebackground="red", command=self.register)
			register_button.grid(row=1, column=1)

			# DISPLAY BUTTON 
			# TO DISPLAY LIST OF EMPLOYEE DETAILS
			display_button = Button(a_window, text=" SHOW EMPLOYEE LIST", bg="white", fg="black", padx=40, pady=20,
									 activebackground="red", command=self.display)
			display_button.grid(row=2, column=1)

			# PARKING BUTTON 
			# TO MODIFY PARKING DETAILS
			parking_button = Button(a_window, text="EDIT PARKING DETAILS", bg="white", fg="black", padx=40, pady=20,
									 activebackground="red", command=self.park_details)
			parking_button.grid(row=3, column=1)


		
		                            


		                                             """ END OF SCRIPT """
import sqlite3  

class Database:


	
		def __init__(self):

			self.con = sqlite3.connect('app_data.db') # CONNECTS TO DATABASE , CREATES DATABASE IF NONE EXIST
			self.c= self.con.cursor()                 # CREATING A CURSOR FOR THE CONNECTION 
			                                          # FOR EXECUTION OF SQL COMMANDS

			self.initialize_database()                # CALLING INITIALIZING FUNCTION


			

		def initialize_database(self):              


            #CREATING TABLES TO STORE DATA OF ADMIN EMPLOYEE AND PARKING STATS      


            # CREATING TABLE TO STORE EMPLOYEE DETAILS        

			try:
				self.c.execute("""CREATE TABLE employee (
						  full_name text NOT NULL,
						  email text NOT NULL UNIQUE,
						  phone text NOT NULL UNIQUE,
						  login_ig text NOT NULL UNIQUE,
						  password text NOT NULL
										)""")
			except:
				pass

			
			# CREATING TABLE TO STORE ADMIN DETAILS

			try:
				self.c.execute("""CREATE TABLE admin (
						  full_name text NOT NULL,
						  email text NOT NULL UNIQUE,
						  phone text NOT NULL UNIQUE,
						  login_ig text NOT NULL UNIQUE,
						  password text NOT NULL
										)""")
			except: 
				pass

			# CREATING TABLE TO STORE PARKING COST

			try:
				self.c.execute("""CREATE TABLE cost (
						  cost_2 text,
						  cost_4 text,
						  total_slots text
										  )""")
			except:
				pass


			# CREATING TABLE TO STORE PARKING STATS 

			try:
				self.c.execute("""CREATE TABLE vehicles (
						  customer_name text NOT NULL,
						  vehicle_type text NOT NULL ,
						  vehicle_number text NOT NULL UNIQUE,
						  customer_phone_number text NOT NULL UNIQUE,
						  check_in_time timestamp,
						  check_out_time timestamp,
						  total_min timestamp
										)""")
			except:
				pass
					

            #INITIALIZING TABLES WITH DEFAULT VALUES AND LOGIN CREDENTIALS


            #INITIALIZES TABLE EMPLOYEE WITH DEFAULT VALUES AND LOGIN CREDENTIALS

			try:                        

				self.c.execute("INSERT INTO employee VALUES ( :full_name, :email, :phone_number, :login_id, :password)",
													  {
													  'full_name':"mukund reddy",
													  'email':"mukundlpunest@gmail.com",
													  'phone_number':"9972439176",
													  'login_id':"mukund_rdd",
													  'password':"$2b$12$Yd9x9dym9xO.pVTVUXqmV.2wj/wo/RxsR9XZSvX2htp59A1VQMqwG"

													  })
			except:
				pass


            #INITIALIZES TABLE ADMIN WITH DEFAULT VALUES AND LOGIN CREDENTIALS	

			try:	
				self.c.execute("INSERT INTO admin VALUES ( :full_name, :email, :phone_number, :login_id, :password)",
													  {
													  'full_name':"mukund reddy",
													  'email':"mukundqwert@gmail.com",
													  'phone_number':"9972439176",
													  'login_id':"Admin",
													  'password':"$2b$12$Yd9x9dym9xO.pVTVUXqmV.2wj/wo/RxsR9XZSvX2htp59A1VQMqwG"

													  })
			except:
				pass

            #INITIALIZES TABLE COST WITH DEFAULT COST VALUES	
				

			try:
				self.c.execute("INSERT INTO cost VALUES ( :cost_2, :cost_4, :total_slots)",
													  {
													  'cost_2':'20',
													  'cost_4': '40',
													  'total_slots':'20'
													  })
			except:
				pass

				
            #INITIALIZES TABLE VEHICLES WITH DEFAULT VALUES 	

			try:
				self.c.execute("""INSERT INTO vehicles VALUES (
						  :customer_name,
						  :vehicle_type,
						  :vehicle_number,
						  :customer_phone_number,
						  :check_in_time,
						  :check_out_time,
						  :total_min
										)""",
						 {'customer_name':' Customer name ',
						  'vehicle_type':' Vehicle Type ',
						  'vehicle_number':'Vehicle Number',
						  'customer_phone_number':'Phone Number',
						  'check_in_time':'In-Time',
						  'check_out_time':'Out-Time',
						  'total_min':'Total Time'

									})
			except:
				pass	
			self.con.commit()  # COMMITING CHANGES TO DATABASE
from tkinter import  *                              # IMPORTING TKINTER LIBRARY CLASSES AND FUNCTIONS 
from tkinter import messagebox                      # IMPORTING TKINTER MESSEGEBOX FOR POP UP WARNINGS AND INFO

import sqlite3                                      # IMPORTING SQL LITE LIBRARY FOR 
                                                    # FETCHING AND STORING VALUES TO DATABASE

import datetime                                     # DATETIME LIBRARY TO FETCH CURRENT DATE AND TIME

from print_invoice import print_bill                # PRINT INVOICE SCRIPT TO SAVE INVOICE AS PDF 

class Employee:                                     #ADMIN CLASS WHICH IS CALLED IN LOGIN SCRIPT
		


		def __init__(self,main_window):             # CONSTRUCTOR TO INITIALIZE CONNECTION WITH DATABASE 
                                                    # AND INTIALIZE VALUES

			self.con = sqlite3.connect('app_data.db')
			self.c= self.con.cursor()	

			self.main_window=main_window            # ASSIGNING MAIN WINDOW OBJECT

			self.employee_window()                  # INVOKING EMPLOYEE GUI WINDOW



		def stats(self):                            # FUNCTION TO DISPLAY PARKING STATISTICS 
			global e_window
			stats_window = Toplevel(e_window)       # CREATING GUI WINDOW
												    # DISPLAY WINDOW ON TOP OF MAIN WINDOW

			stats_window.title(" Employee List ")   # ASSIGNING WINDOW TITLE
			try:
				self.main_window.iconbitmap("main_icon.ico") # SETTING WINDOW ICON (PREFERRED FOR WINDOWS SYSTEM)
			except:
				self.main_window.iconbitmap("@main_icon.xbm") # SETTING WINDOW ICON (PREFERRED FOR LINUX SYSTEM)

			self.c.execute("SELECT * ,oid FROM vehicles")     # FETCHING VEHICLE DETAILS FROM DATABASE
			records=self.c.fetchall()
			total_rows = len(records)
			total_columns = len(records[0])
			for r in range(total_rows):
				for c in range(total_columns):
					dis = Entry(stats_window,width=20,fg="blue",font=('Arial',16,'bold'))
					dis.grid(row=r,column=c)
					dis.insert(END,records[r][c])
				
			self.con.commit()         # COMMITING CHANGES TO DATABAS



		def calc_bill(self,o_v,tot_time):           # FUNCTION TO CALCULATE PARKING BILL
			self.amount_payable=0.0
			tot_time=tot_time
			o_v=o_v
			self.c.execute("SELECT *,oid FROM vehicles where vehicle_number=?",(o_v,)) # FETCHING DETAILS FROM DATABASE
			customer_details=self.c.fetchall()
			self.c.execute("SELECT *,oid FROM cost")                                   # FETCHING DETAILS FROM DATABASE
			cost_details=self.c.fetchall()
			
			v_type=customer_details[0][1]
			


			if v_type =='2-WHEELER':
				self.cost_min=str(int(cost_details[0][0])/60)
				self.amount_payable=float(self.cost_min)*float(tot_time[0])
			elif v_type =='4-WHEELER':
				self.amount_payable=float(cost_details[0][1]/60)*float(tot_time[0])
			else:
				error_msg="INVALID VEHICLE TYPE"
			
			self.display_bill(customer_details,self.cost_min,self.amount_payable)      # CALLING DISPLAY BILL FUNCTION 




		
		def print_details(self,oid,c_name,v_type,v_num,c_p_num,tot_time,cost_min,amount_payable):  # FUNCTION TO SEND PARKING BILL DETAILS
		                                                                                           # TO PRINT INVOICE SCRIPT
			global display_window
			amount_payable=self.amount_payable
			cost_min=self.cost_min
			print_bill(oid,c_name,v_type,v_num,c_p_num,tot_time,cost_min,amount_payable)          # PASSING BILL DETAILS TO CREATE INVOICE
			messagebox.showinfo("Print Invoice", "Print Sucessfull \n Saved In Your Program Folder",parent=display_window)






		def display_bill(self,customer_details,cost_min,amount_payable):  # FUNCTION TO DISPLAY PARKING BILL
			self.amount_payable=0.0

			global check_out_window,display_window
			c_name= customer_details[0][0]   
			v_type=customer_details[0][1]
			v_num = customer_details[0][2]
			c_p_num=customer_details[0][3]
			c_in_time=customer_details[0][4]
			c_out_time=customer_details[0][5]
			tot_time=customer_details[0][6]
			oid=customer_details[0][-1]
			self.amount_payable=amount_payable
			
			display_window =Toplevel(check_out_window)
			display_window.title(" Bill Page ")
			try:
				self.main_window.iconbitmap("main_icon.ico")
			except:
				self.main_window.iconbitmap("@main_icon.xbm")
			display_window.geometry("550x400")

			# MAIN HEADING LABEL 

			l1 = Label(display_window, text="BILL INVOICE", font="Times 20 bold", padx=40, pady=40,bg="blue", fg="black")
			l1.grid(row=0, column=0, columnspan=3, padx=30, pady=30)

			# SET OF LABELS TO DISPLAY PARKING BILL         
			r1=Label(display_window,text="Customer Name:")       # HERE r- REFERS TO ROW
			r1.grid(row=1,column=0)                              # AND c- REPRESENTS COLUMN
			c1=Label(display_window,text=c_name)
			c1.grid(row=1,column=1)
			r2=Label(display_window,text="Phone Number:")
			r2.grid(row=2,column=0)
			c2=Label(display_window,text=c_p_num)
			c2.grid(row=2,column=1)
			r3=Label(display_window,text="Vehicle Type:")
			r3.grid(row=3,column=0)
			c3=Label(display_window,text=v_type)
			c3.grid(row=3,column=1)
			r4=Label(display_window,text="Vehicle Number:")
			r4.grid(row=4,column=0)
			c4=Label(display_window,text=v_num)
			c4.grid(row=4,column=1)
			r5=Label(display_window,text="Check-in Time:")
			r5.grid(row=5,column=0)
			c5=Label(display_window,text=c_in_time)
			c5.grid(row=5,column=1)
			r6=Label(display_window,text="Check-out Time:")
			r6.grid(row=6,column=0)
			c6=Label(display_window,text=c_out_time)
			c6.grid(row=6,column=1)
			r7=Label(display_window,text="Amount Payable:")
			r7.grid(row=7,column=0)
			c7=Label(display_window,text=self.amount_payable)
			c7.grid(row=7,column=1)

			# PRINT BUTTON 
			# TO SAVE BILL DETAILS
			print_button = Button(display_window, text=" PRINT BILL ",font="Times 15 bold" ,bg="white", fg="black",activebackground="green", command=lambda: self.print_details(oid,c_name,v_type,v_num,c_p_num,tot_time,self.cost_min,self.amount_payable))
			print_button.grid(row=8,column=1,pady=30,ipadx=50)







		def checkout_details(self):                   # FUNCTION IS USED TO UPDATE CHECK-OUT TIME OF A VEHICLE
			
			check_out_time= datetime.datetime.now()
			out_vehicle=self.out_vehicle_number.get()

			self.c.execute("SELECT check_in_time,oid FROM vehicles where vehicle_number=?",(out_vehicle,))
			records=self.c.fetchall()

			
		   
			check_in_time = datetime.datetime.strptime(records[0][0], "%Y-%m-%d %H:%M:%S.%f")
			tot_min=check_out_time-check_in_time

			tot_min =  divmod(tot_min.total_seconds(), 60) 

			self.c.execute("UPDATE vehicles SET check_out_time=?,total_min=? where vehicle_number=?",(check_out_time,tot_min[0],out_vehicle))
			self.con.commit()
			self.calc_bill(out_vehicle,tot_min)


			

		def checkout(self):                      # FUNCTION IS USED TO  CHECK-OUT  A VEHICLE
			
			global e_window,check_out_window
			check_out_window =Toplevel(e_window)
			check_out_window.title(" Exit Page ")
			try:
				self.main_window.iconbitmap("main_icon.ico")
			except:
				self.main_window.iconbitmap("@main_icon.xbm")
			check_out_window.geometry("550x400")

			l1 = Label(check_out_window, text="CHECK-OUT VEHICLE", font="Times 20 bold", padx=40, pady=40,bg="blue", fg="black")
			l1.grid(row=0, column=0, columnspan=3, padx=30, pady=30)
		
			self.out_vehicle_number = Entry(check_out_window,width=30)
			self.out_vehicle_number.grid(row=1,column=1,padx=20)
			
			
			
			out_vehicle_number_label=Label(check_out_window,text="Vehical Number")
			out_vehicle_number_label.grid(row=1,column=0)
			
		
			check_out_button = Button(check_out_window, text=" CHECK-OUT ",font="Times 15 bold" ,bg="white", fg="black",activebackground="green", command=self.checkout_details)
			check_out_button.grid(row=2,column=1,pady=30,ipadx=50)




		def entery_details(self):              # FUNCTION IS USED TO SAVE CHECK-IN TIME AND DETAILS OF A VEHICLE

			global check_in_window
			
			self.check_in_time= datetime.datetime.now()

			self.c.execute("INSERT INTO vehicles VALUES ( :customer_name, :vehicle_type,:vehicle_number ,:customer_phone_number, :check_in_time,:check_out_time,:total_min)",
													  {
													  'customer_name':self.customer_name.get(),
													  'vehicle_type':self.vehicle_type.get(),
													  'vehicle_number':self.vehicle_number.get(),
													  'customer_phone_number':self.customer_phone_number.get(),
													  'check_in_time':self.check_in_time,
													  'check_out_time':'0',
													  'total_min':'0'
													  })

			self.con.commit()  # COMMITING CHANGES TO DATABASE
			
			#CLEARING INPUT FEILDS 
			
			self.customer_name.delete(0,END)
		
			self.vehicle_number.delete(0,END)
			self.customer_phone_number.delete(0,END)
			messagebox.showinfo("Registered", "Entry Sucessfull",parent=check_in_window)
			check_in_window.destroy()         #CLOSING CHECK-IN WINDOW AFTER SAVING VALUES




		def checkin(self):                                 # FUNCTION IS USED TO  CHECK-IN  A VEHICLE
			global e_window,check_in_window
			check_in_window =Toplevel(e_window)
			check_in_window.title(" Entry Page ")
			try:
				self.main_window.iconbitmap("main_icon.ico")
			except:
				self.main_window.iconbitmap("@main_icon.xbm")
			check_in_window.geometry("550x400")

			# MAIN HEADING LABEL 

			l1 = Label(check_in_window, text="CHECK-IN VEHICLE", font="Times 20 bold", padx=40, pady=40,bg="blue", fg="black")
			l1.grid(row=0, column=0, columnspan=3, padx=30, pady=30)

			#SET OF ENTRY WIDGETS TO INPUT VALUES
			self.customer_name = Entry(check_in_window,width=30)
			self.customer_name.grid(row=1,column=1,padx=20)
			self.vehicle_type = StringVar(check_in_window)
			self.vehicle_type.set("2-WHEELER")
			self.vehi_type = OptionMenu(check_in_window, self.vehicle_type, "2-WHEELER", "4-WHEELER")
			self.vehi_type.config(bg="WHITE",font="Times 10 bold")
			self.vehi_type.grid(row=2,column=1,padx=20)
			self.vehicle_number = Entry(check_in_window,width=30)
			self.vehicle_number.grid(row=3,column=1,padx=20)
			self.customer_phone_number = Entry(check_in_window,width=30)
			self.customer_phone_number.grid(row=4,column=1,padx=20)

			# SET OF LABELS FOR PROMPTING CHECK-IN DETAILS

			customer_name_label=Label(check_in_window,text="Customer Name:")
			customer_name_label.grid(row=1,column=0)
			vehicle_type_label=Label(check_in_window,text="Vehical Type:")
			vehicle_type_label.grid(row=2,column=0)
			vehicle_number_label=Label(check_in_window,text="Vehical Number")
			vehicle_number_label.grid(row=3,column=0)
			customer_phone_number_label=Label(check_in_window,text="Customer Phone Number")
			customer_phone_number_label.grid(row=4,column=0)

			# CHECK-IN BUTTON 
			# TO SAVE CHECK-IN DETAILS

			check_in_button = Button(check_in_window, text=" SUBMIT ",font="Times 15 bold" ,bg="white", fg="black",activebackground="green", command=self.entery_details)
			check_in_button.grid(row=7,column=1,pady=30,ipadx=50)





		def employee_window(self):            # FUNCTION TO INVOKE EMPLOYEE GUI WINDOW
			global e_window
			e_window = Toplevel(self.main_window) # CREATING GUI WINDOW
												  # EMPLOYEE WINDOW ON TOP OF MAIN WINDOW

			e_window.title(" Executive Page ")    # ASSIGNING WINDOW TITLE
			try:
				self.main_window.iconbitmap("main_icon.ico") # SETTING WINDOW ICON (PREFERRED FOR WINDOWS SYSTEM)
			except:
				self.main_window.iconbitmap("@main_icon.xbm") # SETTING WINDOW ICON (PREFERRED FOR LINUX SYSTEM)  

			e_window.geometry("550x400")          # SETTING GEOMETERY OF WINDOW

			# MAIN HEADING LABEL 

			l1 = Label(e_window, text="  WELCOME BACK \n HAVE A GOOD DAY  ", font="Times 20 bold", padx=40, pady=40,bg="blue", fg="black")
			l1.grid(row=0, column=0, columnspan=3, padx=30, pady=30) # DISPLAYING LABEL IN WINDOW

			# CHECK-IN BUTTON 
			# TO CHECK-IN VEHICLE

			check_in_button = Button(e_window, text=" CHECK-IN", bg="white", fg="black", padx=40, pady=20,
									 activebackground="red", command=self.checkin)
			check_in_button.grid(row=1, column=1)

			# CHECK-OUT BUTTON 
			# TO CHECK-OUT VEHICLE

			check_out_button = Button(e_window, text="CHECK-OUT", bg="white", fg="black", padx=40, pady=20,
									 activebackground="red", command=self.checkout)
			check_out_button.grid(row=2, column=1)

			# BUTTON TO DISPLAY PARKING STATISTICS 
			stats_button = Button(e_window, text="STATISTICS", bg="white", fg="black", padx=40, pady=20,
									 activebackground="red", command=self.stats)
			stats_button.grid(row=3, column=1)
from tkinter import  *                  # IMPORTING TKINTER LIBRARY CLASSES AND FUNCTIONS 
from tkinter import messagebox          # IMPORTING TKINTER MESSEGEBOX FOR POP UP WARNINGS AND INFO

import bcrypt                           # IMPORTING BYCRYPT LIBRARY WHICH USED TO SAVE PASSWORDS SAFELY
import sqlite3                          # IMPORTING SQL LITE LIBRARY FOR 
                                        # FETCHING VALUES FROM DATABASE

from admin_win import Admin             # IMPORTING ADMIN WINDOW SCRIPT TO INVOKE ADMIN WINDOW WHEN PROMPTED

from employee_win import Employee       # IMPORTING EMPLOYEE WINDOW SCRIPT TO INVOKE EMPLOYEE WINDOW WHEN PROMPTED

class Login:
		


		def __init__(self,main_window,user):      # CONSTRUCTOR TO INITIALIZE CONNECTION WITH DATABASE 
                                                  # AND INTIALIZE VALUES
			self.con = sqlite3.connect('app_data.db')
			self.c= self.con.cursor()	
			self.main_window=main_window          # ASSIGNING MAIN WINDOW OBJECT
			self.user=user
			self.login()                          # INVOKING LOGIN GUI WINDOW 



		def verify(self):                         # FUNCTION TO VERIFY USER DETAILS

			global login_window
			uid=StringVar()
			uid= self.user_name.get()             # FETCHING USER ID
			pwd=self.password.get().encode("utf-8")  # FETCHING PASSWORD AND ENCODING IT INTO UTF-8 FORMAT


			
			# VERIFYING USER DETAILS

			if self.user == "ADMIN":  

			    # FETCHING ADMIN RECORDS
				admin_temp={record[0]:record[1] for record in self.con.execute("SELECT login_ig,password from admin") }

				if uid in admin_temp.keys():
					if bcrypt.checkpw(pwd, admin_temp[uid].encode("utf-8")): # CHECKING CRYPTED PASSWORD 
						Label(login_window, text="Valid User",font="10").grid(row=6, column=1, padx=10, pady=10)
						login_window.destroy()
						a=Admin(self.main_window)  # INVOKING ADMIN WINDOW

					else:
						self.result = "Wrong Password"
						Label(login_window, text=self.result,font="10").grid(row=6, column=1, padx=10, pady=10)

				else:
					self.result = "User Does Not Exist"
					Label(login_window, text=self.result,font="10").grid(row=6, column=1, padx=10, pady=10)
			else:

				# FETCHING ADMIN RECORDS

				emp_temp={record[0]:record[1] for record in self.con.execute("SELECT login_ig,password from employee") }

				if uid in emp_temp.keys():
					if bcrypt.checkpw(pwd, emp_temp[uid]): # CHECKING CRYPTED PASSWORD 
						Label(login_window, text="Valid User",font="10").grid(row=6, column=1, padx=10, pady=10)
						login_window.destroy()
						e=Employee(self.main_window)  # INVOKING EMPLOYEE WINDOW

					else:
						self.result = "Wrong Password"
						Label(login_window, text=self.result,font="10").grid(row=6, column=1, padx=10, pady=10)

				else:
					self.result = "User Does Not Exist"
					Label(login_window, text=self.result,font="10").grid(row=6, column=1, padx=10, pady=10)
				




		def login(self):                                  # FUNCTION TO INVOKE LOGIN GUI WINDOW

			global login_window

			login_window = Toplevel(self.main_window)    # CREATING GUI WINDOW
														 # LOGIN WINDOW ON TOP OF MAIN WINDOW

			login_window.title(" Login Page ")           # ASSIGNING WINDOW TITLE

			try:
				self.main_window.iconbitmap("main_icon.ico") # SETTING WINDOW ICON (PREFERRED FOR WINDOWS SYSTEM)
			except:
				self.main_window.iconbitmap("@main_icon.xbm") # SETTING WINDOW ICON (PREFERRED FOR LINUX SYSTEM)

			login_window.geometry("550x400")                  # SETTING GEOMETERY OF WINDOW

            # MAIN HEADING LABEL  
			l1 = Label(login_window, text="   LOGIN   ", font="Times 20 bold", padx=40, pady=40,bg="blue", fg="black")
			l1.grid(row=0, column=0, columnspan=3, padx=30, pady=30) # DISPLAYING LABEL IN WINDOW

            # SET OF LABELS AND ENTERY TO INPUT USER DETAILS

			l2=Label(login_window, text="User Name: ")
			l2.grid(row=1, column=0, padx=10, pady=10)
			self.user_name=StringVar()
			id=Entry(login_window, textvariable=self.user_name)
			id.grid(row=2, column=0, padx=10, pady=10)
			l3=Label(login_window, text="Password: ")
			l3.grid(row=3, column=0, padx=10, pady=10)
			self.password = StringVar()
			pwd=Entry(login_window, textvariable=self.password,show='*')
			pwd.grid(row=4, column=0, padx=10, pady=10)
			
			# LOGIN BUTTON 
			# TO VERIFY USER DETAILS AND INVOKE RESPECTIVE PAGES 
			login_button = Button(login_window, text="   LOGIN   ", bg="white", fg="black", padx=60, pady=20,activebackground="red", command=self.verify)
			login_button.grid(row=5, column=0, padx=10, pady=10)

			# CONFIGURING LABELS FOR FULL SCREEN

			l1.grid_configure(sticky="nsew")
			l2.grid_configure(sticky="nsew")
			l3.grid_configure(sticky="nsew")

			# CONFIGURING MAIN WINDOW FOR FULL SCREEN 

			login_window.grid_rowconfigure(0, weight=1)
			login_window.grid_columnconfigure(0, weight=1)

			# LOOP TO WAIT FOR CAPTURING EVENTS AND VALUES OF LOGIN WINDOW

			login_window.mainloop()
from database import Database    # SCRIPT TO INITIALIZE  DATA BASE AND ASSIGN DEFAULT LOGIN CREDENTIALS
                                 # FOR ADMIN AND EMPLOYEE

from tkinter_win import Gui      # SCRIPT TO INVOKE TKINTER GUI




class Parking:

		def __init__(self):    # CONSTRUCTOR
			self.main()        # CALLING MAIN FUNCTION 

		def main(self):

			dbase=Database() # INITIALIZING DATABASE BY CALLING CONSTRUCTOR OF Database CLASS
			display=Gui()    # INVOKING TKINTER GUI 
			
				
	
Parking()    # CALLING PARKING CLASS 
# Importing Required Module
from reportlab.pdfgen import canvas

from datetime import date 
import math
def print_bill(oid,c_name,v_type,v_num,c_p_num,tot_time,cost_min,amount_payable):
	
	# Creating Canvas
	c = canvas.Canvas(v_num+"_"+"invoice.pdf",pagesize=(200,250),bottomup=0)

	# Logo Section
	# Setting th origin to (10,40)
	c.translate(10,40)
	# Inverting the scale for getting mirror Image of logo
	c.scale(1,-1)
	# Inserting Logo into the Canvas at required position
	c.drawImage("logo.png",0,0,width=50,height=40)

	# Title Section
	# Again Inverting Scale For strings insertion
	c.scale(1,-1)
	# Again Setting the origin back to (0,0) of top-left
	c.translate(-10,-40)
	# Setting the font for Name title of company
	c.setFont("Helvetica-Bold",8)
	# Inserting the name of the company
	c.drawCentredString(125,20,"M$S SOFTWARE SOLUTIONS")
	# For under lining the title
	c.line(70,22,180,22)
	# Changing the font size for Specifying Address
	c.setFont("Helvetica-Bold",5)
	c.drawCentredString(125,30,"Block No. 101, Sky Apartments, Bangalore,")
	c.drawCentredString(125,35,"Karnataka - 56004, India")
	# Changing the font size for Specifying GST Number of firm
	c.setFont("Helvetica-Bold",6)
	c.drawCentredString(125,42,"GSTIN : 07AABCS1429B1Z")

	# Line Seprating the page header from the body
	c.line(5,45,195,45)

	# Document Information
	# Changing the font for Document title
	c.setFont("Courier-Bold",8)
	c.drawCentredString(100,55,"PARKING-INVOICE")

	# This Block Consist of Costumer Details
	c.roundRect(15,63,170,40,10,stroke=1,fill=0)
	c.setFont("Times-Bold",5)
	c.drawRightString(70,70,"INVOICE No. :  "+str(oid))
	c.drawRightString(70,80,"DATE: "+str(date.today()))
	c.drawRightString(96,90,"CUSTOMER NAME: "+ c_name)
	c.drawRightString(86,100,"PHONE No. : "+ str(c_p_num))

	# This Block Consist of Item Description
	c.roundRect(15,108,170,130,10,stroke=1,fill=0)
	c.line(15,120,185,120)
	c.drawCentredString(30,118,"VType")
	c.drawCentredString(75,118,"Vehical Number:")
	c.drawCentredString(115,118,"RATE")
	c.drawCentredString(137,118,"TIME")
	c.drawCentredString(172,118,"AMOUNT")

	c.drawCentredString(30,140,str(v_type))
	c.drawCentredString(75,140,str(v_num))
	c.drawCentredString(115,140,str(math.ceil(float(cost_min)*60)))
	c.drawCentredString(137,140,str(math.ceil(int(tot_time)/60)))
	c.drawCentredString(168,140,str(math.ceil(float(amount_payable))))


	# Drawing table for Item Description
	c.line(15,210,185,210)
	c.line(45,108,45,220)
	c.line(105,108,105,220)
	c.line(125,108,125,220)
	c.line(160,108,160,220)

	# Declaration and Signature
	c.line(15,220,185,220)
	c.line(100,220,100,238)
	c.drawString(20,225,"We declare that above mentioned")
	c.drawString(20,230,"information is true.")
	c.drawString(20,235,"(This is system generated invoive)")
	c.drawRightString(180,235,"Authorised Signatory")

	# End the Page and Start with new
	c.showPage()
	# Saving the PDF
	c.save()
from tkinter import  *                   # IMPORTING TKINTER LIBRARY CLASSES AND FUNCTIONS 
from tkinter import messagebox           # IMPORTING TKINTER MESSEGEBOX FOR POP UP WARNINGS AND INFO

import sqlite3                           # IMPORTING SQL LITE LIBRARY FOR 
                                         # CLOSING CONNECTION WITH DATABASE WHEN MAIN WINDOW CLOSES 

from login import Login                  # IMPORTING LOGIN SCRIPT TO INVOKE LOGIN WINDOW WHEN PROMPTED


class Gui:                               # CLASS FOR GUI ,WHICH IS CALLED IN MAIN SCRIPT


		def __init__(self):              # CONSTRUCTOR TO INITIALIZE CONNECTION WITH DATABASE 
			self.con = sqlite3.connect('app_data.db')
			self.c= self.con.cursor()	

			self.main_win()              # INVOKING MAIN GUI WINDOW 

		def call(self):                  # FUNCTION TO INVOKE OR CALL LOGIN WINDOW
			global main_window

			l=Login(main_window,self.user.get()) # CALLING LOGIN CLASS , PASSING MAIN WINDOW OBJECT AND TYPE OF USER DETAILS

		def on_closing(self):                    # FUNCTION TO HANDEL CLOSING WINDOW EVENT 
			global main_window
			if messagebox.askokcancel("Quit", "Do you want to quit?"):   # ASKING USER CONFIRMATION
				self.con.close()	                                     # CLOSSING CONNECTION WITH DATABASE
				main_window.destroy()	                                 # CLOSING MAIN WINDOW

		def main_win(self):              # MAIN WINDOW FUNCTION 
			global main_window
			main_window = Tk()           # CREATING GUI WINDOW
			main_window.title(" Parking Management ") # ASSIGNING WINDOW TITLE

			try:
				main_window.iconbitmap("main_icon.ico") # SETTING WINDOW ICON (PREFERRED FOR WINDOWS SYSTEM)
			except:
				main_window.iconbitmap("@main_icon.xbm") # SETTING WINDOW ICON (PREFERRED FOR LINUX SYSTEM)

					
			main_window.geometry("550x400")              # SETTING GEOMETERY OF WINDOW 

			# MAIN HEADING LABEL      
			l1=Label(main_window, text="PARKING MANAGEMENT AUTHENTICATION", font="Times 15 bold",padx=10, pady=40, bg="red", fg="black")
			l1.grid(row=0,column=0,columnspan=3,padx=30,pady=30) # DISPLAYING LABEL IN WINDOW
			self.user = StringVar(main_window)                   # VARIABLE TO STORE TYPE OF USER LOGGING-IN
			self.user.set("EMPLOYEE")                            # SETTING DEFAULT USER VALUE

			w = OptionMenu(main_window, self.user, "ADMIN", "EMPLOYEE")  # MENU FOR CHOICING TYPE OF USER
			w.config(bg="WHITE",font="Times 20 bold")                    # SETTING BACKGROUNG COLOR AND FONT
			w.grid(row=1,column=0,columnspan=3,padx=30,pady=30,rowspan=2) # DISPLAYING MENU IN WINDOW
			# LOGIN BUTTON 
			# TO INVOKE LOGIN PAGE
			login_button = Button(main_window, text="LOGIN",font="Times 15 bold", bg="white", fg="black", padx=60, pady=10,activebackground="red", command=self.call)
			login_button.grid(row=3, column=0,columnspan=3,padx=30,pady=30,rowspan=2) # DISPLAYING LOGIN BUTTON IN WINDOW
			l1.grid_configure(sticky="nsew")


			main_window.grid_rowconfigure(0, weight=1)  # CONFIGURING MAIN WINDOW FOR FULL SCREEN 
			main_window.grid_columnconfigure(0, weight=1) # CONFIGURING MAIN WINDOW FOR FULL SCREEN 

			main_window.protocol("WM_DELETE_WINDOW",self.on_closing) # CAPTURING CLOSING EVENT

			main_window.mainloop() # LOOP TO WAIT FOR CAPTURING EVENTS AND VALUES OF MAIN WINDOW
