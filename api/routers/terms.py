from enum import Enum
from fastapi import APIRouter, Query

from pyhpo.ontology import Ontology

from api.helpers import get_hpo_set

router = APIRouter()

gene_model = None
omim_model = None
hpo_model_genes = None
hpo_model_omim = None


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


@router.get(
    '/search/{query}',
    tags=['terms'],
    response_description='List of HPOTerms'
)
async def HPO_search(
    query: str,
    verbose: bool = False,
    limit: int = 10,
    offset: int = 0
):
    """
    Get all HPOTerms via substring match.
    This search searches in name, alternative names and synonyms

    Parameters
    ----------
    query: str
        The substring to search for
    verbose: bool, default False
        Show more info about the HPOTerm
    limit: int, default 10
        The number of results to return
    offset: int, default 0
        For paging, the offset of the first result to show

    Returns
    -------
    dict
        Array of HPOTerms

    """
    res = []
    for idx, term in enumerate(Ontology.search(query)):
        if idx > (offset + limit-1):
            break
        if idx < offset:
            continue
        res.append(term)
    return [t.toJSON(bool(verbose)) for t in res]


@router.get(
    '/intersect/omim',
    tags=['annotations'],
    response_description='List of OMIM Diseases'
)
async def intersecting_OMIM_diseases(
    set1: str = Query(..., example='HP:0007401,HP:0010885,HP:0006530')
):
    """
    Get all OMIM Diseases, associated with several HPOTerms.
    All diseases are returned that are associated with any of the
    provided HPOTerms

    You can look up terms via:

    * **HPO Identifier**: ``'HP:0000003'``
    * **Term name**: ``'Multicystic kidney dysplasia'``
    * **Integer representation of HPO ID**: ``3``

    Parameters
    ----------
    set1: list of int or str
        Comma-separated list of HPOTerm identifiers

    Returns
    -------
    array
        Array of OMIM diseases
    """
    set1 = get_hpo_set(set1)
    diseases = set1.omim_diseases()
    for term in set1:
        diseases = diseases & term.omim_diseases
    return [
            d.toJSON()
            for d in diseases
        ]


@router.get(
    '/intersect/genes',
    tags=['annotations'],
    response_description='List of Genes'
)
async def intersecting_genes(
    set1: str = Query(..., example='HP:0007401,HP:0010885,HP:0006530')
):
    """
    Get all Genes, associated with several HPOTerms.
    All genes are returned that are associated with any of the
    provided HPOTerms

    You can look up terms via:

    * **HPO Identifier**: ``'HP:0000003'``
    * **Term name**: ``'Multicystic kidney dysplasia'``
    * **Integer representation of HPO ID**: ``3``

    Parameters
    ----------
    set1: list of int or str
        Comma-separated list of HPOTerm identifiers

    Returns
    -------
    array
        Array of Genes
    """
    set1 = get_hpo_set(set1)
    genes = set1.all_genes()
    for term in set1:
        genes = genes & term.genes
    return [
            g.toJSON()
            for g in genes
        ]


@router.get(
    '/union/omim',
    tags=['annotations'],
    response_description='List of OMIM Diseases'
)
async def union_OMIM_diseases(
        set1: str = Query(..., example='HP:0007401,HP:0010885,HP:0006530')
):
    """
    Get all OMIM Diseases, associated with several HPOTerms.
    Only diseases are returned that are associated with all provided HPOTerms

    You can look up terms via:

    * **HPO Identifier**: ``'HP:0000003'``
    * **Term name**: ``'Multicystic kidney dysplasia'``
    * **Integer representation of HPO ID**: ``3``

    Parameters
    ----------
    set1: list of int or str
        Comma-separated list of HPOTerm identifiers

    Returns
    -------
    array
        Array of OMIM diseases
    """
    set1 = get_hpo_set(set1)
    diseases = set1.omim_diseases()
    return [
            d.toJSON()
            for d in diseases
        ]


