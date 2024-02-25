# management.py
import customtkinter as ctk
from tkinter import *
from tkinter import ttk
from google.cloud import compute_v1
import os

def start_vm(project_id, zone, instance_name):
    compute_client = compute_v1.InstancesClient()
    
    # Define the instance resource URL
    instance_url = f"projects/{project_id}/zones/{zone}/instances/{instance_name}"

    # Send the request to start the instance
    operation = compute_client.start(project=project_id, zone=zone, instance=instance_name).execute()

    print(f"Starting VM {instance_name}. Operation ID: {operation['name']}")

def launchManagement(project_id, zone, instance_name):
    dashboard_window = ctk.CTkToplevel()
    dashboard_window.geometry("700x400")
    dashboard_window.title("Management Panel")

    # Create a frame
    frame = ctk.CTkFrame(master=dashboard_window)
    frame.pack(pady=20, padx=40, fill='both', expand=True)

    # Set the label inside the frame
    label = ctk.CTkLabel(master=frame, text='Buttons')
    label.pack(pady=12, padx=10)

    # Define buttons
    start_btn = ctk.CTkButton(buttons_frame, text="Start", command=lambda: startVm(project_id,zone,instance_name)
    stop_btn = ctk.CTkButton(buttons_frame, text="Stop", command=lambda: print("Deploy Lab clicked"))
    snapshot_btn = ctk.CTkButton(buttons_frame, text="Snapshot", command=lambda: print("New VM clicked"))
