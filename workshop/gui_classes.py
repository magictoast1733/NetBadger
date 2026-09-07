class Device:
    def __init__(self, host, status):
#        self.name = name
#        self.type = device_type
        self.host = host
        self.status = status
#        self.mac = mac_address

    def add_device(self, host):
        canvas.create_oval(375, 75, 425, 125, fill='green', outline='white')
        canvas.create_text(400, 100, text=self.host, fill='white')

    def set_status(self, host, status):
            if self.status == 'up':
                self.name_label.config(bg="green")
                self.ip_label.config(bg="green")
            else:
                self.name_label.config(bg="red")
                self.ip_label.config(bg="red")