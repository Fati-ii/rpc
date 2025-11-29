import xmlrpc.client

def main():
	server_ip = input("IP du serveur (par défaut 10.163.15.115): ") or "10.163.15.115"
	proxy = xmlrpc.client.ServerProxy(f"http://{server_ip}:9000/")

	idcons = input("ID du consommateur : ").strip()
	try:
		res = proxy.consommateur(idcons)
		if not res:
			print("Aucun message pour cet ID.")
		else:
			print(f"Messages reçus pour {idcons} :")
			# res is expected to be a list of dicts
			for m in res:
				sender = m.get('sender') if isinstance(m, dict) else None
				content = m.get('content') if isinstance(m, dict) else m
				print(f" - De {sender}: {content}")
	except Exception as e:
		print("Erreur de communication avec le serveur :", e)

if __name__ == '__main__':
	main()
