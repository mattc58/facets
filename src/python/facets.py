import json
import os

class FacetStore(object):
    '''
    This is the storage class for our documents and our facets
    '''
    def __init__(self):
        super(FacetStore, self).__init__()
        self._all_docs = {}
        self._indices = {}

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
                    print "exception!"
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
                        if source not in self._indices[field]:
                            self._indices[field][source] = []
                        self._indices[field][source].append(h)

    @property
    def number_docs(self):
        return len(self._all_docs)

    def get_results(self, query):
        '''
        Perform this query on the docs and return
        '''
        return self._all_docs

    def get_facets(self, query, requested_facets):
        '''
        Perform the query and return the facets
        '''
        return {}


