# dashboard.py
import os
import io
import customtkinter as ctk
from tkinter import *
from tkinter import ttk
from google.cloud import compute_v1
from connect_vm import connect_vm
credential_path = "/home/toor/googlecreds"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

def list_instances(project_id,zone):
    instances_list = []
    compute_client = compute_v1.InstancesClient()
    # Make the request to list instances
    for instance in compute_client.list(project=project_id,zone=zone):
        instances_list.append((instance.name,instance.status,instance.network_interfaces[0].access_configs[0].nat_i_p))
    return instances_list
def on_connect_button_click(ip_address, ssh_key_path):
    connect(ip_address, ssh_key_path)
def printFocus(tree):
    curItem = tree.focus()
    print(curItem)
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
        connect_button = ctk.CTkButton(tree, text="Connect", command=lambda ip=instance[2]: on_connect_button_click(ip, "path/to/your/ssh/key.pem"))
        tree.insert("", "end", values=(*instances,connect_button))

    tree.pack(fill='both', expand=True)


   # Buttons frame at the bottom
    buttons_frame = ctk.CTkFrame(master=dashboard_window)
    buttons_frame.pack(side='bottom', fill='x', padx=20, pady=10)

    # Define buttons
    snapshot_btn = ctk.CTkButton(buttons_frame, text="Snapshot", command=lambda: printFocus(tree))
    deploy_lab_btn = ctk.CTkButton(buttons_frame, text="Deploy Lab", command=lambda: print("Deploy Lab clicked"))
    new_vm_btn = ctk.CTkButton(buttons_frame, text="New VM", command=lambda: print("New VM clicked"))
    destroy_btn = ctk.CTkButton(buttons_frame, text="Destroy", command=lambda: print("Destroy clicked"))

    # Place buttons in the buttons_frame
    snapshot_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)
    deploy_lab_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)
    new_vm_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)
    destroy_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)


    dashboard_window.mainloop()
