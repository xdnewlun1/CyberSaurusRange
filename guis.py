# Importing required module 
import customtkinter as ctk 
from tkinter import *
import tkinter.messagebox as tkmb
import dashboard
ctk.set_appearance_mode("light") 
  
# Selecting color theme-blue, green, dark-blue 
ctk.set_default_color_theme("blue") 
  
app = ctk.CTk() 
app.geometry("400x400") 
app.title("CyberSaurus Range") 


# defining the login function 
def login(): 
	# pre-defined username 
	username = "admin"
	# pre-defined password 
	password = "admin" 

	if user_entry.get() == username and user_pass.get() == password: 
		tkmb.showinfo(title="Login Successful", 
		message="You have logged in Successfully") 
		app.withdraw()
		dashboard.launch_dashboard()

	elif user_entry.get() == username and user_pass.get() != password: 
		tkmb.showwarning(title='Wrong password', 
			message='Please check your password') 
		

	elif user_entry.get() != username and user_pass.get() == password: 
		tkmb.showwarning(title='Wrong username', 
			message='Please check your username') 
		
	else: 
		tkmb.showerror(title="Login Failed", 
		message="Invalid Username and password")


# Set the label 
label = ctk.CTkLabel(app,text="CyberSaurus Range") 

label.pack(pady=20) 

# Create a frame 
frame = ctk.CTkFrame(master=app) 
frame.pack(pady=20,padx=40, 
		fill='both',expand=True) 

# Set the label inside the frame 
label = ctk.CTkLabel(master=frame, 
					text='Login') 
label.pack(pady=12,padx=10) 

# Create the text box for taking 
# username input from user 
user_entry= ctk.CTkEntry(master=frame, 
						placeholder_text="Username") 
user_entry.pack(pady=12,padx=10) 

# Create a text box for taking 
# password input from user 
user_pass= ctk.CTkEntry(master=frame, 
						placeholder_text="Password", 
						show="*") 
user_pass.pack(pady=12,padx=10) 

# Create a login button to login 
button = ctk.CTkButton(master=frame, 
					text='Login',command=login) 
button.pack(pady=12,padx=10) 


app.mainloop()
