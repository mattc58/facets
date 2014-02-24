'''
This is the main function for the Python facet server. It will
load the data from the specified file and then start the Tornado server.
'''
import sys
import argparse
import json
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def main():
    # verify that we have the input file specified
    parser = argparse.ArgumentParser(description='Facet server, in Python')
    parser.add_argument('-i', '--inputfile', required=True, help='the input JSON file')
    parser.add_argument('-p', '--port', default=8888, type=int, help='the webserver port to use')

    args = parser.parse_args()
    
    # let's get the data loaded
    pass

    # now let's start the webserver
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(args.port)

    print "Facet Server listening at port ", args.port
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()


