'''
This is the main function for the Python facet server. It will
load the data from the specified file and then start the Tornado server.
'''
import sys
import argparse
import json
import tornado.ioloop
import tornado.web
from facets import FacetStore

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("<h1>Facets</h1><p>Hi, please use <a href='/query/'>/query/</a> to query the facet store or <a href='/status/'>/status/</a> to see some stats.")

class QueryHandler(tornado.web.RequestHandler):
    '''
    This handles the requested queries
    '''
    def initialize(self, facet_store=None):
        self._facet_store = facet_store

    def get(self):
        '''
        Process the query. Keep it simple for now:
            no parameters: show the top 100 results
            ?q=field1:val1+field2:val2+field3:val3
            ?facets=[field1,field2,field3]: facet on these fields
        '''
        query = self.get_argument('q', default=None)
        facets = self.get_argument('facets', default=None)

        # first get the raw docs as asked for by the query
        results = self._facet_store.get_results(query)

        # now get the facets
        facet_resullts = self._facet_store.get_facets(results, facets)

        # turn into a dict and return
        response = {'num_results' : len(results), 'results' : results, 'facets' : facet_resullts}
        self.write(response)


class StatusHandler(tornado.web.RequestHandler):
    '''
    This will show some basic stats
    '''
    def initialize(self, facet_store=None):
        self._facet_store = facet_store
        
    def get(self):
        self.write("<h1>Status</h1><ul><li>Total Docs=%d</li>" % (self._facet_store.number_docs))

def main():
    '''
    Main function. Load the data from the specified and then start the app server
    '''
    # verify that we have the input file specified
    parser = argparse.ArgumentParser(description='Facet server, in Python')
    parser.add_argument('-i', '--inputfile', required=True, help='the input JSON file')
    parser.add_argument('-p', '--port', default=8888, type=int, help='the webserver port to use')

    args = parser.parse_args()
    
    # let's get the data loaded
    fs = FacetStore()
    fs.load_data(args.inputfile)

    # now let's start the webserver
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/query/", QueryHandler, {'facet_store' : fs}),
        (r"/status/", StatusHandler, {'facet_store' : fs})
    ], debug=True)
    application.listen(args.port)

    print "Facet Server listening at port %d with %d docs loaded" % (args.port, fs.number_docs)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()


