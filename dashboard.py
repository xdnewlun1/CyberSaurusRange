# dashboard.py
import os
import io
import re
import sys
import warnings
from typing import Any
import customtkinter as ctk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tkmb
from google.cloud import compute_v1
from connect_vm import connect
from google.api_core.extended_operation import ExtendedOperation

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

project_id = "glossy-window-415318"
zone = "us-west4-b"

master_instance_list = []
instance_fingerprint = ""
compute_client = compute_v1

def setGoogle(credential_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
    
def setSSH(ssh_key):
    global key_path
    key_path = ssh_key
    return key_path
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
        if bool(re.match(r'^[a-z0-9_]+', user_input)) == False:
            tkmb.showwarning(title="Error", message="Group names can only include lowercase characters, numbers, and _!")
            is_running = True
    selected = tree.selection()
    sel_ind = []
    tree_chil = tree.get_children()
    for sel in selected:
        sel_ind.append(tree_chil.index(sel))
    for ind in sel_ind:
        target = tree.get_children()[ind]
        working_item=tree.item(target)
        item_values = working_item['values']
        groups = str(item_values[3]).split(" ")
        new_groups = '-'.join(groups)
        new_groups = new_groups + "-" + user_input
        if "{}" in new_groups:
            new_groups = user_input


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




def getDetails(project_id, zone, instance_id):
    compute_client = compute_v1.InstancesClient()
    instance = compute_client.get(project=project_id, zone=zone, instance=instance_id)
    details = {
        "Name": instance.name,
        "ID": instance.id,
        "Machine Type": instance.machine_type,
        "Description": instance.description,
        "Status": instance.status,
        "Internal IP": instance.network_interfaces[0].network_i_p,
        "External IP": instance.network_interfaces[0].access_configs[0].nat_i_p,
        "Disks": instance.disks[0].source,
        "CPU": instance.cpu_platform,
        "Zone": instance.zone
    }

    return details
  
def printDetails(tree):
    curItem = tree.item(tree.focus())
    instance_id = curItem["values"][0]
    project_id = "glossy-window-415318"
    zone = "us-west4-b"  

    detailed_info = getDetails(project_id, zone, instance_id)

    popup_window = ctk.CTkToplevel()
    popup_window.title(f"Details for Instance: {instance_id}")
    popup_window.geometry("400x300")

    for key, value in detailed_info.items():
        label = ctk.CTkLabel(popup_window, text=f"{key}: {value}")
        label.pack(pady=5, padx=10)

def startVMS(tree):
    selected = tree.selection()
    sel_ind = []
    tree_chil = tree.get_children()
    for sel in selected:
        sel_ind.append(tree_chil.index(sel))
    for ind in sel_ind:
        target = tree.get_children()[ind]
        working_item=tree.item(target)
        item_values = working_item['values']

        request = compute_client.StartInstanceRequest(
            instance=item_values[0],
            project=project_id,
            zone=zone
        )

        response = compute_client.InstancesClient().start(request=request)
        deploy_instance_list(tree, "", True)

def stopVMS(tree):
    selected = tree.selection()
    sel_ind = []
    tree_chil = tree.get_children()
    for sel in selected:
        sel_ind.append(tree_chil.index(sel))
    for ind in sel_ind:
        target = tree.get_children()[ind]
        working_item=tree.item(target)
        item_values = working_item['values']

        request = compute_client.StopInstanceRequest(
            instance=item_values[0],
            project=project_id,
            zone=zone
        )

        response = compute_client.InstancesClient().stop(request=request)
        deploy_instance_list(tree, "", True)

def deleteVMS(tree):
    selected = tree.selection()
    sel_ind = []
    tree_chil = tree.get_children()
    for sel in selected:
        sel_ind.append(tree_chil.index(sel))
    for ind in sel_ind:
        target = tree.get_children()[ind]
        working_item=tree.item(target)
        item_values = working_item['values']
        input_name = ctk.CTkInputDialog(text=f"Confirm Deletion: Type the name of the VM: {item_values[0]}", title="Confirm Delete")
        user_input = input_name.get_input()

        if user_input == item_values[0]:
            tkmb.showwarning(title="Deletion Notice", message=f"You are deleting {item_values[0]}")

            request = compute_client.DeleteInstanceRequest(
                instance=item_values[0],
                project=project_id,
                zone=zone
            )

            response = compute_client.InstancesClient().delete(request=request)
            deploy_instance_list(tree, "", True)
        else:
            tkmb.showwarning(title="Deletion Cancelled", message="Cancelled VM Delete")

def wait_for_extended_operation(
    operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 300
) -> Any:
    result = operation.result(timeout=timeout)

    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
            file=sys.stderr,
            flush=True,
        )
        print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        print(f"Warnings during {verbose_name}:\n", file=sys.stderr, flush=True)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr, flush=True)

    return result

