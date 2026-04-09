import random
import string

def rand_str(n=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/138.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
]

def random_ua():
    return random.choice(USER_AGENTS)

def base_config():
    return '''# Important file paths and locations
private-key-file = "data/keys/conquest-server_x25519_private.key"
database-file = "data/conquest.db"

'''

# if you want to add new template, please think to add theses informations
def ensure_c2_compatibility(profile: str) -> str:


    if "[http-get.agent.heartbeat]" not in profile:
        heartbeat_block = """
[http-get.agent.heartbeat]
placement = { type = "header", name = "Authorization" }
encoding = { type = "base64", url-safe = true }
prepend = "Bearer "
append = ".auto"
"""
        profile += heartbeat_block

    if "[http-get.server.output]" not in profile:
        profile += """
[http-get.server.output]
placement = { type = "body" }
"""

    if "[http-post.agent.output]" not in profile:
        profile += """
[http-post.agent.output]
placement = { type = "body" }
encoding = { type = "base64" }
"""


    if "[http-post.server.output]" not in profile:
        profile += """
[http-post.server.output]
body = "OK"
"""

    return profile


def generate_jquery_profile():
    ua = random_ua()

    profile = base_config() + f'''name = "jquery-profile"

[team-server]
host = "0.0.0.0"
port = {random.randint(20000,60000)}
users = [
{{ username = "{rand_str(6)}", password = "{rand_str(10)}" }}
]

[http-get]
user-agent = "{ua}"
endpoints = ["/ajax/libs/jquery/3.6.0/jquery.min.js"]

[http-get.agent.headers]
Host = "cdnjs.cloudflare.com"
Accept = "*/*"
Connection = "Keep-Alive"

[http-get.server.headers]
Content-Type = "application/javascript"
Server = "cloudflare"

[http-post]
user-agent = "{ua}"
endpoints = ["/ajax/report"]
request-methods = ["POST"]

[http-post.agent.headers]
Host = "cdnjs.cloudflare.com"
Content-Type = "application/json"
'''

    return ensure_c2_compatibility(profile)



def generate_slack_profile():
    ua = random_ua()

    profile = base_config() + f'''name = "slack-profile"

[team-server]
host = "0.0.0.0"
port = {random.randint(20000,60000)}
users = [
{{ username = "{rand_str(6)}", password = "{rand_str(10)}" }}
]

[http-get]
user-agent = "{ua}"
endpoints = ["/messages/C0527B0NM"]

[http-get.agent.headers]
Accept = "*/*"
Accept-Language = "en-US"
Connection = "close"

[http-get.server.headers]
Content-Type = "text/html; charset=utf-8"
Server = "Apache"

[http-post]
user-agent = "{ua}"
endpoints = ["/api/api.test"]
request-methods = ["POST"]

[http-post.agent.headers]
Accept = "*/*"
Accept-Language = "en-US"
'''

    return ensure_c2_compatibility(profile)


def convert_and_fix_profile(raw_profile: str) -> str:
    profile = base_config() + raw_profile
    return ensure_c2_compatibility(profile)


# available templates 
TEMPLATE_NAMES = ["jquery", "slack"]

def generate_profile_by_name(name):
    if name == "jquery":
        return generate_jquery_profile()
    elif name == "slack":
        return generate_slack_profile()
    else:
        raise ValueError("unknown template")