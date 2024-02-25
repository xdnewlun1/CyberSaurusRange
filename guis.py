import customtkinter as ctk
from tkinter import filedialog
import json
import tkinter.messagebox as tkmb
import dashboard
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x400")
app.title("CyberSaurus Range")

credential_path = ""
ssh_key = ""




def select_json_file():
    global credential_path
    credential_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])

def select_ssh_key_file():
    global ssh_key
    ssh_key = filedialog.askopenfilename(filetypes=[("Public SSH Key files", "*")])

def login():
    if not credential_path or not ssh_key:
        tkmb.showwarning(title='File selection', message='Please select both JSON file and SSH key file.')
        return

    
    tkmb.showinfo(title="Login Successful", message="You have logged in Successfully")
    app.withdraw()



    dashboard.setGoogle(credential_path)
    dashboard.setSSH(ssh_key)
    dashboard.launch_dashboard()

def getpaths():
	label = ctk.CTkLabel(app, text="CyberSaurus Range")
	label.pack(pady=20)


	frame = ctk.CTkFrame(master=app)
	frame.pack(pady=20, padx=40, fill='both', expand=True)


	label = ctk.CTkLabel(master=frame, text='File Selection')
	label.pack(pady=12, padx=10)

	# Create buttons to select JSON file and SSH key
	json_button = ctk.CTkButton(master=frame, text="Select JSON File", command=select_json_file)
	json_button.pack(pady=5, padx=10)

	ssh_button = ctk.CTkButton(master=frame, text="Select SSH Key", command=select_ssh_key_file)
	ssh_button.pack(pady=5, padx=10)


	login_button = ctk.CTkButton(master=frame, text='Continue', command=login)
	login_button.pack(pady=12, padx=10)

	app.mainloop()


getpaths()
