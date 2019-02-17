import json

class redirector(object):
    def __init__(self, domain):
        self.config = {}
        self.domain = domain

    def generateCNAMErecord(self, subdomain):
        cname_record = {
            "name": subdomain,
            "type": "CNAME",
            "content": "alias.redirect.name"
        }
        return cname_record

    def generateTXTrecord(self, subdomain, url, type=None):
        types = ['normal', 'permanent', 'wildcard']
        default = {
            "name": "_redirect." + subdomain,
            "type": "TXT",
            "content": "Redirects to " + url
        }
        permanent = {
            "name": "_redirect." + subdomain,
            "type": "TXT",
            "content": "Redirects permanently to " + url
        }
        wildcard = {
            "name": "_redirect." + subdomain,
            "type": "TXT",
            "content": "Redirects from /* " + url
        }
        if type is 'normal' or None:
            return default
        else:
            if type not in types:
                return default
            elif type == 'permanent':
                return permanent
            elif type == 'wildcard':
                prefix = "Redirects from /* to " + url
                if url[-1] == '/':
                    wildcard['content'] =  prefix + '*'
                else:
                    wildcard['content'] = prefix + '/*'
                return wildcard

    def add(self, subdomain, url, type=None):
        config = {
            subdomain: {
                "destination": url,
                "type": str(type)
            }
        }
        if not type:
            config[subdomain]['type'] = 'normal'
            self.config = {**self.config, **config}
        elif type not in ['normal', 'permanent', 'wildcard']:
            exit("INVALID REDIRECT TYPE")
        else:
            self.config = {**self.config, **config}

    def create(self):
        for subdomain in self.config:
            url = self.config[subdomain]['destination']
            type = self.config[subdomain]['type']
            print(self.generateCNAMErecord(subdomain))
            print(self.generateTXTrecord(subdomain, url, type))


redirect = redirector("jayke.me")
redirect.add("git", "https://github.com/jaykepeters", "wildcard")
redirect.add("git2", "https://github.com/jp2")
print(json.dumps((redirect.config), indent=4))
redirect.create()
