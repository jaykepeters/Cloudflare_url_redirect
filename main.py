import CloudFlare
from validator_collection import checkers

cf = CloudFlare.CloudFlare(email='', token='')
class redirector(object):
    def get_zone_id(self, domain):
        zones = cf.zones.get()
        for zone in zones:
            zone_id = zone['id']
            zone_name = zone['name']
            if domain == zone_name:
                return zone_id
            else:
                exit("Invalid Zone Name: " + domain)

    def get_dns_records(self):
        self.dns_records = cf.zones.dns_records.get(self.zone_id, params={'per_page': 100})

    def __init__(self, domain):
        self.config = {}
        self.domain = domain
        self.zone_id = self.get_zone_id(self.domain)
        self.get_dns_records()

    def generateCNAMErecord(self, subdomain):
        cname_record = {
            "name": ".".join([subdomain, self.domain]),
            "type": "CNAME",
            "content": "alias.redirect.name"
        }
        return cname_record

    def generateTXTrecord(self, subdomain, url, type=None):
        types = ['normal', 'permanent', 'wildcard']
        default = {
            "name": "_redirect." + ".".join([subdomain, self.domain]),
            "type": "TXT",
            "content": "Redirects to " + url
        }
        permanent = {
            "name": "_redirect." + ".".join([subdomain, self.domain]),
            "type": "TXT",
            "content": "Redirects permanently to " + url
        }
        wildcard = {
            "name": "_redirect." + ".".join([subdomain, self.domain]),
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
        if checkers.is_url(url):
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
        else:
            print("Invalid URL: " + url)

    def check_existing(self, record):
        searches = ['name', 'type', 'content']
        match = False
        for dns_record in self.dns_records:
            id = dns_record['id']
            dns_record = {
                'name': dns_record['name'],
                'type': dns_record['type'],
                'content': dns_record['content']
            }
            if record == dns_record:
                match = id
        return match

    def create(self):
        if len(self.config) == 0:
            exit("Configuration Blank, exiting...")
        for subdomain in self.config:
            url = self.config[subdomain]['destination']
            type = self.config[subdomain]['type']

            cname_record = self.generateCNAMErecord(subdomain)
            txt_record = self.generateTXTrecord(subdomain, url, type)

            if not self.check_existing(cname_record):
                try:
                    cf.zones.dns_records.post(self.zone_id, data=cname_record)
                except:
                    exit("There was an error creating the cname record for " + cname_record['name'])
                try:
                    cf.zones.dns_records.post(self.zone_id, data=txt_record)
                except:
                    exit("There was an error creating the txt reacord for " + txt_record['name'])
                print("DNS redirect created successfully for " + subdomain)
            else:
                print("record already exists")

    def delete(self, subdomain):
        # Refresh DNS Records
        self.get_dns_records()
        ids = []
        # Correct subdomain
        if not self.domain in subdomain:
            subdomain = ".".join([subdomain, self.domain])
        # Get the CNAME and TXT record IDs
        for dns_record in self.dns_records:
            id = dns_record['id']
            name = dns_record['name']
            type =  dns_record['type']
            if name == subdomain and type == 'CNAME':
                ids.append(id)
            elif name == ".".join(["_redirect", subdomain]) and type == 'TXT':
                ids.append(id)

        if len(ids) == 2:
            for id in ids:
                try:
                    cf.zones.dns_records.delete(self.zone_id, id)
                except:
                    exit("Cannot delete record!")
            print("Successfully deleted: " + subdomain)
        else:
            print("Nonexistent domain: " + subdomain)
