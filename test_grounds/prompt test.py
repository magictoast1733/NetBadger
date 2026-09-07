#from tqdm import tk
import tkinter as tk
from tkinter import ttk
import my_ping



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

        # Dynamioc build a label and input box for each question passed in
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





#def run_back_test(ip, first, last):
#    """back end reseves data no back end prompt"""
#    print("--- Backend Running ---")
#    print(f"target ip: {ip}")
#    print(f"nmapfage

root = tk.Tk()
root.title("tool test")
root.geometry("500x300")

status_label = tk.Label(root, text="system ready", font=("Arial", 12))
status_label.pack(expand=True)

def handle():
    # 1. define questions
    questions = [
        "enter first 3 octets",
        "enter start of ip range",
        "enter end of ip range:"
    ]

    # 2. instantiate class
    # freezes execurion here and wait until users clicks button
    popup = Prompt(root, title="net test conf", prompt=questions)

    # 3. grab list of results and dont just close window
    answer = popup.results

    #if the user filed it out and dinint just close windo
    if answer:
        #unpack the list directly into function argument
        # this mirrors: ping_test.ping(input("Enter first 3 octets of IP range: "), input("range start: "), input("range end: "))
        status_label.config(text="running scan...", fg="orange")

        #result_message = run_back_test(answer[0],answer[1],answer[2])
        result_message = ping_test.ping(answer[0], answer[1], answer[2])

        status_label.config(text=result_message, fg="green")
    else:
        status_label.config(text="scan config caneled", fg="red")

    #make bar
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)

    # link actions
file_menu.add_command(label="new tool run", command=handle)
file_menu.add_command(label="exit", command=root.quit)
menubar.add_cascade(label="file", menu=file_menu)

root.config(menu=menubar)
root.mainloop()