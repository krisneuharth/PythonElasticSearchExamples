from elasticsearch import Elasticsearch
from prospects.prospect import Prospect
from prospects.settings import (
    ES_INDEX, ES_DOC_TYPE
)

import json


# Create our Elastic Search client
es = Elasticsearch()


# http://elasticsearch-py.readthedocs.org/en/latest/api.html

#
# Basic examples from the docs
#


def print_r(msg, response):
    """
    Helper to view the responses
    """

    print '%s:\n%s\n' % (
        msg,
        json.dumps(response, indent=2)
    )


def create_prospect():
    """
    Create a prospect in the index
    """

    prospect = Prospect(111)

    response = es.create(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        id=prospect.id,
        body=prospect.as_dict(),
        refresh=True
    )

    print_r('Created', response)


def update_prospect():
    """
    Update a prospect in the index
    """

    body = '''
    {
        "doc": {
            "name": "Kris Neuharth",
            "email_address": "kneuharth@truecar.com"
        }
    }
    '''
    response = es.update(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        id=111,
        body=body,
        refresh=True
    )

    print_r('Updated', response)


def get_prospect_by_id():
    """
    Get a prospect by id
    """

    response = es.get(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        id=111,
        refresh=True
    )

    print_r('Get Prospect By ID', response)


def get_prospect_by_id_exclude_fields():
    """
    Get a prospect by id, exclude fields
    """

    response = es.get(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        _source_exclude=[
            'id', 'postal_code',
            'prospect_date', 'status', 'program',
            'new_used', 'assigned_to', 'year',
            'make', 'model', 'certificate_id',
            'has_manual_offers', 'has_automated_offers',
            'sold'
        ],
        id=111,
        refresh=True
    )

    print_r('Get Prospect By ID, Exclude Fields', response)


def get_prospect_by_id_include_fields():
    """
    Get a prospect by id, include fields
    """

    response = es.get(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        _source_include=[
            'name', 'email_address'
        ],
        id=111,
        refresh=True
    )

    print_r('Get Prospect By ID, Include Fields', response)


def get_prospect_source_by_id():
    """
    Get prospect data by id
    """

    response = es.get_source(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        id=111,
        refresh=True
    )

    print_r('Get Prospect Source By ID', response)


def get_prospect_source_by_id_exclude_fields():
    """
    Get prospect source by id, exclude fields
    """

    response = es.get_source(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        _source_exclude=[
            'id', 'postal_code',
            'prospect_date', 'status', 'program',
            'new_used', 'assigned_to', 'year',
            'make', 'model', 'certificate_id',
            'has_manual_offers', 'has_automated_offers',
            'sold'
        ],
        id=111,
        refresh=True
    )

    print_r('Get Prospect Source By ID, Exclude Fields', response)


def get_prospect_source_by_id_include_fields():
    """
    Get prospect source by id, include fields
    """

    response = es.get_source(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        _source_include=[
            'name', 'email_address'
        ],
        id=111,
        refresh=True
    )

    print_r('Get Prospect Source By ID, Include Fields', response)


def delete_prospect_by_id():
    """
    Delete a prospect by id
    """

    response = es.delete(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        id=111,
        refresh=True
    )

    print_r('Deleted', response)


def delete_prospects_by_query():
    """
    Delete prospects that match a query
    """

    response = es.delete_by_query(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        body={
            'query': {
                'term': {
                    'email_address': 'kneuharth@truecar.com'
                }
            }
        },
    )

    print_r('Deleted By Query', response)



def prospect_exists():
    """
    Find out if a prospect exists, by id
    """

    response = es.exists(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        id=111,
        refresh=True
    )

    print_r('Prospect Exists', response)


def get_all_prospects():
    """
    Get all prospects
    """

    # Match all
    response = es.search(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        body={
            'query': {
                'match_all': {}
            }
        },
        # Limit the number of results
        size=2,
        _source_include=[
            'status', 'name', 'email_address'
        ],
    )

    print_r('Count', response['hits']['total'])


def get_all_active_prospects():
    """
    Get all active prospects
    """

    # Match
    response = es.search(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        body={
            'query': {
                'match': {'status': 'Active'}
            }
        },
        # Limit the number of results
        size=2,
        _source_include=[
            'status', 'name', 'email_address'
        ],
    )

    print_r('Count', response['hits']['total'])


