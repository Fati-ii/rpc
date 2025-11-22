from xmlrpc.server import SimpleXMLRPCServer

message_buffer = None  # Buffer partagé

def produire(msg):
    global message_buffer
    print("Producteur a déposé :", msg)
    message_buffer = msg
    return "Message déposé"

def consommer():
    global message_buffer
    if message_buffer is None:
        return "Aucun message disponible"
    msg = message_buffer
    message_buffer = None  # Vider le buffer (1 seul message consommable)
    print("Consommateur a lu :", msg)
    return msg

server = SimpleXMLRPCServer(('10.163.15.115', 9000))
print("Serveur tampon actif sur port 9000...")

server.register_function(produire, "produire")
server.register_function(consommer, "consommer")

server.serve_forever()
