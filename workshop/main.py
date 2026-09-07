#----------IMPORT LIBS AND FUCTIONS-----------------
import os
import queue
import sys
import tkinter as tk
import threading
from quopri import EMPTYSTRING
from tkinter import ttk, filedialog, messagebox
import json
import my_ping
import my_nmap
import my_tracert
#----------------VAR CREATION----------------------
know_host = []
host = None
status = None
file_name = "NONE"
dev_info = {}
worker=queue.Queue()
#ip_list = ["10.149.100.1","10.149.100.3","10.149.100.5","10.149.100.10"]
#----------------FUNCTION CREATION-----------------
def load_file():
    file_path = filedialog.askopenfilename(
        title="Open File",
        filetypes=[("json", "*.json"), ("All Files", "*.*")],
    )
    if file_path:
        global file_name, know_host, dev_info
        new_file()
        file_name = file_path
        with open(file_path, "r") as f:
            master_data = json.load(f)
        # restore know ips
        know_host = master_data.get("ip_list", [])
        dev_info = master_data.get("dev_info", {})
        print(f"loaded IP list: {know_host}")

        #restore map
        for shape in master_data.get("shapes",[]):
            if shape['shape_type'] == 'rectangle':
                canvas.create_rectangle(shape['coords'], fill=shape['fill_color'], tags=shape['tag'])
            elif shape['shape_type'] == 'oval':
                canvas.create_oval(shape['coords'], fill=shape['fill_color'], tags=shape['tag'])
            elif shape['shape_type'] == 'text':
                canvas.create_text(shape['coords'], text=shape['text'], fill=shape['fill_color'], tags=shape['tag'])
                canvas.tag_bind(shape['text'], "<Button-1>", lambda event, ip=shape['text']: on_device_click(ip))
        print(f"Successfully loaded data from {file_path}")

def save(file_path):
    shape_data = []
    for item_id in canvas.find_all():
        item_type = canvas.type(item_id)
        coords = canvas.coords(item_id)
        fill_color = canvas.itemcget(item_id, 'fill')
        tag = canvas.itemcget(item_id, 'tag')

        item_dict = {
            'shape_type': item_type,
            'coords': coords,
            'fill_color': fill_color,
            'tag': tag
        }

        if item_type == 'text':
            item_dict['text'] = canvas.itemcget(item_id, 'text')
            item_dict['font'] = canvas.itemcget(item_id, 'font')
        shape_data.append(item_dict)

    master_data = {
        "ip_list": know_host,
        "dev_info": dev_info,
        "shapes": shape_data
    }

    with open(file_path, "w") as f:
        json.dump(master_data, f, indent=4)
    print(f"Map Data Saved!{file_path}")

def save_file():
    if file_name == "NONE":
        save_as()
    else:
        save(file_name)
    print("you just saved!")

def save_as():
    file_path = filedialog.asksaveasfilename(
        title="Save File As",
        defaultextension=".json",
        filetypes=[("Json Files", "*.json"), ("All Files", "*.*")],
    )
    if file_path:
        global file_name
        file_name = file_path
        save(file_name)

def new_file():
    global know_host, dev_info ,file_name
    canvas.delete("all")
    know_host = []
    file_name = "NONE"
    dev_info = {}
    print("this restarted")

def placeholder(): print("Action activated")

def on_device_click(clicked_ip):
    if clicked_ip in dev_info:
        dev = dev_info
        port_list = dev[clicked_ip]["ports"]
        #for port in ports_list:
            #ports=()
        #info_text = (
            #f"IP Address: {clicked_ip}\n"
           # f"MAC Address: {dev['mac']}\n"
           # f"Open Ports: {ports_list}\n"
           # f"Operating System: {dev['os']}"
        #)
        port_str = "\n".join(port_list)
        messagebox.showinfo("Device Info", f"Device IP: {clicked_ip}\n Ports:\n {port_str}")
    else:
        messagebox.showerror("Error", "Device info not found, try running nmap under tools")

def add_device(host_ip, dev_type):
    #calc  bound box (eg 20x20 shaped centerd at x,y
    start_x = 0
    start_y = 0
    shape = canvas.create_line
    if dev_type == "end":
        shape = canvas.create_rectangle
        start_x = canvas.winfo_width() / 4 + 200
        start_y = canvas.winfo_height() / 4
    elif dev_type == "rtr":
        shape = canvas.create_oval
        start_x = canvas.winfo_width() / 2 - 100
    x = start_x
    y = start_y
    dist = 250
    size = 150
    while True:
        x1, y1 = x, y
        x2, y2 = x + size, y + size

        ## check the shape will not go off screen
        if x2 > canvas.winfo_width():
            x = start_x
            y += dist
            continue

        #check if overlap
        overlapping = canvas.find_overlapping(x1, y1, x2, y2)

        if not overlapping:
            break

        x += dist

    shape(x1, y1, x2, y2, fill='green', outline='white', tags=host_ip)
    canvas.tag_bind(host_ip, "<Button-1>", lambda event, ip=host_ip: on_device_click(ip))
    canvas.create_text(x+75, y+75, text=host_ip, fill='white')