def get_prospects_bmw_three_series():
    """
    Get all prospects looking for a 3 Series
    """

    # Match Phrase
    response = es.search(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        body={
            'query': {
                'match_phrase': {'model': '3 Series'}
            }
        },
        # Limit the number of results
        size=2,
        _source_include=[
            'status', 'name', 'email_address'
        ],
    )

    print_r('Count', response['hits']['total'])


def filter_active_in_date_range():
    """
    Find all the prospects in May
    """

    response = es.search(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        body={
            'query': {
                'match_all': {}
            },
            'filter': {
                'range': {
                    'prospect_date': {
                        'from': '2015-05-01',
                        'to': '2015-05-30'
                    }
                }
            }
        },
        # Limit the number of results
        size=2,
        _source_include=[
            'status', 'name', 'email_address'
        ],
    )

    print_r('Found', response)
    print_r('Count', response['hits']['total'])


def filter_date_range_query_sold_make():
    """
    Find all the prospects in May, who bought BMWs
    """
    response = es.search(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        body={
            'query': {
                'filtered': {
                    'query': {
                        'bool': {
                            'must': [
                                {'match': {'sold': True}},
                                {'match': {'make': 'BMW'}},
                            ]
                        }
                    },
                    'filter': {
                        'range': {
                            'prospect_date': {
                                'gte': '2015-05-01',
                                'lte': '2015-05-30'
                            }
                        }
                    }
                }
            }
        },
        # Limit the number of results
        size=2,
        _source_include=[
            'status', 'name', 'email_address'
        ],
    )

    print_r('Found:', response)
    print_r('Count:', response['hits']['total'])

def prospect_search():
    """
    Find prospects by query
    """

    # Lucene syntax
    # response = es.search(
    #     index=ES_INDEX,
    #     doc_type=ES_DOC_TYPE,
    #     q='status:Active',
    #     # Limit the number of results
    #     size=2,
    #     _source_include=[
    #         'status', 'name', 'email_address'
    #     ],
    # )
    #
    # print_r('Found', response)
    # print_r('Count', response['hits']['total'])

    # DSL syntax
    # response = es.search(
    #     index=ES_INDEX,
    #     doc_type=ES_DOC_TYPE,
    #     body={
    #         'query': {
    #             'match': {'status': 'Active'}
    #         }
    #     },
    #     # Limit the number of results
    #     size=2,
    #     _source_include=[
    #         'status', 'name', 'email_address'
    #     ],
    # )
    #
    # print 'Found:', response
    # print 'Count:', response['hits']['total']

    # Find something more complicated
    # response = es.search(
    #     index=ES_INDEX,
    #     doc_type=ES_DOC_TYPE,
    #     body={
    #         'query': {
    #             'bool': {
    #                 'must': [
    #                     {'match': {'status': 'Active'}},
    #                     {'match': {'sold': False}},
    #                     {'match': {'new_used': 'New'}},
    #                     {'match': {'has_manual_offers': True}},
    #                     {'match': {'has_automated_offers': True}},
    #                 ],
    #                 'must_not': [
    #                     {'match': {'make': 'MINI'}},
    #                     {'match': {'year': '2015'}}
    #                 ],
    #                 'should': [
    #                     {'match': {'model': 'X1'}},
    #                     {'match': {'model': 'X3'}}
    #                 ]
    #             }
    #         }
    #     },
    #     # Limit the number of results
    #     size=2,
    #     _source_include=[
    #         'status', 'name', 'email_address'
    #     ],
    # )
    #
    # print_r('Found', response)
    # print_r('Count', response['hits']['total'])

    #
    # # Find all the prospects in May
    # response = es.search(
    #     index=ES_INDEX,
    #     doc_type=ES_DOC_TYPE,
    #     body={
    #         'query': {
    #             'range': {
    #                 'prospect_date': {
    #                     'from': '2015-05-01',
    #                     'to': '2015-05-30'
    #                 }
    #             }
    #         }
    #     }
    # )
    #
    # print 'Found:', response
    # print 'Count:', response['hits']['total']
    #

    # Find all the prospects in May, who bought BMWs
    response = es.search(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        body={
            'query': {
                'filtered': {
                    'query': {
                        'bool': {
                            'must': [
                                {'match': {'sold': True}},
                                {'match': {'make': 'BMW'}},
                            ]
                        }
                    },
                    'filter': {
                        'range': {
                            'prospect_date': {
                                'gte': '2015-05-01',
                                'lte': '2015-05-30'
                            }
                        }
                    }
                }
            }
        },
        # Limit the number of results
        size=2,
        _source_include=[
            'status', 'name', 'email_address'
        ],
    )

    print_r('Found:', response)
    print_r('Count:', response['hits']['total'])


