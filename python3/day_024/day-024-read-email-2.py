#!/usr/bin/env python3

import re



class EmailRFC822:
    ''' an RFC-822 email '''

    def __init__( self ):
        self.indexEndOfHeaders = None
        self.emailRFC822 = None
        self.emailRFC822Headers = None
        self.emailRFC822Body = None
        self.emailFileObject  = None
        self.emailRFC822LineCount = 0
        return


    def readEmailFile( self, emailFilepath ):
        ''' read the lines of an email file into a list '''
        self.indexEndOfHeaders = -1
        self.emailRFC822Lines = list()
        self.emailFileObject  = open( emailFilepath, "r" )
        currentLine = 0
        for line in self.emailFileObject:
            line = line.rstrip('\r\n')
            if( 0 == len(line) ):
                self.indexEndOfHeaders = currentLine
            self.emailRFC822Lines.append( line )
            currentLine+=1
        self.emailRFC822LineCount = currentLine
        self.emailRFC822Headers = self.RFC822Headers( self.emailRFC822Lines, self.indexEndOfHeaders )
        self.emailRFC822Body = self.RFC822Body( self.emailRFC822Lines, self.indexEndOfHeaders, self.emailRFC822Headers )
        return( True )

    def RFC822Headers( self, emailRFC822Lines, indexEndOfHeaders ):
        emailRFC822HeadersObj = RFC822HeaderBlock()
        emailRFC822HeadersObj.parseHeaders( emailRFC822Lines, indexEndOfHeaders )
        return emailRFC822HeadersObj

    def RFC822Body( self, emailRFC822, indexEndOfHeaders, emailRFC822Headers ):
        emailRFC822BodyObj = RFC822BodyBlock()
        return emailRFC822BodyObj



class RFC822HeaderBlock:
    ''' a block of headers of an RFC-822 email. '''

    def __init__( self ):
        self.theRFC822Headers = list()
        return

    def parseHeaders( self, rawRFC822HeadersLines, endIndex ):
        if( 0 == len(rawRFC822HeadersLines[0]) or
            rawRFC822HeadersLines[0].startswith( " ", 0, len(" ") ) or
            rawRFC822HeadersLines[0].startswith( "	", 0, len("	") ) ):
            # The .eml file begins with a blank line or an indented line; this is an ERROR
            return False

        currentLine = -1
        for line in rawRFC822HeadersLines:
            currentLine += 1
            if( endIndex == currentLine ):
                # we've reached the index denoting the end of the RFC-822 headers
                self.theRFC822Headers[len(self.theRFC822Headers)-1].parse()
                break
            if( re.match( "^[a-zA-Z\-]+[ $]+", line ) ):
                # found a line consistent with lines added for file storage purposes (e.g., "^From ..."); ignore it.
                continue
            if( line.startswith( " " ) or
                line.startswith( "	" ) ):
                self.theRFC822Headers[len(self.theRFC822Headers)-1].appendHeaderLine(line)
                continue
            if( re.match( "^[a-zA-Z\-]+:", line ) ):
                # we've found the first line of a new header; parse the contents of the previous header before continuing
                print( "DEBUG: currentLine="+str(currentLine)+" len(self.theRFC822Headers)="+str(len(self.theRFC822Headers)) )
                print( "DEBUG: line="+line[:10]+"..." )
                if( 0 < len(self.theRFC822Headers) ):
                    self.theRFC822Headers[len(self.theRFC822Headers)-1].parse()

            if( line.startswith( "Received: " ) ):
                newHeaderObj = RFC822ReceivedHeader()
                newHeaderObj.appendHeaderLine(line)
                self.theRFC822Headers.append(newHeaderObj)
            elif( line.startswith( "From: " ) ):
                newHeaderObj = RFC822FromHeader()
                newHeaderObj.appendHeaderLine(line)
                self.theRFC822Headers.append(newHeaderObj)
            elif( line.startswith( "To: " ) ):
                newHeaderObj = RFC822ToHeader()
                newHeaderObj.appendHeaderLine(line)
                self.theRFC822Headers.append(newHeaderObj)
            elif( line.startswith( "Cc: " ) ):
                newHeaderObj = RFC822CCHeader()
                newHeaderObj.appendHeaderLine(line)
                self.theRFC822Headers.append(newHeaderObj)
            elif( line.startswith( "Bcc: " ) ):
                newHeaderObj = RFC822BCCHeader()
                newHeaderObj.appendHeaderLine(line)
                self.theRFC822Headers.append(newHeaderObj)
            elif( line.startswith( "Sender: " ) ):
                newHeaderObj = RFC822SenderHeader()
                newHeaderObj.appendHeaderLine(line)
                self.theRFC822Headers.append(newHeaderObj)
            elif( line.startswith( "Reply-To: " ) ):
                newHeaderObj = RFC822ReplyToHeader()
                newHeaderObj.appendHeaderLine(line)
                self.theRFC822Headers.append(newHeaderObj)
            elif( line.startswith( "Date: " ) ):
                newHeaderObj = RFC822DateHeader()
                newHeaderObj.appendHeaderLine(line)
                self.theRFC822Headers.append(newHeaderObj)
            elif( line.startswith( "Subject: " ) ):
                newHeaderObj = RFC822SubjectHeader()
                newHeaderObj.appendHeaderLine(line)
                self.theRFC822Headers.append(newHeaderObj)
            elif( line.startswith( "Message-ID: " ) ):
                newHeaderObj = RFC822MessageIDHeader()
                newHeaderObj.appendHeaderLine(line)
                self.theRFC822Headers.append(newHeaderObj)
            elif( line.startswith( "Content-Type: " ) ):
                print( "DEBUG: Found a Content-Type header:", line )
                newHeaderObj = RFC822ContentTypeHeader()
                newHeaderObj.appendHeaderLine(line)
                self.theRFC822Headers.append(newHeaderObj)
            elif( line.startswith( "Content-Transfer-Encoding: " ) ):
                newHeaderObj = RFC822ContentTransferEncodingHeader()
                newHeaderObj.appendHeaderLine(line)
                self.theRFC822Headers.append(newHeaderObj)
            elif( line.startswith( "Delivered-To: " ) ):
                newHeaderObj = RFC822DeliveredToHeader()
                newHeaderObj.appendHeaderLine(line)
                self.theRFC822Headers.append(newHeaderObj)
            elif( line.startswith( "MIME-Version: " ) ):
                newHeaderObj = RFC822MimeVersionHeader()
                newHeaderObj.appendHeaderLine(line)
                self.theRFC822Headers.append(newHeaderObj)
            else:
                newHeaderObj = Header()
                newHeaderObj.appendHeaderLine(line)
                self.theRFC822Headers.append(newHeaderObj)

        return



class Header:
    def __init__(self):
        self.headers = []
        self.headerType = None

    def __str__(self):
        return self.getFullHeader()

    def __len__(self):
        return len(headers)

    def appendHeaderLine(self, line):
        self.headers.append(line)
        self.headers[len(self.headers)-1] = self.headers[len(self.headers)-1].rstrip("\r\n")

    def getFullHeader(self):
        strHeader = ""
        #strHeader += "DEBUG-Header-Type:"
        #strHeader += "None" if None == self.headerType else self.headerType
        #strHeader += "///"
        for line in self.headers:
            strHeader += line
            strHeader += "\n"
        return strHeader

    def parse(self):
        print( "self:",self)
        self.headerKey = " ".join(self.headers).split(":",1)[0].rstrip(":")
        print( "self.headers:",self.headers)
        self.headerValue = " ".join(self.headers).split(":",1)[1].strip()
        return



# Received: from
# the name the sending computer gave for itself (the name associated with that computer's IP address [its IP address])
# by
# the receiving computer's name (the software that computer uses) (usually Sendmail, qmail or Postfix)
# with protocol (usually SMTP, ESMTP or ESMTPS)
# id id assigned by local computer for logging;
# timestamp (usually given in the computer's localtime; see below for how you can convert these all to your time)

class RFC822ReceivedHeader(Header):
    def __init__(self):
        super().__init__()
        self.headerType = "RECEIVED"
        self.receivedFromSelfIdent = None
        self.receivedFromFQDN = None
        self.receivedFromIP = None
        self.receivedByFQDN = None
        self.receivedByIP = None
        self.receivedBySoftware = None
        self.receivedByProtocol = None
        self.receivedByID = None
        self.receivedTimestampStr = None
        self.receivedTimestampUTC = None
        self.EnvelopeFrom = None
        self.EnvelopeTo = None
        self.misc = None

    def parse(self):
        # First set the key & full value
        self.headerKey = " ".join(self.headers).split(":",1)[0].rstrip(":")
        self.headerValue = " ".join(self.headers).split(":",1)[1].strip()



        # Sample received header formats observed (note: not all MTAs follow a stander - if a standard exists):
        #   R: by <IP Addr> with <protocol>; <timestamp>
        #   R: from <fqdn> ([<IP Addr>]) by <FQDN> ([<IP Addr>]) (<MTA Ident String>) with <protocol> id <string>; <timestamp>
        #   R: from <fqdn> ([<IP Addr>]) by <FQDN> ([<IP Addr>]) (<MTA Ident String>) with <protocol> (<TLS Version, Cipher, Bitsize>) id <string>; <timestamp>
        #   R: from <fqdn> (<IP Addr>) id <string> for \<<email addr>\>; <timestamp> (envelope-from \<<email addr>\>)
        #   R: from <fqdn> (<fqdn> [<IP Addr>]) by <FQDN> (<MTA Ident String>) with <protocol> id <string> for \<<email addr>\>; <timestamp>
        # R: from <fqdn> ([<IP Addr>] <helo key/value string>) by <fqdn> with <protocol> (<MTA Ident String>) (envelope-from <email addr>) id <string>; <timestamp>
        # R: from [<IP Addr] (<port key/value> <helo key/value>) by <fqdn> with <protocol> (<TLS Version, Cipher, Bitsize>) (<MTA Ident String>) (envelope-from <email addr>) id <string>; <timestamp>
        # Key points and possible regex:
        #   from <fqdn>
        #   from <fqdn> ([<IP Addr>] <helo key/value string>)
        #   from <fqdn> [<IP Addr>] (<port key/value string> <helo key/value string>)
        #   from <fqdn> ([<IP Addr>])
        #   from <IP Addr>
        #     "\b(from)\s"(\s(\(?\[?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\]?\)?)|\s(localhost)|\s([a-zA-Z0-9-]+\.([a-zA-Z0-9-]+)+))(\(?((helo|port)=(\d+|[^)]+)){1,2}\))?"
        #   by <IP Addr> optionally followed by (<MTA Ident String>)
        #   by <FQDN> ([<IP Addr>]) optionally followed by (<MTA Ident String>)
        #   by <FQDN> (<MTA Ident String>) optionally followed by (<MTA Ident String>)
        #     "\b(by)\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\)|\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\]|\(\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\]\)|[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*)(\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\])?(?:\s+(\([^)]+\)))?"
        #   with <protocol> optionally followed by (<TLS Version, Cipher, Bitsize>) or (<MTA Ident String>) or both
        #     "\b(with)\s(Microsoft SMTP Server|(?:[a-zA-Z]*\s)?(?:[eE]?[Ss][Mm][Tt][Pp](?:[AaSs]{0,2})))((?:\s\([^)]+\))?(?:\s\([^)]+\))?)"
        #   id <string>
        #     "\b(id)\s([a-zA-Z0-9\.-]+)\b"
        #   ; <timestamp> optionally followed by (envelope-from \<<email addr>\>)
        #     ";\s((?:Mon(?:)?|Tue(?:s)?|Wed(?:nes)?|Thu(?:r?s?)|Fri(?:)?|Sat(?:ur)?|Sun(?:)?)(?:day)?),\s(\d{1,2})\s(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May(?:)?|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s(20\d{2})\s(?:(\d{2}:\d{2}:\d{2}(?:\.\d+)?)(\s[-\+]?\d{4})?(\s\([A-Z]{3}\))?)"
        #   for \<<email addr>\>
        #     "(for)\s(((?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*"))@((?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])))"
        # 
        # 
        # 
        # Figure out which items seem to be present in the header and set a check flag for validation after parsing:
        #   "from"
        m = re.match( """\b(from)\b""", self.headerValue )
        if( m is not None):
            mGroups = m.captures(1)
            fromStrPresent = True if mGroups[0] == None else False

        #   "id"
        m = re.match( """\b(id)\b""", self.headerValue )
        if( m is not None):
            mGroups = m.captures(1)
            idStrPresent = True if mGroups[0] == None else False

        #   "for"
        m = re.match( """\b(for)\b""", self.headerValue )
        if( m is not None):
            mGroups = m.captures(1)
            forStrPresent = True if mGroups[0] == None else False

        #   "by"
        m = re.match( """\b(by)\b""", self.headerValue )
        if( m is not None):
            mGroups = m.captures(1)
            byStrPresent = True if mGroups[0] == None else False

        #   "with"
        m = re.match( """\b(with)\b""", self.headerValue )
        if( m is not None):
            mGroups = m.captures(1)
            withStrPresent = True if mGroups[0] == None else False

        #   "TLS"
        m = re.match( """\b(TLS)\b""", self.headerValue )
        if( m is not None):
            mGroups = m.captures(1)
            tlsStrPresent = True if mGroups[0] == None else False

        #   "version"
        m = re.match( """\b(version)\b""", self.headerValue )
        if( m is not None):
            mGroups = m.captures(1)
            versionStrPresent = True if mGroups[0] == None else False

        #   "cipher"
        m = re.match( """\b(cipher)\b""", self.headerValue )
        if( m is not None):
            mGroups = m.captures(1)
            cipherStrPresent = True if mGroups[0] == None else False

        #   "bits"
        m = re.match( """\b(bits)\b""", self.headerValue )
        if( m is not None):
            mGroups = m.captures(1)
            bitsStrPresent = True if mGroups[0] == None else False

        #   "envelope-from"
        m = re.match( """\b(envelope-from)\b""", self.headerValue )
        if( m is not None):
            mGroups = m.captures(1)
            envelopeFromStrPresent = True if mGroups[0] == None else False

        #   "envelope-to"mber
        m = re.match( """\b(envelope-to)\b""", self.headerValue )
        if( m is not None):
            mGroups = m.captures(1)
            envelopeToStrPresent = True if mGroups[0] == None else False


        # then tease out the pieces of the received header from the value part
        #   "from" - and optional helo name and port nu
        m = re.match( """\b(from)\s"(\s(\(?\[?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\]?\)?)|\s(localhost)|\s([a-zA-Z0-9-]+\.([a-zA-Z0-9-]+)+))(\(?((helo|port)=(\d+|[^)]+)){1,2}\))?""", self.headerValue )
        if( m is not None):
            mGroups = m.captures(1)
            fromStr = mGroups[0]
            beta = mGroups[1]
            charlie = mGroups[2]
        # ZYZZX - need to figure out what the group matches are and possibly tweak the regex to give sonsistent group #s, and maybe set some groups to not produce a match group
        self.receivedFromSelfIdent = None
        self.receivedFromFQDN = None
        self.receivedFromIP = None
        self.receivedByFQDN = None
        self.receivedByIP = None
        self.receivedBySoftware = None
        self.receivedByProtocol = None
        self.receivedByID = None
        self.receivedTimestampStr = None
        self.receivedTimestampUTC = None
        self.EnvelopeFrom = None
        self.EnvelopeTo = None
        self.misc = None



# # From: tokens [822]
class RFC822FromHeader(Header):
    def __init__(self):
        super().__init__()
        self.headerType = "FROM"
        self.addressList = None

    def parse(self):
        self.addressList = None



