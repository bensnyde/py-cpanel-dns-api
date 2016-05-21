"""

Python Library for WHM's API1 DNS Functions

    https://documentation.cpanel.net/display/SDK/Guide+to+WHM+API+1

Author: Benton Snyder
Website: http://bensnyde.me
Created: 7/24/13
Revised: 5/16/16

"""
import base64
import httplib
import urllib
import logging
import json


class CpanelDNS:
    def __init__(self, whm_base_url, whm_username, whm_password):
        """Constructor

        Parameters
            whm_base_url: str whm base url (ex. whm.example.com)
            whm_username: str whm root username
            whm_password: str whm password
        """
        self.whm_base_url = whm_base_url
        self.whm_headers = {'Authorization':'Basic ' + base64.b64encode(whm_username+':'+whm_password).decode('ascii')}


    def _whm_api_query(self, resource, kwargs):
        """WHM API Query

            Queries WHM server's JSON API with specified query string.

        Parameters
            resource: str api resource uri
            kwargs: dict
        Returns
            json
        """
        try:
            conn = httplib.HTTPSConnection(self.whm_base_url, 2087)
            conn.request('GET', '/json-api/%s?%s' % (resource, urllib.urlencode(kwargs)), headers=self.whm_headers)
            response = conn.getresponse()
            data = json.loads(response.read())
            conn.close()
            return data
        except httplib.HTTPException as ex:
            logging.critical("HTTPException from CpanelDNS API: %s" % ex)
        except ValueError as ex:
            logging.critical("ValueError decoding CpanelDNS API response string: %s" % ex)
        except Exception as ex:
            logging.critical("Unhandled Exception while querying CpanelDNS API: %s" % ex)


    def add_zone(self, domain, ip, trueowner=None):
        """Add DNS Zone

            Creates a DNS zone.

                https://documentation.cpanel.net/display/SDK/WHM+API+1+Functions+-+adddns

        Parameters
            domain: str domain name
            ip: str ip address
            trueowner: str cpanel username
        Returns
            json
        """
        return self._whm_api_query('adddns', {
            'domain': domain,
            'ip': ip,
            'trueowner': trueowner
        })


    def add_zone_record(self, kwargs):
        """Add Zone Record

            Adds a record to the specified DNS zone.

                https://documentation.cpanel.net/display/SDK/WHM+API+1+Functions+-+addzonerecord

        Parameters
            zone:str - Name of the zone to be added, expressed like a domain name. (ex. example.com)
            * May or may not be required, depending on the type of record being set
            *name:str - The name of the zone record. (ex. example.com.)
            *address:str - The IP address of the zone being added. (ex. 127.0.0.1)
            *class:str - The class of the record. (typically IN, for "Internet")
            *cname:str - The canonical name in a CNAME record.
            *exchange:str - In an MX record, the name of the destination mail server.
            *nsdname:str - A domain name to use for a nameserver. Example: ns1.example.com
            *ptrdname:str - The domain to which the IP address will point.
            *priority:int - In an MX record, this parameter specifies the priority of the destination mail server. In an SRV record, this parameter specifies the overall priority for the SRV record.
            *type:str - The type of zone record being added.
            *ttl:int - The record's time to live.
            ** Required for SRV records
            **weight:int - The weight of the record, relative to records of the same priority.
            **port:int - The port number on which users can access a particular service.
            **target:str - The hostname of the machine providing a specified service.
        Returns
            json
        """
        return self._whm_api_query('addzonerecord', kwargs)


    def edit_zone_record(self, kwargs):
        """Edit DNS Zone Record

            Modify a DNS zone record on the server.

                https://documentation.cpanel.net/display/SDK/WHM+API+1+Functions+-+editzonerecord

        Parameters
            zone:str - Name of the zone to be added, expressed like a domain name. (ex. example.com)
            Line:str - The number of the zone record line you wish to edit.
            * May or may not be required, depending on the type of record being set
            *address:str - The IP address of the zone being added. (ex. 127.0.0.1)
            *class:str - The class of the record. (typically IN, for "Internet")
            *cname:str - The canonical name in a CNAME record.
            *exchange:str - In an MX record, the name of the destination mail server.
            *preference:int - In an MX record, the priority of the destination mail server. (0 is highest priority)
            *expire:str -  A 32-bit time value that specifies the upper limit on the time interval that can elapse before the zone is no longer authoritative.
            *minimum:int - The unsigned 32-bit minimum time to live field that should be exported with any record from this zone.
            *mname:int - The domain name of the nameserver serving as the original or primary source of data for this zone. Example: ns1.example.com
            *name:str - Domain name. Example: example.com
            *nsdname:str - A domain name to use for a nameserver. Example: ns1.example.com
            *raw:str - Raw line data.
            *refresh:int - 32-bit time interval which will elapse before the zone will be refreshed.
            *retry:int - 32-bit time interval which will elapse before a failed refresh will be retried.
            *rname:str - A domain name which specifies the mailbox of the person responsible for this zone. Example: user.example.com
            *serial:int - The unsigned 32-bit version number of the original copy of the zone.
            *txtdata:str - Text record data.
            *type:str - The type of zone record being added.
            *ttl:int - The record's time to live.
        Returns
            json
        """
        return self._whm_api_query('editzonerecord', kwargs)


    def add_reversed_zone_record(self, zone, name, ptrdname):
        """Add DNS PTR Record

            Add reverse PTR record to specified zone.

                https://documentation.cpanel.net/display/SDK/WHM+API+1+Functions+-+addzonerecord+for+Reverse+DNS

        Parameters
            zone:str - The name of the reverse DNS zone file to create. This value must follow a standardized naming schema.
            name:int - You will need to enter the last octet of the IP address here. If your IP address was 192.168.0.1, you would enter 1 in this parameter.
            ptrdname:str - The name of the domain to which the IP address will resolve (e.g. example.com).
        Returns
            json
        """
        return self._whm_api_query('addzonerecord', {
            'zone': zone,
            'name': name,
            'ptrdname': ptrdname,
            'type': 'PTR'
        })


    def get_zone_record(self, domain, line):
        """Get DNS Zone Record

            Retrieves specified record from specified zone.

                https://documentation.cpanel.net/display/SDK/WHM+API+1+Functions+-+getzonerecord

        Parameters
            domain:str - The domain whose zone record you wish to view.
            line:str - The line you wish to view in the zone record.
        Returns
            json
        """
        return self._whm_api_query('getzonerecord', {
            'domain': domain,
            'line': line
        })


    def delete_zone(self, domain):
        """Delete DNS Zone

            Deletes a DNS zone.

                https://documentation.cpanel.net/display/SDK/WHM+API+1+Functions+-+killdns

        Parameters
            domain:str - Domain name for the zone to be deleted.
        Returns
            json
        """
        return self._whm_api_query('killdns', {
            'domain': domain
        })


    def list_zones(self, cpanel_user=None):
        """List DNS zones

            Retrieves list of all domains and corresponding DNS zones associated with your server.

                https://documentation.cpanel.net/display/SDK/WHM+API+1+Functions+-+listzones

        Parameters
            *cpanel_user: str cpanel account username to call from
        Returns
            json
        """
        return self._whm_api_query('listzones', {})


    def list_zone(self, domain):
        """Get DNS Zone

            Retrieves all records for specified zone.

                https://documentation.cpanel.net/display/SDK/WHM+API+1+Functions+-+dumpzone

        Parameters
            domain:str - Domain for which to show the DNS zone. Example: example.com
        Returns
            json
        """
        return self._whm_api_query('dumpzone', {
            'domain': domain
        })


    def get_nameserver_ip(self, nameserver):
        """Get Nameserver IP

            Retrieve the IP address of a registered nameserver from the root nameservers.

                https://documentation.cpanel.net/display/SDK/WHM+API+1+Functions+-+lookupnsip

        Parameters
            nameserver:str - Hostname of the nameserver whose IP address you want to obtain. Example: ns1.example.com
        Returns
            json
        """
        return self._whm_api_query('lookupnsip', {
            'nameserver': nameserver
        })


    def delete_zone_record(self, zone, line):
        """Delete DNS Zone Record

            Delete a DNS zone record from the server.

                https://documentation.cpanel.net/display/SDK/WHM+API+1+Functions+-+removezonerecord

        Parameters
            zone:str - The domain name whose zone record you wish to remove.
            line:str - The line number of the zone record you wish to remove.
        Returns
            json
        """
        return self._whm_api_query('removezonerecord', {
            'zone': zone,
            'line': line
        })


    def reset_zone(self, domain=None, zone=None, user=None):
        """Reset Zone

            Resets specified zone and any associated subdomains to default settings.

                https://documentation.cpanel.net/display/SDK/WHM+API+1+Functions+-+resetzone

        Parameters
            domain:str - The domain name whose zone should be reset.
            zone:str - The DNS zone's filename.
            *user:str - The user who owns the domain name whose zone should be reset.
            **Only one of domain/zone is required.
        Returns
            json
        """
        if not domain and not zone:
            raise Exception('reset_zone() requires one of [domain,zone]')

        return self._whm_api_query('resetzone', {
            'domain': domain,
            'zone': zone,
            'user': user
        })


    def list_zone_mx_records(self, domain):
        """Get DNS MX Records

            Retrieves MX records for specified domain.

                https://documentation.cpanel.net/display/SDK/WHM+API+1+Functions+-+listmxs

        Parameters
            domain:str - The domain corresponding to the MX records that you wish to view.
        Returns
            json
        """
        return self._whm_api_query('listmxs', {
            'api.version': 1,
            'domain': domain
        })


    def add_zone_mx_record(self, domain, name, exchange, preference, mxclass=None, serialnum=None, ttl=None):
        """Add DNS MX Record

            Add an MX record to specified domain.

                https://documentation.cpanel.net/display/SDK/WHM+API+1+Functions+-+savemxs

        Parameters
            domain:str - The domain corresponding to the MX records that you wish to view.
            name:str - The name of the new MX record.
            exchange:str - The exchanger to which the domain will point. (e.g., example.com)
            preference:int - The new MX entry's preference. Lower values indicate a higher preference.
            *class:str - The MX record's class.
            *serialnum:int - The serial number of the MX record.
            *ttl:int - The new record's time to live.

        Returns
            json
        """
        return self._whm_api_query('savemxs', {
            'api.version': 1,
            'domain': domain,
            'name': name,
            'exchange': exchange,
            'preference': preference,
            'class': mxclass,
            'serialnum': serialnum,
            'ttl': ttl
        })