@router.get(
    '/union/genes',
    tags=['annotations'],
    response_description='List of Genes'
)
async def union_genes(
        set1: str = Query(..., example='HP:0007401,HP:0010885,HP:0006530')
):
    """
    Get all Genes, associated with several HPOTerms.
    Only genes are returned that are associated with all provided HPOTerms

    You can look up terms via:

    * **HPO Identifier**: ``'HP:0000003'``
    * **Term name**: ``'Multicystic kidney dysplasia'``
    * **Integer representation of HPO ID**: ``3``

    Parameters
    ----------
    set1: list of int or str
        Comma-separated list of HPOTerm identifiers

    Returns
    -------
    array
        Array of Genes
    """
    set1 = get_hpo_set(set1)
    genes = set1.all_genes()
    return [
            g.toJSON()
            for g in genes
        ]


@router.get(
    '/similarity',
    tags=['similarity'],
    response_description='Similarity score'
)
async def terms_similarity(
    set1: str = Query(..., example='HP:0007401,HP:0010885,HP:0006530'),
    set2: str = Query(..., example='HP:0200070,HP:0002754,HP:0031630'),
    method: str = 'graphic',
    combine: str = 'funSimAvg',
    kind: str = 'omim'
):
    """
    Similarity score of two different HPOSets

    You can identify terms via:

    * **HPO Identifier**: ``'HP:0000003'``
    * **Term name**: ``'Multicystic kidney dysplasia'``
    * **Integer representation of HPO ID**: ``3``

    Parameters
    ----------
    set1: list of int or str
        Comma-separated list of HPOTerm identifiers
    set2: list of int or str
        Comma-separated list of HPOTerm identifiers
    kind: str, default ``None``
        Which kind of information content should be calculated.
        Options are ['omim', 'orpha', 'decipher', 'gene']
        See :func:`pyhpo.HPOTerm.similarity_score` for options

    method: string, default ``None``
        The method to use to calculate the similarity.

        Available options:

        * **resnik** - Resnik P, Proceedings of the 14th IJCAI, (1995)
        * **lin** - Lin D, Proceedings of the 15th ICML, (1998)
        * **jc** - Jiang J, Conrath D, ROCLING X, (1997)
          Implementation according to R source code
        * **jc2** - Jiang J, Conrath D, ROCLING X, (1997)
          Implementation according to paper from R ``hposim`` library
          Deng Y, et. al., PLoS One, (2015)
        * **rel** - Relevance measure - Schlicker A, et.al.,
          BMC Bioinformatics, (2006)
        * **ic** - Information coefficient - Li B, et. al., arXiv, (2010)
        * **graphic** - Graph based Information coefficient -
          Deng Y, et. al., PLoS One, (2015)
        * **dist** - Distance between terms
        * **equal** - Calculates exact matches between both sets

    combine: string, default ``funSimAvg``
        The method to combine similarity measures.

        Available options:

        * **funSimAvg** - Schlicker A, BMC Bioinformatics, (2006)
        * **funSimMax** - Schlicker A, BMC Bioinformatics, (2006)
        * **BMA** - Deng Y, et. al., PLoS One, (2015)

    Returns
    -------
    float
        The similarity score to the other HPOSet
    """
    set1 = get_hpo_set(set1)
    set2 = get_hpo_set(set2)

    return {
        'set1': set1.toJSON(),
        'set2': set2.toJSON(),
        'similarity': set1.similarity(
            set2,
            kind=kind,
            method=method,
            combine=combine
        )
    }


