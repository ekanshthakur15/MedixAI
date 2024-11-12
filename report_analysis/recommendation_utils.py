import json

from django.conf import settings
from elasticsearch import Elasticsearch, exceptions

# Initialize Elasticsearch client
es = Elasticsearch(
    "https://127.0.0.1:9200",
    basic_auth=("elastic", settings.ELASTICSEARCH_PASSOWRD),
    ca_certs="/Users/ekanshthakur/elasticsearch-8.15.3/config/certs/http_ca.crt")

# Name of the index where articles will be stored
INDEX_NAME = 'articles'


def create_index():
    """
    Create the Elasticsearch index if it doesn't exist.
    """
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME)
        print(f"Index '{INDEX_NAME}' created.")
    else:
        print(f"Index '{INDEX_NAME}' already exists.")


def index_articles(articles):
    """
    Index a list of articles (in JSON format) into Elasticsearch.
    Each article must be a dictionary with 'title', 'tags', and 'content'.
    """
    for idx, article in enumerate(articles):
        try:
            es.index(index=INDEX_NAME, id=idx, body=article)
            print(f"Article indexed with ID {idx}")
        except exceptions.ElasticsearchException as e:
            print(f"Error indexing article: {e}")


def search_articles(query):
    """
    Search for articles based on the query string.
    Returns a list of articles matching the query.
    """
    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "tags", "content"]
            }
        }
    }
    response = es.search(index=INDEX_NAME, body=search_body)
    articles = [hit["_source"] for hit in response['hits']['hits']]
    return articles
