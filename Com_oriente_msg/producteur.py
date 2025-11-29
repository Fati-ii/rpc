# producteur
import xmlrpc.client

def main():
	server_ip = input("IP du serveur (par défaut 10.163.15.115): ") or "10.163.15.115"
	proxy = xmlrpc.client.ServerProxy(f"http://{server_ip}:9000/")

	idprod = input("ID du producteur : ").strip()
	# Authentification / possibilité d'inscription
	create = input("Créer un compte ? (o/n) : ").strip().lower()
	if create == 'o':
		pwd = input("Mot de passe : ")
		pwd2 = input("Confirmer le mot de passe : ")
		if pwd != pwd2:
			print("Les mots de passe ne correspondent pas.")
			exit(1)
		res_reg = proxy.register(idprod, pwd)
		print(res_reg)

	passwd = input("Mot de passe : ")
	if not proxy.authenticate(idprod, passwd):
		print("Authentification échouée. Fin.")
		exit(1)

	iddest = input("ID destinataire : ").strip()
	contenu = input("Contenu du message : ")

	try:
		res = proxy.production(idprod, contenu, iddest)
		print("Serveur :", res)
	except Exception as e:
		print("Erreur de communication avec le serveur :", e)

if __name__ == '__main__':
	main()
