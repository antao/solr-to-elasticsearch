#!/usr/bin/python3
''' Simple script to allow data export from solr cores to elasticsearch indexes '''

import argparse
import json
from itertools import islice, count
import uuid
import pysolr

from progress.bar import Bar
from elasticsearch import Elasticsearch

def parse_args():
    ''' Parse input arguments '''
    parser = argparse.ArgumentParser()
    parser.add_argument('solr_url', type=str)
    parser.add_argument('elasticsearch_url', type=str)
    parser.add_argument('elasticsearch_index', type=str)
    parser.add_argument('elasticsearch_doctype', type=str)
    parser.add_argument('--pagesize', type=int, default=500)
    parser.add_argument('--timeout', type=int, default=60)
    return vars(parser.parse_args())

def create_elastic_index(elastic, index_name):
    ''' Create an elastic index '''
    if elastic.indices.exists(index_name):
        print("Deleting '%s' index." % (index_name))
        print(elastic.indices.delete(index_name, [400, 404]))
    print("Creating '%s' index." % (index_name))
    print(elastic.indices.create(index_name))
    return

def main():
    ''' Main '''
    try:
        args = parse_args()
        elastic = Elasticsearch(args['elasticsearch_url'])
        solr = pysolr.Solr(args['solr_url'], timeout=args['timeout'])
        query = solr.search(q='*:*', rows=0, fl='numFound')
        create_elastic_index(elastic, args['elasticsearch_index'])
        progress_bar = Bar('Indexing', max=query.hits, suffix='%(index)d/%(max)d - %(percent).1f%% - %(eta)ds')
        for i in islice(count(), 0, query.hits, args['pagesize']):
            solr_response = solr.search(q='*:*', start=i, rows=args['pagesize'])
            data = []
            for document in solr_response.docs:
                progress_bar.next()
                data.append('{"index": {"_id":"%s"}}\n %s \n' % (uuid.uuid4(), json.dumps(document)))
            elastic.bulk(index=args['elasticsearch_index'], doc_type=args['elasticsearch_doctype'], body=''.join(data))
        progress_bar.finish()
    except KeyboardInterrupt:
        print('Interrupted')

if __name__ == "__main__":
    main()
