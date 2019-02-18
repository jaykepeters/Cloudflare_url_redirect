# Cloudflare DNS URL Redirect
## URL Redirection using only DNS: CNAME and TXT records with http://redirect.name

# Installation
```
$ git clone repo 
$ cd repo name
$ pip install -m requirements.txt
$ chmod +x main.py (add bang instead of using `python name`
```

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
