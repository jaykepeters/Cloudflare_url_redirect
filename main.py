import CloudFlare, json
cf = CloudFlare.CloudFlare(email='admin@domain.com', token='1234')

class url_redirect(object):
    def __init__(self, subdomain, url):
        self.domain = ''
        self.cname_record = {
            "name": subdomain,
            "type": "CNAME",
            "content": 'alias.redirect.name'
        }
        self.txt_record = {
                "name": "_redirect." + subdomain,
                "type": "TXT",
                "content": "Redirects to " + url
        }

    def create(self):
        try:
            cf.zones.dns_records.post(get_zone_id("jayke.me"), data=self.cname_record)
            cf.zones.dns_records.post(get_zone_id("jayke.me"), data=self.txt_record)
            print("RECORD CREATED: ", self.cname_record['name'])
        except(CloudFlare.exceptions.CloudFlareAPIError):
            print("RECORD EXISTS: ", self.cname_record['name'], self.txt_record['content'])

def get_zone_id(domain):
    zones = cf.zones.get(params={'per_page': 100})
    for zone in zones:
        zone_id = zone['id']
        zone_name = zone['name']

        if domain == zone_name:
            return zone_id
            break
        else:
            exit("INVALID DOMAIN")

for record in cf.zones.dns_records.get(get_zone_id("jayke.me")):
    r = record

redirects = {
    "support": "https://support.jpits.us/open.php",
    "website": "http://www.jaykepeters.com",
    "snap": "https://www.snapchat.com/add/jayke_peters",
    "insta": "https://www.instagram.com/jayke_peters",
    "tweet": "https://www.twitter.com/jayke_peters",
    "git": "https://www.github.com/jaykepeters"
}

for redirect in redirects:
    subdomain = redirect
    url = redirects[redirect]
    new_redirect = url_redirect(subdomain, url)
    new_redirect.create()
