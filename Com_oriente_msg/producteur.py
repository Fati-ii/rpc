# producteur
import xmlrpc.client

def main():
	server_ip = input("IP du serveur (par défaut 10.163.15.115): ") or "10.163.15.115"
	proxy = xmlrpc.client.ServerProxy(f"http://{server_ip}:9000/")

	idprod = input("ID du producteur : ").strip()
	iddest = input("ID destinataire : ").strip()
	contenu = input("Contenu du message : ")

	try:
		res = proxy.production(idprod, contenu, iddest)
		print("Serveur :", res)
	except Exception as e:
		print("Erreur de communication avec le serveur :", e)

if __name__ == '__main__':
	main()
