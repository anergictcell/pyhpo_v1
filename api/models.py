from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class Information_Content(BaseModel):
    gene: float
    omim: float
    orpha: float
    decipher: float

    class Config:
        schema_extra = {
            'omim': 5.528020005103167,
            'gene': 4.915866634310163,
            'orpha': 6.491229223514548,
            'decipher': 0
        }


class HPO(BaseModel):
    int: int
    id: str
    name: str
    definition: Optional[str]
    comment: Optional[str]
    xref: Optional[List[str]]
    is_a: Optional[List[str]]
    ic: Optional[Information_Content]

    class Config:
        schema_extra = {
            'example': {
                'int': 7401,
                'id': 'HP:0007401',
                'name': 'Macular atrophy',
                'definition': (
                    '"Well-demarcated area(s) of partial or complete '
                    'depigmentation in the macula, reflecting atrophy '
                    'of the retinal pigment epithelium with associated '
                    'retinal photoreceptor loss." [ORCID:0000-0003-0986-4123]'
                ),
                'comment': None,
                'synonym': [],
                'xref': [
                    'MSH:D057088',
                    'SNOMEDCT_US:238828009',
                    'UMLS:C1288283'
                ],
                'is_a': [
                    'HP:0000608 ! Macular degeneration',
                    'HP:0001105 ! Retinal atrophy'
                ],
                'ic': {
                    'omim': 5.528020005103167,
                    'gene': 4.915866634310163,
                    'orpha': 6.491229223514548,
                    'decipher': 0
                }
            }
        }


class HPOSimple(BaseModel):
    int: int
    id: str
    name: str

    class Config:
        schema_extra = {
            'example': {
                'int': 7401,
                'id': 'HP:0007401',
                'name': 'Macular atrophy',
                }
            }


class Similarity_Score(BaseModel):
    set1: List[HPOSimple]
    set2: List[HPOSimple]
    similarity: float

    class Config:
        schema_extra = {
            'example': {
                'set1': [HPOSimple.Config.schema_extra['example']],
                'set2': [HPOSimple.Config.schema_extra['example']],
                'similarity': 0.3422332
            }
        }


class Batch_Similarity_Set(BaseModel):
    name: str
    set2: List[HPOSimple]
    similarity: float


class Batch_Similarity_Score(BaseModel):
    set1: List[HPOSimple]
    other_sets: List[Batch_Similarity_Set]

    class Config:
        schema_extra = {
            'example': {
                "set1": [{
                    "int": 7401,
                    "id": "HP:0007401",
                    "name": "Macular atrophy"
                }, {
                    "int": 6530,
                    "id": "HP:0006530",
                    "name": "Interstitial pulmonary abnormality"
                }, {
                    "int": 10885,
                    "id": "HP:0010885",
                    "name": "Avascular necrosis"
                }],
                "other_sets": [{
                    "name": "Comparison-Set 123",
                    "set2": [{
                        "int": 2754,
                        "id": "HP:0002754",
                        "name": "Osteomyelitis"
                    }, {
                        "int": 31630,
                        "id": "HP:0031630",
                        "name": "Abnormal subpleural morphology"
                    }, {
                        "int": 200070,
                        "id": "HP:0200070",
                        "name": "Peripheral retinal atrophy"
                    }],
                    "similarity": 0.3763421567579537
                }, {
                    "name": "Comparison-Set FooBar",
                    "set2": [{
                        "int": 12337,
                        "id": "HP:0012337",
                        "name": "Abnormal homeostasis"
                    }, {
                        "int": 2098,
                        "id": "HP:0002098",
                        "name": "Respiratory distress"
                    }, {
                        "int": 12332,
                        "id": "HP:0012332",
                        "name": "Abnormal autonomic nervous system physiology"
                    }, {
                        "int": 2094,
                        "id": "HP:0002094",
                        "name": "Dyspnea"
                    }],
                    "similarity": 0.03963063153301517
                }]
            }
        }


class Similarity_Method(Enum):
    resnik = 'resnik'
    lin = 'lin'
    jc = 'jc'
    jc2 = 'jc2'
    rel = 'rel'
    ic = 'ic'
    graphic = 'graphic'
    dist = 'dist'
    equal = 'equal'


class Combination_Method(Enum):
    funSimAvg = 'funSimAvg'
    funSimMax = 'funSimMax'
    BMA = 'BMA'


class POST_HPOSet(BaseModel):
    """
    Defines the POST body for an HPO Set
    """
    set2: str
    name: str


class POST_Batch(BaseModel):
    set1: str
    other_sets: List[POST_HPOSet]

    class Config:
        schema_extra = {
            "example": {
                "set1": "HP:0007401,HP:0010885,HP:0006530",
                "other_sets": [
                    {
                        "set2": "HP:0200070,HP:0002754,HP:0031630",
                        "name": "Comparison-Set 123"
                    }, {
                        "set2": "HP:0012332,HP:0002094,HP:0012337,HP:0002098",
                        "name": "Comparison-Set FooBar"
                    }
                ]
            }
        }
