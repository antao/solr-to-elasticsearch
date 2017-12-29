# solr-to-elasticsearch


## Usage
```
usage: src [-h] [--pagesize PAGESIZE] [--timeout TIMEOUT] 
           solr_url elasticsearch_url elasticsearch_index elasticsearch_doctype
```

`--pagesize` defaults to `500`

`--timeout` defaults to `60`


```bash
solr-to-elasticsearch.py https://localhost:8080/searcher/#/core/ https://localhost:9200/ elastic_index document_type
```

## Notes
Could not use solr deep paging because version in use is < 4.6 
