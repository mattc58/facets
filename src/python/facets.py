import json
import os

class FacetStore(object):
    '''
    This is the storage class for our documents and our facets
    '''
    def __init__(self):
        super(FacetStore, self).__init__()
        self._all_docs = {}
        self._indices = {'geo_c' : {}, 'geo_city' : {}, 'ip' : {}, 'name' : {}, 'port' : {}}

    def load_data(self, infile):
        '''
        Load the data from the given file
        Sample incoming JSON dict:
        { "_id" : { "ip" : "173.254.69.102", "p" : 22, "h" : "440ac8ebaa6ea38e2a542d54fe1065e8" }, "ip" : "173.254.69.102", "port" : 22, "proto" : "tcp", "banner" : "SSH-2.0-OpenSSH_5.3\r\n\\x00", "geo" : { "c" : "USA", "city" : "Provo", "reg" : "UT", "loc" : [ 40.21810150146484, -111.6132965087891 ] }, "name" : "ssh", "t" : { "$date" : 1359698414000 } }}
        '''
        with open(infile) as f:
            for line in f:
                try:
                    data = json.loads(line)
                except:
                    continue
                if '_id' not in data:
                    continue

                h = data['_id'].get('h')
                if not h:
                    continue

                self._all_docs[h] = data
                for field in self._indices.keys():
                    # and here's where a bloom filter would help
                    if field.startswith('geo'):
                        if 'geo' in data and data['geo']:
                            source = data['geo'].get(field[4:])
                        else:
                            continue
                    else:
                        source = data.get(field)
                    if source:
                        source = unicode(source)
                        if source not in self._indices[field]:
                            self._indices[field][source] = []
                        self._indices[field][source].append(h)


    @property
    def number_docs(self):
        return len(self._all_docs)

    def get_results(self, query, size):
        '''
        Perform this query on the docs and return
        '''
        results = []

        # for now we're just supporting ANDs
        match_sets = []
        for term, value in query:
            term = unicode(term)
            # make sure we recognize the search term (the field)
            if term not in self._indices:
                continue

            # search in that index to get the list of documents that match
            match = self._indices[term].get(value, [])
            match_sets.append(set(match))

        # now we have our match sets. Since we're ANDing we need to intersect these.
        hashes = set.intersection(*match_sets)

        # we know which hashes we need
        results = [self._all_docs.get(item) for item in hashes]
        return results[:size]


    def get_facets(self, query, requested_facets):
        '''
        Perform the query and return the facets
        '''
        return {}


