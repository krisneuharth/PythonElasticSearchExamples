import json
import uuid
import random
from faker import Factory
from faker.providers import BaseProvider
from elasticsearch import Elasticsearch

# Helpful configs
ES_INDEX = 'prospects'
ES_DOC_TYPE = 'prospect'
ES_DOC_COUNT = 100
VERBOSE = False


# Create our faker
fake = Factory.create()
fake.seed(43210)

# Create our Elastic Search client
es = Elasticsearch()


class ProspectProvider(BaseProvider):
    """
    Create a Provider to fake Prospect data
    """

    def status(self):
        return random.choice([
            'Active', 'Inactive'
        ])

    def program(self):
        return random.choice([
            'TrueCar', 'USAA',
            'GEICO', 'PenFed',
            'AAA', 'AllState',
            'Progressive',
            'Nationwide'
        ])

    def prospect_date(self):
        dd = fake.date()
        split_dd = dd.split('-')

        # Replace the year with something guaranteed
        # to be recent
        split_dd[0] = str(
            random.choice(['2014', '2015'])
        )

        return '-'.join(split_dd)

    def postal_code(self):
        return random.choice([
            '90210', '90401', '90232',
            '90832', '91495', '90090',
            '91601', '93599', '91102',
            '91322', '90059', '91371'

        ])

    def new_used(self):
        return random.choice([
            'New', 'Used'
        ])

    def assigned_to(self):
        return random.choice([
            'Kris Neuharth',
            'Chad Rempp',
            'Eliot Shiosaki',
            'Peter Morawiec',
            'Priyanka Halder',
            'Nic Walder'
        ])

    def year(self):
        return random.choice([
            '2014', '2015', '2016'
        ])

    def make(self):
        return random.choice([
            'BMW',
            'MINI'
        ])

    def model(self, make):

        if make == 'BMW':
            return random.choice([
                '2 Series',
                '3 Series',
                '3 Series Gran Turismo',
                '4 Series',
                '5 Series',
                '5 Series Gran Turismo',
                '6 Series',
                '7 Series',
                'M3', 'M4', 'M5', 'M6',
                'X1', 'X3', 'X4', 'X5', 'X5 M', 'X6', 'X6 M',
                'Z3', 'Z4',
                'i3', 'i8',
            ])

        if make == 'MINI':
            return random.choice([
                "Cooper Clubman",
                "Cooper Convertible",
                "Cooper Countryman",
                "Cooper Coupe",
                "Cooper Hardtop",
                "Cooper Hardtop 4 Door",
                "Cooper Paceman",
                "Cooper Roadster",
            ])

    def certificate_id(self):
        # Generate a 6 character alphanumeric string
        return str(uuid.uuid4())[0:6].upper()

    def has_manual_offers(self):
        return random.choice([
            True, False
        ])

    def has_automated_offers(self):
        return random.choice([
            True, False
        ])

    def sold(self):
        return random.choice([
            True, False
        ])

# Register the faker provider
fake.add_provider(ProspectProvider)


class Prospect(object):
    """
    Helper class to represent and transform a Prospect
    """

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email_address": self.email_address,
            "postal_code": self.postal_code,
            "prospect_date": self.prospect_date,
            "status": self.status,
            "program": self.program,
            "new_used": self.new_used,
            "assigned_to": self.assigned_to,
            "year": self.year,
            "make": self.make,
            "model": self.model,
            "certificate_id": self.certificate_id,
            "has_manual_offers": self.has_manual_offers,
            "has_automated_offers": self.has_automated_offers,
            "sold": self.sold,
        }

    def __repr__(self):
        return json.dumps(
            self.as_dict(),
            sort_keys=True,
            indent=2
        )


def generate_prospect(id):
    """
    Generate a fake Prospect
    :param id
    :return: Prospect
    """

    prospect = Prospect()
    prospect.id = id
    prospect.name = fake.name()
    prospect.email_address = fake.email()
    prospect.postal_code = fake.postal_code()

    prospect.prospect_date = fake.prospect_date()
    prospect.status = fake.status()
    prospect.program = fake.program()
    prospect.new_used = fake.new_used()
    prospect.assigned_to = fake.assigned_to()

    prospect.year = fake.year()
    prospect.make = fake.make()
    prospect.model = fake.model(prospect.make)
    prospect.certificate_id = fake.certificate_id()

    prospect.has_manual_offers = fake.has_manual_offers()
    prospect.has_automated_offers = fake.has_automated_offers()
    prospect.sold = fake.sold()

    return prospect


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
        pp = generate_prospect(id)
        index_prospect(pp)

    # Refresh the index
    print '\n\nRefreshing the index...'
    es.indices.refresh(index=ES_INDEX)

    # Find out how many we imported
    count = str(es.count(index=ES_INDEX)['count'])

    print 'Done.\n'

    print 'Imported documents: %s\n' % count