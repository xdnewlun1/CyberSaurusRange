# dashboard.py
import os
import io
import customtkinter as ctk
from tkinter import *
from google.cloud import compute_v1
credential_path = "/home/toor/googlecreds"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

def list_instances(project_id,zone):
    instances_list = []
    compute_client = compute_v1.InstancesClient()
    # Make the request to list instances
    for instance in compute_client.list(project=project_id,zone=zone):
        instances_list.append(instance.name)
    return instances_list

def launch_dashboard():
    project_id = "glossy-window-415318"
    zone = "us-west4-b"

    dashboard_window = ctk.CTkToplevel()
    dashboard_window.geometry("400x400")
    dashboard_window.title("CyberSaurus Dashboard")
    
   # Create a frame 
    frame = ctk.CTkFrame(master=dashboard_window) 
    frame.pack(pady=20,padx=40, 
	fill='both',expand=True) 

    # Set the label inside the frame 
    label = ctk.CTkLabel(master=frame, 
	text='VMs') 
    label.pack(pady=12,padx=10) 

    instances = list_instances(project_id,zone)
    for instance_name in instances:
        instance_label = ctk.CTkLabel(master=frame, text=instance_name)
        instance_label.pack()

    dashboard_window.mainloop()