# To: tokens [822]
class RFC822ToHeader(Header):
    def __init__(self):
        super().__init__()
        self.headerType = "TO"
        self.addressList = None

    def parse(self):
        self.addressList = None



# # Cc: tokens [822]
# class CCHeader(Header):
#     def __init__(self):
#         super().__init__()
#         self.headerType = "CC"
#         self.addressList = None
# 
#     def parse(self):
#         self.addressList = None
# 
# 
# 
# # Bcc: user tokens [822]
# class BCCHeader(Header):
#     def __init__(self):
#         super().__init__()
#         self.headerType = "BCC"
#         self.addressList = None
# 
#     def parse(self):
#         self.addressList = None
# 
# 
# 
# # Sender: tokens [822]
# class SenderHeader(Header):
#     def __init__(self):
#         super().__init__()
#         self.headerType = "SENDER"
#         self.addressList = None
# 
#     def parse(self):
#         self.addressList = None
# 
# 
# 
# # Reply-To: tokens [822]
# class ReplyToHeader(Header):
#     def __init__(self):
#         super().__init__()
#         self.headerType = "REPLYTO"
#         self.addressList = None
# 
#     def parse(self):
#         self.addressList = None
# 
# 
# 
# Date: tokens [822]
class RFC822DateHeader(Header):
    def __init__(self):
        super().__init__()
        self.headerType = "DATE"

    def parse(self):
        self.dateStr = None



# Subject: [822]
class RFC822SubjectHeader(Header):
    def __init__(self):
        super().__init__()
        self.headerType = "SUBJECT"

    def parse(self):
        self.subjectStr = None



# Message-ID: tokens [822]
class RFC822MessageIDHeader(Header):
    def __init__(self):
        super().__init__()
        self.headerType = "MESSAGEID"

    def parse(self):
        self.messageIDStr = None



