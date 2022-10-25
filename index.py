from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from datetime import *
from pymysql import *
import csv

#---------------------------------user defined exception classes------------------------

class DataException(Exception):
	def __init__(self,msg):
		self.msg=msg

#------------------------------------functions-------------------------------------------
def f0():						#count of the persons
	con=None
	try:
		con=connect(host='localhost',user='root',password='hanisha',database='mysql_project')
		cursor=con.cursor()
		sql='select * from bmi_persons'
		cursor.execute(sql)
		data=cursor.fetchall()
		count=cursor.rowcount
		return 'Count = '+str(count)		

	except Exception as e:
		showerror('Failure',e)
		con.rollback()
	finally:

		if con is not None:
			con.close()

def f1():						#to calculate the current time greeting phrase
	time=datetime.now()
	hour=time.hour
	greeting=''
	if 4<=hour<=11:
		greeting='Good Morning'
	elif 12<=hour<=16:
		greeting='Good Afternoon'
	else:
		greeting='Good Evening'
	time=str(time)
	return time+'\n'+greeting

def f2():						#main window to calculate window 
	calc_window.deiconify()
	main_window.withdraw() 

def f3():						#main window to view window and view data
	main_window.withdraw()
	view_window.deiconify()
	view_st_data.delete(1.0,END)
	info=''
	con=None
	try:
		con=connect(host='localhost',user='root',password='hanisha',database='mysql_project')
		cursor=con.cursor()
		sql='select * from bmi_persons'
		cursor.execute(sql)
		data=cursor.fetchall()
		for d in data:
			info=info+"Name = "+str(d[1])+"\nAge = "+str(d[2])+"\nPhone = "+str(d[3])+"\nGender = "+str(d[4])+"\nBMI = "+str(d[5])+'\n-----------------------------------------------------------\n'
		view_st_data.insert(INSERT,info)

	except DataException as e:
		showerror('Improper',e.msg)
		con.rollback()

	except Exception as e:
		showerror('Failure',e)
		con.rollback()

	finally:
		if con is not None:
			con.close()			

def f4():						#main window to export data
	con=None
	try:
		con=connect(host='localhost',user='root',password='hanisha',database='mysql_project')
		cursor=con.cursor()
		sql='select * from bmi_persons'
		cursor.execute(sql)
		data=cursor.fetchall()

		if data:
			result=[]
			column_names=[]
			for i in cursor.description:
				column_names.append(i[0])
			result.append(column_names)
			for row in data:
				result.append(row)
			time=datetime.now()
			year=time.year
			month=time.month
			day=time.day
			hour=time.hour
			minute=time.minute
			second=time.second
			file_name='patient_'+str(year)+'_'+str(month)+'_'+str(day)+'_'+str(hour)+'_'+str(minute)+'_'+str(second)+".csv"
			csv_path='F:\\PROJECTS\\bmi_data\\'+file_name
			with open(csv_path,'w',newline='') as csvfile:   #here newline parameter is empty to prevent extra lines between rows
				csvwriter=csv.writer(csvfile,delimiter=',')
				for row in result:
					csvwriter.writerow(row)
		else:
			raise DataException("No rows found")

	except DataException as e:
		showerror('Improper',e.msg)
		con.rollback()

	except Exception as e:
		showerror('Failure',e)
		con.rollback()

	finally:
		if con is not None:
			con.close()	

def f5():						#calculate window to main window back btn
	calc_window.withdraw()
	main_window.deiconify()
	value=f0()
	main_lb_count.config(text=value)