def create_snapshot(
    project_id: str, disk_name: str, snapshot_name: str, *, zone: str | None = None, region: str | None = None, location: str | None = None, disk_project_id: str | None = None,
) -> compute_client.Snapshot:
    if zone is None and region is None:
        tkmb.showwarning(title="Snapshot Failed", message=f"No zone or region specified! See an Admin")
    if zone is not None and region is not None:
        tkmb.showwarning(title="Snapshot Failed", message=f"You cant set both zone and region")
    if disk_project_id is None:
        disk_project_id = project_id
    if zone is not None:
        disk_client = compute_client.DisksClient()
        disk = disk_client.get(project=disk_project_id, zone=zone, disk=disk_name)
    else:
        regio_disk_client = compute_client.RegionDisksClient()
        disk = regio_disk_client.get(
            project=disk_project_id, region=region, disk=disk_name
        )

    snapshot = compute_client.Snapshot()
    snapshot.source_disk = disk.self_link
    snapshot.name = snapshot_name
    if location:
        snapshot.storage_locations = [location]

    snapshot_client = compute_client.SnapshotsClient()
    operation = snapshot_client.insert(project=project_id, snapshot_resource=snapshot)
    tkmb.showwarning(title="Snapshot Notice", message="Snapshots can take a few minutes. Please be patient...")
    wait_for_extended_operation(operation, "snapshot creation")

    return snapshot_client.get(project=project_id, snapshot=snapshot_name)

def snapshot_creation_manager(tree):
    is_running = True
    while is_running:
        input_name = ctk.CTkInputDialog(text="Enter the Snapshot Name:", title="Snapshot Name")
        user_input = input_name.get_input()
        is_running = False
        if bool(re.match(r'^[a-z0-9-]+', user_input)) == False:
            is_running = True
            tkmb.showwarning(title="Snapshot Error", message="Snapshot Name must be all lowercase, numbers, or -")

    selected = tree.selection()
    sel_ind = []
    tree_chil = tree.get_children()
    for sel in selected:
        sel_ind.append(tree_chil.index(sel))
    for ind in sel_ind:
        target = tree.get_children()[ind]
        working_item=tree.item(target)
        item_values = working_item['values']
        create_snapshot(project_id=project_id, disk_name=item_values[0], snapshot_name=item_values[0]+"-snapshot", zone=zone)

def get_image_from_family(project: str, family: str) -> compute_v1.Image:
    image_client = compute_v1.ImagesClient()
    newest_image = image_client.get_from_family(project=project, family=family)
    return newest_image

def disk_from_image(disk_type: str, disk_size_gb: int, boot: bool, source_image: str, auto_delete: bool = True) -> compute_v1.AttachedDisk:
    boot_disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_image = source_image
    initialize_params.disk_size_gb = disk_size_gb
    initialize_params.disk_type = disk_type
    boot_disk.initialize_params = initialize_params
    boot_disk.auto_delete = auto_delete
    boot_disk.boot = boot
    return boot_disk

def create_instance(project_id: str, zone: str, instance_name: str, disks: list[compute_v1.AttachedDisk], machine_type: str = "e2-micro", network_link: str = "global/networks/default", subnetwork_link: str = None, internal_ip: str = None, external_access: bool = True, external_ipv4: str = None, accelerators: list[compute_v1.AcceleratorConfig] = None, preemptible: bool = False, spot: bool = False, instance_termination_Action: str = "STOP", custom_hostname: str = None, delete_protection: bool = False, ) -> compute_client.Instance:
    instance_client = compute_client.InstancesClient()
    network_interfaces = compute_v1.NetworkInterface()
    network_interfaces.network = network_link
    network_interfaces.subnetwork = f"projects/{project_id}/regions/us-west4/subnetworks/default"

    if internal_ip:
        network_interfaces.network_i_p = internal_ip

    if external_access:
        access = compute_v1.AccessConfig()
        access.type_ = compute_v1.AccessConfig.Type.ONE_TO_ONE_NAT.name
        access.name = "External NAT"
        access.network_tier = access.NetworkTier.PREMIUM.name
        if external_ipv4:
            access.nat_i_p = external_ipv4
        network_interfaces.access_configs = [access]

    instance = compute_v1.Instance()
    instance.network_interfaces = [network_interfaces]
    instance.name = instance_name
    instance.disks = disks
    if re.match(r"^zones/[a-z\d\-]+/machineTypes/[a-z\d\-]+$", machine_type):
        instance.machine_type = machine_type
    else:
        instance.machine_type = f"zones/{zone}/machineTypes/{machine_type}"

    instance.scheduling = compute_v1.Scheduling()
    if accelerators:
        instance.guest_accelerators = accelerators
        instance.scheduling.on_host_maintenance = (
            compute_v1.Scheduling.OnHostMaintenance.TERMINATE.name
        )

    if preemptible:
        warnings.warn(
            "Preemptible VMs are being replaced by Spot VMs.", DeprecationWarning
        )
        instance.scheduling = compute_v1.Scheduling()
        instance.scheduling.preemptible = True

    if spot:
        instance.scheduling.provisioning_model = (
            compute_v1.Scheduling.ProvisioningModel.SPOT.name
        )
        instance.scheduling.instance_terminiation_action = instance_terminiation_action

    if custom_hostname is not None:
        instance.hostname = custom_hostname

    if delete_protection:
        instance.deletion_protection = True

    request = compute_v1.InsertInstanceRequest()
    request.zone = zone
    request.project = project_id
    request.instance_resource = instance
    tkmb.showwarning(title="Instance Created", message="Creating Instance; This will take a few moments! Please be patient")

    operation = instance_client.insert(request=request)
    wait_for_extended_operation(operation, "instance creation")

    tkmb.showwarning(title="Instance Created", message="Instance Created!")
    return instance_client.get(project=project_id, zone=zone, instance=instance_name)

