import json
from elasticsearch import Elasticsearch

# Helpful configs
ES_INDEX = 'prospects'
ES_DOC_TYPE = 'prospect'
VERBOSE = False


# Create our Elastic Search client
es = Elasticsearch()


# http://elasticsearch-py.readthedocs.org/en/latest/api.html


#
# Basic examples from the docs
#

# Create a doc
doc = es.create(
    index=ES_INDEX,
    doc_type=ES_DOC_TYPE,
    body={

    },
    refresh=True
)

# Delete a doc by id
#es.delete()

# Delete a doc by query
#es.delete_by_query()

# Does a document exist?
#es.exists()

# Explain how a document matches a query or not
#es.explain()

# Get a doc by id
#es.get()

# Get a doc, limit the fields returned
#es.get(_source_exclude['', ''])

# Try to get more like this
#es.mlt()

# Search, you know
#es.search()

# Do any matching docs match?
#es.search_exists()

#es.suggest()

# Update a doc
#es.update()


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

    print 1