def device_down(host_ip):
    canvas.itemconfig(host_ip, fill='red', outline='white')

def device_up(host_ip):
    canvas.itemconfig(host_ip, fill='green', outline='white')


# noinspection DuplicatedCode
def ping_prompt():
    def result():
        for ip in result_message[0]:
            print(ip)
            if ip not in know_host:
                add_device(ip, "end")
                know_host.append(ip)
            print(know_host)
            device_up(ip)
        for ip2 in result_message[1]:
            if ip2 in know_host:
                device_down(ip2)
            #else:
                #device_up(ip2)
        # clears old values from resuslts
        result_message.clear()
    ping_q = ["Do you want to do a range or target"]
    pop = Prompt(root, title="Ping Type", prompt=ping_q)
    ans = pop.results
    if ans:
        if ans[0] == "target":
            questions = [
                "enter first 3 octets",
                "enter start of ip range",
                "enter end of ip range:"
            ]
            # 2. instantiate class
            # freezes execurion here and wait until users clicks button
            popup = Prompt(root, title="Ping info", prompt=questions)

            # 3. grab list of results and don't just close window
            answer = popup.results

            # if the user filed it out and dinint just close windo
            if answer:

                # unpack the list directly into function argument
                # this mirrors: my_ping.ping(input("Enter first 3 octets of IP range: "), input("range start: "), input("range end: "))
                # result_message = my_ping.ping("10.149.100", "1", "15")
                result_message = my_ping.single_ping(answer[0], answer[1], answer[2])

                trt_mess = tracert(result_message[0])
                for ip in trt_mess:
                    print(ip)
                    if ip not in know_host:
                        add_device(ip, dev_type="rtr")
                        know_host.append(ip)
                    print(know_host)
                    device_up(ip)
                result()
                return result_message

        elif ans[0] == "range":
            questions = [
                "enter your ip cidr(ex.192.168.10.0): ",
                "enter your ip subnet(ex.24): "
            ]
            # 2. instantiate class
            # freezes execurion here and wait until users clicks button
            popup = Prompt(root, title="Ping info", prompt=questions)

            # 3. grab list of results and don't just close window
            answer = popup.results

            # if the user filed it out and dinint just close windo
            if answer:

                # unpack the list directly into function argument
                # this mirrors: my_ping.ping(input("Enter first 3 octets of IP range: "), input("range start: "), input("range end: "))
                # result_message = my_ping.ping("10.149.100", "1", "15")
                result_message = my_ping.multi_ping(answer[0], answer[1])

                trt_mess = tracert(result_message[0])
                for ip in trt_mess:
                    print(ip)
                    if ip not in know_host:
                        add_device(ip, dev_type="rtr")
                        know_host.append(ip)
                    print(know_host)
                    device_up(ip)
                result()
                return result_message
        else:
            messagebox.showinfo(message="please enter range or target")
            ping_prompt()


      #  worker.put(know_host)
        #place holder for class that will function to create shapes
    #else:

def nmap_prompt():
    global dev_info
    ping_q = ["Do you want to ping first? y/n \n !!!Warning if no a nmap scan will scan!!! \n  !!!ALL hosts seen in this file!!! \n If you want to ping a specific ip choose yes and use pings target scan"]
    popup_1 = Prompt(root, title="Ping info", prompt=ping_q)
    nmap_opt = ['Please enter nmap options with spaces \n (Default is: -p 1-1024 --open -n -Pn -T4)']
    popup_2 = Prompt(root, title="NMAP Options", prompt=nmap_opt)
    # 3. grab list of results and don't just close window
    #ping_a = popup_1.results
    ping_a = popup_1.results
    option = popup_2.results

    if option == ['']:
      option='-p 1-1024 --open -n -Pn -T4'
    # if the user filed it out and dinint just close windo
    if ping_a:
        if ping_a[0] == "y":
            temp_host = ping_prompt()
           # wait=worker.get()
            info = my_nmap.my_nm(temp_host, option)
            for ip, ports in info.items():
                dev_info[ip] = ports
        elif ping_a[0] == "n":
            info = my_nmap.my_nm(know_host, option)
            for ip, ports in info.items():
                dev_info[ip] = ports
        else:
            messagebox.showinfo(message="please enter y/n")
            nmap_func()
    print(f"this is: {dev_info}")

