#ESP 32
packet = b','.join(x if isinstance(x, bytes) else str(x).encode() for x in combined_data) + b'\n'


#Server 
data = s.recv(1024).decode().splitlines()[0] #Recieves data from esp32