def f6():						#calculate window calculate btn
	con=None
	try:
		name=calc_ent_name.get()
		age=calc_ent_age.get()
		phone=calc_ent_phone.get()
		gender=g.get()
		height=calc_ent_hmtr.get()
		weight=calc_ent_wkg.get()
		if name=='':
			raise DataException('Name entered is blank')
		elif name.isdigit():
			raise DataException('Name should be string')
		elif len(name)<2:
			raise DataException('Name should be more than 2 letters')
		elif age=='':
			raise DataException('Age entered is blank')
		elif age.isalpha():
			raise DataException('Age should be a number')
		elif age.isdigit()==False:
			raise DataException('Invalid age entered')
		elif 18>int(age)  or int(age)>99:
			raise DataException('Age should be between 18 and 99')
		elif phone=='':
			raise DataException('Phone no. entered blank')
		elif phone.isalpha():
			raise DataException('Phone no. should be a number')
		elif len(phone)!=10:
			raise DataException('Phone no. should be of 10 digits')
		elif height=='':
			raise DataException("Height should not be empty")
		elif height.isalpha()==True:	
			raise DataException("Height should be a integer")
		elif 0.5>=float(height) or float(height)>=2.7:
			raise DataException("Feet should be between 0.5 and 2.7 m")
		elif weight=='':
			raise DataException("weight should not be empty")
		elif weight.isalpha()==True:	
			raise DataException("Weight should be a integer")
		elif weight.isdigit()==False:
			raise DataException("Weight should be positive and not in float")
		elif 10>int(weight) or int(weight)>=180:
			raise DataException("Weight should be between 10 and 180")

		age=int(age)
		phone=int(phone)	
		height=float(height)
		weight=int(weight)

		bmi=round(weight/(height**2),2)
		bmi_result=''
		if 16<=bmi<=18.4:
			bmi_result='Underweight'
		elif 18.5<=bmi<=24.9:
			bmi_result='Normal'
		elif 25<=bmi<=30:
			bmi_result='Overweight'
		elif 30.1<=bmi<55:
			bmi_result='Obese'
		else:
			raise DataException('BMI out of range')

		msg='Name = '+name+'\nAge = '+str(age)+'\nPhone = '+str(phone)+'\nGender = '+gender+'\nBMI = '+str(bmi)+'\n'+bmi_result
		showinfo('BMI',msg)
		#-----------------------data entry in database---------------
				

		calc_ent_name.delete(0,'end')
		calc_ent_age.delete(0,'end')
		calc_ent_phone.delete(0,'end')
		calc_ent_hmtr.delete(0,'end')
		calc_ent_wkg.delete(0,'end')

		con=connect(host='localhost',user='root',password='hanisha',database='mysql_project')
		cur=con.cursor()
		sql="Insert into bmi_persons (id,name,age,phone,gender,bmi) values (default,'%s','%s','%s','%s','%s')"
		cur.execute(sql % (name,age,phone,gender,bmi))
		con.commit()
		
	except DataException as e:
		showerror('Improper',e.msg)
		con.rollback()

	except Exception as e:
		showerror('Failure',e)
		con.rollback()
	finally:
		if con is not None:
			con.close()			

def f7():						#calculate window to convert window
	calc_window.withdraw()
	convert_window.deiconify()

def f8():						#convert window convert btn
	try:
		feet=convert_ent_feet.get()
		inch=convert_ent_inch.get()
		if feet=='':
			raise DataException("Feet should not be empty")
		elif feet.isalpha()==True:	
			raise DataException("Feet should be a integer")
		elif feet.isdigit()==False:
			raise DataException("Feet should be positive and not in float")
		elif 0>=int(feet) or int(feet)>=13:
			raise DataException("Feet should be between 1 and 12")
		elif inch=='':
			raise DataException("Inches should not be empty")
		elif inch.isalpha()==True:	
			raise DataException("Inches should be a integer")
		elif inch.isdigit()==False:
			raise DataException("Inch should be positive and not in float")
		elif 0>int(inch) or int(inch)>=13:
			raise DataException("Inches should be between 0 and 12")
		feet=int(feet)
		inch=int(inch)
		height_in_inches=feet*12+inch
		height_in_cm=height_in_inches*2.54
		height_in_m=height_in_cm/100
		showinfo('Meters',str(height_in_m)+'  m')
		convert_ent_feet.delete(0,'end')
		convert_ent_inch.delete(0,'end')
		convert_window.withdraw()
		calc_window.deiconify()

	except DataException as e:
		showerror('Improper',e.msg)

	except Exception as e:
		showerror('Failure',e)	

def f9():						#view window to main window back btn
	view_window.withdraw()
	main_window.deiconify()
#----------------------------------splash--------------------------------------------
splash=Tk()
splash.title('Welcome')
splash.after(1000,splash.destroy)
splash.wm_attributes('-fullscreen','true')
splash.config(bg='green')
msg=Label(splash,text='BMI Calculator',font=('Calibri',100,'bold'),fg='white',bg='green')
msg.place(x=360,y=300)
splash.mainloop()

#-------------------------------main window----------------------------------------
main_window=Tk()
main_window.title("BMI Calculator")
main_window.geometry('600x600+400+100')
main_window.config(bg='#c64756')

timevar=f1()							#it is a time variable to store the value generated by fn f1
font1=('Book Antiqua',18,'bold')

count=f0()							#holding count

main_lb_time=Label(main_window,text=timevar,font=font1,bg='#e4fbff')
main_btn_calc=Button(main_window,text='Calculate BMI',font=font1,width=20,command=f2,bg='#e4fbff')
main_btn_view=Button(main_window,text='View History',font=font1,width=20,command=f3,bg='#e4fbff')
main_btn_export=Button(main_window,text='Export Data',font=font1,width=20,command=f4,bg='#e4fbff')
main_lb_count=Label(main_window,text=count,font=font1,bg='#e4fbff')

