import argparse
import re
from generator import generate_profile_by_name, convert_and_fix_profile

def parse_headers(block):
    return re.findall(r'header\s+"([^"]+)"\s+"([^"]+)"', block)

def parse_parameters(block):
    return re.findall(r'parameter\s+"([^"]+)"\s+"([^"]+)"', block)

def extract_blocks(content, block_name):
    blocks = []
    pattern = re.compile(rf'{block_name}\s*\{{', re.IGNORECASE)
    pos = 0
    while True:
        m = pattern.search(content, pos)
        if not m:
            break
        start = m.end()
        depth = 1
        end = start
        while depth > 0 and end < len(content):
            if content[end] == '{':
                depth += 1
            elif content[end] == '}':
                depth -= 1
            end += 1
        blocks.append(content[start:end-1].strip())
        pos = end
    return blocks

def cobalt_to_toml(content: str) -> str:
    toml = []
    toml.append('name = "cobalt-converted"\n\n')
    toml.append('[team-server]\n')
    toml.append('host = "0.0.0.0"\n')
    toml.append('port = 4444\n')
    toml.append('users = [{ username = "jenaye", password = "alazeub" }]\n\n')

    ua_match = re.search(r'set useragent\s+"([^"]+)"', content)
    ua_val = ua_match.group(1) if ua_match else "Mozilla/5.0"

    for proto in ["http-get", "http-post"]:
        main_blocks = extract_blocks(content, proto)

        for block in main_blocks:
            toml.append(f'[{proto}]\n')
            toml.append(f'user-agent = "{ua_val}"\n')

            uri_match = re.search(r'set uri\s+"([^"]+)"', block)
            if uri_match:
                toml.append(f'endpoints = ["{uri_match.group(1)}"]\n')
                if proto == "http-post":
                    toml.append('request-methods = ["POST"]\n')

            toml.append('\n')

            # CLIENT
            client_blocks = extract_blocks(block, "client")
            for client in client_blocks:
                headers = parse_headers(client)
                parameters = parse_parameters(client)

                if headers:
                    toml.append(f'[{proto}.agent.headers]\n')
                    for h in headers:
                        toml.append(f'{h[0]} = "{h[1]}"\n')
                    toml.append('\n')

                if parameters:
                    toml.append(f'[{proto}.agent.parameters]\n')
                    for p in parameters:
                        toml.append(f'{p[0]} = ["{p[1]}"]\n')
                    toml.append('\n')

            # SERVER
            server_blocks = extract_blocks(block, "server")
            for server in server_blocks:
                headers = parse_headers(server)

                if headers:
                    toml.append(f'[{proto}.server.headers]\n')
                    for h in headers:
                        toml.append(f'{h[0]} = "{h[1]}"\n')
                    toml.append('\n')

    return ''.join(toml)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", help="generate profile using internal template (jquery/slack atm)")
    parser.add_argument("--cobalt-converter", help="convert cobalt profile to TOML")

    args = parser.parse_args()

    if args.generate:
        try:
            profile = generate_profile_by_name(args.generate)
            print(profile)
        except ValueError as e:
            print(f"err: {e}")

    elif args.cobalt_converter:
        try:
            with open(args.cobalt_converter, "r") as f:
                content = f.read()
                toml_profile = cobalt_to_toml(content)
                fixed_profile = convert_and_fix_profile(toml_profile)

                print(fixed_profile)

        except FileNotFoundError:
            print(f"file not found : {args.cobalt_converter}")


if __name__ == "__main__":
    main()