# dashboard.py
import os
import io
import customtkinter as ctk
from tkinter import *
from tkinter import ttk
from google.cloud import compute_v1
from connect_vm import connect
credential_path = "C:\\Users\\xandy\\OneDrive\\Documents\\Rowdy24\\CyberSaurusRange\\glossy-window-415318-c67566dcade4.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

project_id = "glossy-window-415318"
zone = "us-west4-b"

master_instance_list = []

def list_instances():
    instances_list = []
    compute_client = compute_v1.InstancesClient()
    # Make the request to list instances
    for instance in compute_client.list(project=project_id,zone=zone):
        instances_list.append([instance.name,instance.status,instance.network_interfaces[0].access_configs[0].nat_i_p])
    return instances_list

def deploy_instance_list(tree, search="", reload=True):
    tree.delete(*tree.get_children())
    global master_instance_list
    if reload:
        instances = list_instances()
        master_instance_list = instances
    for instance in master_instance_list:
        if search in instance[0]:
            connect_button = ctk.CTkButton(tree, text="Connect", command=lambda ip=instance[2]: on_connect_button_click(ip, "path/to/your/ssh/key.pem"))
            tree.insert("", "end", values=instance)

    tree.pack(fill='both', expand=True)

def on_connect_button_click(ip_address, ssh_key_path):
    connect(ip_address, ssh_key_path)

def printFocus(tree):
    curItem = tree.item(tree.focus())
    connect(curItem["values"][2],"C:\\Users\\xandy\\.ssh\\id_rsa")

def search_instances(event, tree):
    deploy_instance_list(tree,event.widget.get(), False)

def launch_dashboard():

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


    # Table-like structure using Treeview
    tree = ttk.Treeview(master=frame, columns=("VM", "Status","IP","Action"), show="headings")
    tree.heading("VM", text="VM")
    tree.heading("Status", text="Status")
    tree.heading("IP", text="IP")
    tree.heading("Action", text="Action")

    deploy_instance_list(tree)

     # Create Search box
    search = ctk.CTkEntry(master=frame,placeholder_text="Search")
    search.pack(pady=12,anchor='e',padx=10)
    search.bind("<Key>", command=lambda event, tree=tree: search_instances(event, tree))


   # Buttons frame at the bottom
    buttons_frame = ctk.CTkFrame(master=dashboard_window)
    buttons_frame.pack(side='bottom', fill='x', padx=20, pady=10)

    # Define buttons
    snapshot_btn = ctk.CTkButton(buttons_frame, text="Snapshot", command=lambda: printFocus(tree))
    deploy_lab_btn = ctk.CTkButton(buttons_frame, text="Deploy Lab", command=lambda: deploy_instance_list(project_id, zone, tree))
    new_vm_btn = ctk.CTkButton(buttons_frame, text="New VM", command=lambda: print("New VM clicked"))
    destroy_btn = ctk.CTkButton(buttons_frame, text="Destroy", command=lambda: print("Destroy clicked"))

    # Place buttons in the buttons_frame
    snapshot_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)
    deploy_lab_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)
    new_vm_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)
    destroy_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)


    dashboard_window.mainloop()
