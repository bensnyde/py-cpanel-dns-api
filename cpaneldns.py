from httplib import HTTPSConnection
from base64 import b64encode
import pprint

class CpanelDNS:
        def __init__(self, url, username, password):
                self.url = url
                self.authHeader = {'Authorization':'Basic ' + b64encode(username+':'+password).decode('ascii')}

        def cQuery(self, queryStr):
                """
                Queries specified WHM server's JSON API with specified query string.

                Arguments
                ---
                queryStr:str - HTTP GET formatted query string.

                Returns JSON response from server
                """
                conn = HTTPSConnection(self.url, 2087)
                conn.request('GET', '/json-api/'+queryStr, headers=self.authHeader)
                response = conn.getresponse()
                data = response.read()
                conn.close()
                return data

        def addZone(self, domain, ip, trueowner=None):
                """
                This function creates a DNS zone. All zone information other than domain name and IP address
                is created based on the standard zone template in WHM.

                Arguments
                ---
                domain:str - Domain name for the zone that will be added.
                ip:str - IP address associated with the domain name.
                trueowner:str - The username that will own the DNS zone.

                Returns JSON
                ---
                adddns
                -result
                --status:bool - Status of the deletion request.
                --statusmsg:str - Information about the status of the request.
                """
                return self.cQuery('adddns?domain='+domain+'&ip='+ip+'&trueowner='+trueowner)

        #FINISH ME
        def addZoneRecord(self, zone, *args):
                """
                This function will add a DNS zone record to the server.

                Arguments
                ---
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

                Returns JSON
                ---
                addzonerecord
                -result
                --status:bool - Status of the request.
                --statusmsg:str - Additional information from the server about the addition of the DNS zone.
                """
                querystr =      'addzonerecord?zone='+zone+'&'
                for name,val in args:
                        querystr = querystr + name + '=' + val + '&'
                return cQuery(querystr)

        # FINISH ME
        def editZoneRecord(self, domain, line, *args):
                """
                This function allows you to edit a DNS zone record on the server.

                Arguments
                ---
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

                Returns JSON
                ---
                editzonerecord
                -result
                --status:bool - Status of the request.
                --statusmsg:str - Message about the result of the function.
                """
                querystr =      'editzonerecord?zone='+zone+'&Line='+line+'&'
                for name,val in args:
                        querystr = querystr + name + '=' + val + '&'
                return cQuery(querystr)

        def addReverseZoneRecord(self, zone, name, ptrdname):
                """
                The addzonerecord function allows you to add reverse DNS functionality using PTR records.
                PTR records are used in reverse DNS lookups that convert IP addresses into domain names.

                Arguments
                ---
                zone:str - The name of the reverse DNS zone file to create. This value must follow a standardized naming schema.
                name:int - You will need to enter the last octet of the IP address here. If your IP address was 192.168.0.1, you would enter 1 in this parameter.
                ptrdname:str - The name of the domain to which the IP address will resolve (e.g. example.com).

                Returns JSON
                ---
                addzonerecord
                -result
                --status:bool - Status of the request.
                --statusmsg:str - Additional information from the server about the addition of the DNS zone.
                """
                return self.cQuery('addzonerecord?zone='+zone+'&name='+name+'&ptrdname='+ptrdname+'&type=PTR')

        def getZoneRecord(self, domain, line):
                """
                This function will return zone records for a domain.

                Arguments
                ---
                domain:str - The domain whose zone record you wish to view.
                line:str - The line you wish to view in the zone record.

                Returns JSON
                ---
                getzonerecord
                -result
                --record
                ---name:str - Domain name. Example: example.com
                ---Line:str - The number of the zone record line retrieved by the function.
                ---address:str - The IP address associated with the zone record.
                ---class:str - The class of the record. (typically IN, for "Internet")
                ---raw:str - Raw line data.
                ---ttl:int - The record's time to live.
                ---type:str - The DNS record type. Example: NS, SOA, A, etc.
                --status:bool - Result of the function.
                --statusmsg:str - Message about the result of the function.
                """
                return self.cQuery('getzonerecord?domain='+domain+'&line='+line)

        def deleteZone(self, domain):
                """
                This function deletes a DNS zone.

                Arguments
                ---
                domain:str - Domain name for the zone to be deleted.

                Returns JSON
                ---
                killdns
                -result
                --rawout:html - Raw output in HTML.
                --status:bool - Status of the deletion request.
                --statusmsg:str - Information about the status of the request.
                """
                return self.cQuery('killdns?domain='+domain)

        def listZones(self):
                """
                This function will generate a list of all domains and corresponding DNS zones associated with your server.

                Returns JSON
                ---
                listzones
                -zone
                --domain:str - Domain name. Example: example.com
                --zonefile:str - Zone file name. Example: example.com.db
                """
                return self.cQuery('listzones')

        def listZone(self, domain):
                """
                This function displays the DNS zone configuration for a specific domain.

                Arguments
                ---
                domain:str - Domain for which to show the DNS zone. Example: example.com

                Returns JSON
                ---
                dumpzone
                -result
                --status:bool - Status of the display request.
                --statusmsg:str - Information about the status of the request.
                --record
                ---name:str - Domain name. Example: example.com
                ---Line:str - Line number in the zone file.
                ---Lines:int - Number of lines. (only appears if more than 1 line)
                ---address:str - IP address. Example: 127.0.0.1
                ---class:str - The class of the record. (typically IN for "Internet")
                ---exchange:str - In an MX record, the name of the destination mail server.
                ---preference:int - In an MX record, the priority of the destination mail server. (0 is highest priority)
                ---expire:str - A 32-bit time value that specifies the upper limit on the time interval that can elapse before the zone is no longer authoritative.
                ---minimum:int - The unsigned 32-bit minimum TTL field that should be exported with any record from this zone.
                ---mname:str - The domain name of the name server that was the original or primary source of data for this zone. Example: ns1.example.com
                ---nsdname:str - A domain name which specifies a host which should be authoritative for the specified class and domain. Example: ns1.example.com
                ---cname:str - The "canonical" domain name for which the specified domain is an alias. Example: example.com
                ---raw:str - Raw line output.
                ---referesh:int - A 32-bit time interval before the zone should be refreshed.
                ---retry:int - A 32-bit time interval that should elapse before a failed refresh should be retried.
                ---rname:str - A domain name which specifies the mailbox of the person responsible for this zone. Example: user.example.com (user.example.com instead of user@example.com)
                ---serial:int - The unsigned 32-bit version number of the original copy of the zone.
                ---ttl:int - The record's time to live.
                ---type:str - The DNS record type. Example: NS, SOA, A, etc.
                ---txtdata:str - Text record data.
                """
                return self.cQuery('dumpzone?domain='+domain)

        def getNameserverIP(self, nameserver):
                """
                This function obtains the IP address of a registered nameserver from the root nameservers.

                Arguments
                ---
                nameserver:str - Hostname of the nameserver whose IP address you want to obtain. Example: ns1.example.com

                Returns JSON
                ---
                lookupnsip
                -ip:str - IP address of the nameserver.
                """
                return self.cQuery('lookupnsip?nameserver='+nameserver)

        def deleteZoneRecord(self, zone, line):
                """
                This function allows you to remove a DNS zone record from the server.

                Arguments
                ---
                zone:str - The domain name whose zone record you wish to remove.
                line:str - The line number of the zone record you wish to remove.

                Returns JSON
                ---
                removezonerecord
                -result
                --status:bool - Whether the call was successful.
                --statusmsg:str - Message about the result of the function.
                """
                return self.cQuery('removezonerecord?zone='+zone+'&line='+line)

        def resetZone(self, domain=None, zone=None, user=None):
                """
                You can use this function to restore a DNS zone to its default values. This includes
                any subdomain DNS records associated with the domain.

                Arguments
                ---
                domain:str - The domain name whose zone should be reset.
                zone:str - The DNS zone's filename.
                *user:str - The user who owns the domain name whose zone should be reset.
                **Only one of domain/zone is required.

                Returns JSON
                ---
                resetzone
                -result
                --status:bool - Whether the call was successful.
                --statusmsg:str - Status or error message about the setresellernameservers function call.
                """
                if domain is None and zone is None:
                        return false

                query = 'resetzone?'
                if domain:
                        query = query + 'domain=' + domain + '&'
                if zone:
                        query = query + 'zone=' + zone + '&'
                if user:
                        query = query + 'user=' + user

                return cQuery(query)

        def resolveDomainToIP(self, domain):
                """
                This function will attempt to resolve an IP address for a specified domain name.

                Arguments
                ---
                domain:str - The domain whose IP address should be resolved.

                Returns JSON
                ---
                result
                -data
                --record
                ---ip:str - The IP address for the domain, if it resolved.
                -metadata
                --result:bool - A boolean value that indicates success or failure.
                --reason:str - A string value that contains a message of success or a reason for failure.
                --version:int - The XML API version number, 1 in this case.
                --command:str - The function that was just called. In this case, resolvedomainname.
                """
                return self.cQuery('resolvedomainname?api.version=1&domain='+domain)

        def listZoneMXRecords(self, domain):
                """
                This function will list a specified domain's MX records.

                Arguments
                ---
                domain:str - The domain corresponding to the MX records that you wish to view.

                Returns JSON
                ---
                result
                -data
                --record
                ---line:int - The line number of the MX record, from within the zone file.
                ---ttl:str - The record's time to live.
                ---class:str - The class of the record.
                ---exchange:str - The exchanger to which the domain will point. (e.g. example.com)
                ---preference:int - The MX record's preference value.
                ---type:str - The type of record you are viewing.
                ---name:str - The name of the record.
                -metadata
                --result:bool - A boolean value that indicates success or failure.
                --reason:str - A string value that contains a message of success or a reason for failure.
                --version:int - The XML API version number, 1 in this case.
                --command:str - The function that has just run, listmxs in this case.
                """
                return self.cQuery('listmxs?api.version=1&domain='+domain)

        def addZoneMXRecord(self, domain, name, exchange, preference, aclass=None, serialnum=None, ttl=None):
                """
                This function will add an MX record.

                Arguments
                ---
                domain:str - The domain corresponding to the MX records that you wish to view.
                name:str - The name of the new MX record.
                exchange:str - The exchanger to which the domain will point. (e.g., example.com)
                preference:int - The new MX entry's preference. Lower values indicate a higher preference.
                *class:str - The MX record's class.
                *serialnum:int - The serial number of the MX record.
                *ttl:int - The new record's time to live.

                Returns JSON
                ---
                result
                -metadata
                --result:bool - A boolean value that indicates success or failure.
                --reason:str - A string value that contains a message of success or a reason for failure.
                --version:int - The XML API version number, 1 in this case.
                --command:str - The function that has just run, savemxs in this case.
                """
                return self.Cquery('savemxs?api.version=1&domain='+domain+'&name='+name+'&exchange='+exchange+'&preference'+preference)
