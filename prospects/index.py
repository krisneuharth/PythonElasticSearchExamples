from elasticsearch import Elasticsearch

from prospects.prospect import Prospect
from prospects.settings import (
    ES_INDEX, ES_DOC_TYPE,
    ES_DOC_COUNT, VERBOSE
)


# Create our Elastic Search client
es = Elasticsearch()


def index_prospect(prospect):
    """
    Index the given Prospect in Elastic Search
    :param prospect
    """

    try:
        if VERBOSE:
            print prospect
        else:
            print '.',

        es.index(
            index=ES_INDEX,
            doc_type=ES_DOC_TYPE,
            id=prospect.id,
            body=prospect.as_dict()
        )
    except Exception as e:
        # Don't care for demo purposes
        pass


if __name__ == "__main__":
    """
    Test Driver
    """

    # In case we had one already from a previous import
    print 'Dropping index...'
    es.indices.delete(index=ES_INDEX, ignore=[400, 404])

    # Create the index anew
    print 'Creating new index...'
    es.indices.create(index=ES_INDEX, ignore=400)

    # Generate and index the prospects
    print 'Generating and indexing...'
    for id in range(1000, ES_DOC_COUNT * 100):
        pp = Prospect(id)
        index_prospect(pp)

    # Refresh the index
    print '\n\nRefreshing the index...'
    es.indices.refresh(index=ES_INDEX)

    # Find out how many we imported
    count = str(es.count(index=ES_INDEX)['count'])

    print 'Done.\n'

    print 'Imported documents: %s\n' % count
