"""

Python Library for WHM's API1 DNS Functions

	https://documentation.cpanel.net/display/SDK/WHM+API+1+Functions#WHMAPI1Functions-DNSfunctions

Author: Benton Snyder
Website: http://bensnyde.me
Created: 7/24/13
Revised: 1/1/15

"""
import base64
import httplib
import json
import logging
import socket

# Log handler
apilogger = "apilogger"

class Cpanel:
    def __init__(self, whm_base_url, whm_username, whm_password):
        """Constructor

            Cpanel FTP library public constructor.

        Parameters
            whm_base_url: str whm base url (ex. whm.example.com)
            whm_username: str whm root username
            whm_password: str whm password
        """
        self.whm_base_url = whm_base_url
        self.whm_username = whm_username
        self.whm_password = whm_password


    def _whm_api_query(self, query):
        """Query API

            Queries WHM server's JSON API with specified query string.

        Parameters
            query: str url safe string
        Returns
            json decoded response from remote server
        """
        try:
            conn = httplib.HTTPSConnection(self.whm_base_url, 2087)
            conn.request('GET', '/json-api/%s' % query, headers={'Authorization':'Basic ' + base64.b64encode(self.whm_username+':'+self.whm_password).decode('ascii')})
            response = conn.getresponse()
            data = json.loads(response.read())
            conn.close()

            return data
        except httplib.HTTPException as ex:
            logging.getLogger(apilogger).critical("HTTPException from CpanelDNS API: %s" % ex)
        except socket.error as ex:
            logging.getLogger(apilogger).critical("Socket.error connecting to CpanelDNS API: %s" % ex)
        except ValueError as ex:
            logging.getLogger(apilogger).critical("ValueError decoding CpanelDNS API response string: %s" % ex)
        except Exception as ex:
            logging.getLogger(apilogger).critical("Unhandled Exception while querying CpanelDNS API: %s" % ex)


    def add_zone(self, domain, ip, trueowner=None):
        """Add DNS Zone

            Creates a DNS zone.

            	https://documentation.cpanel.net/display/SDK/WHM+API+1+-+adddns

        Parameters
            domain: str domain name
            ip: str ip address
            trueowner: str cpanel username
        Returns
            result: bool api result status
        """
        querystr = 'adddns?domain=%s&ip=%s&trueowner=%s' % (domain, ip, trueowner)
        result = self._whm_api_query(querystr)

        try:
            if result["result"][0]["status"] == 1:
                return True
        except Exception as ex:
            logging.getLogger(apilogger).error('%s returned unexpected results: %s' % (querystr, ex))

        return False


    def add_zone_record(self, **kwargs):
        """Add Zone Record

        	Adds a record to the specified DNS zone.

        		https://documentation.cpanel.net/display/SDK/WHM+API+1+-+addzonerecord

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
            result: bool api result status
        """
        querystr =     'addzonerecord?'
        for name,val in kwargs.iteritems():
            querystr = querystr + "&%s=%s" % (name, val)

        result = self._whm_api_query(querystr)

        try:
            if result["result"][0]["status"] == 1:
                return True
        except Exception as ex:
            logging.getLogger(apilogger).error('%s returned unexpected results: %s' % (querystr, ex))

        return False


    def edit_zone_record(self, domain, line, *args):
        """Edit DNS Zone Record

        	Modify a DNS zone record on the server.

        		https://documentation.cpanel.net/display/SDK/WHM+API+1+-+editzonerecord

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
            result: bool api result status
        """
        querystr = 'editzonerecord?zone=%s&Line=%s' % (domain, line)
        for name,val in args:
            querystr = querystr + "&%s=%s" % (name, val)

        result = self._whm_api_query(querystr)

        try:
            if result["result"][0]["status"] == 1:
                return True
        except Exception as ex:
            logging.getLogger(apilogger).error('%s returned unexpected results: %s' % (querystr, ex))

        return False


    def add_reversed_zone_record(self, zone, name, ptrdname):
        """Add DNS PTR Record

            Add reverse PTR record to specified zone.

            	https://documentation.cpanel.net/display/SDK/WHM+API+1+-+addzonerecord+for+Reverse+DNS

        Parameters
            zone:str - The name of the reverse DNS zone file to create. This value must follow a standardized naming schema.
            name:int - You will need to enter the last octet of the IP address here. If your IP address was 192.168.0.1, you would enter 1 in this parameter.
            ptrdname:str - The name of the domain to which the IP address will resolve (e.g. example.com).
        Returns
            result: bool api result status
        """
        querystr = 'addzonerecord?zone=%s&name=%s&ptrdname=%s&type=PTR' % (zone, name, ptrdname)
        result = self._whm_api_query(querystr)

        try:
            if result["result"][0]["status"] == 1:
                return True
        except:
            logging.getLogger(apilogger).error('%s returned unexpected results: %s' % (querystr, ex))

        return False


    def get_zone_record(self, domain, line):
        """Get DNS Zone Record

            Retrieves specified record from specified zone.

            	https://documentation.cpanel.net/display/SDK/WHM+API+1+-+getzonerecord

        Parameters
            domain:str - The domain whose zone record you wish to view.
            line:str - The line you wish to view in the zone record.
        Returns
            record:
                name:str - Domain name. Example: example.com
                Line:str - The number of the zone record line retrieved by the function.
                address:str - The IP address associated with the zone record.
                class:str - The class of the record. (typically IN, for "Internet")
                raw:str - Raw line data.
                ttl:int - The record's time to live.
                type:str - The DNS record type. Example: NS, SOA, A, etc.
        """
        querystr = 'getzonerecord?domain=%s&line=%s' % (domain, lineline)
        result = self._whm_api_query(querystr)

        try:
            if result["result"][0]["status"] == 1:
                return result["result"][0]["record"]
        except Exception as ex:
            logging.getLogger(apilogger).error('%s returned unexpected results: %s' % (querystr, ex))

        return False


    def delete_zone(self, domain):
        """Delete DNS Zone

            Deletes a DNS zone.

            	https://documentation.cpanel.net/display/SDK/WHM+API+1+-+killdns

        Parameters
            domain:str - Domain name for the zone to be deleted.
        Returns
            result: bool api result status
        """
        querystr = 'killdns?domain=%s' % domain
        result = self._whm_api_query(querystr)
        logging.getLogger(apilogger).error("result: %s" % result)
        try:
            if result["result"][0]["status"] == 1:
                return True
        except Exception as ex:
            logging.getLogger(apilogger).error('%s returned unexpected results: %s' % (querystr, ex))

        return False


    def list_zones(self, cpanel_user=None):
        """List DNS zones

            Retrieves list of all domains and corresponding DNS zones associated with your server.

            	https://documentation.cpanel.net/display/SDK/WHM+API+1+-+listzones

        Parameters
            *cpanel_user: str cpanel account username to call from
        Returns
            zones:
                domain:str - Domain name. Example: example.com
                zonefile:str - Zone file name. Example: example.com.db
        """
        if cpanel_user:
            querystr = 'cpanel?cpanel_jsonapi_module=DomainLookup&cpanel_jsonapi_func=getbasedomains&cpanel_xmlapi_version=2&cpanel_jsonapi_user=%s' % cpanel_user
        else:
            querystr = 'listzones'

        result = self._whm_api_query(querystr)

        try:
            if result["cpanelresult"]["event"]["result"] == 1:
                return result["cpanelresult"]["data"]
        except Exception as ex:
            logging.getLogger(apilogger).error('%s returned unexpected results: %s' % (querystr, ex))

        return False


    def list_zone(self, domain):
        """Get DNS Zone

            Retrieves all records for specified zone.

            	https://documentation.cpanel.net/display/SDK/WHM+API+1+-+dumpzone

        Parameters
            domain:str - Domain for which to show the DNS zone. Example: example.com
        Returns
            record:
                name:str - Domain name. Example: example.com
                Line:str - Line number in the zone file.
                Lines:int - Number of lines. (only appears if more than 1 line)
                address:str - IP address. Example: 127.0.0.1
                class:str - The class of the record. (typically IN for "Internet")
                exchange:str - In an MX record, the name of the destination mail server.
                preference:int - In an MX record, the priority of the destination mail server. (0 is highest priority)
                expire:str - A 32-bit time value that specifies the upper limit on the time interval that can elapse before the zone is no longer authoritative.
                minimum:int - The unsigned 32-bit minimum TTL field that should be exported with any record from this zone.
                mname:str - The domain name of the name server that was the original or primary source of data for this zone. Example: ns1.example.com
                nsdname:str - A domain name which specifies a host which should be authoritative for the specified class and domain. Example: ns1.example.com
                cname:str - The "canonical" domain name for which the specified domain is an alias. Example: example.com
                raw:str - Raw line output.
                referesh:int - A 32-bit time interval before the zone should be refreshed.
                retry:int - A 32-bit time interval that should elapse before a failed refresh should be retried.
                rname:str - A domain name which specifies the mailbox of the person responsible for this zone. Example: user.example.com (user.example.com instead of user@example.com)
                serial:int - The unsigned 32-bit version number of the original copy of the zone.
                ttl:int - The record's time to live.
                type:str - The DNS record type. Example: NS, SOA, A, etc.
                txtdata:str - Text record data.
        """
        querystr = 'dumpzone?domain=%s' % domain
        result = self._whm_api_query(querystr)

        try:
            if result["result"][0]["status"] == 1:
                return result["result"][0]["record"]
        except Exception as ex:
            logging.getLogger(apilogger).error('%s returned unexpected results: %s' % (querystr, ex))

        return False


    def get_nameserver_ip(self, nameserver):
        """Get Nameserver IP

            Retrieve the IP address of a registered nameserver from the root nameservers.

            	https://documentation.cpanel.net/display/SDK/WHM+API+1+-+lookupnsip

        Parameters
            nameserver:str - Hostname of the nameserver whose IP address you want to obtain. Example: ns1.example.com
        Returns
            ip: str ip address
        """
        querystr = 'lookupnsip?nameserver=%s' % nameserver
        result = self._whm_api_query(querystr)

        try:
            if result["result"][0]["status"] == 1:
                return result[0]["ip"]
        except Exception as ex:
            logging.getLogger(apilogger).error('%s returned unexpected results: %s' % (querystr, ex))

        return False


    def delete_zone_record(self, zone, line):
        """Delete DNS Zone Record

            Delete a DNS zone record from the server.

            	https://documentation.cpanel.net/display/SDK/WHM+API+1+-+removezonerecord

        Parameters
            zone:str - The domain name whose zone record you wish to remove.
            line:str - The line number of the zone record you wish to remove.
        Returns
            result: bool api result status
        """
        querystr = 'removezonerecord?zone=%s&line=%s' % (zone, line)
        result = self._whm_api_query(querystr)

        try:
            if result["result"][0]["status"] == 1:
                return True
            else:
                logging.getLogger(apilogger).error(result)
        except Exception as ex:
            logging.getLogger(apilogger).error('%s returned unexpected results: %s' % (querystr, ex))

        return False


    def reset_zone(self, domain=None, zone=None, user=None):
        """Reset Zone

            Resets specified zone and any associated subdomains to default settings.

            	https://documentation.cpanel.net/display/SDK/WHM+API+1+-+resetzone

        Parameters
            domain:str - The domain name whose zone should be reset.
            zone:str - The DNS zone's filename.
            *user:str - The user who owns the domain name whose zone should be reset.
            **Only one of domain/zone is required.
        Returns
            result: bool api result status
        """
        if not domain and not zone:
            return False

        querystr = 'resetzone?'
        if domain:
            querystr = querystr + 'domain=' + domain + '&'
        if zone:
            querystr = querystr + 'zone=' + zone + '&'
        if user:
            querystr = querystr + 'user=' + user

        result = self._whm_api_query(querystr)

        try:
            if result["result"][0]["status"] == 1:
                return True
            else:
                logging.getLogger(apilogger).error(result)
        except Exception as ex:
            logging.getLogger(apilogger).error('%s returned unexpected results: %s' % (querystr, ex))

        return False


    def list_zone_mx_records(self, domain):
        """Get DNS MX Records

            Retrieves MX records for specified domain.

            	https://documentation.cpanel.net/display/SDK/WHM+API+1+-+listmxs

        Parameters
            domain:str - The domain corresponding to the MX records that you wish to view.
        Returns
            record:
                line:int - The line number of the MX record, from within the zone file.
                ttl:str - The record's time to live.
                class:str - The class of the record.
                exchange:str - The exchanger to which the domain will point. (e.g. example.com)
                preference:int - The MX record's preference value.
                type:str - The type of record you are viewing.
                name:str - The name of the record.
        """
        querystr = 'listmxs?api.version=1&domain=%s' % domain
        result = self._whm_api_query(querystr)

        try:
            if result["result"][0]["status"] == 1:
                return result["result"][0]["record"]
        except Exception as ex:
            logging.getLogger(apilogger).error('%s returned unexpected results: %s' % (querystr, ex))

        return False


    def add_zone_mx_record(self, domain, name, exchange, preference, aclass=None, serialnum=None, ttl=None):
        """Add DNS MX Record

            Add an MX record to specified domain.

            	https://documentation.cpanel.net/display/SDK/WHM+API+1+-+savemxs

        Parameters
            domain:str - The domain corresponding to the MX records that you wish to view.
            name:str - The name of the new MX record.
            exchange:str - The exchanger to which the domain will point. (e.g., example.com)
            preference:int - The new MX entry's preference. Lower values indicate a higher preference.
            *class:str - The MX record's class.
            *serialnum:int - The serial number of the MX record.
            *ttl:int - The new record's time to live.

        Returns
            result: bool api result status
        """
        querystr = 'savemxs?api.version=1&domain=%s&name=%s&exchange=%s&preference%s' % (domain, name, exchange, preference)
        result = self._whm_api_query(querystr)

        try:
            if result["result"][0]["metadata"]["result"] == 1:
                return True
        except Exception as ex:
            logging.getLogger(apilogger).error('%s returned unexpected results: %s' % (querystr, ex))

        return False