def prospect_search_with_aggregations():
    """
    Get all the prospects in May who bought cars,
    get stats using aggregations
    """
    response = es.search(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        body={
            'query': {
                'filtered': {
                    'query': {
                        'bool': {
                            'must': [
                                {'match': {'sold': True}}
                            ]
                        }
                    },
                    'filter': {
                        'range': {
                            'prospect_date': {
                                'gte': '2015-05-01',
                                'lte': '2015-05-30'
                            }
                        }
                    }
                }
            },
            'aggs': {
                'per_make': {'terms': {'field': 'make'}},
                'per_program': {'terms': {'field': 'program'}},
                'per_new_used': {'terms': {'field': 'new_used'}},
                'per_postal_code': {'terms': {'field': 'postal_code'}},
            }
        }
    )

    print_r('Year Buckets', response['aggregations']['per_make'])
    print_r('Program Buckets', response['aggregations']['per_program'])
    print_r('New/Used Buckets', response['aggregations']['per_new_used'])
    print_r('Postal Code Buckets', response['aggregations']['per_postal_code'])


#
# Prospect Search examples
#

# Search by a field name: (Last Name, First Name, Email, ID, or Cert ID)
def omni_search_bar(last_name, first_name, email_address, certificate_id):
    response = es.search(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        body={
            'query': {
                'filtered': {
                    'query': {
                        'bool': {
                            'should': [
                                {'term': {'last_name': ''}},
                                {'term': {'first_name': ''}},
                                {'term': {'email_address': ''}},
                                {'term': {'certificate_id': ''}},

                            ]
                        }
                    }
                }
            }
        }
    )

    print 'Found:', response
    print 'Count:', response['hits']['total']

# Search for all 'Active' Prospects

# Search for all 'Sold' Prospects

# Search for all 'Unassigned' Prospects

# Get all Prospects for the recent months (not using aggregators)

# Get all Prospects for the recent months (using aggregators)

# Get all Prospects within a Date Range

# Get all Prospects that are looking for a Make

# Get all Prospects that are looking for a Make and Model

# Get all Prospects looking for a New vehicle

# Get all Prospects looking for a Used vehicle

# Get all Prospects from a Program

# Get all Prospects from a particular Postal Code


#
# Advanced Queries
#

# Get all Prospects that are Active, from a Program, Assigned To a Dealer, Looking for New

# Get all Prospects that are Active, from a Program, Assigned To a Dealer, Looking for New/Used

# Get all Prospects that are Active, from a Program, Assigned To a Dealer, Looking for New/Used, within a Date Range



if __name__ == "__main__":
    """
    Test Driver
    """

    # Make sure we don't get conflicts
    #delete_prospect_by_id()

    # Create new doc
    #create_prospect()

    # See if the doc exists now
    #prospect_exists()

    # Get the doc again
    #get_prospect_by_id()

    # Get just the source data, not the doc
    #get_prospect_source_by_id()

    # Get the doc, only some fields
    #get_prospect_by_id_exclude_fields()
    #get_prospect_by_id_include_fields()

    # Get just the source data, only some fields
    #get_prospect_source_by_id_exclude_fields()
    #get_prospect_source_by_id_include_fields()

    # Update the doc
    #update_prospect()

    #get_prospect_by_id()

    # See the updates
    #get_prospect_source_by_id_include_fields()

    # See if the doc exists now
    #prospect_exists()

    # Delete the doc by id
    #delete_prospect_by_id()

    # Delete docs matching a query
    #delete_prospects_by_query()

    # Find some prospects
    #prospect_search()

    #get_all_prospects()

    #get_all_active_prospects()

    #get_prospects_three_series()

    #filter_active_in_date_range()

    # Find some prospects, with additional aggregations
    prospect_search_with_aggregations()