# Content-Type:
# Base Types:
#   Content-Type: application
#   Content-Type: audio
#   Content-Type: chemical
#   Content-Type: image
#   Content-Type: message
#   Content-Type: model
#   Content-Type: multipart
#   Content-Type: text
#   Content-Type: video
#   Content-Type: x-conference
# Examples:
#   Content-Type: application/andrew-inset
#   Content-Type: application/applixware
#   Content-Type: application/atomcat+xml
#   Content-Type: application/atomsvc+xml
#   Content-Type: application/atom+xml
#   Content-Type: application/cals-1840
#   Content-Type: application/ccxml+xml,
#   Content-Type: application/cdmi-capability
#   Content-Type: application/cdmi-container
#   Content-Type: application/cdmi-domain
#   Content-Type: application/cdmi-object
#   Content-Type: application/cdmi-queue
#   Content-Type: application/cu-seeme
#   Content-Type: application/davmount+xml
#   Content-Type: application/dssc+der
#   Content-Type: application/dssc+xml
#   Content-Type: application/ecmascript
#   Content-Type: application/emma+xml
#   Content-Type: application/epub+zip
#   Content-Type: application/exi
#   Content-Type: application/font-tdpfr
#   Content-Type: application/hyperstudio
#   Content-Type: application/ipfix
#   Content-Type: application/java-archive
#   Content-Type: application/javascript
#   Content-Type: application/java-serialized-object
#   Content-Type: application/java-vm
#   Content-Type: application/json
#   Content-Type: application/mac-binhex40
#   Content-Type: application/mac-compactpro
#   Content-Type: application/mads+xml
#   Content-Type: application/marc
#   Content-Type: application/marcxml+xml
#   Content-Type: application/mathematica
#   Content-Type: application/mathml+xml
#   Content-Type: application/mbox
#   Content-Type: application/mediaservercontrol+xml
#   Content-Type: application/metalink4+xml
#   Content-Type: application/mets+xml
#   Content-Type: application/mods+xml
#   Content-Type: application/mp21
#   Content-Type: application/mp4
#   Content-Type: application/msword
#   Content-Type: application/mxf
#   Content-Type: application/news-message-id
#   Content-Type: application/news-transmission
#   Content-Type: application/octet-stream
#   Content-Type: application/octet-stream;
#   Content-Type: application/octet-stream; name="Resume.pdf"
#   Content-Type: application/oda
#   Content-Type: application/oebps-package+xml
#   Content-Type: application/ogg
#   Content-Type: application/onenote
#   Content-Type: application/patch-ops-error+xml
#   Content-Type: application/pdf
#   Content-Type: application/pdf; name=RSAC17InvoiceReceipt.pdf
#   Content-Type: application/pgp-encrypted
#   Content-Type: application/pgp-keys
#   Content-Type: application/pgp-signature
#   Content-Type: application/pics-rules
#   Content-Type: application/pkcs10
#   Content-Type: application/pkcs7-mime
#   Content-Type: application/pkcs7-MIME
#   Content-Type: application/pkcs7-signature
#   Content-Type: application/pkcs8
#   Content-Type: application/pkix-attr-cert
#   Content-Type: application/pkix-cert
#   Content-Type: application/pkixcmp
#   Content-Type: application/pkix-crl
#   Content-Type: application/pkix-pkipath
#   Content-Type: application/pls+xml
#   Content-Type: application/postscript
#   Content-Type: application/prs.cww
#   Content-Type: application/pskc+xml
#   Content-Type: application/rdf+xml
#   Content-Type: application/reginfo+xml
#   Content-Type: application/relax-ng-compact-syntax
#   Content-Type: application/remote-printing
#   Content-Type: application/resource-lists-diff+xml
#   Content-Type: application/resource-lists+xml
#   Content-Type: application/rls-services+xml
#   Content-Type: application/rsd+xml
#   Content-Type: application/rss+xml
#   Content-Type: application/rtf
#   Content-Type: application/sbml+xml
#   Content-Type: application/scvp-cv-request
#   Content-Type: application/scvp-cv-response
#   Content-Type: application/scvp-vp-request
#   Content-Type: application/scvp-vp-response
#   Content-Type: application/sdp
#   Content-Type: application/set-payment-initiation
#   Content-Type: application/set-registration-initiation
#   Content-Type: application/sgml
#   Content-Type: application/shf+xml
#   Content-Type: application/smil+xml
#   Content-Type: application/sparql-query
#   Content-Type: application/sparql-results+xml
#   Content-Type: application/srgs
#   Content-Type: application/srgs+xml
#   Content-Type: application/sru+xml
#   Content-Type: application/ssml+xml
#   Content-Type: application/tei+xml
#   Content-Type: application/thraud+xml
#   Content-Type: application/timestamped-data
#   Content-Type: application/vnd.3gpp2.tcap
#   Content-Type: application/vnd.3gpp.pic-bw-large
#   Content-Type: application/vnd.3gpp.pic-bw-small
#   Content-Type: application/vnd.3gpp.pic-bw-var
#   Content-Type: application/vnd.3m.post-it-notes
#   Content-Type: application/vnd.accpac.simply.aso
#   Content-Type: application/vnd.accpac.simply.imp
#   Content-Type: application/vnd.acucobol
#   Content-Type: application/vnd.acucorp
#   Content-Type: application/vnd.adobe.air-application-installer-package+zip
#   Content-Type: application/vnd.adobe.fxp
#   Content-Type: application/vnd.adobe.xdp+xml
#   Content-Type: application/vnd.adobe.xfdf
#   Content-Type: application/vnd.ahead.space
#   Content-Type: application/vnd.airzip.filesecure.azf
#   Content-Type: application/vnd.airzip.filesecure.azs
#   Content-Type: application/vnd.amazon.ebook
#   Content-Type: application/vnd.americandynamics.acc
#   Content-Type: application/vnd.amiga.ami
#   Content-Type: application/vnd.android.package-archive
#   Content-Type: application/vnd.anser-web-certificate-issue-initiation
#   Content-Type: application/vnd.anser-web-funds-transfer-initiation
#   Content-Type: application/vnd.antix.game-component
#   Content-Type: application/vnd.apple.installer+xml
#   Content-Type: application/vnd.apple.mpegurl
#   Content-Type: application/vnd.aristanetworks.swi
#   Content-Type: application/vnd.audiograph
#   Content-Type: application/vnd.blueice.multipass
#   Content-Type: application/vnd.bmi
#   Content-Type: application/vnd.businessobjects
#   Content-Type: application/vnd.chemdraw+xml
#   Content-Type: application/vnd.chipnuts.karaoke-mmd
#   Content-Type: application/vnd.cinderella
#   Content-Type: application/vnd.claymore
#   Content-Type: application/vnd.cloanto.rp9
#   Content-Type: application/vnd.clonk.c4group
#   Content-Type: application/vnd.cluetrust.cartomobile-config
#   Content-Type: application/vnd.cluetrust.cartomobile-config-pkg
#   Content-Type: application/vnd.commonspace
#   Content-Type: application/vnd.contact.cmsg
#   Content-Type: application/vnd.cosmocaller
#   Content-Type: application/vnd.crick.clicker
#   Content-Type: application/vnd.crick.clicker.keyboard
#   Content-Type: application/vnd.crick.clicker.palette
#   Content-Type: application/vnd.crick.clicker.template
#   Content-Type: application/vnd.crick.clicker.wordbank
#   Content-Type: application/vnd.criticaltools.wbs+xml
#   Content-Type: application/vnd.ctc-posml
#   Content-Type: application/vnd.cups-ppd
#   Content-Type: application/vnd.curl.car
#   Content-Type: application/vnd.curl.pcurl
#   Content-Type: application/vnd.data-vision.rdz
#   Content-Type: application/vnd.denovo.fcselayout-link
#   Content-Type: application/vnd.dna
#   Content-Type: application/vnd.dolby.mlp
#   Content-Type: application/vnd.dpgraph
#   Content-Type: application/vnd.dreamfactory
#   Content-Type: application/vnd.dvb.ait
#   Content-Type: application/vnd.dvb.service
#   Content-Type: application/vnd.dynageo
#   Content-Type: application/vnd.ecowin.chart
#   Content-Type: application/vnd.enliven
#   Content-Type: application/vnd.epson.esf
#   Content-Type: application/vnd.epson.msf
#   Content-Type: application/vnd.epson.quickanime
#   Content-Type: application/vnd.epson.salt
#   Content-Type: application/vnd.epson.ssf
#   Content-Type: application/vnd.eszigno3+xml
#   Content-Type: application/vnd.ezpix-album
#   Content-Type: application/vnd.ezpix-package
#   Content-Type: application/vnd.fdf
#   Content-Type: application/vnd.fdsn.seed
#   Content-Type: application/vnd.flographit
#   Content-Type: application/vnd.fluxtime.clip
#   Content-Type: application/vnd.framemaker
#   Content-Type: application/vnd.frogans.fnc
#   Content-Type: application/vnd.frogans.ltf
#   Content-Type: application/vnd.fsc.weblaunch
#   Content-Type: application/vnd.fujitsu.oasys
#   Content-Type: application/vnd.fujitsu.oasys2
#   Content-Type: application/vnd.fujitsu.oasys3
#   Content-Type: application/vnd.fujitsu.oasysgp
#   Content-Type: application/vnd.fujitsu.oasysprs
#   Content-Type: application/vnd.fujixerox.ddd
#   Content-Type: application/vnd.fujixerox.docuworks
#   Content-Type: application/vnd.fujixerox.docuworks.binder
#   Content-Type: application/vnd.fuzzysheet
#   Content-Type: application/vnd.genomatix.tuxedo
#   Content-Type: application/vnd.geogebra.file
#   Content-Type: application/vnd.geogebra.tool
#   Content-Type: application/vnd.geometry-explorer
#   Content-Type: application/vnd.geonext
#   Content-Type: application/vnd.geoplan
#   Content-Type: application/vnd.geospace
#   Content-Type: application/vnd.gmx
#   Content-Type: application/vnd.google-earth.kml+xml
#   Content-Type: application/vnd.google-earth.kmz
#   Content-Type: application/vnd.grafeq
#   Content-Type: application/vnd.groove-account
#   Content-Type: application/vnd.groove-help
#   Content-Type: application/vnd.groove-identity-message
#   Content-Type: application/vnd.groove-injector
#   Content-Type: application/vnd.groove-tool-message
#   Content-Type: application/vnd.groove-tool-template
#   Content-Type: application/vnd.groove-vcard
#   Content-Type: application/vnd.hal+xml
#   Content-Type: application/vnd.handheld-entertainment+xml
#   Content-Type: application/vnd.hbci
#   Content-Type: application/vnd.hhe.lesson-player
#   Content-Type: application/vnd.hp-hpgl
#   Content-Type: application/vnd.hp-hpid
#   Content-Type: application/vnd.hp-hps
#   Content-Type: application/vnd.hp-jlyt
#   Content-Type: application/vnd.hp-pcl
#   Content-Type: application/vnd.hp-pclxl
#   Content-Type: application/vnd.hydrostatix.sof-data
#   Content-Type: application/vnd.hzn-3d-crossword
#   Content-Type: application/vnd.ibm.minipay
#   Content-Type: application/vnd.ibm.modcap
#   Content-Type: application/vnd.ibm.rights-management
#   Content-Type: application/vnd.ibm.secure-container
#   Content-Type: application/vnd.iccprofile
#   Content-Type: application/vnd.igloader
#   Content-Type: application/vnd.immervision-ivp
#   Content-Type: application/vnd.immervision-ivu
#   Content-Type: application/vnd.insors.igm
#   Content-Type: application/vnd.intercon.formnet
#   Content-Type: application/vnd.intergeo
#   Content-Type: application/vnd.intu.qbo
#   Content-Type: application/vnd.intu.qfx
#   Content-Type: application/vnd.ipunplugged.rcprofile
#   Content-Type: application/vnd.irepository.package+xml
#   Content-Type: application/vnd.isac.fcs
#   Content-Type: application/vnd.is-xpr
#   Content-Type: application/vnd.jam
#   Content-Type: application/vnd.jcp.javame.midlet-rms
#   Content-Type: application/vnd.jisp
#   Content-Type: application/vnd.joost.joda-archive
#   Content-Type: application/vnd.kahootz
#   Content-Type: application/vnd.kde.karbon
#   Content-Type: application/vnd.kde.kchart
#   Content-Type: application/vnd.kde.kformula
#   Content-Type: application/vnd.kde.kivio
#   Content-Type: application/vnd.kde.kontour
#   Content-Type: application/vnd.kde.kpresenter
#   Content-Type: application/vnd.kde.kspread
#   Content-Type: application/vnd.kde.kword
#   Content-Type: application/vnd.kenameaapp
#   Content-Type: application/vnd.kidspiration
#   Content-Type: application/vnd.kinar
#   Content-Type: application/vnd.koan
#   Content-Type: application/vnd.kodak-descriptor
#   Content-Type: application/vnd.las.las+xml
#   Content-Type: application/vnd.llamagraphics.life-balance.desktop
#   Content-Type: application/vnd.llamagraphics.life-balance.exchange+xml
#   Content-Type: application/vnd.lotus-1-2-3
#   Content-Type: application/vnd.lotus-approach
#   Content-Type: application/vnd.lotus-freelance
#   Content-Type: application/vnd.lotus-notes
#   Content-Type: application/vnd.lotus-organizer
#   Content-Type: application/vnd.lotus-screencam
#   Content-Type: application/vnd.lotus-wordpro
#   Content-Type: application/vnd.macports.portpkg
#   Content-Type: application/vnd.mcd
#   Content-Type: application/vnd.medcalcdata
#   Content-Type: application/vnd.mediastation.cdkey
#   Content-Type: application/vnd.mfer
#   Content-Type: application/vnd.mfmp
#   Content-Type: application/vnd.micrografx.flo
#   Content-Type: application/vnd.micrografx.igx
#   Content-Type: application/vnd.mif
#   Content-Type: application/vnd.mobius.daf
#   Content-Type: application/vnd.mobius.dis
#   Content-Type: application/vnd.mobius.mbk
#   Content-Type: application/vnd.mobius.mqy
#   Content-Type: application/vnd.mobius.msl
#   Content-Type: application/vnd.mobius.plc
#   Content-Type: application/vnd.mobius.txf
#   Content-Type: application/vnd.mophun.application
#   Content-Type: application/vnd.mophun.certificate
#   Content-Type: application/vnd.mozilla.xul+xml
#   Content-Type: application/vnd.ms-artgalry
#   Content-Type: application/vnd.ms-cab-compressed
#   Content-Type: application/vnd.mseq
#   Content-Type: application/vnd.ms-excel
#   Content-Type: application/vnd.ms-excel.addin.macroenabled.12
#   Content-Type: application/vnd.ms-excel.sheet.binary.macroenabled.12
#   Content-Type: application/vnd.ms-excel.sheet.macroenabled.12
#   Content-Type: application/vnd.ms-excel.template.macroenabled.12
#   Content-Type: application/vnd.ms-fontobject
#   Content-Type: application/vnd.ms-htmlhelp
#   Content-Type: application/vnd.ms-ims
#   Content-Type: application/vnd.ms-lrm
#   Content-Type: application/vnd.ms-officetheme
#   Content-Type: application/vnd.ms-pki.seccat
#   Content-Type: application/vnd.ms-pki.stl
#   Content-Type: application/vnd.ms-powerpoint
#   Content-Type: application/vnd.ms-powerpoint.addin.macroenabled.12
#   Content-Type: application/vnd.ms-powerpoint.presentation.macroenabled.12
#   Content-Type: application/vnd.ms-powerpoint.slide.macroenabled.12
#   Content-Type: application/vnd.ms-powerpoint.slideshow.macroenabled.12
#   Content-Type: application/vnd.ms-powerpoint.template.macroenabled.12
#   Content-Type: application/vnd.ms-project
#   Content-Type: application/vnd.ms-word.document.macroenabled.12
#   Content-Type: application/vnd.ms-word.template.macroenabled.12
#   Content-Type: application/vnd.ms-works
#   Content-Type: application/vnd.ms-wpl
#   Content-Type: application/vnd.ms-xpsdocument
#   Content-Type: application/vnd.musician
#   Content-Type: application/vnd.muvee.style
#   Content-Type: application/vnd.neurolanguage.nlu
#   Content-Type: application/vnd.noblenet-directory
#   Content-Type: application/vnd.noblenet-sealer
#   Content-Type: application/vnd.noblenet-web
#   Content-Type: application/vnd.nokia.n-gage.data
#   Content-Type: application/vnd.nokia.n-gage.symbian.install
#   Content-Type: application/vnd.nokia.radio-preset
#   Content-Type: application/vnd.nokia.radio-presets
#   Content-Type: application/vnd.novadigm.edm
#   Content-Type: application/vnd.novadigm.edx
#   Content-Type: application/vnd.novadigm.ext
#   Content-Type: application/vnd.oasis.opendocument.chart
#   Content-Type: application/vnd.oasis.opendocument.chart-template
#   Content-Type: application/vnd.oasis.opendocument.database
#   Content-Type: application/vnd.oasis.opendocument.formula
#   Content-Type: application/vnd.oasis.opendocument.formula-template
#   Content-Type: application/vnd.oasis.opendocument.graphics
#   Content-Type: application/vnd.oasis.opendocument.graphics-template
#   Content-Type: application/vnd.oasis.opendocument.image
#   Content-Type: application/vnd.oasis.opendocument.image-template
#   Content-Type: application/vnd.oasis.opendocument.presentation
#   Content-Type: application/vnd.oasis.opendocument.presentation-template
#   Content-Type: application/vnd.oasis.opendocument.spreadsheet
#   Content-Type: application/vnd.oasis.opendocument.spreadsheet-template
#   Content-Type: application/vnd.oasis.opendocument.text
#   Content-Type: application/vnd.oasis.opendocument.text-master
#   Content-Type: application/vnd.oasis.opendocument.text-template
#   Content-Type: application/vnd.oasis.opendocument.text-web
#   Content-Type: application/vnd.olpc-sugar
#   Content-Type: application/vnd.oma.dd2+xml
#   Content-Type: application/vnd.openofficeorg.extension
#   Content-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation
#   Content-Type: application/vnd.openxmlformats-officedocument.presentationml.slide
#   Content-Type: application/vnd.openxmlformats-officedocument.presentationml.slideshow
#   Content-Type: application/vnd.openxmlformats-officedocument.presentationml.template
#   Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
#   Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.template
#   Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
#   Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.template
#   Content-Type: application/vnd.osgeo.mapguide.package
#   Content-Type: application/vnd.osgi.dp
#   Content-Type: application/vnd.palm
#   Content-Type: application/vnd.pawaafile
#   Content-Type: application/vnd.pg.format
#   Content-Type: application/vnd.pg.osasli
#   Content-Type: application/vnd.picsel
#   Content-Type: application/vnd.pmi.widget
#   Content-Type: application/vnd.pocketlearn
#   Content-Type: application/vnd.powerbuilder6
#   Content-Type: application/vnd.previewsystems.box
#   Content-Type: application/vnd.proteus.magazine
#   Content-Type: application/vnd.publishare-delta-tree
#   Content-Type: application/vnd.pvi.ptid1
#   Content-Type: application/vnd.quark.quarkxpress
#   Content-Type: application/vnd.realvnc.bed
#   Content-Type: application/vnd.recordare.musicxml
#   Content-Type: application/vnd.recordare.musicxml+xml
#   Content-Type: application/vnd.rig.cryptonote
#   Content-Type: application/vnd.rim.cod
#   Content-Type: application/vnd.rn-realmedia
#   Content-Type: application/vnd.route66.link66+xml
#   Content-Type: application/vnd.sailingtracker.track
#   Content-Type: application/vnd.seemail
#   Content-Type: application/vnd.sema
#   Content-Type: application/vnd.semd
#   Content-Type: application/vnd.semf
#   Content-Type: application/vnd.shana.informed.formdata
#   Content-Type: application/vnd.shana.informed.formtemplate
#   Content-Type: application/vnd.shana.informed.interchange
#   Content-Type: application/vnd.shana.informed.package
#   Content-Type: application/vnd.simtech-mindmapper
#   Content-Type: application/vnd.smaf
#   Content-Type: application/vnd.smart.teacher
#   Content-Type: application/vnd.solent.sdkm+xml
#   Content-Type: application/vnd.spotfire.dxp
#   Content-Type: application/vnd.spotfire.sfs
#   Content-Type: application/vnd.stardivision.calc
#   Content-Type: application/vnd.stardivision.draw
#   Content-Type: application/vnd.stardivision.impress
#   Content-Type: application/vnd.stardivision.math
#   Content-Type: application/vnd.stardivision.writer
#   Content-Type: application/vnd.stardivision.writer-global
#   Content-Type: application/vnd.stepmania.stepchart
#   Content-Type: application/vnd.sun.xml.calc
#   Content-Type: application/vnd.sun.xml.calc.template
#   Content-Type: application/vnd.sun.xml.draw
#   Content-Type: application/vnd.sun.xml.draw.template
#   Content-Type: application/vnd.sun.xml.impress
#   Content-Type: application/vnd.sun.xml.impress.template
#   Content-Type: application/vnd.sun.xml.math
#   Content-Type: application/vnd.sun.xml.writer
#   Content-Type: application/vnd.sun.xml.writer.global
#   Content-Type: application/vnd.sun.xml.writer.template
#   Content-Type: application/vnd.sus-calendar
#   Content-Type: application/vnd.svd
#   Content-Type: application/vnd.symbian.install
#   Content-Type: application/vnd.syncml.dm+wbxml
#   Content-Type: application/vnd.syncml.dm+xml
#   Content-Type: application/vnd.syncml+xml
#   Content-Type: application/vnd.tao.intent-module-archive
#   Content-Type: application/vnd.tmobile-livetv
#   Content-Type: application/vnd.trid.tpt
#   Content-Type: application/vnd.triscape.mxs
#   Content-Type: application/vnd.trueapp
#   Content-Type: application/vnd.ufdl
#   Content-Type: application/vnd.uiq.theme
#   Content-Type: application/vnd.umajin
#   Content-Type: application/vnd.unity
#   Content-Type: application/vnd.uoml+xml
#   Content-Type: application/vnd.vcx
#   Content-Type: application/vnd.visio
#   Content-Type: application/vnd.visio2013
#   Content-Type: application/vnd.visionary
#   Content-Type: application/vnd.vsf
#   Content-Type: application/vnd.wap.wbxml
#   Content-Type: application/vnd.wap.wmlc
#   Content-Type: application/vnd.wap.wmlscriptc
#   Content-Type: application/vnd.webturbo
#   Content-Type: application/vnd.wolfram.player
#   Content-Type: application/vnd.wordperfect
#   Content-Type: application/vnd.wqd
#   Content-Type: application/vnd.wt.stf
#   Content-Type: application/vnd.xara
#   Content-Type: application/vnd.xfdl
#   Content-Type: application/vnd.yamaha.hv-dic
#   Content-Type: application/vnd.yamaha.hv-script
#   Content-Type: application/vnd.yamaha.hv-voice
#   Content-Type: application/vnd.yamaha.openscoreformat
#   Content-Type: application/vnd.yamaha.openscoreformat.osfpvg+xml
#   Content-Type: application/vnd.yamaha.smaf-audio
#   Content-Type: application/vnd.yamaha.smaf-phrase
#   Content-Type: application/vnd.yellowriver-custom-menu
#   Content-Type: application/vnd.zul
#   Content-Type: application/vnd.zzazz.deck+xml
#   Content-Type: application/voicexml+xml
#   Content-Type: application/widget
#   Content-Type: application/winhlp
#   Content-Type: application/wsdl+xml
#   Content-Type: application/wspolicy+xml
#   Content-Type: application/x400-bp
#   Content-Type: application/x-7z-compressed
#   Content-Type: application/x-abiword
#   Content-Type: application/x-ace-compressed
#   Content-Type: application/x-apple-diskimage
#   Content-Type: application/x-authorware-bin
#   Content-Type: application/x-authorware-map
#   Content-Type: application/x-authorware-seg
#   Content-Type: application/x-bcpio
#   Content-Type: application/x-bittorrent
#   Content-Type: application/x-bzip
#   Content-Type: application/x-bzip2
#   Content-Type: application/xcap-diff+xml
#   Content-Type: application/x-cdlink
#   Content-Type: application/x-chat
#   Content-Type: application/x-chess-pgn
#   Content-Type: application/x-cpio
#   Content-Type: application/x-csh
#   Content-Type: application/x-debian-package
#   Content-Type: application/x-director
#   Content-Type: application/x-doom
#   Content-Type: application/x-dtbncx+xml
#   Content-Type: application/x-dtbook+xml
#   Content-Type: application/x-dtbresource+xml
#   Content-Type: application/x-dvi
#   Content-Type: application/xenc+xml
#   Content-Type: application/x-font-bdf
#   Content-Type: application/x-font-ghostscript
#   Content-Type: application/x-font-linux-psf
#   Content-Type: application/x-font-otf
#   Content-Type: application/x-font-pcf
#   Content-Type: application/x-font-snf
#   Content-Type: application/x-font-ttf
#   Content-Type: application/x-font-type1
#   Content-Type: application/x-font-woff
#   Content-Type: application/x-futuresplash
#   Content-Type: application/x-gnumeric
#   Content-Type: application/x-gtar
#   Content-Type: application/x-hdf
#   Content-Type: application/xhtml+xml
#   Content-Type: application/x-java-jnlp-file
#   Content-Type: application/x-latex
#   Content-Type: application/xml
#   Content-Type: application/xml-dtd
#   Content-Type: application/x-mobipocket-ebook
#   Content-Type: application/x-msaccess
#   Content-Type: application/x-ms-application
#   Content-Type: application/x-msbinder
#   Content-Type: application/x-mscardfile
#   Content-Type: application/x-msclip
#   Content-Type: application/x-msdownload
#   Content-Type: application/x-msmediaview
#   Content-Type: application/x-msmetafile
#   Content-Type: application/x-msmoney
#   Content-Type: application/x-mspublisher
#   Content-Type: application/x-msschedule
#   Content-Type: application/x-msterminal
#   Content-Type: application/x-ms-wmd
#   Content-Type: application/x-ms-wmz
#   Content-Type: application/x-mswrite
#   Content-Type: application/x-ms-xbap
#   Content-Type: application/x-netcdf
#   Content-Type: application/xop+xml
#   Content-Type: application/x-pkcs12
#   Content-Type: application/x-pkcs7-certificates
#   Content-Type: application/x-pkcs7-certreqresp
#   Content-Type: application/x-rar-compressed
#   Content-Type: application/x-sh
#   Content-Type: application/x-shar
#   Content-Type: application/x-shockwave-flash
#   Content-Type: application/x-silverlight-app
#   Content-Type: application/xslt+xml
#   Content-Type: application/xspf+xml
#   Content-Type: application/x-stuffit
#   Content-Type: application/x-stuffitx
#   Content-Type: application/x-sv4cpio
#   Content-Type: application/x-sv4crc
#   Content-Type: application/x-tar
#   Content-Type: application/x-tcl
#   Content-Type: application/x-tex
#   Content-Type: application/x-texinfo
#   Content-Type: application/x-tex-tfm
#   Content-Type: application/x-ustar
#   Content-Type: application/xv+xml
#   Content-Type: application/x-wais-source
#   Content-Type: application/x-x509-ca-cert
#   Content-Type: application/x-xfig
#   Content-Type: application/x-xpinstall
#   Content-Type: application/yang
#   Content-Type: application/yin+xml
#   Content-Type: application/zip
#   Content-Type: audio/32kadpcm
#   Content-Type: audio/adpcm
#   Content-Type: audio/basic
#   Content-Type: audio/midi
#   Content-Type: audio/mp4
#   Content-Type: audio/mpeg
#   Content-Type: audio/ogg
#   Content-Type: audio/vnd.dece.audio
#   Content-Type: audio/vnd.digital-winds
#   Content-Type: audio/vnd.dra
#   Content-Type: audio/vnd.dts
#   Content-Type: audio/vnd.dts.hd
#   Content-Type: audio/vnd.lucent.voice
#   Content-Type: audio/vnd.ms-playready.media.pya
#   Content-Type: audio/vnd.nuera.ecelp4800
#   Content-Type: audio/vnd.nuera.ecelp7470
#   Content-Type: audio/vnd.nuera.ecelp9600
#   Content-Type: audio/vnd.rip
#   Content-Type: audio/webm
#   Content-Type: audio/x-aac
#   Content-Type: audio/x-aiff
#   Content-Type: audio/x-mpegurl
#   Content-Type: audio/x-ms-wax
#   Content-Type: audio/x-ms-wma
#   Content-Type: audio/x-pn-realaudio
#   Content-Type: audio/x-pn-realaudio-plugin
#   Content-Type: audio/x-wav
#   Content-Type: chemical/x-cdx
#   Content-Type: chemical/x-cif
#   Content-Type: chemical/x-cmdf
#   Content-Type: chemical/x-cml
#   Content-Type: chemical/x-csml
#   Content-Type: chemical/x-xyz
#   Content-Type: image/bmp
#   Content-Type: image/cgm
#   Content-Type: image/g3fax
#   Content-Type: image/gif
#   Content-Type: image/ief
#   Content-Type: image/jpeg
#   Content-Type: image/jpeg; name="image001.jpg"
#   Content-Type: image/jpeg; name="TemptationShortcut.jpg"
#   Content-Type: image/ktx
#   Content-Type: image/pjpeg
#   Content-Type: image/png
#   Content-Type: image/prs.btif
#   Content-Type: image/svg+xml
#   Content-Type: image/tiff
#   Content-Type: image/vnd.adobe.photoshop
#   Content-Type: image/vnd.dece.graphic
#   Content-Type: image/vnd.djvu
#   Content-Type: image/vnd.dvb.subtitle
#   Content-Type: image/vnd.dwg
#   Content-Type: image/vnd.dxf
#   Content-Type: image/vnd.fastbidsheet
#   Content-Type: image/vnd.fpx
#   Content-Type: image/vnd.fst
#   Content-Type: image/vnd.fujixerox.edmics-mmr
#   Content-Type: image/vnd.fujixerox.edmics-rlc
#   Content-Type: image/vnd.ms-modi
#   Content-Type: image/vnd.net-fpx
#   Content-Type: image/vnd.wap.wbmp
#   Content-Type: image/vnd.xiff
#   Content-Type: image/webp
#   Content-Type: image/x-citrix-jpeg
#   Content-Type: image/x-citrix-png
#   Content-Type: image/x-cmu-raster
#   Content-Type: image/x-cmx
#   Content-Type: image/x-freehand
#   Content-Type: image/x-icon
#   Content-Type: image/x-pcx
#   Content-Type: image/x-pict
#   Content-Type: image/x-png
#   Content-Type: image/x-portable-anymap
#   Content-Type: image/x-portable-bitmap
#   Content-Type: image/x-portable-graymap
#   Content-Type: image/x-portable-pixmap
#   Content-Type: image/x-rgb
#   Content-Type: image/x-xbitmap
#   Content-Type: image/x-xpixmap
#   Content-Type: image/x-xwindowdump
#   Content-Type: message/delivery-status
#   Content-Type: message/disposition-notification-to
#   Content-Type: message/external-body
#   Content-Type: message/http
#   Content-Type: message/partial
#   Content-Type: message/rfc822
#   Content-Type: model/iges
#   Content-Type: model/mesh
#   Content-Type: model/vnd.collada+xml
#   Content-Type: model/vnd.dwf
#   Content-Type: model/vnd.gdl
#   Content-Type: model/vnd.gtw
#   Content-Type: model/vnd.mts
#   Content-Type: model/vnd.vtu
#   Content-Type: model/vrml
#   Content-Type: multipart/alternative;
#   Content-Type: multipart/alternative; boundary=001a113a2dc6dd3487053f79bc24
#   Content-Type: multipart/alternative; boundary="001a11456c8817dd1d055d352f8c"
#   Content-Type: multipart/alternative; boundary="_----056dTAi7CnMb4YC6zcuzcw===_CB/19-64684-8C2612A5"
#   Content-Type: multipart/alternative; boundary="089e082b9ca8b3811005607e8c7d"
#   Content-Type: multipart/alternative; boundary=12781cc67c6d4bdc5c62fe572df6f07067ed31bca7176f259611800bc7ed
#   Content-Type: multipart/alternative; boundary="===============2300963478671213537=="
#   Content-Type: multipart/alternative; boundary="6kpfp7cF1q82tUL7as8jVsg6vSxX=_GkhV"
#   Content-Type: multipart/alternative; boundary="cdf82e78-582d-4a55-9037-dacf81ae37d3"
#   Content-Type: multipart/alternative; boundary="de3m6f=_VUkD4F9LsJ1SCYvVv7MXYQfySv"
#   Content-Type: multipart/alternative; boundary="__slack_222209002__"
#   Content-Type: multipart/byteranges; boundary="94eb2c0e6238d7dc6f05607ea548"
#   Content-Type: multipart/digest; boundary="089e082b9ca8b3811005607e8c7d"
#   Content-Type: multipart/encrypted; boundary="94eb2c0e6238d7dc6f05607ea548"
#   Content-Type: multipart/form-data; boundary="94eb2c0e6238d7dc6f05607ea548"
#   Content-Type: multipart/mixed;
#   Content-Type: multipart/mixed; boundary=001a113ed43687e70b053d097387
#   Content-Type: multipart/mixed; boundary="94eb2c0e6238d7dc6f05607ea548"
#   Content-Type: multipart/mixed-replace; boundary="94eb2c0e6238d7dc6f05607ea548"
#   Content-Type: multipart/parallel
#   Content-Type: multipart/related;
#   Content-Type: multipart/related; boundary="94eb2c0e6238d7dc6f05607ea548"
#   Content-Type: multipart/report; boundary="94eb2c0e6238d7dc6f05607ea548"
#   Content-Type: multipart/signed; boundary="94eb2c0e6238d7dc6f05607ea548"
#   Content-Type: text/calendar
#   Content-Type: text/css
#   Content-Type: text/csv
#   Content-Type: text/enriched
#   Content-Type: text/html
#   Content-Type: text/html;
#   Content-Type: text/html; charset="us-ascii"
#   Content-Type: text/html; charset="utf-8"
#   Content-Type: text/html; charset=utf-8
#   Content-Type: text/html; charset = "utf-8"
#   Content-Type: text/html; charset="UTF-8"
#   Content-Type: text/html; charset=UTF-8
#   Content-Type: text/n3
#   Content-Type: text/plain
#   Content-Type: text/plain;
#   Content-Type: text/plain-bas
#   Content-Type: text/plain; charset="us-ascii"
#   Content-Type: text/plain; charset="us-ascii";
#   Content-Type: text/plain; charset="US-ASCII"; name="test_text_file.txt"
#   Content-Type: text/plain; charset="utf-8"
#   Content-Type: text/plain; charset=utf-8
#   Content-Type: text/plain; charset = "utf-8"
#   Content-Type: text/plain; charset="UTF-8"
#   Content-Type: text/plain; charset=UTF-8
#   Content-Type: text/plain; charset=utf-8; format=flowed
#   Content-Type: text/plain; charset=windows-1252; format=flowed
#   Content-Type: text/prs.lines.tag
#   Content-Type: text/rfc822-headers
#   Content-Type: text/richtext
#   Content-Type: text/sgml
#   Content-Type: text/tab-separated-values
#   Content-Type: text/troff
#   Content-Type: text/turtle
#   Content-Type: text/uri-list
#   Content-Type: text/vnd.curl
#   Content-Type: text/vnd.curl.dcurl
#   Content-Type: text/vnd.curl.mcurl
#   Content-Type: text/vnd.curl.scurl
#   Content-Type: text/vnd.fly
#   Content-Type: text/vnd.fmi.flexstor
#   Content-Type: text/vnd.graphviz
#   Content-Type: text/vnd.in3d.3dml
#   Content-Type: text/vnd.in3d.spot
#   Content-Type: text/vnd.sun.j2me.app-descriptor
#   Content-Type: text/vnd.wap.wml
#   Content-Type: text/vnd.wap.wmlscript
#   Content-Type: text/x-asm
#   Content-Type: text/x-c
#   Content-Type: text/x-fortran
#   Content-Type: text/x-java-source,java
#   Content-Type: text/x-markdown; charset="US-ASCII"; name="README.md"
#   Content-Type: text/x-pascal
#   Content-Type: text/x-setext
#   Content-Type: text/x-uuencode
#   Content-Type: text/x-vcalendar
#   Content-Type: text/x-vcard
#   Content-Type: text/yaml
#   Content-Type: video/3gpp
#   Content-Type: video/3gpp2
#   Content-Type: video/h261
#   Content-Type: video/h263
#   Content-Type: video/h264
#   Content-Type: video/jpeg
#   Content-Type: video/jpm
#   Content-Type: video/mj2
#   Content-Type: video/mp4
#   Content-Type: video/mpeg
#   Content-Type: video/ogg
#   Content-Type: video/quicktime
#   Content-Type: video/vnd.dece.hd
#   Content-Type: video/vnd.dece.mobile
#   Content-Type: video/vnd.dece.pd
#   Content-Type: video/vnd.dece.sd
#   Content-Type: video/vnd.dece.video
#   Content-Type: video/vnd.fvt
#   Content-Type: video/vnd.mpegurl
#   Content-Type: video/vnd.ms-playready.media.pyv
#   Content-Type: video/vnd.uvvu.mp4
#   Content-Type: video/vnd.vivo
#   Content-Type: video/webm
#   Content-Type: video/x-f4v
#   Content-Type: video/x-fli
#   Content-Type: video/x-flv
#   Content-Type: video/x-m4v
#   Content-Type: video/x-ms-asf
#   Content-Type: video/x-msvideo
#   Content-Type: video/x-ms-wm
#   Content-Type: video/x-ms-wmv
#   Content-Type: video/x-ms-wmx
#   Content-Type: video/x-ms-wvx
#   Content-Type: video/x-sgi-movie
#   Content-Type: x-conference/x-cooltalk
class RFC822ContentTypeHeader(Header):
    def __init__(self):
        super().__init__()
        self.headerType = "CONTENTTYPE"

    # Content-Type := type "/" subtype *[";" parameter] 
    # type :=          "application"     / "audio" 
    #           / "image"           / "message" 
    #           / "multipart"  / "text" 
    #           / "video"           / x-token 
    # x-token := <The two characters "X-" followed, with no 
    #            intervening white space, by any token> 
    # subtype := token 
    # parameter := attribute "=" value 
    # attribute := token 
    # value := token / quoted-string 
    # token := 1*<any CHAR except SPACE, CTLs, or tspecials> 
    # tspecials :=  "(" / ")" / "<" / ">" / "@"  ; Must be in 
    #            /  "," / ";" / ":" / "\" / <">  ; quoted-string, 
    #            /  "/" / "[" / "]" / "?" / "."  ; to use within 
    #            /  "="                        ; parameter values
    def parse(self):
        print( "DEBUG: In Content-Type header parse:" )
        self.contentTypeStr = None
        self.contentSubTypeStr = None
        self.headerOnOneLine = ""
        for line in self.headers:
            self.headerOnOneLine += line.strip()
        self.headerOnOneLine = self.headerOnOneLine[len("Content-Type:"):]
        for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
            if( element.startswith( "application" ) ):
                self.parseApplicationType()
                break
            elif( element.startswith( "audio" ) ):
                self.parseAudioType()
                break
            elif( element.startswith( "chemical" ) ):
                self.parseChemicalType()
                break
            elif( element.startswith( "image" ) ):
                self.parseImageType()
                break
            elif( element.startswith( "message" ) ):
                self.parseMessageType()
                break
            elif( element.startswith( "model" ) ):
                self.parseModelType()
                break
            elif( element.startswith( "multipart" ) ):
                self.parseMultipartType()
                break
            elif( element.startswith( "text" ) ):
                self.parseTextType()
                break
            elif( element.startswith( "video" ) ):
                self.parseVideoType()
                break
            elif( element.startswith( "x-conference" ) ):
                self.parseXConferenceType()
                break



    def parseApplicationType(self):
        print( "DEBUG: In Content-Type header parse:" )
        self.contentTypeStr = "application"
        for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
            print( "DEBUG:" )



    def parseAudioType(self):
        print( "DEBUG: In Content-Type header parse:" )
        self.contentTypeStr = "audio"
        for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
            print( "DEBUG:" )



    def parseChemicalType(self):
        print( "DEBUG: In Content-Type header parse:" )
        self.contentTypeStr = "chemical"
        for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
            print( "DEBUG:" )



    def parseImageType(self):
        print( "DEBUG: In Content-Type header parse:" )
        self.contentTypeStr = "image"
        for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
            print( "DEBUG:" )



    def parseMessageType(self):
        print( "DEBUG: In Content-Type header parse:" )
        self.contentTypeStr = "message"
        for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
            print( "DEBUG:" )



    def parseModelType(self):
        print( "DEBUG: In Content-Type header parse:" )
        self.contentTypeStr = "model"
        for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
            print( "DEBUG:" )



    def parseMultipartType(self):
        print( "DEBUG: In Content-Type header parseMultipartType:" )
        self.contentTypeStr = "multipart"
        for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
            print( "DEBUG: In Content-Type header parseMultipartType: element:",element )
            if( element.startswith( self.contentTypeStr ) ):
                t1, t2 = [x.strip() for x in element.split("/")]
                self.contentSubTypeStr = t2
                print( "DEBUG: In Content-Type header parseMultipartType: element: multipart:",t2 )
            elif( element.startswith( "boundary" ) ):
                t1, t2 = [x.strip() for x in element.split("=")]
                self.multipartBoundaryStr = t2
                print( "DEBUG: In Content-Type header parseMultipartType: element: boundary:",t2 )



    def parseTextType(self):
        print( "DEBUG: In Content-Type header parse:" )
        self.contentTypeStr = "text"
        for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
            print( "DEBUG:" )



    def parseVideoType(self):
        print( "DEBUG: In Content-Type header parse:" )
        self.contentTypeStr = "video"
        for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
            print( "DEBUG:" )



    def parseXConferenceType(self):
        print( "DEBUG: In Content-Type header parse:" )
        self.contentTypeStr = "x-conference"
        for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
            print( "DEBUG:" )



