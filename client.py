import socket
import select
import errno
from threading import Thread
from tkinter import *

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP, PORT))

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

def send_msg():
    message = txt.get()
    if message:
        lbl.insert(END, message + '\n', 'mymessage')
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
    txt.delete(0, 'end')

window = Tk()
window.title(my_username)
window['bg']='gray98'
window['padx']=10
window['pady']=10

txt = Entry(window)
txt['width']=40
txt['relief']=GROOVE
txt['bg']='white'
txt['fg']='green'
txt['font']=("",18)
txt.grid(column=0,row=1,padx=5,pady=15)

send = Button(window,text="send", command=send_msg)
send['relief']=GROOVE
send['bg']='white'
send['fg']='green'
send['activebackground']='ivory3'
send['padx']=3
send['font']=("",18)
send.grid(column=1,row=1,padx=5,pady=15)

lbl = Text(window, width=70, height=30, bg = '#fff', padx=3)
lbl.grid(columnspan=2,column=0,row=0,padx=5)
lbl.tag_config('mymessage', foreground="green", justify='right')
scroll = Scrollbar(window)
scroll.grid(columnspan=2, column=2, row=0, padx=5, sticky=N+S)
scroll.config(command=lbl.yview)

def receive():
    while True:
        try:
            while True:
                username_header = client_socket.recv(HEADER_LENGTH)
                print('Connection closed by the server')
                sys.exit()

                username_length = int(username_header.decode('utf-8').strip())

                username = client_socket.recv(username_length).decode('utf-8')

                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_length).decode('utf-8')

                lbl.insert(END, username + ' : ' + message + '\n')

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()
            continue

        except Exception as e:
            print('Reading error: '.format(str(e)))
            sys.exit()
control_thread = Thread(target=receive, daemon=True)
control_thread.start()

window.mainloop()
