# Code blocks that are given as hints.

# Check that these values match the values at the CTF
REMOTE_IP = "127.0.0.1"
REMOTE_PORT = 53


def query(typ: str, domain: str, ignore_fail: bool = False):
    from dns import resolver
    resolver = resolver.Resolver(configure=False)
    resolver.nameservers = [REMOTE_IP]
    resolver.port = REMOTE_PORT
    return resolver.resolve(domain, typ, raise_on_no_answer=not ignore_fail)


def get_new_game_uuid():
    """Creates a new game. Returns the UUID"""
    import re
    uuid_re = re.compile('([a-f0-9]+)\.dnstris\.ctf.')
    uuid_response = query('A', 'dnstris.ctf.')
    for reply in uuid_response.response.answer:
        mtch = re.fullmatch(uuid_re, reply.name.__str__())
        if mtch is not None:
            return mtch[1]
    raise "could not find uuid"


def get_data(game_uuid: str) -> dict:
    """Returns data about the game"""
    from dns.rdatatype import RdataType

    status_domain = f"{game_uuid}.dnstris.ctf."
    status_response = query('TXT', status_domain)
    response = dict()
    for answer in status_response.response.answer:
        if answer.rdtype != RdataType.TXT:
            continue

        for answer in answer.items:
            answer = str(answer)[1:-1].split("=")
            key = answer[0]
            value = answer[1]
            response[key] = value

    return response


def send_command(command_name: str, game_uuid: str):
    """Sends the given command to the game with given UUID"""
    query("TXT", f"{command_name}.{game_uuid}.dnstris.ctf", True)
