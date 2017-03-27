import MySQLdb
from Tkinter import *
import tkMessageBox
import tkSimpleDialog
import  PIL
from PIL import ImageTk, Image

db = MySQLdb.connect(host = "localhost", user = "root", passwd = "",  )
returnPath = "mysql"

def donothingg():
	tkMessageBox.showinfo("Information","Application Created By Muhammad Shahriyar Sheikh \n Roll Number: 13K-2015")

def donothing():
	root.destroy()
	exit()


def queryMaker(source,sourcet,dest,destt):
	p = source + "." + sourcet
	o = dest + "." + destt
	return "INSERT INTO " + o + " SELECT * from " + p

	
def databases():
	tab = db.cursor()
	tab.execute("Show Databases")
	
	re = tab.fetchall()
	tkMessageBox.showinfo("Available Databases ...\n",re)
	tab.close()


def tablesinsource():
	tab = db.cursor()
	tab.execute("Show tables from %s"%sou)
	re = tab.fetchall()
	tkMessageBox.showinfo("Tables in '%s' ...          "%sou, re)
	tab.close()

def tablesindest():
	tab = db.cursor()
	tab.execute("Show tables from %s"%des)
	re = tab.fetchall()
	tkMessageBox.showinfo("Tables in '%s' ...          "%des, re)
	tab.close()


def theHardestPart():


	maincursor = db.cursor()

	stabl = tkSimpleDialog.askstring("Table from '%s'"%sou,"Enter A Table which exists in the Source Database")
	dtabl = tkSimpleDialog.askstring("Table from '%s'"%des,"Enter A Table which exists in the Destination Database")

	if stabl == "" or dtabl == "":
		tkMessageBox.showerror("Error","Please enter the proper information\n Terminating abrubtly!")
		exit()

	#SAME COLUMN METHOD STARTS HERE .. . . 


	cur = db.cursor()
	sqli = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + stabl + "' AND TABLE_SCHEMA = '"+ sou + "'"
	cur.execute(sqli)
	re = cur.fetchone()

	sqli = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + dtabl + "' AND TABLE_SCHEMA = '"+ des + "'"
	cur.execute(sqli)
	de = cur.fetchone()
	cur.close()

	if re[0] != de[0] and stabl == dtabl:
		tkMessageBox.showerror("Error","Cannot Perform Append Because Both tables have different Number of Columns")
		

	#SAME COLUMN METHOD END HERE ..........................



	fsou = sou + "." + stabl
	fdest = des + "." + dtabl
	maincursor.execute("Select * from %s"%fsou)
	if maincursor.fetchone == None:
		tkMessageBox.showerror("Error","Cannot Perform Because Source Table Is Empty.\n In Other words, there is nothing to Copy ")
	else :



		sql = queryMaker(sou,stabl,des,dtabl)

		#fdest = des + "." + dtabl

		maincursor.execute("SELECT * FROM %s"%fdest)
		if maincursor.fetchone() == None:                                    #if the destination table selected does not contain any tuple/ rows of data

			maincursor.execute(sql)
			#maincursor.execute("SELECT * from %s"%fdest)
			#temp = maincursor.fetchall()

			flag = tkMessageBox.askyesno("Copy Machine B","Tables have successfully been copied, Do you wish to COMMIT?")
			if flag == True:
				db.commit()
				


		else:                                                                #Otherwise
			tempInput = tkSimpleDialog.askstring("Wait!","This table in the destination database allready consists of data. Do you wish to Overwrite? OR Do you wish to append (Press 'a' for append OR 'o' for overwrite)")

			
			
			if tempInput == 'a' or tempInput == 'A':
				
				cura = db.cursor()
				sqli = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + stabl + "' AND TABLE_SCHEMA = '"+ sou + "'"
				cura.execute(sqli)
				re = cura.fetchone()
				cura.execute("SHOW fields from %s"%fsou)
				numb = cura.fetchone()


				sqli = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + dtabl + "' AND TABLE_SCHEMA = '"+ des + "'"
				cura.execute(sqli)
				de = cura.fetchone()
				cura.execute("SHOW fields from %s"%fdest)
				numb2 = cura.fetchone()


				cura.close()
				#print re[0]
				#print de[0]
				if re[0] == de[0] and numb[0] == numb2[0]:

					maincursor.execute(sql)												#Append starts here
					#maincursor.execute("SELECT * from %s"%fdest)
					#temp = maincursor.fetchall()
					flag = tkMessageBox.askyesno("Copy Machine B)","Tables have successfully been copied, Do you wish to COMMIT?")
					if flag == True:
						db.commit()															
				else:
					tkMessageBox.showerror("Error","Cannot Perform Append Because Both tables have different Number of Columns")#Append Ends here

			elif tempInput == 'o' or tempInput == 'O':

				
				curo = db.cursor()
				sqli = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + stabl + "' AND TABLE_SCHEMA = '"+ sou + "'"
				curo.execute(sqli)
				re = curo.fetchone()
				curo.execute("SHOW fields from %s"%fsou)
				numb = curo.fetchone()



				sqli = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + dtabl + "' AND TABLE_SCHEMA = '"+ des + "'"
				curo.execute(sqli)
				de = curo.fetchone()
				curo.execute("SHOW fields from %s"%fdest)
				numb2 = curo.fetchone()



				curo.close()
				#print re[0]
				#print de[0]
				if re[0] == de[0] and numb[0] == numb2[0] :                  #name same but column different OR column same but name different


					maincursor.execute("TRUNCATE TABLE %s"%fdest)							#Overwrite Starts here
					maincursor.execute(sql)
					
					#maincursor.execute("SELECT * from %s"%fdest)
					#temp = maincursor.fetchall()										
					flag = tkMessageBox.askyesno("Copy Machine B)","Tables have successfully been copied, Do you wish to COMMIT?")
					if flag == True:
						db.commit()	
																				#Overwrite Ends Here

				else:
					tkMessageBox.showerror("Error","Cannot Perform Overwrite Because Both tables have different Number of Columns")#Append Ends here
					


				# maincursor.execute("DROP TABLE %s"%fdest)							#Overwrite Starts here
				# over = "Create table " + fdest + " AS SELECT * FROM " + fsou
				# maincursor.execute(over)
				# #maincursor.execute("SELECT * from %s"%fdest)
				# #temp = maincursor.fetchall()										
				# flag = tkMessageBox.askyesno("Copy Machine B)","Tables have successfully been copied, Do you wish to COMMIT?")
				# if flag == true:
				# 	db.commit()															#Overwrite Ends Here




			else:
				print "Sorry wrong option Entered" 
				exit()









