# dashboard.py
import os
import io
import customtkinter as ctk
from tkinter import *
from tkinter import ttk
from google.cloud import compute_v1
from connect_vm import connect
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

def setGoogle(credential_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
    
def setSSH(ssh_key):
    global key_path
    key_path = ssh_key
    return key_path
def list_instances(project_id,zone):
    instances_list = []
    compute_client = compute_v1.InstancesClient()
    # Make the request to list instances
    for instance in compute_client.list(project=project_id,zone=zone):
        instances_list.append([instance.name,instance.status,instance.network_interfaces[0].access_configs[0].nat_i_p])
    return instances_list
def on_connect_button_click(ip_address, key_path):
    connect(ip_address, key_path)
def printFocus(tree,key_path):
    curItem = tree.item(tree.focus())
    connect(curItem["values"][2],key_path)
def launch_dashboard():
    project_id = "glossy-window-415318"
    zone = "us-west4-b"

    dashboard_window = ctk.CTkToplevel()
    dashboard_window.geometry("700x400")
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


    # Table-like structure using Treeview
    tree = ttk.Treeview(master=frame, columns=("VM", "Status","IP","Action"), show="headings")
    tree.heading("VM", text="VM")
    tree.heading("Status", text="Status")
    tree.heading("IP", text="IP")
    tree.heading("Action", text="Action")

    for instance in instances:
        tree.insert("", "end", values=instance)

    tree.pack(fill='both', expand=True)


   # Buttons frame at the bottom
    buttons_frame = ctk.CTkFrame(master=dashboard_window)
    buttons_frame.pack(side='bottom', fill='x', padx=20, pady=10)

    # Define buttons
    snapshot_btn = ctk.CTkButton(buttons_frame, text="Snapshot", command=lambda: printFocus(tree,key_path))
    deploy_lab_btn = ctk.CTkButton(buttons_frame, text="Deploy Lab", command=lambda: print("Deploy Lab clicked"))
    new_vm_btn = ctk.CTkButton(buttons_frame, text="New VM", command=lambda: print("New VM clicked"))
    destroy_btn = ctk.CTkButton(buttons_frame, text="Destroy", command=lambda: print("Destroy clicked"))

    # Place buttons in the buttons_frame
    snapshot_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)
    deploy_lab_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)
    new_vm_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)
    destroy_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)


    dashboard_window.mainloop()
