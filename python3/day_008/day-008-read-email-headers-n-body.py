#!/usr/bin/env python3

class Header:
    def __init__(self):
        self.headers = []
        self.headersLen = 0
        self.headerType = None

    def __str__(self):
        return self.getFullHeader()

    def __len__(self):
        return headerLen

    def appendHeaderLine(self, line):
        self.headers.append(line)
        self.headers[len(headers)-1] = headers[len(headers)-1].rstrip("\r\n")

    def getFullHeader(self):
        strHeader = ""
        for line in self.headers:
            strHeader.append(line)
            strHeader.append("\n")
        return strHeader




# Received: from
# the name the sending computer gave for itself (the name associated with that computer's IP address [its IP address])
# by
# the receiving computer's name (the software that computer uses) (usually Sendmail, qmail or Postfix)
# with protocol (usually SMTP, ESMTP or ESMTPS)
# id id assigned by local computer for logging;
# timestamp (usually given in the computer's localtime; see below for how you can convert these all to your time)

class ReceivedHeader(Header):
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



class FromHeader(Header):
    def __init__(self):
        super().__init__()
        self.headerType = "FROM"
        self.addressList = None

    def parse(self):
        self.addressList = None



class ToHeader(Header):
    def __init__(self):
        super().__init__()
        self.headerType = "TO"
        self.addressList = None

    def parse(self):
        self.addressList = None



class CCHeader(Header):
    def __init__(self):
        super().__init__()
        self.headerType = "CC"
        self.addressList = None

    def parse(self):
        self.addressList = None



class BCCHeader(Header):
    def __init__(self):
        super().__init__()
        self.headerType = "BCC"
        self.addressList = None

    def parse(self):
        self.addressList = None



class SenderHeader(Header):
    def __init__(self):
        super().__init__()
        self.headerType = "SENDER"
        self.addressList = None

    def parse(self):
        self.addressList = None



class ReplyToHeader(Header):
    def __init__(self):
        super().__init__()
        self.headerType = "REPLYTO"
        self.addressList = None

    def parse(self):
        self.addressList = None



class DateHeader(Header):
    def __init__(self):
        super().__init__()
        self.headerType = "DATE"

    def parse(self):



class SubjectHeader(Header):
    def __init__(self):
        super().__init__()
        self.headerType = "SUBJECT"

    def parse(self):



class MessageIDHeader(Header):
    def __init__(self):
        super().__init__()
        self.headerType = "MESSAGEID"

    def parse(self):



# Acknowledge-To:
# Also-Control:
# Alternate-Recipient:
# Apparently-To:
# Approved:
# Article-Names:
# Article-Updates:
# Auto-Forwarded:
# Autoforwarded: [1327]
# Auto-Submitted:
# Bcc: user tokens [822]
# Cc: tokens [822]
# Comments: [822]
# Confirm-Delivery:
# Confirm-Reading:
# Content-Base:
# Content-Conversion:
# Content-Description:
# Content-Disposition:
# Content-ID:
# Content-Identifier: [1327]
# Content-Language:
# Content-Length: mailbox
# Content-Location:
# Content-MD5:
# Content-Return:
# Content-SGML-Entity:
# Content-Transfer-Encoding:
# Content-Type:
# Control:
# Conversion: [1327]
# Conversion-With-Loss: [1327]
# Date: tokens [822]
# Deferred-Delivery: [1327]
# Delivered-By-The-Graces-Of:
# Delivered-To:
# Delivery-Date: [1327]
# Discarded-X400-IPMS-Extensions: [1327]
# Discarded-X400-MTS-Extensions: [1327]
# Disclose-Recipients:
# Disposition-Notification-To:
# Distribution:
# DL-Expansion-History: [1327]
# Encoding:
# Encrypted: [822]
# Envelope-Recipient:
# Envelope-Sender:
# Errors-To:
# Expires:
# Expiry-Date: [1327]
# Fax:
# Fcc: user
# Followup-To:
# For-Comment:
# For-Handling:
# From: tokens [822]
# Generate-Delivery-Report:
# Importance: [1327]
# In-Reply-To: tokens [822]
# Incomplete-Copy: [1327]
# Keywords: [822]
# Language: [1327]
# Latest-Delivery-Time: [1327]
# Lines:
# List-Archive:
# List-Help:
# List-ID:
# List-Owner:
# List-Subscribe:
# List-Unsubscribe:
# Mail-Followup-To: tokens
# Mail-Reply-To: tokens
# Mail-System-Version:
# Mailer:
# Mailing-List:
# Message-ID: tokens [822]
# Message-Type: [1327]
# MIME-Version:
# Newsgroups:
# Notice-Requested-Upon-Delivery-To: tokens [spec]
# Obsoletes: [1327]
# Organization:
# Original-Encoded-Information-Types: [1327]
# Originating-Client:
# Originator-Info:
# Originator-Return-Address: [1327]
# Path:
# Phone:
# Precedence:
# Prevent-Nondelivery-Report:
# Priority: [1327]
# Received: tokens [822]
# References: tokens [822]
# Reply-By: [1327]
# Reply-To: tokens [822]
# Requested-Delivery-Method: [1327]
# Return-Path: tokens [822]
# Return-Receipt-To: [info]
# See-Also:
# Sender: tokens [822]
# Sensitivity: [1327]
# Status: mailbox
# Subject: [822]
# Summary:
# Supersedes:
# Telefax:
# To: tokens [822]
# Versions:
# X-Confirm-Reading-To:
# X-Mailer:
# X-MS-Embedded-Report:
# X-Newsreader:
# X-PMRQC:
# X-Priority:
# X-Sender:
# X-Status: mailbox
# X-X-Sender:
# X400-Content-Return:
# X400-Content-Type: [1327]
# X400-MTS-Identifier: [1327]
# X400-Originator: [1327]
# X400-Received: [1327]
# X400-Recipients: [1327]
# Xref: 



def main():
    emailHeadersLines = []
    emailBodyLines = []
    emailFilepath = "test_email_001.eml"
    file_object  = open(emailFilepath, "r")
    #lasttell = -1
    #currenttell = file_object.tell()
    readingHeaders = True
    readingBody = False
    #while( currenttell > lasttell ):
    for line in file_object:
        #line = file_object.readline()
        #print( "DEBUG:", currenttell, lasttell, line )
        print( "DEBUG:", line )
        line = line.strip('\n')
        line = line.strip('\r')
        #lasttell = currenttell
        #currenttell = file_object.tell()
        #if( currenttell > lasttell ):
        if( 0 == len(line) ):
            readingHeaders = False
        if( True == readingHeaders ):
            emailHeadersLines.append(line)
        elif( True == readingBody ):
            emailBodyLines.append(line)
        else:
            readingBody = True
                
    print( "Emails Header Lines:", emailHeadersLines)
    print( "Emails Body Lines:", emailBodyLines)

    return



main()

