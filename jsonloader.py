import json

class MashupsJSON:
    ID_ATTRIBUTES = 1
    ID_TARGETS = 2
    ID_ENDPOINTS = 3
    ID_MASHUPURLS = 4

    def __init__(self, obj):
        self._obj = obj
        self._items = obj[1]

    def get_items(self):
        return self._items

    def get_item(self, idx):
        return self._items[idx]

    def get_vid(self, item):
        return item[ID_ATTRIBUTES]['vid']

    def get_title(self, item):
        return item[ID_ATTRIBUTES]['title'].replace('\/', '/')

    def is_mashup(self, item):
        return item[ID_ATTRIBUTES]['type'] == 'mashup'

    def get_lscompvid(self, item):
        # only when type == 'mashup' (!= 'api')

        ls = []
        for t in item[ID_TARGETS][1:]:
            ls.append(t[1])
        return ls

    def get_lsendpoint(self, item):
        ls = []
        for t in item[ID_ENDPOINTS][1:]:
            try:
                ls.append(t[1])
            except IndexError:
                # IndexError means the item has no endpoint info
                pass
        return ls

    def get_lsmashupurls(self, item):
        ls = []
        for t in item[ID_MASHUPURLS][1:]:
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
    apis = {} # api and mashups {id:degree, ...}

    mashups = MashupsJSON(obj)
    items = mashups.get_items()

    for item in items:
        vid = mashups.get_vid(item)

        if not apis.has_key(vid):
            # vid not found, add to the dictionary
            apis[vid] = 0

        if mashups.is_mashup(item):
            # mashup components 
            lscomps = mashups.get_lscompvid()
            for compvid in lscomps:
                if not apis.has_key(compvid):
                    # vid not found, add to the dictionary
                    apis[compvid] = 0

                # increment the degree
                apis[compvid] += 1

    # transform to list

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
#
#if __name__ == '__main__':
#    sys.exit(main(sys.argv))