@router.get(
    '/enrichment/genes',
    tags=['enrichment'],
    response_description='Enrichment scores'
)
async def gene_enrichment(
    set1: str = Query(..., example='HP:0007401,HP:0010885,HP:0006530'),
    method: str = 'hypergeom',
    limit: int = 10,
    offset: int = 0
):
    """
    Enrichment of genes in an HPOSet

    You can identify terms via:

    * **HPO Identifier**: ``'HP:0000003'``
    * **Term name**: ``'Multicystic kidney dysplasia'``
    * **Integer representation of HPO ID**: ``3``

    Parameters
    ----------
    set1: list of int or str
        Comma-separated list of HPOTerm identifiers
    method: str, default ``hypergeom``
        Algorithm for enrichment calculation
        Options are ['hypergeom']
    limit: int, default 10
        The number of results to return
    offset: int, default 0
        For paging, the offset of the first result to show

    Returns
    -------
    list of dict
        A ordered list with enriched genes
    """
    set1 = get_hpo_set(set1)
    res = gene_model.enrichment(method, set1)
    return [{
        'gene:': x['item'].toJSON(),
        'count': x['count'],
        'enrichment': x['enrichment']
    } for x in res[offset:(limit+offset)]]


@router.get(
    '/enrichment/omim',
    tags=['enrichment'],
    response_description='Enrichment scores'
)
async def omim_enrichment(
    set1: str = Query(..., example='HP:0007401,HP:0010885,HP:0006530'),
    method: str = 'hypergeom',
    limit: int = 10,
    offset: int = 0
):
    """
    Enrichment of OMIM diseases in an HPOSet

    You can identify terms via:

    * **HPO Identifier**: ``'HP:0000003'``
    * **Term name**: ``'Multicystic kidney dysplasia'``
    * **Integer representation of HPO ID**: ``3``

    Parameters
    ----------
    set1: list of int or str
        Comma-separated list of HPOTerm identifiers

    method: str, default ``hypergeom``
        Algorithm for enrichment calculation
        Options are ['hypergeom']

    limit: int, default 10
        The number of results to return

    offset: int, default 0
        For paging, the offset of the first result to show

    Returns
    -------
    list of dict
        A ordered list with enriched genes
    """
    set1 = get_hpo_set(set1)
    res = omim_model.enrichment(method, set1)
    return [{
        'omim:': x['item'].toJSON(),
        'count': x['count'],
        'enrichment': x['enrichment']
    } for x in res[offset:(limit+offset)]]


@router.get(
    '/suggest/',
    tags=['enrichment'],
    response_description='HPOTerm list'
)
async def hpo_suggest(
    set1: str = Query(..., example='HP:0007401,HP:0010885,HP:0006530'),
    method: str = 'hypergeom',
    limit: int = 10,
    offset: int = 0,
    n_genes: int = 5,
    n_omim: int = 5
):
    """
    Suggest 'similar' HPOterms based on a given list of Terms

    What happens in the background when you call this:

    * Search for the most enriched Genes and OMIM diseases based
      on the provided HPOTerm list (like the enrichment call)
    * Use the enriched genes and diseases and look for enriched
      HPO terms among them

    You can identify terms via:

    * **HPO Identifier**: ``'HP:0000003'``
    * **Term name**: ``'Multicystic kidney dysplasia'``
    * **Integer representation of HPO ID**: ``3``

    Parameters
    ----------
    set1: list of int or str
        Comma-separated list of HPOTerm identifiers

    method: str, default 'hypergeom'
        Enrichment method to use

    limit: int, default 10
        The number of results to return

    offset: int, default 0
        For paging, the offset of the first result to show

    n_genes: int, default 5
        Consider HPO terms from the Top X enriched genes

    n_omim: int, default 5
        Consider HPO terms from the Top X enriched OMIM diseases
    """

    set1 = get_hpo_set(set1)

    if n_omim:
        omim_res = hpo_model_omim.enrichment(
            method,
            [x['item'] for x in omim_model.enrichment(method, set1)[0:n_omim]]
        )
    else:
        omim_res = []
    if n_genes:
        gene_res = hpo_model_genes.enrichment(
            method,
            [x['item'] for x in gene_model.enrichment(method, set1)[0:n_genes]]
        )
    else:
        gene_res = []

    res = sorted(omim_res + gene_res, key=lambda x: x['enrichment'])[offset:]

    hpos = []
    while len(hpos) < limit:
        hpo = res.pop(0)['hpo']
        if hpo not in hpos and hpo not in set1:
            hpos.append(hpo)
    return [x.toJSON() for x in hpos]
