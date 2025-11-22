# producteur
import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://10.163.15.115:9000/")  # IP du serveur

msg = input("Message à déposer : ")
res = proxy.produire(msg)
print("Serveur :", res)
