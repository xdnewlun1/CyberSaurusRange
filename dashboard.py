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
    dashboard_window.geometry("800x800")
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
        instance_label.pack(anchor='w')

   # Buttons frame at the bottom
    buttons_frame = ctk.CTkFrame(master=dashboard_window)
    buttons_frame.pack(side='bottom', fill='x', padx=20, pady=10)

    # Define buttons
    snapshot_btn = ctk.CTkButton(buttons_frame, text="Snapshot", command=lambda: print("Snapshot clicked"))
    deploy_lab_btn = ctk.CTkButton(buttons_frame, text="Deploy Lab", command=lambda: print("Deploy Lab clicked"))
    new_vm_btn = ctk.CTkButton(buttons_frame, text="New VM", command=lambda: print("New VM clicked"))
    destroy_btn = ctk.CTkButton(buttons_frame, text="Destroy", command=lambda: print("Destroy clicked"))

    # Place buttons in the buttons_frame
    snapshot_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)
    deploy_lab_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)
    new_vm_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)
    destroy_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)


    dashboard_window.mainloop()
