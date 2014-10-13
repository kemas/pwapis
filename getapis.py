import sys
import requests
#from lxml import etree
#from io import BytesIO

OPT_APIS = '-a'
OPT_MASHUPS = '-m'
OPT_USERS = '-u'
OPT_OUTFILE = '-f'
OPT_APIKEY = '-k'
OPT_LIMIT = '-l'
OPT_KEYWORDS = '-q'
OPT_SHOWRESP = '-s'
OPT_OFFSET = '-o'
OPT_NOINPUT = (OPT_APIS, OPT_MASHUPS, OPT_USERS, OPT_SHOWRESP)
OPTS = (OPT_APIS, OPT_MASHUPS, OPT_USERS, OPT_OUTFILE, OPT_APIKEY, OPT_LIMIT, OPT_KEYWORDS, OPT_SHOWRESP, OPT_OFFSET)

APIKEY = 'Lfc9J7ZjRSdkU7ZrEn4kyACRkQK6uLTC'
URL_GETAPIS = 'http://www.programmableweb.com/pw-api/views/query_apis'
URL_GETMASHUPS = 'http://www.programmableweb.com/pw-api/views/query_mashups'
URL_GETUSERS = 'http://www.programmableweb.com/pw-api/views/query_users'
FILENAME = 'pwapi.xml'

def savetofile(content, fout=None):
    # save the whole result to the file fout

    f = open(fout or FILENAME, 'wb')
    try:
        f.write(content)
    finally:
        f.close()

def printusage():
    print "Usage: python getapis.py [-a|-m|-u] [OPTIONS]"
    #print "Example: python getapis.py -a avgfile.json -f data1.json data2.json -c field1 field2"
    sys.exit()

def readargv(argv, pos=1, opt='', dictarg={}):
#    print 'pos: %d' % pos
#    print 'len: %d' % len(argv)
    if pos >= len(argv):
        return {}

    currarg = argv[pos]
    if currarg[0] == '-':
        if currarg not in OPTS:
            printusage()

        if currarg in OPT_NOINPUT:
            # the option expects no parameter, add to dictarg
            dictarg[currarg] = None

        # read the option's parameter
        readargv(argv, pos + 1, currarg, dictarg)

    else:
#        if dictarg.has_key(opt):
#            # add value for multiple values option (if any)
#            dictarg[opt].append(currarg)
#        else:
#            dictarg[opt] = [currarg]
        dictarg[opt] = currarg
        readargv(argv, pos + 1, opt, dictarg)

    return dictarg

def getargval(dictarg, key, ifnone=None):
    if dictarg.has_key(key):
        return dictarg[key]
    else:
        return ifnone

def main(argv):
    dictarg = readargv(argv)
#    print dictarg ###
    params = {'api-key': getargval(dictarg, OPT_APIKEY, APIKEY)}

    if dictarg.has_key(OPT_MASHUPS):
        opt_mode = dictarg.pop(OPT_MASHUPS)
#        params['display_id'] = 'mashup'
        url = URL_GETMASHUPS

    elif dictarg.has_key(OPT_USERS):
        opt_mode = dictarg.pop(OPT_USERS)
        params['display_id'] = 'services_member_details'
        url = URL_GETUSERS

    else:
        opt_mode = OPT_APIS
        params['display_id'] = 'api'
        url = URL_GETAPIS

    if dictarg.has_key(OPT_LIMIT):
        params['limit'] = getargval(dictarg, OPT_LIMIT)

    if dictarg.has_key(OPT_OFFSET):
        params['offset'] = getargval(dictarg, OPT_OFFSET)

#    print params ###

    r = requests.get(url, params=params)
    print '* URL: %s' % r.url
    
    if dictarg.has_key(OPT_SHOWRESP):
        print '* Response:'
        print r.text
    else:
        savetofile(r.content, getargval(dictarg, OPT_OUTFILE))

#    tree = etree.parse(BytesIO(r.content))
#    x = tree.xpath('/result/openSearch_totalResults')
#    print '* Number of records: %s' % x[0].text
#
#    #getrequests(getargval(dictarg, ''), params)
#    #average(getargval(dictarg, '-a')[0], files=getargval(dictarg, '-f'), fields=getargval(dictarg, '-c'))

if __name__ == '__main__':
    sys.exit(main(sys.argv))

