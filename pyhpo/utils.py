from pyhpo.ontology import Ontology
from pyhpo.set import BasicHPOSet


class DiseaseSet:
    _sets = {}
    @classmethod
    def build(cls):
        cls._sets = [(
            d,
            BasicHPOSet.from_queries(d.hpo))
            for d in Ontology.omim_diseases
        ]
    @classmethod
    def all(cls):
        return cls._sets
