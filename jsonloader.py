import sys
import json
import unicodecsv

class MashupsJSON:
    def __init__(self, obj):
        self._ID_ATTRIBUTES = 1
        self._ID_TARGETS = 2
        self._ID_ENDPOINTS = 3
        self._ID_MASHUPURLS = 4

        self._obj = obj
        self._items = obj[1:]

    def get_items(self):
        return self._items

    def get_item(self, idx):
        return self._items[idx]

    def get_vid(self, item):
        return item[self._ID_ATTRIBUTES]['vid']

    def get_title(self, item):
        return item[self._ID_ATTRIBUTES]['title']

    def is_mashup(self, item):
        return item[self._ID_ATTRIBUTES]['type'] == 'mashup'

    def get_lscompvid(self, item):
        # only when type == 'mashup' (!= 'api')

        ls = []
        for t in item[self._ID_TARGETS][1:]:
            ls.append(t[1])
        return ls

    def get_lsendpoint(self, item):
        ls = []
        for t in item[self._ID_ENDPOINTS][1:]:
            try:
                ls.append(t[1])
            except IndexError:
                # IndexError means the item has no endpoint info
                pass
        return ls

    def get_lsmashupurls(self, item):
        ls = []
        for t in item[self._ID_MASHUPURLS][1:]:
            try:
                ls.append(t[1])
            except IndexError:
                # IndexError means the item has no mashupurls info
                pass
        return ls

def load(filename):
    with open(filename) as f:
        obj = json.load(f)

    return obj

def readdeg(obj):
    apis = {} # api and mashups {id:[indegree, outdegree, name, [parent, ...], [child, ...]], ...}

    mashups = MashupsJSON(obj)
    items = mashups.get_items()
#    children = {} # {childid:[parentid, ...], ...}

    for item in items:
        vid = mashups.get_vid(item)

        if not apis.has_key(vid):
            # vid not found, add to the dictionary
            apis[vid] = [0, 0, mashups.get_title(item), [], []]
        elif not apis[vid][2]:
            # vid is in the dictionary but name/title is not defined
            apis[vid][2] = mashups.get_title(item)

        if mashups.is_mashup(item):
            # mashup components 
            lscomps = mashups.get_lscompvid(item)
            # increment the outdegree
            apis[vid][1] += len(lscomps)

            for compvid in lscomps:
#                # add compvid to children if does not exist
#                if not children.has_key(compvid):
#                    children[compvid] = []
#                # add vid to the child's parent list
#                children[compvid].append(vid)

                if not apis.has_key(compvid):
                    # compvid not found, add to the dictionary
                    apis[compvid] = [0, 0, None, [], []]

                # increment the indegree
                apis[compvid][0] += 1

                # add compvid's parent
                apis[compvid][3].append(vid)
                # add vid's child
                apis[vid][4].append(compvid)

    # build result
    maxdeg = 0; maxdegid = None
    mashupid = apis.keys()
    indegree = []
    outdegree = []
    mashupname = []
    depth = {} # vid:[depth, meandepth]
    maxdepth = 0; avgdepth = 0.0
    avgmeandepth = 0.0

    for key in mashupid:
        ind = apis[key][0]

        if ind > maxdeg:
            maxdeg = degree
            maxdegid = key

        indegree.append(ind)
        outdegree.append(apis[key][1])
        mashupname.append(apis[key][2])

        if not depth.has_key(key):
            # calculate depth recursively to parents and children
            pass

    # return the degrees as json readable format for pyplot, and max degree id
    return {'indegree':indegree
        , 'outdegree':outdegree
        , 'mashupid':mashupid
        , 'mashupname':mashupname
        , 'maxindegree':maxdeg
        , 'maxindegreeid':maxdegid
        , 'depth':depth.values()
        , 'maxdepth':maxdepth
        , 'avgdepth':avgdepth
        , 'meandepth':meandepth
        , 'avgmeandepth':avgmeandepth}

### depth

def savetofile(ds, filename):
    with open(filename, 'w') as f:
        json.dump(ds, f)

#def gethubs(thold, indegrees):
#    ls = []; lsidx = []
#
#    i = 0
#    for deg in indegrees:
#        if deg >= thold:
#            ls.append(deg)
#            lsidx.append(i)
#        
#        i += 1
#
#    return ls, lsidx

def dstocsv(ds, filename):
    with open(filename, 'w') as f:
        csvwr = unicodecsv.UnicodeWriter(f)
        for i in range(len(ds['mashupid'])):
            row = [ds['mashupid'][i], ds['mashupname'][i] or '', str(ds['indegree'][i])]
            print row
            csvwr.writerow(row)

def main(argv):
    fmashupsjson = argv[1]
    foutjson = argv[2]

    obj = load(fmashupsjson)
    ds = readdeg(obj)
    savetofile(ds, foutjson)

    if len(argv) > 3:
        foutcsv = argv[3]
        dstocsv(ds, foutcsv)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
