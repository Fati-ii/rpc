import xmlrpc.client

server_ip = "10.163.13.238"  # <-- IP de la machine A
proxy = xmlrpc.client.ServerProxy(f"http://{server_ip}:8000/")

res = proxy.message("Salut depuis la machine B")
print("Réponse du serveur :", res)
#import socket

# s = socket.socket()
# s.connect(("10.163.13.238", 5000))

# print("Mon IP locale :", s.getsockname()[0])   # IP utilisée pour sortir
# print("IP du serveur :", s.getpeername()[0])