def vm_creation_manager(tree):
    is_running = True
    while is_running:
        input_name = ctk.CTkInputDialog(text="Enter the new VM name:", title="Instance Name")
        user_input = input_name.get_input()
        is_running = False
        if bool(re.match(r'^[a-z0-9-/]+', user_input)) == False:
            is_running = True
            tkmb.showwarning(title="VM Error", message="VM Name must be all lowercase, numbers, or -")


    is_running = True
    while is_running:
        input_name = ctk.CTkInputDialog(text="Enter the VM Image Path, or type `default` for debian", title="VM Image Selection")
        user_input_img = input_name.get_input()
        input_size = ctk.CTkInputDialog(text="VM Image Size (GB): ", title="VM Disk Size")
        user_input_size = int(input_size.get_input())
        is_running = False
        if user_input_img == "default":
            user_input_img = "projects/debian-cloud/global/images/debian-12-bookworm-v20240213"
        if bool(re.match(r'^[a-z0-9-/]+', user_input_img)) == False:
            is_running = True
            tkmb.showwarning(title="VM Error", message="VM Name must be all lowercase, numbers, or -")

    create_instance(project_id=project_id, zone=zone, instance_name=user_input, disks=[disk_from_image(f"zones/{zone}/diskTypes/pd-standard", disk_size_gb=input_size, boot=True, source_image=user_input_img)])
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

    tree.bind("<Double-Button-1>", lambda event: printDetails(tree))

   # Buttons frame at the bottom
    buttons_frame = ctk.CTkFrame(master=dashboard_window)
    buttons_frame.pack(side='bottom', fill='x', padx=20, pady=10)

    #Instance Buttons
    test_button = ctk.CTkButton(master=frame, text="Connect to VM", command=lambda: printFocus(tree))
    test_button.pack(side='left', expand=True, fill='both', padx=5, pady=5)


    # Define top buttons
    start_btn = ctk.CTkButton(buttons_frame, text="Start VMs", command=lambda: startVMS(tree))
    stop_btn = ctk.CTkButton(buttons_frame, text="Stop VMs", command=lambda: stopVMS(tree))
    snapshot_btn = ctk.CTkButton(buttons_frame, text="Snapshot VMs", command=lambda: snapshot_creation_manager(tree))
    tbd_btn = ctk.CTkButton(buttons_frame, text="Create VM", command=lambda: vm_creation_manager(tree))

    # Place buttons in the buttons_frame
    #start_btn.pack(side='top', expand=True, fill='both', padx=5, pady=5)
    #stop_btn.pack(side='top', expand=True, fill='both', padx=5, pady=5)
    #snapshot_btn.pack(side='top', expand=True, fill='both', padx=5, pady=5)
    #tbd_btn.pack(sid='top',anchor='w', fill='both', padx=5, pady=5)

    #buttons with grid
    start_btn.grid(row=0, column=0, padx=5, pady=5)
    stop_btn.grid(row=0, column=1, padx=5, pady=5)
    snapshot_btn.grid(row=0, column=2, padx=5, pady=5)
    tbd_btn.grid(row=0, column=3, padx=5, pady=5)


    # Define buttons
    tbd2_btn = ctk.CTkButton(buttons_frame, text="Clone VM", command=lambda: printFocus(tree))
    deploy_lab_btn = ctk.CTkButton(buttons_frame, text="Reload VMs", command=lambda: deploy_instance_list(tree, "", True))
    new_vm_btn = ctk.CTkButton(buttons_frame, text="Add Group", command=lambda: add_group(tree))
    destroy_btn = ctk.CTkButton(buttons_frame, text="Destroy VMs", command=lambda: deleteVMS(tree))

    # Place buttons in the buttons_frame
    #tbd2_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)
    #deploy_lab_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)
    #new_vm_btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)
    #destroy_btn.pack(anchor='w', fill='both', padx=5, pady=5)

    tbd2_btn.grid(row=1, column=0, padx=5, pady=5)
    deploy_lab_btn.grid(row=1, column=1, padx=5, pady=5)
    new_vm_btn.grid(row=1, column=2, padx=5, pady=5)
    destroy_btn.grid(row=1, column=3, padx=5, pady=5)

    
    
    dashboard_window.mainloop()
