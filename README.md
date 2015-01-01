py-cpanel-dns-api
=================

**Python Library for WHM's API1 DNS Functions**

https://documentation.cpanel.net/display/SDK/WHM+API+1+Functions#WHMAPI1Functions-DNSfunctions

- Author: Benton Snyder
- Website: http://bensnyde.me
- Created: 7/24/13
- Revised: 1/1/15

Usage
---
```
cpanel = Cpanel("whm.example.com", "root", "strongpassword")
print cpanel.list_zones()
```