def tracert(lit):
    lst=[]
    for i in lit:
        ls = my_tracert.route(i) ## feeds in to my custome trace route function
        print(f"{i}: {ls}")
        lst.append(ls)
        print(lst)
    # Find the shortest array
    sho = min(lst, key=len)

    # Print the last value
    print(f'this is shortest: {sho[-1]}')
    return sho

def connect_device(ip1, ip2):
    # Get the bounding box coordinates (x0, y0, x1, y1) for both rectangles
    shape1_coords = canvas.coords(ip1)
    shape2_coords = canvas.coords(ip2)

    # Calculate the center (x, y) of the right face of the first rectangle
    x1 = shape1_coords[2]  # right x-coordinate
    y1 = (shape1_coords[1] + shape1_coords[3]) / 2  # vertical midpoint

    # Calculate the center (x, y) of the left face of the second rectangle
    x2 = shape2_coords[0]  # left x-coordinate
    y2 = (shape2_coords[1] + shape2_coords[3]) / 2  # vertical midpoint

    # Draw a line between the two calculated face points
    canvas.create_line(x1, y1, x2, y2, fill="red", width=3)

#----------------CLASS CREATION-------------------
class Prompt(tk.Toplevel):
    def __init__(self, parent, title, prompt):
        """
        :param parent:  The root TKinter window
        :param title:  The Title of the window
        :param prompt: a list of strings representing the prompt
        """
        super().__init__(parent)
        self.title(title)
        self.geometry("400x250")
        self.resizable(False, False)

        # make window modal
        self.transient(parent)
        self.grab_set()

        self.prompt = prompt
        self.entries = []
        self.results = None  # this will store final answers

        # Dynamioc build a lable and input box for each question passed in
        for prompt in self.prompt:
            frame = tk.Frame(self)
            frame.pack(fill="x", padx=15, pady=8)

            label = ttk.Label(frame, text=prompt, font=("arial", 10))
            label.pack(anchor="w")

            entry = ttk.Entry(frame, width=40)
            entry.pack(fill="x", pady=2)
            self.entries.append(entry)
        # make sub button
        submit_btn = ttk.Button(self, text="Submit", command=self.on_submit)
        submit_btn.pack(pady=15)

        # focus on the first entry box auto
        if self.entries:
            self.entries[0].focus_set()

        # wait here until popup window is closed or destoryed
        self.wait_window()

    def on_submit(self):
        """Gather data from all fields and closes the window"""
        # read the text out every entry feld in to a list
        self.results = [entry.get().strip() for entry in self.entries]
        self.destroy()

#class Device:
#    def __init__(self, host, status):
#        #        self.name = name
#        #        self.type = device_type
#        self.host = host
#        self.status = status

    #        self.mac = mac_address

#    def add_device(self, host):
#        canvas.create_oval(375, 75, 425, 125, fill='green', outline='white')
#        canvas.create_text(400, 100, text=self.host, fill='white')

#    def set_status(self, host, status):
#        if self.status == 'up':
#            self.name_label.config(bg="green")
#            self.ip_label.config(bg="green")
#        else:
#            self.name_label.config(bg="red")
#            self.ip_label.config(bg="red")

# for ip in know_host
#    if ip not in result_message:
#       device down
#       self.host = down
#    elif self.host == down:
#       device_up

#----------------Make Main window-----------------

#--------------------THREADS--------------------------
def ping_func():
    ping_thread = threading.Thread(target=ping_prompt)
    ping_thread.start()
def nmap_func():
    nmap_thread = threading.Thread(target=nmap_prompt)
    nmap_thread.start()

#----------------MAIN BODY OF SCRIPT-------------------
root = tk.Tk()
root.attributes('-zoomed', True)
#root.attributes('-fullscreen', True)
#root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False))
root.title("Network Map")
#height = 1600, width = 1200
canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill="both", expand=True)

#ADD MENU BAR
menubar = tk.Menu(root)

for menu_title, commands in [
    ("File", [
        ("New", new_file),
        ("Save", save_file),
        ("Save As...", save_as),
        ("Load", load_file),
        ("Exit", root.quit)
    ]),
    ("Scan", [
        ("PING", ping_func),
        ("NMAP", nmap_func),
    ])
]:

    menu_object = tk.Menu(menubar, tearoff=0)
    for label, cmd in commands:
        menu_object.add_command(label=label, command=cmd)
    menubar.add_cascade(label=menu_title, menu=menu_object)

#messagebox.showinfo("Version 1 Info", f"This is NetBadger V1 \n The Features of this version are: \n saving, loading, new files \n under the scan tab you can run a ping sweep that will auto map host and if you run the ping again it and a host is not up the color will change from green to red, right now ping can only do /24 and it works best if you are hitting the same /24 every time or hosts will show as down even if they are not, \n and nmap that will fill in ports for hosts when you click them ")


# Attach the menubar to window
root.config(menu=menubar)
root.mainloop()