# # Content-Transfer-Encoding:
# # Content-Transfer-Encoding: quoted-printable
# class ContentTransferEncodingHeader(Header):
#     def __init__(self):
#         super().__init__()
#         self.headerType = "CONTENTTRANSFERENCODING"
# 
#     def parse(self):
#         self.ContentTransferEncodingStr = None
# 
# 
# 
# Delivered-To:
class RFC822DeliveredToHeader(Header):
    def __init__(self):
        super().__init__()
        self.headerType = "DELIVEREDTO"

    def parse(self):
        self.deliveredToStr = None



# MIME-Version:
class RFC822MimeVersionHeader(Header):
    def __init__(self):
        super().__init__()
        self.headerType = "MIMEVERSION"

    def parse(self):
        self.mimeVersionStr = None



class RFC822BodyBlock:
    def __init__( self ):
        return


def testCase( theCase ):
    theEmail = EmailRFC822()
    if( "SimpleDefault" == theCase ):
        testFile = "SimpleDefault.eml"
        return( theEmail.readEmailFile( testFile ) )
    elif( "SimpleTextPlain" == theCase ):
        testFile = "SimpleTextPlain.eml"
        return( theEmail.readEmailFile( testFile ) )
    elif( "SimpleTextHtml" == theCase ):
        testFile = "SimpleTextHtml.eml"
        return( theEmail.readEmailFile( testFile ) )
    elif( "MultipartAlternativeTextPlain" == theCase ):
        testFile = "MultipartAlternativeTextPlain.eml"
        return( theEmail.readEmailFile( testFile ) )
    elif( "MultipartParallelTextPlain" == theCase ):
        testFile = "MultipartParallelTextPlain.eml"
        return( theEmail.readEmailFile( testFile ) )
    elif( "MultipartMixedTextPlain" == theCase ):
        testFile = "MultipartMixedTextPlain.eml"
        return( theEmail.readEmailFile( testFile ) )
    elif( "MultipartAlternativeTextHtml" == theCase ):
        testFile = "MultipartAlternativeTextHtml.eml"
        return( theEmail.readEmailFile( testFile ) )
    elif( "MultipartParallelTextHtml" == theCase ):
        testFile = "MultipartParallelTextHtml.eml"
        return( theEmail.readEmailFile( testFile ) )
    elif( "MultipartMixedTextHtml" == theCase ):
        testFile = "MultipartMixedTextHtml.eml"
        return( theEmail.readEmailFile( testFile ) )
    elif( "MultipartAlternativeTextPlainHtml" == theCase ):
        testFile = "MultipartAlternativeTextPlainHtml.eml"
        return( theEmail.readEmailFile( testFile ) )
    elif( "MultipartParallelTextPlainHtml" == theCase ):
        testFile = "MultipartParallelTextPlainHtml.eml"
        return( theEmail.readEmailFile( testFile ) )
    elif( "MultipartMixedTextPlainHtml" == theCase ):
        testFile = "MultipartMixedTextPlainHtml.eml"
        return( theEmail.readEmailFile( testFile ) )
    elif( "MultipartAlternativeTextPlainHtml1Attachment" == theCase ):
        testFile = "MultipartAlternativeTextPlainHtml1Attachment.eml"
        return( theEmail.readEmailFile( testFile ) )
    elif( "MultipartParallelTextPlainHtml1Attachment" == theCase ):
        testFile = "MultipartParallelTextPlainHtml1Attachment.eml"
        return( theEmail.readEmailFile( testFile ) )
    elif( "MultipartMixedTextPlainHtml1Attachment" == theCase ):
        testFile = "MultipartMixedTextPlainHtml1Attachment.eml"
        return( theEmail.readEmailFile( testFile ) )
    elif( "MultipartAlternativeTextPlainHtml2Attachment" == theCase ):
        testFile = "MultipartAlternativeTextPlainHtml2Attachment.eml"
        return( theEmail.readEmailFile( testFile ) )
    elif( "MultipartParallelTextPlainHtml2Attachment" == theCase ):
        testFile = "MultipartParallelTextPlainHtml2Attachment.eml"
        return( theEmail.readEmailFile( testFile ) )
    elif( "MultipartMixedTextPlainHtml2Attachment" == theCase ):
        testFile = "MultipartMixedTextPlainHtml2Attachment.eml"
        return( theEmail.readEmailFile( testFile ) )
    else:
        return( False )



