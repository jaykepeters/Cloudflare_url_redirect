# Cloudflare DNS URL Redirect
## URL Redirection using only DNS: CNAME and TXT records with http://redirect.name

# Python 3 or greater and Pip are required!
# Installation
Enter the following commands in your preffered terminal application:
```
$ git clone https://github.com/jaykepeters/Cloudflare_url_redirect.git
$ cd Cloudflare_url_redirect
$ pip install -r requirements.txt
```
That's it! 
## Run as command line tool
1. Append the following to the top of main.py `#!/usr/bin/env python3`
2. `$ chmod a+x main.py`

# Setup
1. Navigate to https://dash.cloudflare.com/profile and click on "Global API Key"
2. Authenticate, then copy the API key to your clipboard
3. At the top of main.py, you should see a line like: `cf = CloudFlare.CloudFlare(email='', token='')`, edit that line and replace email with your Cloudflare account email, and then paste your Global API Key into the token variable. That's it! 

# Examples
## Adding new redirects
Create a new redirector object
```
my_redirect = redirector("mydomain.com")
```

Add a new normal redirect
```
my_redirect.add("subdomain", "http://www.example.com")
```
OR
```
my_redirect.add("subdomain", "http://www.example.com", type="normal")
```

Add a permanent (301) redirect
```
my_redirect.add("subdomain", "http://www.example.com", type="permanent")
```
Add a new wildcard redirect 
- Redirects all traffic from http://subdomain/* to http://www.example.com/*
- Customization coming in the next update
```
my_redirect.add("subdomain", "http://www.example.com", type="wildcard")
```

## Create all redirects added in the redirector object
```
my_redirect.create()
```

## Delete a redirect record
```
my_redirect.delete("subdomain")
```
OR
```
my_redirect.delete("subdomain.mydomain.com")
```

# Upcoming Features
- Ability to list all redirects
- Abilty to modify redirects
- Ability to import or save them to a file
- Ability to customize wildcard redirects
