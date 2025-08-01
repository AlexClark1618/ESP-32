import socket
import ustruct
import time
import network
import select

# ---------- Functions ----------
def con_to_wifi(ssid, password):
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
    print("Wi-Fi connected.")
    return None
 
packet_format = "!IIIIIIIII"

def data_packing(packet_format: str):
    packet = ustruct.pack(packet_format, 
        inst,            # char (1 byte)
        ID,
        RF,              # char (1 byte)
        cal,              # uint8 (1 byte)
        ch,          # uint8 (1 byte)
        w_num,      	 # uint32 (4 bytes) #Q for 8 byte uint64
        ms,         # uint32 (4 bytes)
        sub_ms,
        event_num                  # uint32 (4 bytes)
    )
    
    return packet

def connect_socket(host, port):
    s = socket.socket()
    try:
        s.connect((host, port))
        print("Socket connected.")
        return s
    except OSError as e:
        print("Failed to connect socket:", e)
        return None

# ---------- Wi-Fi Setup ----------
#ssid = 'TP-Link_FB80'
#password = 'Beau&River'

ssid = 'ONet'
password = ''

#These can be moved to the main wifi function, but I thinks its more versitile to define them as globals
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

con_to_wifi(ssid, password)
mac_id = wlan.config('mac')[-1]  # last byte of MAC

# ---------- Connecting to Server ----------
#HOST = '192.168.0.93'
HOST = '134.69.200.155'
PORT = 12345

s = connect_socket(HOST,PORT)

# ---------- For peeking ----------
poller = select.poll()
poller.register(s, select.POLLIN)

# ---------- Main Loop ----------

while True:
    if not wlan.isconnected():
        con_to_wifi(ssid, password)
    
    events = poller.poll(100) #Checks for socket activity
    
    #Checks for wifi disconnections. (May want to move this to an exception handle)
    
    try:
        if events:
            print('Data rec')
            req = s.recv(1024) #Request from server
            
            
            if req: #If request proceed
                #print(req.decode())        
                chunk = req.decode().strip().split('\n') #Break request packet
                print(chunk)
                
                for event in chunk:
                    print("event", event)
                    cmd = event.strip().split(';')
                    print("cmd" , cmd)
                #print('Data recieved:' , req)
                
                    if cmd[0] == "CMD: 0": #Processes data and collects requested integer and specified length around it                                
                       
                        inst = 0            
                        ID = 1
                        RF = 0               
                        cal = 0             
                        ch = 0         
                        w_num = int(time.time())  
                        ms = int(time.time())      
                        sub_ms = int(time.time())
                        event_num = int(cmd[2].replace("Event #:", ""))
                        print(event_num)
                        
                        try:
                            packet = data_packing(packet_format)

                            data = s.send(packet)
                            print(f'Bytes sent: {data}') #Prints byte size

                        except OSError as e: 
                            print("Socket error:", e)
                            try:
                                poller.unregister(s)
                                s.close()
                            except:
                                pass
                            
                            time.sleep(1)
                            s = connect_socket(HOST, PORT)
                            if s:
                                poller.register(s, select.POLLIN)
                                continue

    except Exception as e:
        print(f"Error sending to {s}:{e}")
        pass


