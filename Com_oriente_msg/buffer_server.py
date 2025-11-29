from xmlrpc.server import SimpleXMLRPCServer
import sys
import os
import csv
import hashlib
from datetime import datetime

# messages stored as dicts: {'sender': idprod, 'recipient': iddest, 'content': contenu, 'timestamp': ts}
messages = []
accounts = {}  # username -> password_hash

ROOT_DIR = os.path.dirname(__file__)
ACCOUNTS_CSV = os.path.join(ROOT_DIR, 'accounts.csv')
MESSAGES_CSV = os.path.join(ROOT_DIR, 'messages.csv')

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def load_accounts():
    accounts.clear()
    if not os.path.exists(ACCOUNTS_CSV):
        return
    with open(ACCOUNTS_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            username = row.get('username')
            pwd = row.get('password_hash')
            if username and pwd:
                accounts[username] = pwd

def save_account(username, password_hash):
    file_exists = os.path.exists(ACCOUNTS_CSV)
    with open(ACCOUNTS_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['username', 'password_hash'])
        writer.writerow([username, password_hash])

def register(username, password):
    """Créer un compte (username unique)."""
    if username in accounts:
        return {'status': 'error', 'message': 'Utilisateur existe déjà'}
    pwd_hash = _hash_password(password)
    accounts[username] = pwd_hash
    save_account(username, pwd_hash)
    print(f"Compte créé: {username}")
    return {'status': 'ok'}

def authenticate(username, password):
    """Vérifie les identifiants. Retourne True/False."""
    if username not in accounts:
        return False
    return accounts.get(username) == _hash_password(password)

def load_messages():
    messages.clear()
    if not os.path.exists(MESSAGES_CSV):
        return
    with open(MESSAGES_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # row contains keys: sender, recipient, content, timestamp
            messages.append({'sender': row.get('sender'), 'recipient': row.get('recipient'), 'content': row.get('content'), 'timestamp': row.get('timestamp')})

def save_all_messages():
    with open(MESSAGES_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['sender', 'recipient', 'content', 'timestamp'])
        for m in messages:
            writer.writerow([m.get('sender'), m.get('recipient'), m.get('content'), m.get('timestamp')])

def append_message_csv(m):
    file_exists = os.path.exists(MESSAGES_CSV)
    with open(MESSAGES_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['sender', 'recipient', 'content', 'timestamp'])
        writer.writerow([m.get('sender'), m.get('recipient'), m.get('content'), m.get('timestamp')])

def production(idproducteur, contenu, iddestinataire):
    """Déposer un message destiné à `iddestinataire` venant de `idproducteur`."""
    ts = datetime.utcnow().isoformat()
    msg = {'sender': idproducteur, 'recipient': iddestinataire, 'content': contenu, 'timestamp': ts}
    messages.append(msg)
    append_message_csv(msg)
    print(f"Producteur {idproducteur} a déposé pour {iddestinataire}: {contenu}")
    return {'status': 'ok', 'stored': msg}

def consommateur(idconsommateur):
    """Retourne et supprime tous les messages destinés à `idconsommateur`."""
    found = [m for m in messages if m.get('recipient') == idconsommateur]
    if not found:
        print(f"Aucun message pour {idconsommateur}")
        return []
    # remove delivered messages
    remaining = [m for m in messages if m.get('recipient') != idconsommateur]
    messages.clear()
    messages.extend(remaining)
    # persist remaining messages
    save_all_messages()
    print(f"Consommateur {idconsommateur} a lu {len(found)} message(s)")
    return found

def _preload_message(spec):
    # expected format: sender|recipient|content
    parts = spec.split('|', 2)
    if len(parts) == 3:
        ts = datetime.utcnow().isoformat()
        messages.append({'sender': parts[0], 'recipient': parts[1], 'content': parts[2], 'timestamp': ts})

def main():
    # CLI: buffer_server.py [ip] [msg1] [msg2] ... where msgN is sender|recipient|content
    bind_ip = '10.163.15.115'
    if len(sys.argv) >= 2:
        bind_ip = sys.argv[1]
    if len(sys.argv) > 2:
        for spec in sys.argv[2:]:
            _preload_message(spec)

    # load persistent data
    load_accounts()
    load_messages()

    server = SimpleXMLRPCServer((bind_ip, 9000), allow_none=True)
    print(f"Serveur tampon actif sur {bind_ip}:9000...")

    # register RPC functions
    server.register_function(production, "production")
    server.register_function(consommateur, "consommateur")
    server.register_function(register, "register")
    server.register_function(authenticate, "authenticate")

    server.serve_forever()

if __name__ == '__main__':
    main()