main_lb_time.pack(pady=22)
main_btn_calc.pack(pady=22)
main_btn_view.pack(pady=22)
main_btn_export.pack(pady=22)
main_lb_count.pack(pady=22)

#-------------------------------calculation window----------------------------------
calc_window=Toplevel(main_window)
calc_window.title('Calculate')
calc_window.geometry('600x600+400+100')
calc_window.config(bg='#c64756')

calc_lb_name=Label(calc_window,text='Enter Name:',font=font1,bg='#e4fbff')
calc_ent_name=Entry(calc_window,font=font1,bd=5)
calc_lb_age=Label(calc_window,text='Enter Age:',font=font1,bg='#e4fbff')
calc_ent_age=Entry(calc_window,font=font1,bd=5)
calc_lb_phone=Label(calc_window,text='Enter Phone:',font=font1,bg='#e4fbff')
calc_ent_phone=Entry(calc_window,font=font1,bd=5)
calc_lb_gender=Label(calc_window,text='Gender:',font=font1,bg='#e4fbff')
#creating radiobutton
g=StringVar(calc_window,'m')
values={"Male":'m',"Female":'f'}
calc_rb_male=Radiobutton(calc_window,text='Male',value='m',variable=g,font=font1,bg='#e4fbff')
calc_rb_female=Radiobutton(calc_window,text='Female',value='f',variable=g,font=font1,bg='#e4fbff')
calc_lb_hmtr=Label(calc_window,text='Enter height in mtr:',font=font1,bg='#e4fbff')
calc_ent_hmtr=Entry(calc_window,font=font1,bd=5)
calc_btn_convert=Button(calc_window,text='Convert',font=font1,command=f7,bg='#e4fbff')
calc_lb_wkg=Label(calc_window,text='Enter weight in kg:',font=font1,bg='#e4fbff')
calc_ent_wkg=Entry(calc_window,font=font1,bd=5)
calc_btn_calc=Button(calc_window,text='Calculate',font=font1,bg='#e4fbff',command=f6)
calc_btn_back=Button(calc_window,text='Back',font=font1,command=f5,bg='#e4fbff')

calc_lb_name.grid(row=0,column=0,pady=15)
calc_ent_name.grid(row=0,column=1,pady=15)
calc_lb_age.grid(row=1,column=0,pady=15)
calc_ent_age.grid(row=1,column=1,pady=15)
calc_lb_phone.grid(row=2,column=0,pady=15)
calc_ent_phone.grid(row=2,column=1,pady=15)
calc_lb_gender.grid(row=3,column=0,pady=15)
calc_rb_male.grid(row=3,column=1,pady=15)
calc_rb_female.grid(row=3,column=2,padx=10,pady=15)
calc_lb_hmtr.grid(row=4,column=0,pady=15)
calc_ent_hmtr.grid(row=4,column=1,pady=15)
calc_btn_convert.grid(row=4,column=2,pady=15)
calc_lb_wkg.grid(row=5,column=0,pady=15)
calc_ent_wkg.grid(row=5,column=1,pady=15)
calc_btn_calc.grid(row=6,column=0,padx=20)
calc_btn_back.grid(row=6,column=1,padx=20)
calc_window.withdraw()

#-------------------------------convert window----------------------------------
convert_window=Toplevel(calc_window)
convert_window.title('Convert')
convert_window.geometry('600x600+400+100')
convert_window.config(bg='#c64756')

convert_lb_height=Label(convert_window,text="Enter your height",font=font1,bg='#e4fbff')
convert_lb_feet=Label(convert_window,text='Feet',font=font1,bg='#e4fbff')
convert_ent_feet=Entry(convert_window,font=font1,bd=5)
convert_lb_inch=Label(convert_window,text="Inch",font=font1,bg='#e4fbff')
convert_ent_inch=Entry(convert_window,font=font1,bd=5)
convert_btn_con=Button(convert_window,text='Convert',font=font1,bg='#e4fbff',command=f8)

convert_lb_height.pack(pady=20)
convert_lb_feet.pack(pady=20)
convert_ent_feet.pack(pady=20)
convert_lb_inch.pack(pady=20)
convert_ent_inch.pack(pady=20)
convert_btn_con.pack(pady=20)

convert_window.withdraw()

#-------------------------------view window----------------------------------
view_window=Toplevel(main_window)
view_window.title('View')
view_window.geometry('600x600+400+100')
view_window.config(bg='#c64756')

view_st_data=ScrolledText(view_window,width=45,height=17,font=font1)
view_btn_back=Button(view_window,text='Back',font=font1,command=f9,bg='#e4fbff')

view_st_data.pack(pady=10)
view_btn_back.pack(pady=10)

view_window.withdraw()

main_window.mainloop()	