if( "__main__" == __name__ ):
    # execute only if run as a script
    print( "Test Case: Simple Default Email = " + ("SUCCESS" if( testCase("SimpleDefault") ) else "FAILED" ) )






# class Body:
#     def __init__(self):
#         self.bodyParts = []
#         self.bodyType = None
#         return
# 
#     def __str__(self):
#         return self.getAllBodyParts()
# 
#     def __len__(self):
#         return len(self.bodyParts)
# 
#     def getAllBodyParts(self):
#         theBody = ""
#         for part in bodyParts:
#             theBody += part
#         return theBody
# 
#     def addBodyPart(self,bodyPart,bodyPartType):
#         if( "" == bodyPartType ):
#             # do something
#         elif( "" == bodyPartType ):
#             # do something
#         elif( "" == bodyPartType ):
#             # do something
#         else:
#             # do default something
# 
#         return
# 
# 
# 
# class BodyPart:
#     def __init__(self):
#         return
# 
#     def __str__(self):
#         return self.something()
# 
#     def __len__(self):
#         return len(self.sometin)
# 
#     def somethingElse(self):
#         return
# 
# 
# 
# class Header:
#     def __init__(self):
#         self.headers = []
#         self.headerType = None
# 
#     def __str__(self):
#         return self.getFullHeader()
# 
#     def __len__(self):
#         return len(headers)
# 
#     def appendHeaderLine(self, line):
#         self.headers.append(line)
#         self.headers[len(self.headers)-1] = self.headers[len(self.headers)-1].rstrip("\r\n")
# 
#     def getFullHeader(self):
#         strHeader = ""
#         #strHeader += "DEBUG-Header-Type:"
#         #strHeader += "None" if None == self.headerType else self.headerType
#         #strHeader += "///"
#         for line in self.headers:
#             strHeader += line
#             strHeader += "\n"
#         return strHeader
# 
# 
# 
# 
# # Received: from
# # the name the sending computer gave for itself (the name associated with that computer's IP address [its IP address])
# # by
# # the receiving computer's name (the software that computer uses) (usually Sendmail, qmail or Postfix)
# # with protocol (usually SMTP, ESMTP or ESMTPS)
# # id id assigned by local computer for logging;
# # timestamp (usually given in the computer's localtime; see below for how you can convert these all to your time)
# 
# class ReceivedHeader(Header):
#     def __init__(self):
#         super().__init__()
#         self.headerType = "RECEIVED"
#         self.receivedFromSelfIdent = None
#         self.receivedFromFQDN = None
#         self.receivedFromIP = None
#         self.receivedByFQDN = None
#         self.receivedByIP = None
#         self.receivedBySoftware = None
#         self.receivedByProtocol = None
#         self.receivedByID = None
#         self.receivedTimestampStr = None
#         self.receivedTimestampUTC = None
#         self.EnvelopeFrom = None
#         self.EnvelopeTo = None
#         self.misc = None
# 
#     def parse(self):
#         self.receivedFromSelfIdent = None
#         self.receivedFromFQDN = None
#         self.receivedFromIP = None
#         self.receivedByFQDN = None
#         self.receivedByIP = None
#         self.receivedBySoftware = None
#         self.receivedByProtocol = None
#         self.receivedByID = None
#         self.receivedTimestampStr = None
#         self.receivedTimestampUTC = None
#         self.EnvelopeFrom = None
#         self.EnvelopeTo = None
#         self.misc = None
# 
# 
# 
# # From: tokens [822]
# class FromHeader(Header):
#     def __init__(self):
#         super().__init__()
#         self.headerType = "FROM"
#         self.addressList = None
# 
#     def parse(self):
#         self.addressList = None
# 
# 
# 
# # To: tokens [822]
# class ToHeader(Header):
#     def __init__(self):
#         super().__init__()
#         self.headerType = "TO"
#         self.addressList = None
# 
#     def parse(self):
#         self.addressList = None
# 
# 
# 
# # Cc: tokens [822]
# class CCHeader(Header):
#     def __init__(self):
#         super().__init__()
#         self.headerType = "CC"
#         self.addressList = None
# 
#     def parse(self):
#         self.addressList = None
# 
# 
# 
# # Bcc: user tokens [822]
# class BCCHeader(Header):
#     def __init__(self):
#         super().__init__()
#         self.headerType = "BCC"
#         self.addressList = None
# 
#     def parse(self):
#         self.addressList = None
# 
# 
# 
# # Sender: tokens [822]
# class SenderHeader(Header):
#     def __init__(self):
#         super().__init__()
#         self.headerType = "SENDER"
#         self.addressList = None
# 
#     def parse(self):
#         self.addressList = None
# 
# 
# 
# # Reply-To: tokens [822]
# class ReplyToHeader(Header):
#     def __init__(self):
#         super().__init__()
#         self.headerType = "REPLYTO"
#         self.addressList = None
# 
#     def parse(self):
#         self.addressList = None
# 
# 
# 
# # Date: tokens [822]
# class DateHeader(Header):
#     def __init__(self):
#         super().__init__()
#         self.headerType = "DATE"
# 
#     def parse(self):
#         self.dateStr = None
# 
# 
# 
# # Subject: [822]
# class SubjectHeader(Header):
#     def __init__(self):
#         super().__init__()
#         self.headerType = "SUBJECT"
# 
#     def parse(self):
#         self.subjectStr = None
# 
# 
# 
# # Message-ID: tokens [822]
# class MessageIDHeader(Header):
#     def __init__(self):
#         super().__init__()
#         self.headerType = "MESSAGEID"
# 
#     def parse(self):
#         self.messageIDStr = None
# 
# 
# 
# # Content-Type:
# # Base Types:
# #   Content-Type: application
# #   Content-Type: audio
# #   Content-Type: chemical
# #   Content-Type: image
# #   Content-Type: message
# #   Content-Type: model
# #   Content-Type: multipart
# #   Content-Type: text
# #   Content-Type: video
# #   Content-Type: x-conference
# # Examples:
# #   Content-Type: application/andrew-inset
# #   Content-Type: application/applixware
# #   Content-Type: application/atomcat+xml
# #   Content-Type: application/atomsvc+xml
# #   Content-Type: application/atom+xml
# #   Content-Type: application/cals-1840
# #   Content-Type: application/ccxml+xml,
# #   Content-Type: application/cdmi-capability
# #   Content-Type: application/cdmi-container
# #   Content-Type: application/cdmi-domain
# #   Content-Type: application/cdmi-object
# #   Content-Type: application/cdmi-queue
# #   Content-Type: application/cu-seeme
# #   Content-Type: application/davmount+xml
# #   Content-Type: application/dssc+der
# #   Content-Type: application/dssc+xml
# #   Content-Type: application/ecmascript
# #   Content-Type: application/emma+xml
# #   Content-Type: application/epub+zip
# #   Content-Type: application/exi
# #   Content-Type: application/font-tdpfr
# #   Content-Type: application/hyperstudio
# #   Content-Type: application/ipfix
# #   Content-Type: application/java-archive
# #   Content-Type: application/javascript
# #   Content-Type: application/java-serialized-object
# #   Content-Type: application/java-vm
# #   Content-Type: application/json
# #   Content-Type: application/mac-binhex40
# #   Content-Type: application/mac-compactpro
# #   Content-Type: application/mads+xml
# #   Content-Type: application/marc
# #   Content-Type: application/marcxml+xml
# #   Content-Type: application/mathematica
# #   Content-Type: application/mathml+xml
# #   Content-Type: application/mbox
# #   Content-Type: application/mediaservercontrol+xml
# #   Content-Type: application/metalink4+xml
# #   Content-Type: application/mets+xml
# #   Content-Type: application/mods+xml
# #   Content-Type: application/mp21
# #   Content-Type: application/mp4
# #   Content-Type: application/msword
# #   Content-Type: application/mxf
# #   Content-Type: application/news-message-id
# #   Content-Type: application/news-transmission
# #   Content-Type: application/octet-stream
# #   Content-Type: application/octet-stream;
# #   Content-Type: application/octet-stream; name="Resume.pdf"
# #   Content-Type: application/oda
# #   Content-Type: application/oebps-package+xml
# #   Content-Type: application/ogg
# #   Content-Type: application/onenote
# #   Content-Type: application/patch-ops-error+xml
# #   Content-Type: application/pdf
# #   Content-Type: application/pdf; name=RSAC17InvoiceReceipt.pdf
# #   Content-Type: application/pgp-encrypted
# #   Content-Type: application/pgp-keys
# #   Content-Type: application/pgp-signature
# #   Content-Type: application/pics-rules
# #   Content-Type: application/pkcs10
# #   Content-Type: application/pkcs7-mime
# #   Content-Type: application/pkcs7-MIME
# #   Content-Type: application/pkcs7-signature
# #   Content-Type: application/pkcs8
# #   Content-Type: application/pkix-attr-cert
# #   Content-Type: application/pkix-cert
# #   Content-Type: application/pkixcmp
# #   Content-Type: application/pkix-crl
# #   Content-Type: application/pkix-pkipath
# #   Content-Type: application/pls+xml
# #   Content-Type: application/postscript
# #   Content-Type: application/prs.cww
# #   Content-Type: application/pskc+xml
# #   Content-Type: application/rdf+xml
# #   Content-Type: application/reginfo+xml
# #   Content-Type: application/relax-ng-compact-syntax
# #   Content-Type: application/remote-printing
# #   Content-Type: application/resource-lists-diff+xml
# #   Content-Type: application/resource-lists+xml
# #   Content-Type: application/rls-services+xml
# #   Content-Type: application/rsd+xml
# #   Content-Type: application/rss+xml
# #   Content-Type: application/rtf
# #   Content-Type: application/sbml+xml
# #   Content-Type: application/scvp-cv-request
# #   Content-Type: application/scvp-cv-response
# #   Content-Type: application/scvp-vp-request
# #   Content-Type: application/scvp-vp-response
# #   Content-Type: application/sdp
# #   Content-Type: application/set-payment-initiation
# #   Content-Type: application/set-registration-initiation
# #   Content-Type: application/sgml
# #   Content-Type: application/shf+xml
# #   Content-Type: application/smil+xml
# #   Content-Type: application/sparql-query
# #   Content-Type: application/sparql-results+xml
# #   Content-Type: application/srgs
# #   Content-Type: application/srgs+xml
# #   Content-Type: application/sru+xml
# #   Content-Type: application/ssml+xml
# #   Content-Type: application/tei+xml
# #   Content-Type: application/thraud+xml
# #   Content-Type: application/timestamped-data
# #   Content-Type: application/vnd.3gpp2.tcap
# #   Content-Type: application/vnd.3gpp.pic-bw-large
# #   Content-Type: application/vnd.3gpp.pic-bw-small
# #   Content-Type: application/vnd.3gpp.pic-bw-var
# #   Content-Type: application/vnd.3m.post-it-notes
# #   Content-Type: application/vnd.accpac.simply.aso
# #   Content-Type: application/vnd.accpac.simply.imp
# #   Content-Type: application/vnd.acucobol
# #   Content-Type: application/vnd.acucorp
# #   Content-Type: application/vnd.adobe.air-application-installer-package+zip
# #   Content-Type: application/vnd.adobe.fxp
# #   Content-Type: application/vnd.adobe.xdp+xml
# #   Content-Type: application/vnd.adobe.xfdf
# #   Content-Type: application/vnd.ahead.space
# #   Content-Type: application/vnd.airzip.filesecure.azf
# #   Content-Type: application/vnd.airzip.filesecure.azs
# #   Content-Type: application/vnd.amazon.ebook
# #   Content-Type: application/vnd.americandynamics.acc
# #   Content-Type: application/vnd.amiga.ami
# #   Content-Type: application/vnd.android.package-archive
# #   Content-Type: application/vnd.anser-web-certificate-issue-initiation
# #   Content-Type: application/vnd.anser-web-funds-transfer-initiation
# #   Content-Type: application/vnd.antix.game-component
# #   Content-Type: application/vnd.apple.installer+xml
# #   Content-Type: application/vnd.apple.mpegurl
# #   Content-Type: application/vnd.aristanetworks.swi
# #   Content-Type: application/vnd.audiograph
# #   Content-Type: application/vnd.blueice.multipass
# #   Content-Type: application/vnd.bmi
# #   Content-Type: application/vnd.businessobjects
# #   Content-Type: application/vnd.chemdraw+xml
# #   Content-Type: application/vnd.chipnuts.karaoke-mmd
# #   Content-Type: application/vnd.cinderella
# #   Content-Type: application/vnd.claymore
# #   Content-Type: application/vnd.cloanto.rp9
# #   Content-Type: application/vnd.clonk.c4group
# #   Content-Type: application/vnd.cluetrust.cartomobile-config
# #   Content-Type: application/vnd.cluetrust.cartomobile-config-pkg
# #   Content-Type: application/vnd.commonspace
# #   Content-Type: application/vnd.contact.cmsg
# #   Content-Type: application/vnd.cosmocaller
# #   Content-Type: application/vnd.crick.clicker
# #   Content-Type: application/vnd.crick.clicker.keyboard
# #   Content-Type: application/vnd.crick.clicker.palette
# #   Content-Type: application/vnd.crick.clicker.template
# #   Content-Type: application/vnd.crick.clicker.wordbank
# #   Content-Type: application/vnd.criticaltools.wbs+xml
# #   Content-Type: application/vnd.ctc-posml
# #   Content-Type: application/vnd.cups-ppd
# #   Content-Type: application/vnd.curl.car
# #   Content-Type: application/vnd.curl.pcurl
# #   Content-Type: application/vnd.data-vision.rdz
# #   Content-Type: application/vnd.denovo.fcselayout-link
# #   Content-Type: application/vnd.dna
# #   Content-Type: application/vnd.dolby.mlp
# #   Content-Type: application/vnd.dpgraph
# #   Content-Type: application/vnd.dreamfactory
# #   Content-Type: application/vnd.dvb.ait
# #   Content-Type: application/vnd.dvb.service
# #   Content-Type: application/vnd.dynageo
# #   Content-Type: application/vnd.ecowin.chart
# #   Content-Type: application/vnd.enliven
# #   Content-Type: application/vnd.epson.esf
# #   Content-Type: application/vnd.epson.msf
# #   Content-Type: application/vnd.epson.quickanime
# #   Content-Type: application/vnd.epson.salt
# #   Content-Type: application/vnd.epson.ssf
# #   Content-Type: application/vnd.eszigno3+xml
# #   Content-Type: application/vnd.ezpix-album
# #   Content-Type: application/vnd.ezpix-package
# #   Content-Type: application/vnd.fdf
# #   Content-Type: application/vnd.fdsn.seed
# #   Content-Type: application/vnd.flographit
# #   Content-Type: application/vnd.fluxtime.clip
# #   Content-Type: application/vnd.framemaker
# #   Content-Type: application/vnd.frogans.fnc
# #   Content-Type: application/vnd.frogans.ltf
# #   Content-Type: application/vnd.fsc.weblaunch
# #   Content-Type: application/vnd.fujitsu.oasys
# #   Content-Type: application/vnd.fujitsu.oasys2
# #   Content-Type: application/vnd.fujitsu.oasys3
# #   Content-Type: application/vnd.fujitsu.oasysgp
# #   Content-Type: application/vnd.fujitsu.oasysprs
# #   Content-Type: application/vnd.fujixerox.ddd
# #   Content-Type: application/vnd.fujixerox.docuworks
# #   Content-Type: application/vnd.fujixerox.docuworks.binder
# #   Content-Type: application/vnd.fuzzysheet
# #   Content-Type: application/vnd.genomatix.tuxedo
# #   Content-Type: application/vnd.geogebra.file
# #   Content-Type: application/vnd.geogebra.tool
# #   Content-Type: application/vnd.geometry-explorer
# #   Content-Type: application/vnd.geonext
# #   Content-Type: application/vnd.geoplan
# #   Content-Type: application/vnd.geospace
# #   Content-Type: application/vnd.gmx
# #   Content-Type: application/vnd.google-earth.kml+xml
# #   Content-Type: application/vnd.google-earth.kmz
# #   Content-Type: application/vnd.grafeq
# #   Content-Type: application/vnd.groove-account
# #   Content-Type: application/vnd.groove-help
# #   Content-Type: application/vnd.groove-identity-message
# #   Content-Type: application/vnd.groove-injector
# #   Content-Type: application/vnd.groove-tool-message
# #   Content-Type: application/vnd.groove-tool-template
# #   Content-Type: application/vnd.groove-vcard
# #   Content-Type: application/vnd.hal+xml
# #   Content-Type: application/vnd.handheld-entertainment+xml
# #   Content-Type: application/vnd.hbci
# #   Content-Type: application/vnd.hhe.lesson-player
# #   Content-Type: application/vnd.hp-hpgl
# #   Content-Type: application/vnd.hp-hpid
# #   Content-Type: application/vnd.hp-hps
# #   Content-Type: application/vnd.hp-jlyt
# #   Content-Type: application/vnd.hp-pcl
# #   Content-Type: application/vnd.hp-pclxl
# #   Content-Type: application/vnd.hydrostatix.sof-data
# #   Content-Type: application/vnd.hzn-3d-crossword
# #   Content-Type: application/vnd.ibm.minipay
# #   Content-Type: application/vnd.ibm.modcap
# #   Content-Type: application/vnd.ibm.rights-management
# #   Content-Type: application/vnd.ibm.secure-container
# #   Content-Type: application/vnd.iccprofile
# #   Content-Type: application/vnd.igloader
# #   Content-Type: application/vnd.immervision-ivp
# #   Content-Type: application/vnd.immervision-ivu
# #   Content-Type: application/vnd.insors.igm
# #   Content-Type: application/vnd.intercon.formnet
# #   Content-Type: application/vnd.intergeo
# #   Content-Type: application/vnd.intu.qbo
# #   Content-Type: application/vnd.intu.qfx
# #   Content-Type: application/vnd.ipunplugged.rcprofile
# #   Content-Type: application/vnd.irepository.package+xml
# #   Content-Type: application/vnd.isac.fcs
# #   Content-Type: application/vnd.is-xpr
# #   Content-Type: application/vnd.jam
# #   Content-Type: application/vnd.jcp.javame.midlet-rms
# #   Content-Type: application/vnd.jisp
# #   Content-Type: application/vnd.joost.joda-archive
# #   Content-Type: application/vnd.kahootz
# #   Content-Type: application/vnd.kde.karbon
# #   Content-Type: application/vnd.kde.kchart
# #   Content-Type: application/vnd.kde.kformula
# #   Content-Type: application/vnd.kde.kivio
# #   Content-Type: application/vnd.kde.kontour
# #   Content-Type: application/vnd.kde.kpresenter
# #   Content-Type: application/vnd.kde.kspread
# #   Content-Type: application/vnd.kde.kword
# #   Content-Type: application/vnd.kenameaapp
# #   Content-Type: application/vnd.kidspiration
# #   Content-Type: application/vnd.kinar
# #   Content-Type: application/vnd.koan
# #   Content-Type: application/vnd.kodak-descriptor
# #   Content-Type: application/vnd.las.las+xml
# #   Content-Type: application/vnd.llamagraphics.life-balance.desktop
# #   Content-Type: application/vnd.llamagraphics.life-balance.exchange+xml
# #   Content-Type: application/vnd.lotus-1-2-3
# #   Content-Type: application/vnd.lotus-approach
# #   Content-Type: application/vnd.lotus-freelance
# #   Content-Type: application/vnd.lotus-notes
# #   Content-Type: application/vnd.lotus-organizer
# #   Content-Type: application/vnd.lotus-screencam
# #   Content-Type: application/vnd.lotus-wordpro
# #   Content-Type: application/vnd.macports.portpkg
# #   Content-Type: application/vnd.mcd
# #   Content-Type: application/vnd.medcalcdata
# #   Content-Type: application/vnd.mediastation.cdkey
# #   Content-Type: application/vnd.mfer
# #   Content-Type: application/vnd.mfmp
# #   Content-Type: application/vnd.micrografx.flo
# #   Content-Type: application/vnd.micrografx.igx
# #   Content-Type: application/vnd.mif
# #   Content-Type: application/vnd.mobius.daf
# #   Content-Type: application/vnd.mobius.dis
# #   Content-Type: application/vnd.mobius.mbk
# #   Content-Type: application/vnd.mobius.mqy
# #   Content-Type: application/vnd.mobius.msl
# #   Content-Type: application/vnd.mobius.plc
# #   Content-Type: application/vnd.mobius.txf
# #   Content-Type: application/vnd.mophun.application
# #   Content-Type: application/vnd.mophun.certificate
# #   Content-Type: application/vnd.mozilla.xul+xml
# #   Content-Type: application/vnd.ms-artgalry
# #   Content-Type: application/vnd.ms-cab-compressed
# #   Content-Type: application/vnd.mseq
# #   Content-Type: application/vnd.ms-excel
# #   Content-Type: application/vnd.ms-excel.addin.macroenabled.12
# #   Content-Type: application/vnd.ms-excel.sheet.binary.macroenabled.12
# #   Content-Type: application/vnd.ms-excel.sheet.macroenabled.12
# #   Content-Type: application/vnd.ms-excel.template.macroenabled.12
# #   Content-Type: application/vnd.ms-fontobject
# #   Content-Type: application/vnd.ms-htmlhelp
# #   Content-Type: application/vnd.ms-ims
# #   Content-Type: application/vnd.ms-lrm
# #   Content-Type: application/vnd.ms-officetheme
# #   Content-Type: application/vnd.ms-pki.seccat
# #   Content-Type: application/vnd.ms-pki.stl
# #   Content-Type: application/vnd.ms-powerpoint
# #   Content-Type: application/vnd.ms-powerpoint.addin.macroenabled.12
# #   Content-Type: application/vnd.ms-powerpoint.presentation.macroenabled.12
# #   Content-Type: application/vnd.ms-powerpoint.slide.macroenabled.12
# #   Content-Type: application/vnd.ms-powerpoint.slideshow.macroenabled.12
# #   Content-Type: application/vnd.ms-powerpoint.template.macroenabled.12
# #   Content-Type: application/vnd.ms-project
# #   Content-Type: application/vnd.ms-word.document.macroenabled.12
# #   Content-Type: application/vnd.ms-word.template.macroenabled.12
# #   Content-Type: application/vnd.ms-works
# #   Content-Type: application/vnd.ms-wpl
# #   Content-Type: application/vnd.ms-xpsdocument
# #   Content-Type: application/vnd.musician
# #   Content-Type: application/vnd.muvee.style
# #   Content-Type: application/vnd.neurolanguage.nlu
# #   Content-Type: application/vnd.noblenet-directory
# #   Content-Type: application/vnd.noblenet-sealer
# #   Content-Type: application/vnd.noblenet-web
# #   Content-Type: application/vnd.nokia.n-gage.data
# #   Content-Type: application/vnd.nokia.n-gage.symbian.install
# #   Content-Type: application/vnd.nokia.radio-preset
# #   Content-Type: application/vnd.nokia.radio-presets
# #   Content-Type: application/vnd.novadigm.edm
# #   Content-Type: application/vnd.novadigm.edx
# #   Content-Type: application/vnd.novadigm.ext
# #   Content-Type: application/vnd.oasis.opendocument.chart
# #   Content-Type: application/vnd.oasis.opendocument.chart-template
# #   Content-Type: application/vnd.oasis.opendocument.database
# #   Content-Type: application/vnd.oasis.opendocument.formula
# #   Content-Type: application/vnd.oasis.opendocument.formula-template
# #   Content-Type: application/vnd.oasis.opendocument.graphics
# #   Content-Type: application/vnd.oasis.opendocument.graphics-template
# #   Content-Type: application/vnd.oasis.opendocument.image
# #   Content-Type: application/vnd.oasis.opendocument.image-template
# #   Content-Type: application/vnd.oasis.opendocument.presentation
# #   Content-Type: application/vnd.oasis.opendocument.presentation-template
# #   Content-Type: application/vnd.oasis.opendocument.spreadsheet
# #   Content-Type: application/vnd.oasis.opendocument.spreadsheet-template
# #   Content-Type: application/vnd.oasis.opendocument.text
# #   Content-Type: application/vnd.oasis.opendocument.text-master
# #   Content-Type: application/vnd.oasis.opendocument.text-template
# #   Content-Type: application/vnd.oasis.opendocument.text-web
# #   Content-Type: application/vnd.olpc-sugar
# #   Content-Type: application/vnd.oma.dd2+xml
# #   Content-Type: application/vnd.openofficeorg.extension
# #   Content-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation
# #   Content-Type: application/vnd.openxmlformats-officedocument.presentationml.slide
# #   Content-Type: application/vnd.openxmlformats-officedocument.presentationml.slideshow
# #   Content-Type: application/vnd.openxmlformats-officedocument.presentationml.template
# #   Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
# #   Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.template
# #   Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
# #   Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.template
# #   Content-Type: application/vnd.osgeo.mapguide.package
# #   Content-Type: application/vnd.osgi.dp
# #   Content-Type: application/vnd.palm
# #   Content-Type: application/vnd.pawaafile
# #   Content-Type: application/vnd.pg.format
# #   Content-Type: application/vnd.pg.osasli
# #   Content-Type: application/vnd.picsel
# #   Content-Type: application/vnd.pmi.widget
# #   Content-Type: application/vnd.pocketlearn
# #   Content-Type: application/vnd.powerbuilder6
# #   Content-Type: application/vnd.previewsystems.box
# #   Content-Type: application/vnd.proteus.magazine
# #   Content-Type: application/vnd.publishare-delta-tree
# #   Content-Type: application/vnd.pvi.ptid1
# #   Content-Type: application/vnd.quark.quarkxpress
# #   Content-Type: application/vnd.realvnc.bed
# #   Content-Type: application/vnd.recordare.musicxml
# #   Content-Type: application/vnd.recordare.musicxml+xml
# #   Content-Type: application/vnd.rig.cryptonote
# #   Content-Type: application/vnd.rim.cod
# #   Content-Type: application/vnd.rn-realmedia
# #   Content-Type: application/vnd.route66.link66+xml
# #   Content-Type: application/vnd.sailingtracker.track
# #   Content-Type: application/vnd.seemail
# #   Content-Type: application/vnd.sema
# #   Content-Type: application/vnd.semd
# #   Content-Type: application/vnd.semf
# #   Content-Type: application/vnd.shana.informed.formdata
# #   Content-Type: application/vnd.shana.informed.formtemplate
# #   Content-Type: application/vnd.shana.informed.interchange
# #   Content-Type: application/vnd.shana.informed.package
# #   Content-Type: application/vnd.simtech-mindmapper
# #   Content-Type: application/vnd.smaf
# #   Content-Type: application/vnd.smart.teacher
# #   Content-Type: application/vnd.solent.sdkm+xml
# #   Content-Type: application/vnd.spotfire.dxp
# #   Content-Type: application/vnd.spotfire.sfs
# #   Content-Type: application/vnd.stardivision.calc
# #   Content-Type: application/vnd.stardivision.draw
# #   Content-Type: application/vnd.stardivision.impress
# #   Content-Type: application/vnd.stardivision.math
# #   Content-Type: application/vnd.stardivision.writer
# #   Content-Type: application/vnd.stardivision.writer-global
# #   Content-Type: application/vnd.stepmania.stepchart
# #   Content-Type: application/vnd.sun.xml.calc
# #   Content-Type: application/vnd.sun.xml.calc.template
# #   Content-Type: application/vnd.sun.xml.draw
# #   Content-Type: application/vnd.sun.xml.draw.template
# #   Content-Type: application/vnd.sun.xml.impress
# #   Content-Type: application/vnd.sun.xml.impress.template
# #   Content-Type: application/vnd.sun.xml.math
# #   Content-Type: application/vnd.sun.xml.writer
# #   Content-Type: application/vnd.sun.xml.writer.global
# #   Content-Type: application/vnd.sun.xml.writer.template
# #   Content-Type: application/vnd.sus-calendar
# #   Content-Type: application/vnd.svd
# #   Content-Type: application/vnd.symbian.install
# #   Content-Type: application/vnd.syncml.dm+wbxml
# #   Content-Type: application/vnd.syncml.dm+xml
# #   Content-Type: application/vnd.syncml+xml
# #   Content-Type: application/vnd.tao.intent-module-archive
# #   Content-Type: application/vnd.tmobile-livetv
# #   Content-Type: application/vnd.trid.tpt
# #   Content-Type: application/vnd.triscape.mxs
# #   Content-Type: application/vnd.trueapp
# #   Content-Type: application/vnd.ufdl
# #   Content-Type: application/vnd.uiq.theme
# #   Content-Type: application/vnd.umajin
# #   Content-Type: application/vnd.unity
# #   Content-Type: application/vnd.uoml+xml
# #   Content-Type: application/vnd.vcx
# #   Content-Type: application/vnd.visio
# #   Content-Type: application/vnd.visio2013
# #   Content-Type: application/vnd.visionary
# #   Content-Type: application/vnd.vsf
# #   Content-Type: application/vnd.wap.wbxml
# #   Content-Type: application/vnd.wap.wmlc
# #   Content-Type: application/vnd.wap.wmlscriptc
# #   Content-Type: application/vnd.webturbo
# #   Content-Type: application/vnd.wolfram.player
# #   Content-Type: application/vnd.wordperfect
# #   Content-Type: application/vnd.wqd
# #   Content-Type: application/vnd.wt.stf
# #   Content-Type: application/vnd.xara
# #   Content-Type: application/vnd.xfdl
# #   Content-Type: application/vnd.yamaha.hv-dic
# #   Content-Type: application/vnd.yamaha.hv-script
# #   Content-Type: application/vnd.yamaha.hv-voice
# #   Content-Type: application/vnd.yamaha.openscoreformat
# #   Content-Type: application/vnd.yamaha.openscoreformat.osfpvg+xml
# #   Content-Type: application/vnd.yamaha.smaf-audio
# #   Content-Type: application/vnd.yamaha.smaf-phrase
# #   Content-Type: application/vnd.yellowriver-custom-menu
# #   Content-Type: application/vnd.zul
# #   Content-Type: application/vnd.zzazz.deck+xml
# #   Content-Type: application/voicexml+xml
# #   Content-Type: application/widget
# #   Content-Type: application/winhlp
# #   Content-Type: application/wsdl+xml
# #   Content-Type: application/wspolicy+xml
# #   Content-Type: application/x400-bp
# #   Content-Type: application/x-7z-compressed
# #   Content-Type: application/x-abiword
# #   Content-Type: application/x-ace-compressed
# #   Content-Type: application/x-apple-diskimage
# #   Content-Type: application/x-authorware-bin
# #   Content-Type: application/x-authorware-map
# #   Content-Type: application/x-authorware-seg
# #   Content-Type: application/x-bcpio
# #   Content-Type: application/x-bittorrent
# #   Content-Type: application/x-bzip
# #   Content-Type: application/x-bzip2
# #   Content-Type: application/xcap-diff+xml
# #   Content-Type: application/x-cdlink
# #   Content-Type: application/x-chat
# #   Content-Type: application/x-chess-pgn
# #   Content-Type: application/x-cpio
# #   Content-Type: application/x-csh
# #   Content-Type: application/x-debian-package
# #   Content-Type: application/x-director
# #   Content-Type: application/x-doom
# #   Content-Type: application/x-dtbncx+xml
# #   Content-Type: application/x-dtbook+xml
# #   Content-Type: application/x-dtbresource+xml
# #   Content-Type: application/x-dvi
# #   Content-Type: application/xenc+xml
# #   Content-Type: application/x-font-bdf
# #   Content-Type: application/x-font-ghostscript
# #   Content-Type: application/x-font-linux-psf
# #   Content-Type: application/x-font-otf
# #   Content-Type: application/x-font-pcf
# #   Content-Type: application/x-font-snf
# #   Content-Type: application/x-font-ttf
# #   Content-Type: application/x-font-type1
# #   Content-Type: application/x-font-woff
# #   Content-Type: application/x-futuresplash
# #   Content-Type: application/x-gnumeric
# #   Content-Type: application/x-gtar
# #   Content-Type: application/x-hdf
# #   Content-Type: application/xhtml+xml
# #   Content-Type: application/x-java-jnlp-file
# #   Content-Type: application/x-latex
# #   Content-Type: application/xml
# #   Content-Type: application/xml-dtd
# #   Content-Type: application/x-mobipocket-ebook
# #   Content-Type: application/x-msaccess
# #   Content-Type: application/x-ms-application
# #   Content-Type: application/x-msbinder
# #   Content-Type: application/x-mscardfile
# #   Content-Type: application/x-msclip
# #   Content-Type: application/x-msdownload
# #   Content-Type: application/x-msmediaview
# #   Content-Type: application/x-msmetafile
# #   Content-Type: application/x-msmoney
# #   Content-Type: application/x-mspublisher
# #   Content-Type: application/x-msschedule
# #   Content-Type: application/x-msterminal
# #   Content-Type: application/x-ms-wmd
# #   Content-Type: application/x-ms-wmz
# #   Content-Type: application/x-mswrite
# #   Content-Type: application/x-ms-xbap
# #   Content-Type: application/x-netcdf
# #   Content-Type: application/xop+xml
# #   Content-Type: application/x-pkcs12
# #   Content-Type: application/x-pkcs7-certificates
# #   Content-Type: application/x-pkcs7-certreqresp
# #   Content-Type: application/x-rar-compressed
# #   Content-Type: application/x-sh
# #   Content-Type: application/x-shar
# #   Content-Type: application/x-shockwave-flash
# #   Content-Type: application/x-silverlight-app
# #   Content-Type: application/xslt+xml
# #   Content-Type: application/xspf+xml
# #   Content-Type: application/x-stuffit
# #   Content-Type: application/x-stuffitx
# #   Content-Type: application/x-sv4cpio
# #   Content-Type: application/x-sv4crc
# #   Content-Type: application/x-tar
# #   Content-Type: application/x-tcl
# #   Content-Type: application/x-tex
# #   Content-Type: application/x-texinfo
# #   Content-Type: application/x-tex-tfm
# #   Content-Type: application/x-ustar
# #   Content-Type: application/xv+xml
# #   Content-Type: application/x-wais-source
# #   Content-Type: application/x-x509-ca-cert
# #   Content-Type: application/x-xfig
# #   Content-Type: application/x-xpinstall
# #   Content-Type: application/yang
# #   Content-Type: application/yin+xml
# #   Content-Type: application/zip
# #   Content-Type: audio/32kadpcm
# #   Content-Type: audio/adpcm
# #   Content-Type: audio/basic
# #   Content-Type: audio/midi
# #   Content-Type: audio/mp4
# #   Content-Type: audio/mpeg
# #   Content-Type: audio/ogg
# #   Content-Type: audio/vnd.dece.audio
# #   Content-Type: audio/vnd.digital-winds
# #   Content-Type: audio/vnd.dra
# #   Content-Type: audio/vnd.dts
# #   Content-Type: audio/vnd.dts.hd
# #   Content-Type: audio/vnd.lucent.voice
# #   Content-Type: audio/vnd.ms-playready.media.pya
# #   Content-Type: audio/vnd.nuera.ecelp4800
# #   Content-Type: audio/vnd.nuera.ecelp7470
# #   Content-Type: audio/vnd.nuera.ecelp9600
# #   Content-Type: audio/vnd.rip
# #   Content-Type: audio/webm
# #   Content-Type: audio/x-aac
# #   Content-Type: audio/x-aiff
# #   Content-Type: audio/x-mpegurl
# #   Content-Type: audio/x-ms-wax
# #   Content-Type: audio/x-ms-wma
# #   Content-Type: audio/x-pn-realaudio
# #   Content-Type: audio/x-pn-realaudio-plugin
# #   Content-Type: audio/x-wav
# #   Content-Type: chemical/x-cdx
# #   Content-Type: chemical/x-cif
# #   Content-Type: chemical/x-cmdf
# #   Content-Type: chemical/x-cml
# #   Content-Type: chemical/x-csml
# #   Content-Type: chemical/x-xyz
# #   Content-Type: image/bmp
# #   Content-Type: image/cgm
# #   Content-Type: image/g3fax
# #   Content-Type: image/gif
# #   Content-Type: image/ief
# #   Content-Type: image/jpeg
# #   Content-Type: image/jpeg; name="image001.jpg"
# #   Content-Type: image/jpeg; name="TemptationShortcut.jpg"
# #   Content-Type: image/ktx
# #   Content-Type: image/pjpeg
# #   Content-Type: image/png
# #   Content-Type: image/prs.btif
# #   Content-Type: image/svg+xml
# #   Content-Type: image/tiff
# #   Content-Type: image/vnd.adobe.photoshop
# #   Content-Type: image/vnd.dece.graphic
# #   Content-Type: image/vnd.djvu
# #   Content-Type: image/vnd.dvb.subtitle
# #   Content-Type: image/vnd.dwg
# #   Content-Type: image/vnd.dxf
# #   Content-Type: image/vnd.fastbidsheet
# #   Content-Type: image/vnd.fpx
# #   Content-Type: image/vnd.fst
# #   Content-Type: image/vnd.fujixerox.edmics-mmr
# #   Content-Type: image/vnd.fujixerox.edmics-rlc
# #   Content-Type: image/vnd.ms-modi
# #   Content-Type: image/vnd.net-fpx
# #   Content-Type: image/vnd.wap.wbmp
# #   Content-Type: image/vnd.xiff
# #   Content-Type: image/webp
# #   Content-Type: image/x-citrix-jpeg
# #   Content-Type: image/x-citrix-png
# #   Content-Type: image/x-cmu-raster
# #   Content-Type: image/x-cmx
# #   Content-Type: image/x-freehand
# #   Content-Type: image/x-icon
# #   Content-Type: image/x-pcx
# #   Content-Type: image/x-pict
# #   Content-Type: image/x-png
# #   Content-Type: image/x-portable-anymap
# #   Content-Type: image/x-portable-bitmap
# #   Content-Type: image/x-portable-graymap
# #   Content-Type: image/x-portable-pixmap
# #   Content-Type: image/x-rgb
# #   Content-Type: image/x-xbitmap
# #   Content-Type: image/x-xpixmap
# #   Content-Type: image/x-xwindowdump
# #   Content-Type: message/delivery-status
# #   Content-Type: message/disposition-notification-to
# #   Content-Type: message/external-body
# #   Content-Type: message/http
# #   Content-Type: message/partial
# #   Content-Type: message/rfc822
# #   Content-Type: model/iges
# #   Content-Type: model/mesh
# #   Content-Type: model/vnd.collada+xml
# #   Content-Type: model/vnd.dwf
# #   Content-Type: model/vnd.gdl
# #   Content-Type: model/vnd.gtw
# #   Content-Type: model/vnd.mts
# #   Content-Type: model/vnd.vtu
# #   Content-Type: model/vrml
# #   Content-Type: multipart/alternative;
# #   Content-Type: multipart/alternative; boundary=001a113a2dc6dd3487053f79bc24
# #   Content-Type: multipart/alternative; boundary="001a11456c8817dd1d055d352f8c"
# #   Content-Type: multipart/alternative; boundary="_----056dTAi7CnMb4YC6zcuzcw===_CB/19-64684-8C2612A5"
# #   Content-Type: multipart/alternative; boundary="089e082b9ca8b3811005607e8c7d"
# #   Content-Type: multipart/alternative; boundary=12781cc67c6d4bdc5c62fe572df6f07067ed31bca7176f259611800bc7ed
# #   Content-Type: multipart/alternative; boundary="===============2300963478671213537=="
# #   Content-Type: multipart/alternative; boundary="6kpfp7cF1q82tUL7as8jVsg6vSxX=_GkhV"
# #   Content-Type: multipart/alternative; boundary="cdf82e78-582d-4a55-9037-dacf81ae37d3"
# #   Content-Type: multipart/alternative; boundary="de3m6f=_VUkD4F9LsJ1SCYvVv7MXYQfySv"
# #   Content-Type: multipart/alternative; boundary="__slack_222209002__"
# #   Content-Type: multipart/byteranges; boundary="94eb2c0e6238d7dc6f05607ea548"
# #   Content-Type: multipart/digest; boundary="089e082b9ca8b3811005607e8c7d"
# #   Content-Type: multipart/encrypted; boundary="94eb2c0e6238d7dc6f05607ea548"
# #   Content-Type: multipart/form-data; boundary="94eb2c0e6238d7dc6f05607ea548"
# #   Content-Type: multipart/mixed;
# #   Content-Type: multipart/mixed; boundary=001a113ed43687e70b053d097387
# #   Content-Type: multipart/mixed; boundary="94eb2c0e6238d7dc6f05607ea548"
# #   Content-Type: multipart/mixed-replace; boundary="94eb2c0e6238d7dc6f05607ea548"
# #   Content-Type: multipart/parallel
# #   Content-Type: multipart/related;
# #   Content-Type: multipart/related; boundary="94eb2c0e6238d7dc6f05607ea548"
# #   Content-Type: multipart/report; boundary="94eb2c0e6238d7dc6f05607ea548"
# #   Content-Type: multipart/signed; boundary="94eb2c0e6238d7dc6f05607ea548"
# #   Content-Type: text/calendar
# #   Content-Type: text/css
# #   Content-Type: text/csv
# #   Content-Type: text/enriched
# #   Content-Type: text/html
# #   Content-Type: text/html;
# #   Content-Type: text/html; charset="us-ascii"
# #   Content-Type: text/html; charset="utf-8"
# #   Content-Type: text/html; charset=utf-8
# #   Content-Type: text/html; charset = "utf-8"
# #   Content-Type: text/html; charset="UTF-8"
# #   Content-Type: text/html; charset=UTF-8
# #   Content-Type: text/n3
# #   Content-Type: text/plain
# #   Content-Type: text/plain;
# #   Content-Type: text/plain-bas
# #   Content-Type: text/plain; charset="us-ascii"
# #   Content-Type: text/plain; charset="us-ascii";
# #   Content-Type: text/plain; charset="US-ASCII"; name="test_text_file.txt"
# #   Content-Type: text/plain; charset="utf-8"
# #   Content-Type: text/plain; charset=utf-8
# #   Content-Type: text/plain; charset = "utf-8"
# #   Content-Type: text/plain; charset="UTF-8"
# #   Content-Type: text/plain; charset=UTF-8
# #   Content-Type: text/plain; charset=utf-8; format=flowed
# #   Content-Type: text/plain; charset=windows-1252; format=flowed
# #   Content-Type: text/prs.lines.tag
# #   Content-Type: text/rfc822-headers
# #   Content-Type: text/richtext
# #   Content-Type: text/sgml
# #   Content-Type: text/tab-separated-values
# #   Content-Type: text/troff
# #   Content-Type: text/turtle
# #   Content-Type: text/uri-list
# #   Content-Type: text/vnd.curl
# #   Content-Type: text/vnd.curl.dcurl
# #   Content-Type: text/vnd.curl.mcurl
# #   Content-Type: text/vnd.curl.scurl
# #   Content-Type: text/vnd.fly
# #   Content-Type: text/vnd.fmi.flexstor
# #   Content-Type: text/vnd.graphviz
# #   Content-Type: text/vnd.in3d.3dml
# #   Content-Type: text/vnd.in3d.spot
# #   Content-Type: text/vnd.sun.j2me.app-descriptor
# #   Content-Type: text/vnd.wap.wml
# #   Content-Type: text/vnd.wap.wmlscript
# #   Content-Type: text/x-asm
# #   Content-Type: text/x-c
# #   Content-Type: text/x-fortran
# #   Content-Type: text/x-java-source,java
# #   Content-Type: text/x-markdown; charset="US-ASCII"; name="README.md"
# #   Content-Type: text/x-pascal
# #   Content-Type: text/x-setext
# #   Content-Type: text/x-uuencode
# #   Content-Type: text/x-vcalendar
# #   Content-Type: text/x-vcard
# #   Content-Type: text/yaml
# #   Content-Type: video/3gpp
# #   Content-Type: video/3gpp2
# #   Content-Type: video/h261
# #   Content-Type: video/h263
# #   Content-Type: video/h264
# #   Content-Type: video/jpeg
# #   Content-Type: video/jpm
# #   Content-Type: video/mj2
# #   Content-Type: video/mp4
# #   Content-Type: video/mpeg
# #   Content-Type: video/ogg
# #   Content-Type: video/quicktime
# #   Content-Type: video/vnd.dece.hd
# #   Content-Type: video/vnd.dece.mobile
# #   Content-Type: video/vnd.dece.pd
# #   Content-Type: video/vnd.dece.sd
# #   Content-Type: video/vnd.dece.video
# #   Content-Type: video/vnd.fvt
# #   Content-Type: video/vnd.mpegurl
# #   Content-Type: video/vnd.ms-playready.media.pyv
# #   Content-Type: video/vnd.uvvu.mp4
# #   Content-Type: video/vnd.vivo
# #   Content-Type: video/webm
# #   Content-Type: video/x-f4v
# #   Content-Type: video/x-fli
# #   Content-Type: video/x-flv
# #   Content-Type: video/x-m4v
# #   Content-Type: video/x-ms-asf
# #   Content-Type: video/x-msvideo
# #   Content-Type: video/x-ms-wm
# #   Content-Type: video/x-ms-wmv
# #   Content-Type: video/x-ms-wmx
# #   Content-Type: video/x-ms-wvx
# #   Content-Type: video/x-sgi-movie
# #   Content-Type: x-conference/x-cooltalk
# class ContentTypeHeader(Header):
#     def __init__(self):
#         super().__init__()
#         self.headerType = "CONTENTTYPE"
# 
#     # Content-Type := type "/" subtype *[";" parameter] 
#     # type :=          "application"     / "audio" 
#     #           / "image"           / "message" 
#     #           / "multipart"  / "text" 
#     #           / "video"           / x-token 
#     # x-token := <The two characters "X-" followed, with no 
#     #            intervening white space, by any token> 
#     # subtype := token 
#     # parameter := attribute "=" value 
#     # attribute := token 
#     # value := token / quoted-string 
#     # token := 1*<any CHAR except SPACE, CTLs, or tspecials> 
#     # tspecials :=  "(" / ")" / "<" / ">" / "@"  ; Must be in 
#     #            /  "," / ";" / ":" / "\" / <">  ; quoted-string, 
#     #            /  "/" / "[" / "]" / "?" / "."  ; to use within 
#     #            /  "="                        ; parameter values
#     def parse(self):
#         print( "DEBUG: In Content-Type header parse:" )
#         self.contentTypeStr = None
#         self.contentSubTypeStr = None
#         self.headerOnOneLine = ""
#         for line in self.headers:
#             self.headerOnOneLine += line.strip()
#         self.headerOnOneLine = self.headerOnOneLine[len("Content-Type:"):]
#         for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
#             if( element.startswith( "application" ) ):
#                 self.parseApplicationType()
#                 break
#             elif( element.startswith( "audio" ) ):
#                 self.parseAudioType()
#                 break
#             elif( element.startswith( "chemical" ) ):
#                 self.parseChemicalType()
#                 break
#             elif( element.startswith( "image" ) ):
#                 self.parseImageType()
#                 break
#             elif( element.startswith( "message" ) ):
#                 self.parseMessageType()
#                 break
#             elif( element.startswith( "model" ) ):
#                 self.parseModelType()
#                 break
#             elif( element.startswith( "multipart" ) ):
#                 self.parseMultipartType()
#                 break
#             elif( element.startswith( "text" ) ):
#                 self.parseTextType()
#                 break
#             elif( element.startswith( "video" ) ):
#                 self.parseVideoType()
#                 break
#             elif( element.startswith( "x-conference" ) ):
#                 self.parseXConferenceType()
#                 break
# 
# 
# 
#     def parseApplicationType(self):
#         print( "DEBUG: In Content-Type header parse:" )
#         self.contentTypeStr = "application"
#         for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
#             print( "DEBUG:" )
# 
# 
# 
#     def parseAudioType(self):
#         print( "DEBUG: In Content-Type header parse:" )
#         self.contentTypeStr = "audio"
#         for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
#             print( "DEBUG:" )
# 
# 
# 
#     def parseChemicalType(self):
#         print( "DEBUG: In Content-Type header parse:" )
#         self.contentTypeStr = "chemical"
#         for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
#             print( "DEBUG:" )
# 
# 
# 
#     def parseImageType(self):
#         print( "DEBUG: In Content-Type header parse:" )
#         self.contentTypeStr = "image"
#         for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
#             print( "DEBUG:" )
# 
# 
# 
#     def parseMessageType(self):
#         print( "DEBUG: In Content-Type header parse:" )
#         self.contentTypeStr = "message"
#         for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
#             print( "DEBUG:" )
# 
# 
# 
#     def parseModelType(self):
#         print( "DEBUG: In Content-Type header parse:" )
#         self.contentTypeStr = "model"
#         for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
#             print( "DEBUG:" )
# 
# 
# 
#     def parseMultipartType(self):
#         print( "DEBUG: In Content-Type header parseMultipartType:" )
#         self.contentTypeStr = "multipart"
#         for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
#             print( "DEBUG: In Content-Type header parseMultipartType: element:",element )
#             if( element.startswith( self.contentTypeStr ) ):
#                 t1, t2 = [x.strip() for x in element.split("/")]
#                 self.contentSubTypeStr = t2
#                 print( "DEBUG: In Content-Type header parseMultipartType: element: multipart:",t2 )
#             elif( element.startswith( "boundary" ) ):
#                 t1, t2 = [x.strip() for x in element.split("=")]
#                 self.multipartBoundaryStr = t2
#                 print( "DEBUG: In Content-Type header parseMultipartType: element: boundary:",t2 )
# 
# 
# 
#     def parseTextType(self):
#         print( "DEBUG: In Content-Type header parse:" )
#         self.contentTypeStr = "text"
#         for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
#             print( "DEBUG:" )
# 
# 
# 
#     def parseVideoType(self):
#         print( "DEBUG: In Content-Type header parse:" )
#         self.contentTypeStr = "video"
#         for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
#             print( "DEBUG:" )
# 
# 
# 
#     def parseXConferenceType(self):
#         print( "DEBUG: In Content-Type header parse:" )
#         self.contentTypeStr = "x-conference"
#         for element in [x.strip() for x in self.headerOnOneLine.split(";")]:
#             print( "DEBUG:" )
# 
# 
# 
# # Content-Transfer-Encoding:
# # Content-Transfer-Encoding: quoted-printable
# class ContentTransferEncodingHeader(Header):
#     def __init__(self):
#         super().__init__()
#         self.headerType = "CONTENTTRANSFERENCODING"
# 
#     def parse(self):
#         self.ContentTransferEncodingStr = None
# 
# 
# 
# # Delivered-To:
# class DeliveredToHeader(Header):
#     def __init__(self):
#         super().__init__()
#         self.headerType = "DELIVEREDTO"
# 
#     def parse(self):
#         self.deliveredToStr = None
# 
# 
# 
# MIME-Version:
# class RFC822MimeVersionHeader(Header):
#     def __init__(self):
#         super().__init__()
#         self.headerType = "MIMEVERSION"
# 
#     def parse(self):
#         self.mimeVersionStr = None
# 
# 
# 
# # Acknowledge-To:
# # Also-Control:
# # Alternate-Recipient:
# # Apparently-To:
# # Approved:
# # Article-Names:
# # Article-Updates:
# # Auto-Forwarded:
# # Autoforwarded: [1327]
# # Auto-Submitted:
# # Comments: [822]
# # Confirm-Delivery:
# # Confirm-Reading:
# # Content-Base:
# # Content-Conversion:
# # Content-Description:
# # Content-Disposition:
# # Content-ID:
# # Content-Identifier: [1327]
# # Content-Language:
# # Content-Length: mailbox
# # Content-Location:
# # Content-MD5:
# # Content-Return:
# # Content-SGML-Entity:
# # Control:
# # Conversion: [1327]
# # Conversion-With-Loss: [1327]
# # Deferred-Delivery: [1327]
# # Delivered-By-The-Graces-Of:
# # Delivery-Date: [1327]
# # Discarded-X400-IPMS-Extensions: [1327]
# # Discarded-X400-MTS-Extensions: [1327]
# # Disclose-Recipients:
# # Disposition-Notification-To:
# # Distribution:
# # DL-Expansion-History: [1327]
# # Encoding:
# # Encrypted: [822]
# # Envelope-Recipient:
# # Envelope-Sender:
# # Errors-To:
# # Expires:
# # Expiry-Date: [1327]
# # Fax:
# # Fcc: user
# # Followup-To:
# # For-Comment:
# # For-Handling:
# # Generate-Delivery-Report:
# # Importance: [1327]
# # In-Reply-To: tokens [822]
# # Incomplete-Copy: [1327]
# # Keywords: [822]
# # Language: [1327]
# # Latest-Delivery-Time: [1327]
# # Lines:
# # List-Archive:
# # List-Help:
# # List-ID:
# # List-Owner:
# # List-Subscribe:
# # List-Unsubscribe:
# # Mail-Followup-To: tokens
# # Mail-Reply-To: tokens
# # Mail-System-Version:
# # Mailer:
# # Mailing-List:
# # Message-Type: [1327]
# # Newsgroups:
# # Notice-Requested-Upon-Delivery-To: tokens [spec]
# # Obsoletes: [1327]
# # Organization:
# # Original-Encoded-Information-Types: [1327]
# # Originating-Client:
# # Originator-Info:
# # Originator-Return-Address: [1327]
# # Path:
# # Phone:
# # Precedence:
# # Prevent-Nondelivery-Report:
# # Priority: [1327]
# # Received: tokens [822]
# # References: tokens [822]
# # Reply-By: [1327]
# # Requested-Delivery-Method: [1327]
# # Return-Path: tokens [822]
# # Return-Receipt-To: [info]
# # See-Also:
# # Sensitivity: [1327]
# # Status: mailbox
# # Summary:
# # Supersedes:
# # Telefax:
# # Versions:
# # X-Confirm-Reading-To:
# # X-Mailer:
# # X-MS-Embedded-Report:
# # X-Newsreader:
# # X-PMRQC:
# # X-Priority:
# # X-Sender:
# # X-Status: mailbox
# # X-X-Sender:
# # X400-Content-Return:
# # X400-Content-Type: [1327]
# # X400-MTS-Identifier: [1327]
# # X400-Originator: [1327]
# # X400-Received: [1327]
# # X400-Recipients: [1327]
# # Xref: 
# 
# 
# 
# def main():
#     #emailHeadersLines = []
#     emailHeadersObjects = []
#     emailBodyLines = []
#     emailFilepath = "test_email_003a.eml"
#     file_object  = open(emailFilepath, "r")
#     readingHeaders = True
#     readingBody = False
#     for line in file_object:
#         # print( "DEBUG:", line )
#         line = line.strip('\r\n')
#         if( 0 == len(line) ):
#             readingHeaders = False
#         if( True == readingHeaders ):
#             print( "Line Length:", len(line) )
#             if( line.startswith( "Received:", 0, len("Received:") ) ):
#                 newHeaderObj = ReceivedHeader()
#                 newHeaderObj.appendHeaderLine(line)
#                 emailHeadersObjects.append(newHeaderObj)
#             elif( line.startswith( "From:", 0, len("From:") ) ):
#                 newHeaderObj = FromHeader()
#                 newHeaderObj.appendHeaderLine(line)
#                 emailHeadersObjects.append(newHeaderObj)
#             elif( line.startswith( "To:", 0, len("To:") ) ):
#                 newHeaderObj = ToHeader()
#                 newHeaderObj.appendHeaderLine(line)
#                 emailHeadersObjects.append(newHeaderObj)
#             elif( line.startswith( "Cc:", 0, len("Cc:") ) ):
#                 newHeaderObj = CCHeader()
#                 newHeaderObj.appendHeaderLine(line)
#                 emailHeadersObjects.append(newHeaderObj)
#             elif( line.startswith( "Bcc:", 0, len("Bcc:") ) ):
#                 newHeaderObj = BCCHeader()
#                 newHeaderObj.appendHeaderLine(line)
#                 emailHeadersObjects.append(newHeaderObj)
#             elif( line.startswith( "Sender:", 0, len("Sender:") ) ):
#                 newHeaderObj = SenderHeader()
#                 newHeaderObj.appendHeaderLine(line)
#                 emailHeadersObjects.append(newHeaderObj)
#             elif( line.startswith( "Reply-To:", 0, len("Reply-To:") ) ):
#                 newHeaderObj = ReplyToHeader()
#                 newHeaderObj.appendHeaderLine(line)
#                 emailHeadersObjects.append(newHeaderObj)
#             elif( line.startswith( "Date:", 0, len("Date:") ) ):
#                 newHeaderObj = DateHeader()
#                 newHeaderObj.appendHeaderLine(line)
#                 emailHeadersObjects.append(newHeaderObj)
#             elif( line.startswith( "Subject:", 0, len("Subject:") ) ):
#                 newHeaderObj = SubjectHeader()
#                 newHeaderObj.appendHeaderLine(line)
#                 emailHeadersObjects.append(newHeaderObj)
#             elif( line.startswith( "Message-ID:", 0, len("Message-ID:") ) ):
#                 newHeaderObj = MessageIDHeader()
#                 newHeaderObj.appendHeaderLine(line)
#                 emailHeadersObjects.append(newHeaderObj)
#             elif( line.startswith( "Content-Type:", 0, len("Content-Type:") ) ):
#                 print( "DEBUG: Found a Content-Type header:", line )
#                 newHeaderObj = ContentTypeHeader()
#                 newHeaderObj.appendHeaderLine(line)
#                 emailHeadersObjects.append(newHeaderObj)
#             elif( line.startswith( "Content-Transfer-Encoding:", 0, len("Content-Transfer-Encoding:") ) ):
#                 newHeaderObj = ContentTransferEncodingHeader()
#                 newHeaderObj.appendHeaderLine(line)
#                 emailHeadersObjects.append(newHeaderObj)
#             elif( line.startswith( "Delivered-To:", 0, len("Delivered-To:") ) ):
#                 newHeaderObj = DeliveredToHeader()
#                 newHeaderObj.appendHeaderLine(line)
#                 emailHeadersObjects.append(newHeaderObj)
#             elif( line.startswith( "MIME-Version:", 0, len("MIME-Version:") ) ):
#                 newHeaderObj = MimeVersionHeader()
#                 newHeaderObj.appendHeaderLine(line)
#                 emailHeadersObjects.append(newHeaderObj)
#             elif( line.startswith( " ", 0, len(" ") ) or
#                   line.startswith( "	", 0, len("	") ) ):
#                 emailHeadersObjects[len(emailHeadersObjects)-1].appendHeaderLine(line)
#             else:
#                 newHeaderObj = Header()
#                 newHeaderObj.appendHeaderLine(line)
#                 emailHeadersObjects.append(newHeaderObj)
#         elif( readingBody == True ):
#             emailBodyLines.append(line)
#         else:
#             readingBody = True
# 
#     for hdrObj in emailHeadersObjects:
#         hdrObj.parse()
#                 
#     # print( "Emails Header Lines:", emailHeadersLines)
#     # print( "Emails Body Lines:", emailBodyLines)
#     print( "Emails Header Objects:", emailHeadersObjects)
#     for hdrObj in emailHeadersObjects:
#         print( "  Header Object:", hdrObj )
# 
#     return
# 
# 
# 
# main()
# 
