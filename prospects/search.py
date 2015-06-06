from elasticsearch import Elasticsearch
from prospects.prospect import Prospect
from prospects.settings import (
    ES_INDEX, ES_DOC_TYPE
)


# Create our Elastic Search client
es = Elasticsearch()


# http://elasticsearch-py.readthedocs.org/en/latest/api.html

#
# Basic examples from the docs
#


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

    print 'Created:', response


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

    print 'Updated:', response


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

    print 'Prospect:', response


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

    print 'Prospect:', response


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

    print 'Prospect:', response


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

    print 'Prospect:', response


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

    print 'Prospect:', response


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

    print 'Prospect:', response


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

    print 'Deleted:', response


def prospect_exists():
    """
    Find out if a prospect exists, by id
    """

    exists = es.exists(
        index=ES_INDEX,
        doc_type=ES_DOC_TYPE,
        id=111,
        refresh=True
    )

    print 'Exists:', exists


# Delete a doc by query
#es.delete_by_query()

# Try to get more like this
#es.mlt()

# Search, you know
#es.search()

# Do any matching docs match?
#es.search_exists()

#es.suggest()


#
# Prospect Search examples
#

# Search by a field name: (Last Name, First Name, Email, ID, or Cert ID)

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
    delete_prospect_by_id()

    # Create new doc
    create_prospect()

    # See if the doc exists now
    prospect_exists()

    # Get the doc again
    get_prospect_by_id()

    # Get just the source data, not the doc
    get_prospect_source_by_id()

    # Get the doc, only some fields
    get_prospect_by_id_exclude_fields()
    get_prospect_by_id_include_fields()

    # Get just the source data, only some fields
    get_prospect_source_by_id_exclude_fields()
    get_prospect_source_by_id_include_fields()

    # Update the doc
    update_prospect()

    # See the updates
    get_prospect_source_by_id_include_fields()

    # Delete the doc by id
    #delete_prospect_by_id()

    # See if the doc exists now
    prospect_exists()

    # Delete docs matching a query
    #delete_prospects_by_query()
