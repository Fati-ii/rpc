import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://10.163.15.115:9000/")

res = proxy.consommer()
print("Message lu par consommateur :", res)
