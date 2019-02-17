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
    def generateTXTrecord(sself, subdomain, url, type=None):
        types = ['permanent', 'wildcard']
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
        if type is None:
            return default
        else:
            if type not in types:
                exit("Invalid redirect type: " + type)
            elif type == 'permanent':
                return permanent
            elif type == 'wildcard':
                prefix = "Redirects from /* to " + url
                if url[-1] == '/':
                    wildcard['content'] =  prefix + '*'
                else:
                    wildcard['content'] = prefix + '/*'
                return wildcard

    def add(self, subdomain, url):
        redirect = {subdomain: url}
        self.config.update(redirect)

    def create(self):
        for subdomain in self.config:
            cname_record = self.generateCNAMErecord(subdomain)
            txt_record = self.generateTXTrecord(subdomain, self.config[subdomain])
            return cname_record, txt_record 

redirect = redirector("jayke.me")
redirect.add("git", "https://github.com/jaykepeters")
print(redirect.create())