root = Tk()
root.withdraw()
databases()

#*******************************************************************************************************************************
sou = tkSimpleDialog.askstring("Source Database", "Enter the Source Database (Where do you want to copy from)")

cur1 = db.cursor()                          #To Check the existence of the first db
firstDbExists = cur1.execute("Show Databases like '%s'"%sou)
if firstDbExists != 1:
	tkMessageBox.showwarning("Nope","Cannot Find any database named '%s'" % sou)
	exit()

checking = db.cursor()										#checks whether the database selected by the user is not an empty one
checking.execute("Show tables from %s"%sou)
itIsEmpty = checking.fetchone()
if itIsEmpty == None:
	tkMessageBox.showwarning("Nope"," The database you selected '%s', is empty .....\n Even if you wanted to copy something from here, you wont be able to :/" % sou)
	exit()







#******************************************************************************************************************************
des = tkSimpleDialog.askstring("Destination Database", "Enter the Destination Database (Where do you want to copy to)")
cur2 = db.cursor()                          #To Check the existence of the second db
secDbExists = cur2.execute("Show Databases like '%s'"%des)
if secDbExists != 1:
	tkMessageBox.showwarning("Nope","Cannot Find any database named '%s'" % sou)
	exit()



#******************************************************************************************************************************
root.deiconify()
#root.geometry("700x500+320+80")


menu = Menu(root)
root.config(menu = menu)          #ima gonna cinfigure a parameter

submenu = Menu(menu)                #menu item within a menu item
menu.add_cascade(label = "File", menu = submenu)
submenu.add_command(label = "About The Creator", command = donothingg)
submenu.add_command(label = "Exit", command = donothing)




if firstDbExists == 1 & secDbExists == 1:

	path = "cool.png"

	imga = ImageTk.PhotoImage(Image.open(path))

	panel = Label(root, image = imga)

	panel.pack(side = "top", fill = "both")

	# thelabel = Label(root, text = "< DATABASES '%s' & '%s' ARE CONNECTED >"%(sou,des),font=("Segoe UI Semibold", 16))
	# thelabel.pack() 




cur1.close()
cur2.close()
checking.close()


#@!#%$@#%@$^@$#&%#&*$^#&#$%^#$#%$#^#
topFrame = Frame(root)  #imma gonna make an invisible window which is going to take root
topFrame.pack()         #to display anything, we need to pack it in
bottomFrame = Frame(root)
bottomFrame.pack(side = BOTTOM)      # parameter tells us were to put

b1 = Button(topFrame,text = "Press This Button to view all tables inside '%s' Database"%sou, command = tablesinsource)
b2 = Button(topFrame,text = "Press This Button to view all tables inside '%s' Database"%des, command = tablesindest)
b3 = Button(bottomFrame,text = "Press This Button to select a table from the Source Database to be copied into the Destination Database", command = theHardestPart)

b1.pack(side = LEFT)
b1.config(font=('helvetica', 10), bd=8, relief=RAISED)
b2.pack(side = LEFT)
b2.config(font=('helvetica', 10), bd=8, relief=RAISED)




path = "data.png"
#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
img = ImageTk.PhotoImage(Image.open(path))
#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
panel = Label(root, image = img)
#The Pack geometry manager packs widgets in rows or columns.
panel.pack(side = "bottom", fill = "both", expand = "yes")






b3.pack(side=LEFT)
b3.config(font=('helvetica', 10), bd=8, relief=RAISED)




root = mainloop()

db.close()


