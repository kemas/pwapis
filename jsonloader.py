import json

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
    apis = {} # api and mashups {id:[degree,name], ...}

    mashups = MashupsJSON(obj)
    items = mashups.get_items()

    for item in items:
        vid = mashups.get_vid(item)

        if not apis.has_key(vid):
            # vid not found, add to the dictionary
            apis[vid] = [0, mashups.get_title(item)]

        if mashups.is_mashup(item):
            # mashup components 
            lscomps = mashups.get_lscompvid(item)
            for compvid in lscomps:
                if not apis.has_key(compvid):
                    # vid not found, add to the dictionary
                    apis[compvid] = [0, mashups.get_title(item)]

                # increment the degree
                apis[compvid][0] += 1

    # build result
    maxdeg = 0; maxdegid = None
    mashupid = apis.keys()
    indegree = []; mashupname = []

    for key in mashupid:
        degree = apis[key][0]

        if degree > maxdeg:
            maxdeg = degree
            maxdegid = key

        indegree.append(degree)
        mashupname.append(apis[key][1])

    # return the degrees as json readable format for pyplot, and max degree id
    return {'indegree':indegree, 'mashupid':mashupid, 'mashupname':mashupname, 'maxindegree':maxdeg, 'maxindegreeid':maxdegid}

def savetofile(ds, filename):
    f = open(filename, 'w')
    try:
        json.dump(ds, f)
    finally:
        f.close()

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

if __name__ == '__main__':
    sys.exit(main(sys.argv))
