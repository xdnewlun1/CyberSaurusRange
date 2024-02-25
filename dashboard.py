# dashboard.py
import os
import io
import re
import customtkinter as ctk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tkmb
from google.cloud import compute_v1
from connect_vm import connect
credential_path = "C:\\Users\\xandy\\OneDrive\\Documents\\Rowdy24\\CyberSaurusRange\\glossy-window-415318-c67566dcade4.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

project_id = "glossy-window-415318"
zone = "us-west4-b"

master_instance_list = []
instance_fingerprint = ""
compute_client = compute_v1

def list_instances():
    instances_list = []
    # Make the request to list instances
    for instance in compute_client.InstancesClient().list(project=project_id,zone=zone):
        global instance_fingerprint
        instance_fingerprint = instance.label_fingerprint
        instances_list.append([instance.name,instance.status,instance.network_interfaces[0].access_configs[0].nat_i_p,instance.labels["groups"].split("-")],)
        print(instance.labels["groups"])
    return instances_list

def deploy_instance_list(tree, search="", reload=True):
    tree.delete(*tree.get_children())
    global master_instance_list
    if reload:
        instances = list_instances()
        master_instance_list = instances
    for instance in master_instance_list:
        if search in instance[0]:
            tree.insert("", "end", values=instance)

    tree.pack(fill='both', expand=True)

def on_connect_button_click(ip_address, ssh_key_path):
    connect(ip_address, ssh_key_path)

def printFocus(tree):
    curItem = tree.item(tree.focus())
    connect(curItem["values"][2],"C:\\Users\\xandy\\.ssh\\id_rsa")

def search_instances(event, tree):
    deploy_instance_list(tree,event.widget.get(), False)

def add_group(tree, group_name="new_group"):
    user_input = ""

    is_running = True
    while is_running:
        input_name = ctk.CTkInputDialog(text="Enter New Group Name:", title="New Group")
        user_input = input_name.get_input()
        is_running = False
        if bool(re.match(r'^[a-z0-9_-]+', user_input)) == False:
            tkmb.showwarning(title="Error", message="Group names can only include lowercase characters, numbers, and - or _!")
            is_running = True
    selected = tree.selection()
    for target in selected:
        working_item=tree.item(target)
        item_values = working_item['values']
        groups = str(item_values[3]).split(" ")
        new_groups = '-'.join(groups)
        new_groups = new_groups + "-" + user_input


        test = compute_client.GetInstanceRequest(
                instance=item_values[0],
                project=project_id,
                zone=zone
            )

        test_res = compute_client.InstancesClient().get(request=test)


        instance_fingerprint = test_res.label_fingerprint
        request_body = {
            'labels': {
                'groups': new_groups,
            },
            'label_fingerprint': instance_fingerprint
        }
        response = compute_client.InstancesClient().set_labels(project=project_id, zone=zone, instance=item_values[0], instances_set_labels_request_resource=compute_client.InstancesSetLabelsRequest(request_body))
        deploy_instance_list(tree, "", True)



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
    tree = ttk.Treeview(master=frame, columns=("VM", "Status","IP", "Groups"), show="headings")
    tree.heading("VM", text="VM")
    tree.heading("Status", text="Status")
    tree.heading("IP", text="IP")
    tree.heading("Groups",text="Groups")

    deploy_instance_list(tree)

     # Create Search box
    search = ctk.CTkEntry(master=frame,placeholder_text="Search")
    search.pack(pady=12,anchor='e',padx=10)
    search.bind("<Key>", command=lambda event, tree=tree: search_instances(event, tree))


   # Buttons frame at the bottom
    buttons_frame = ctk.CTkFrame(master=dashboard_window)
    buttons_frame.pack(side='bottom', fill='x', padx=20, pady=10)

    #Instance Buttons
    test_button = ctk.CTkButton(master=frame, text="Open Instance", command=lambda: print("Clicked!"))
    test_button.pack(side='left', expand=True, fill='both', padx=5, pady=5)

    # Define buttons
    snapshot_btn = ctk.CTkButton(buttons_frame, text="Connect", command=lambda: printFocus(tree))
    deploy_lab_btn = ctk.CTkButton(buttons_frame, text="Reload VMs", command=lambda: deploy_instance_list(tree, "", True))
    new_vm_btn = ctk.CTkButton(buttons_frame, text="Add Group", command=lambda: add_group(tree))
    destroy_btn = ctk.CTkButton(buttons_frame, text="Destroy", command=lambda: print("Destroy clicked"))

    # Place buttons in the buttons_frame
    snapshot_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)
    deploy_lab_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)
    new_vm_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)
    destroy_btn.pack(anchor='w', fill='both', padx=5, pady=5)


    dashboard_window.mainloop()
