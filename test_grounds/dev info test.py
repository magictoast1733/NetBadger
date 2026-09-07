import tkinter as tk
from tkinter import messagebox
import nmap



# Dictionary to store nmap data using the Canvas circle ID as the key
# Example structure: { circle_id: {"ip": "...", "ports": "...", "mac": "...", "os": "..."} }
canvas_hosts_map = {}



def run_network_scan(target):
    """Scans the network and returns structured host details."""
    nm = nmap.PortScanner()
    print(f"Scanning target: {target}... (OS/MAC detection requires sudo/admin)")

    # -O for OS, -sV for service version, -sP or default for discovery
    nm.scan(hosts=target, arguments='-O -sV')

    scanned_devices = []

    for host in nm.all_hosts():
         device_info = {
             "ip": host,
             "ports": "None",
             "mac": "Unknown",
             "os": "Unknown"
         }

         # 1. Extract MAC Address
         if 'addresses' in nm[host] and 'mac' in nm[host]['addresses']:
            device_info["mac"] = nm[host]['addresses']['mac']

         # 2. Extract Open Ports
         ports_list = []
         for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in sorted(lport):
                 if nm[host][proto][port]['state'] == 'open':
                    ports_list.append(str(port))
            if ports_list:
                device_info["ports"] = ", ".join(ports_list)

         # 3. Extract OS Details
         if 'osmatch' in nm[host] and len(nm[host]['osmatch']) > 0:
            device_info["os"] = nm[host]['osmatch'][0]['name']

         scanned_devices.append(device_info)

         return scanned_devices



def on_circle_click(event):
    """Triggers when a user clicks a circle shape on the canvas."""
    # Find the unique canvas ID of the item closest to the mouse click
    canvas = event.widget
    clicked_item = canvas.find_closest(event.x, event.y)[0]

         # Retrieve the data linked to this canvas ID
    if clicked_item in canvas_hosts_map:
         dev = canvas_hosts_map[clicked_item]

         # Format the display text
         info_text = (
         f"IP Address: {dev['ip']}\n"
         f"MAC Address: {dev['mac']}\n"
         f"Open Ports: {dev['ports']}\n"
         f"Operating System: {dev['os']}"
         )

         messagebox.showinfo(f"Device Details [{dev['ip']}]", info_text)



def create_gui(devices):
    """Creates the main window and draws the clickable host map."""
    root = tk.Tk()
    root.title("Network Device Map")
    root.geometry("600x400")

    # Create canvas for drawing
    canvas = tk.Canvas(root, width=600, height=400, bg="#1e1e1e")
    canvas.pack(fill=tk.BOTH, expand=True)

    # Layout configuration for positioning circles horizontally
    start_x = 80
    y_pos = 180
    spacing = 120
    radius = 30

    for index, dev in enumerate(devices):
         # Calculate coordinate bounds for the circle bounding box
        x_pos = start_x + (index * spacing)
        x1, y1 = x_pos - radius, y_pos - radius
        x2, y2 = x_pos + radius, y_pos + radius

        # Draw the circle shape
        circle_id = canvas.create_oval(
        x1, y1, x2, y2,
            fill="#00adb5",
            outline="#eeeeee",
            width=2,
            tags="host_node"
        )

        # Draw IP label under the circle
        canvas.create_text(
            x_pos, y_pos + 45,
            text=dev['ip'],
            fill="#eeeeee",
            font=("Arial", 10, "bold")
        )

        # Critical Step: Link the unique circle ID to the host attributes
        canvas_hosts_map[circle_id] = dev
        # Bind a left-mouse click event specifically to objects with the "host_node" tag
        canvas.tag_bind("host_node", "<Button-1>", on_circle_click)

    root.mainloop()



if __name__ == "__main__":
    # Target string: Change to your subnet, e.g., '192.168.1.0/24'
    # MAC addresses will not show for localhost ('127.0.0.1') loops
    TARGET_SUBNET = '10.149.100.0/28'

    # Step 1: Gather and store the data
    discovered_devices = run_network_scan(TARGET_SUBNET)

    # Step 2: Render interactive canvas if devices are found
    if discovered_devices:
        create_gui(discovered_devices)
    else:
        print("No active hosts discovered.")