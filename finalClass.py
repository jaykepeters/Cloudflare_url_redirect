import CloudFlare
cf = CloudFlare.CloudFlare(email='', token='')

from validator_collection import checkers
import json

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
    def __init__(self, domain):
        self.config = {}
        self.domain = domain
        self.zone_id = self.get_zone_id(self.domain)


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
        dns_records = cf.zones.dns_records.get(self.zone_id)
        for dns_record in dns_records:
            dns_record = {
                "name": dns_record['name'],
                "type": dns_record['type'],
                "content": dns_record['content']
            }
            matched = False
            if record == dns_record:
                matched = True
        return matched

    def create(self):
        for subdomain in self.config:
            url = self.config[subdomain]['destination']
            type = self.config[subdomain]['type']

            cname_record = self.generateCNAMErecord(subdomain)
            txt_record = self.generateTXTrecord(subdomain, url, type)

            if not self.check_existing(cname_record) and not self.check_existing(txt_record):
                print(cname_record)
                print(txt_record)
            else:
                print("Redirect already exists: " + subdomain)

redirect = redirector("jayke.me")
redirect.add("snap", "https://www.snapchat.com/add/jayke_peters")
redirect.create()

## DELTEA DNS RECORD
#cf.zones.dns_records.delete(redirect.zone_id, '895576b5b266cbd883e89c3bce754336')
