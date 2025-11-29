from xmlrpc.server import SimpleXMLRPCServer
import sys

# messages stored as dicts: {'sender': idprod, 'recipient': iddest, 'content': contenu}
messages = []

def production(idproducteur, contenu, iddestinataire):
    
    msg = {'sender': idproducteur, 'recipient': iddestinataire, 'content': contenu}
    messages.append(msg)
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
    print(f"Consommateur {idconsommateur} a lu {len(found)} message(s)")
    return found

def _preload_message(spec):
    # expected format: sender|recipient|content
    parts = spec.split('|', 2)
    if len(parts) == 3:
        messages.append({'sender': parts[0], 'recipient': parts[1], 'content': parts[2]})

def main():
    # CLI: buffer_server.py [ip] [msg1] [msg2] ... where msgN is sender|recipient|content
    bind_ip = '10.163.15.115'
    if len(sys.argv) >= 2:
        bind_ip = sys.argv[1]
    if len(sys.argv) > 2:
        for spec in sys.argv[2:]:
            _preload_message(spec)

    server = SimpleXMLRPCServer((bind_ip, 9000), allow_none=True)
    print(f"Serveur tampon actif sur {bind_ip}:9000...")

    server.register_function(production, "production")
    server.register_function(consommateur, "consommateur")

    server.serve_forever()

if __name__ == '__main__':
    main()
