from elasticsearch import Elasticsearch, helpers
from config.global_config import config_harvester
from project.server.main.logger import get_logger

client = None
logger = get_logger(__name__)


def get_client():
    global client
    if client is None:
        client = Elasticsearch(config_harvester["ES_URL"], http_auth=(config_harvester["ES_LOGIN_BSO_BACK"],
                                                                      config_harvester["ES_PASSWORD_BSO_BACK"]))
    return client


def get_doi_not_in_index(index, dois):
    es = get_client()
    results = es.search(
        index=index,
        body={"query": {"bool": {"filter": [{'terms': {'doi.keyword': dois}}]}}, "fields": ['doi'], "size": len(dois),
              "_source": False},
        request_timeout=60 * 5
    )
    existing_dois = set([e['fields']['doi'][0] for e in results['hits']['hits']])
    not_indexed_dois = set(dois) - existing_dois
    res = []
    for doi in list(not_indexed_dois):
        res += get_doi_not_in_index_one(index, doi)
    logger.debug(f'{len(res)} dois not in index detected')
    return res


def get_doi_not_in_index_one(index, doi):
    es = get_client()
    results = es.search(
        index=index,
        request_cache=False,
        body={"query": {"bool": {"filter": [{'term': {'doi.keyword': doi}}]}}, "fields": ['doi'], "_source": True},
        request_timeout=60 * 5
    )
    existing_dois = set([e['fields']['doi'][0] for e in results['hits']['hits']])
    not_indexed_dois = set([doi]) - existing_dois
    return list(not_indexed_dois)


def update_local_affiliations(index, current_dois, local_affiliations):
    es = get_client()
    logger.debug(f'updating with local affiliations {local_affiliations} for {len(current_dois)} dois')
    body = {
        "script": {
            "lang": "painless",
            "refresh": True,
            "conflicts": "proceed",
            "inline": "if (ctx._source.bso_local_affiliations == null) {ctx._source.bso_local_affiliations ="
                      " new ArrayList();} ctx._source.bso_local_affiliations.addAll(params.local_affiliations);"
                      "ctx._source.bso_local_affiliations = ctx._source.bso_local_affiliations.stream().distinct()"
                      ".sorted().collect(Collectors.toList())",
            "params": {"local_affiliations": local_affiliations}
        },
        "query": {
            "bool": {
                "filter": [{
                    "terms": {
                        "doi.keyword": current_dois
                    }
                }]
            }
        }
    }
    es.update_by_query(index=index, body=body, request_timeout=60 * 5)


def delete_index(index: str) -> None:
    logger.debug(f'Deleting {index}')
    es = get_client()
    response = es.indices.delete(index=index, ignore=[400, 404])
    logger.debug(response)


def update_alias(alias: str, old_index: str, new_index: str) -> None:
    es = get_client()
    logger.debug(f'updating alias {alias} from {old_index} to {new_index}')
    response = es.indices.update_aliases({
        'actions': [
            {'remove': {'index': old_index, 'alias': alias}},
            {'add': {'index': new_index, 'alias': alias}}
        ]
    })
    logger.debug(response)


def get_analyzers() -> dict:
    return {
        'light': {
            'tokenizer': 'icu_tokenizer',
            'filter': [
                'lowercase',
                'french_elision',
                'icu_folding'
            ]
        }
    }


def get_filters() -> dict:
    return {
        'french_elision': {
            'type': 'elision',
            'articles_case': True,
            'articles': ['l', 'm', 't', 'qu', 'n', 's', 'j', 'd', 'c', 'jusqu', 'quoiqu', 'lorsqu', 'puisqu']
        }
    }


def reset_index(index: str) -> None:
    es = get_client()
    delete_index(index)

    settings = {
        'analysis': {
            'filter': get_filters(),
            'analyzer': get_analyzers()
        }
    }

    dynamic_match = None
    if 'bso-publications' in index:
        # dynamic_match = "*oa_locations"
        dynamic_match = None
    elif 'publications-' in index:
        dynamic_match = "*authors"

    mappings = {'properties': {}}
    # attention l'analyzer .keyword ne sera pas présent pour ce champs !
    for f in ['z_authors.family', 'z_authors.given', 'title', 'journal_name', 'keywords.keyword',
              'affiliations.name', 'authors.first_name', 'authors.last_name', 'authors.full_name',
              'authors.affiliations.name', 'title_first_author']:
        mappings['properties'][f] = {
            'type': 'text',
            'analyzer': 'light'
        }

    if dynamic_match:
        mappings["dynamic_templates"] = [
            {
                "objects": {
                    "match": dynamic_match,
                    "match_mapping_type": "object",
                    "mapping": {
                        "type": "nested"
                    }
                }
            }
        ]
    response = es.indices.create(
        index=index,
        body={'settings': settings, 'mappings': mappings},
        ignore=400  # ignore 400 already exists code
    )
    if 'acknowledged' in response and response['acknowledged']:
        response = str(response['index'])
        logger.debug(f'Index mapping success for index: {response}')


def load_in_es(data: list, index: str) -> list:
    es = get_client()
    actions = [{'_index': index, '_source': datum} for datum in data]
    ix = 0
    indexed = []
    for success, info in helpers.parallel_bulk(client=es, actions=actions, chunk_size=500, request_timeout=60,
                                               raise_on_error=False):
        if not success:
            logger.debug(f'A document failed: {info}')
        else:
            indexed.append(data[ix])
        ix += 1
    logger.debug(f'{len(data)} elements imported into {index}')
    return indexed