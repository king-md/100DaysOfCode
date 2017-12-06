#!/usr/bin/env python3

import sys
import dns.resolver




def main():
#    print( len(sys.argv) )
#    if( 2 == len(sys.argv) ):
#        name_server = '8.8.8.8' #Google's DNS server
#        ADDITIONAL_RDCLASS = 65535
#        request = dns.message.make_query('google.com', dns.rdatatype.ANY)
#        request.flags |= dns.flags.AD
#        request.find_rrset(request.additional, dns.name.root, ADDITIONAL_RDCLASS, dns.rdatatype.OPT, create=True, force_unique=True)       
#        response = dns.query.udp(request, name_server)
#        print( "response:", response )
#        #answer=dns.resolver.query("google.com", "all")
#        #for data in answer:
#        #    print( data.strings )
#    else:
#        print( "invalid arguments." )
#
#    return


    import sys
    import socket
    import dns.resolver
    
    print( 'Argument List:', str(sys.argv) )
    site = sys.argv[1]
    dns_server = sys.argv[2]
    
    # Basic CNAME query the host's DNS
    #for rdata in dns.resolver.query(site, 'CNAME') :
    #    print( rdata.target )
    
    # Basic A query the host's DNS
    for rdata in dns.resolver.query(site, 'A') :
        print( rdata.address )
    
    # Setting an specific DNS Server
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [socket.gethostbyname(dns_server)]
    
    # Basic CNAME query with the specific DNS server
    #answer = resolver.query(site, 'CNAME');
    #for rdata in answer :
    #    print( rdata.target )
    
    # Basic A query with the specific DNS server
    answer = resolver.query(site, 'A');
    for rdata in answer :
        print( rdata.address )
    
    # Basic AAAA query with the specific DNS server
    answer = resolver.query(site, 'AAAA');
    for rdata in answer :
        print( rdata.address )
    
    # Basic TXT query with the specific DNS server
    answer = resolver.query(site, 'TXT');
    for rdata in answer :
        print( rdata.strings )

    return



main()

