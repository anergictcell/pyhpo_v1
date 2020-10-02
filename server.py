from fastapi import FastAPI, HTTPException, Query
from enum import Enum

from pyhpo.ontology import Ontology
from pyhpo.annotations import Gene, Omim
from pyhpo.set import HPOSet
from pyhpo.stats import EnrichmentModel, HPOEnrichment

app = FastAPI()
_ = Ontology()

gene_model = EnrichmentModel('gene')
omim_model = EnrichmentModel('omim')
hpo_model_genes = HPOEnrichment('gene')
hpo_model_omim = HPOEnrichment('omim')


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


def get_hpo_id(termid):
    try:
        return int(termid)
    except ValueError:
        return termid


@app.get(
    '/term/{term_id}',
    tags=['terms'],
    response_description='HPOTerm object'
)
async def HPO_term(term_id, verbose: bool = False):
    """
    Show info about a single HPO term.

    You can look up terms via:

    * **HPO Identifier**: ``'HP:0000003'``
    * **Term name**: ``'Multicystic kidney dysplasia'``
    * **Integer representation of HPO ID**: ``3``

    Parameters
    ----------
    term_id: int or str
        The HPO Term ID
    verbose: bool, default False
        Show more info about the HPOTerm

    Returns
    -------
    dict
        HPOTerm as JSON object

    """
    term_id = get_hpo_id(term_id)
    try:
        return Ontology.get_hpo_object(term_id).toJSON(bool(verbose))
    except AttributeError:
        raise HTTPException(status_code=404, detail="HPO Term does not exist")


@app.get(
    '/term/{term_id}/parents',
    tags=['terms'],
    response_description='HPOTerm object'
)
async def parent_terms(term_id, verbose: bool = False):
    """
    Get all parents of an HPOterm

    You can look up terms via:

    * **HPO Identifier**: ``'HP:0000003'``
    * **Term name**: ``'Multicystic kidney dysplasia'``
    * **Integer representation of HPO ID**: ``3``

    Parameters
    ----------
    term_id: int or str
        The HPO Term ID
    verbose: bool, default False
        Show more info about the HPOTerm

    Returns
    -------
    dict
        Array of HPOTerms

    """
    term_id = get_hpo_id(term_id)
    try:
        return [
            t.toJSON(verbose)
            for t in Ontology.get_hpo_object(term_id).parents
            ]
    except AttributeError:
        raise HTTPException(status_code=404, detail="HPO Term does not exist")


@app.get(
    '/term/{term_id}/children',
    tags=['terms'],
    response_description='HPOTerm object'
)
async def child_terms(term_id, verbose: bool = False):
    """
    Get all children of an HPOterm

    You can look up terms via:

    * **HPO Identifier**: ``'HP:0000003'``
    * **Term name**: ``'Multicystic kidney dysplasia'``
    * **Integer representation of HPO ID**: ``3``

    Parameters
    ----------
    term_id: int or str
        The HPO Term ID
    verbose: bool, default False
        Show more info about the HPOTerm

    Returns
    -------
    dict
        Array of HPOTerms

    """
    term_id = get_hpo_id(term_id)
    try:
        return [
            t.toJSON(verbose)
            for t in Ontology.get_hpo_object(term_id).children
            ]
    except AttributeError:
        raise HTTPException(status_code=404, detail="HPO Term does not exist")


@app.get(
    '/term/{term_id}/genes',
    tags=['terms', 'annotations'],
    response_description='List of Genes'
)
async def term_associated_genes(term_id):
    """
    Get all Genes, associated with an HPOTerm

    You can look up terms via:

    * **HPO Identifier**: ``'HP:0000003'``
    * **Term name**: ``'Multicystic kidney dysplasia'``
    * **Integer representation of HPO ID**: ``3``

    Parameters
    ----------
    term_id: int or str
        The HPO Term ID

    Returns
    -------
    array
        Array of Genes
    """
    term_id = get_hpo_id(term_id)
    try:
        return [
            g.toJSON()
            for g in Ontology.get_hpo_object(term_id).genes
        ]
    except AttributeError:
        raise HTTPException(status_code=404, detail="HPO Term does not exist")


@app.get(
    '/term/{term_id}/omim',
    tags=['terms', 'annotations'],
    response_description='List of OMIM Diseases'
)
async def term_associated_OMIM_diseases(term_id):
    """
    Get OMIM Diseases, associated with all provided HPOTerms

    You can look up terms via:

    * **HPO Identifier**: ``'HP:0000003'``
    * **Term name**: ``'Multicystic kidney dysplasia'``
    * **Integer representation of HPO ID**: ``3``

    Parameters
    ----------
    term_id: int or str
        The HPO Term ID

    Returns
    -------
    array
        Array of OMIM diseases
    """
    term_id = get_hpo_id(term_id)
    try:
        return [
            d.toJSON()
            for d in Ontology.get_hpo_object(term_id).omim_diseases
        ]
    except AttributeError:
        raise HTTPException(status_code=404, detail="HPO Term does not exist")


@app.get(
    '/term/{term_id}/intersect/omim',
    tags=['terms', 'annotations'],
    response_description='List of OMIM Diseases'
)
async def intersecting_OMIM_diseases(term_id, q: str):
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
    term_id: int or str
        The HPO Term ID
    q: list of int or str
        Comma-separated list of HPOTerm identifiers

    Returns
    -------
    array
        Array of OMIM diseases
    """
    term_id = get_hpo_id(term_id)
    diseases = Ontology.get_hpo_object(term_id).omim_diseases
    for t2 in q.split(','):
        t2_id = get_hpo_id(t2)
        diseases = diseases & Ontology.get_hpo_object(t2_id).omim_diseases
    return [
            d.toJSON()
            for d in diseases
        ]


@app.get(
    '/term/{term_id}/intersect/genes',
    tags=['terms', 'annotations'],
    response_description='List of Genes'
)
async def intersecting_genes(term_id, q: str):
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
    term_id: int or str
        The HPO Term ID
    q: list of int or str
        Comma-separated list of HPOTerm identifiers

    Returns
    -------
    array
        Array of Genes
    """
    term_id = get_hpo_id(term_id)
    genes = Ontology.get_hpo_object(term_id).genes
    for t2 in q.split(','):
        t2_id = get_hpo_id(t2)
        genes = genes & Ontology.get_hpo_object(t2_id).genes
    return [
            g.toJSON()
            for g in genes
        ]


@app.get(
    '/term/{term_id}/union/omim',
    tags=['terms', 'annotations'],
    response_description='List of OMIM Diseases'
)
async def union_OMIM_diseases(term_id, q: str):
    """
    Get all OMIM Diseases, associated with several HPOTerms.
    Only diseases are returned that are associated with all provided HPOTerms

    You can look up terms via:

    * **HPO Identifier**: ``'HP:0000003'``
    * **Term name**: ``'Multicystic kidney dysplasia'``
    * **Integer representation of HPO ID**: ``3``

    Parameters
    ----------
    term_id: int or str
        The HPO Term ID
    q: list of int or str
        Comma-separated list of HPOTerm identifiers

    Returns
    -------
    array
        Array of OMIM diseases
    """
    term_id = get_hpo_id(term_id)
    diseases = Ontology.get_hpo_object(term_id).omim_diseases
    for t2 in q.split(','):
        t2_id = get_hpo_id(t2)
        diseases = diseases | Ontology.get_hpo_object(t2_id).omim_diseases
    return [
            d.toJSON()
            for d in diseases
        ]


@app.get(
    '/term/{term_id}/union/genes',
    tags=['terms', 'annotations'],
    response_description='List of Genes'
)
async def union_genes(term_id, q: str):
    """
    Get all Genes, associated with several HPOTerms.
    Only genes are returned that are associated with all provided HPOTerms

    You can look up terms via:

    * **HPO Identifier**: ``'HP:0000003'``
    * **Term name**: ``'Multicystic kidney dysplasia'``
    * **Integer representation of HPO ID**: ``3``

    Parameters
    ----------
    term_id: int or str
        The HPO Term ID
    q: list of int or str
        Comma-separated list of HPOTerm identifiers

    Returns
    -------
    array
        Array of Genes
    """
    term_id = get_hpo_id(term_id)
    genes = Ontology.get_hpo_object(term_id).genes
    for t2 in q.split(','):
        t2_id = get_hpo_id(t2)
        genes = genes | Ontology.get_hpo_object(t2_id).genes
    return [
            g.toJSON()
            for g in genes
        ]


@app.get(
    '/search/term/{query}',
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


@app.get(
    '/omim/{omim_id}',
    tags=['diseases'],
    response_description='OMIM Disease'
)
async def omim_disease(omim_id: int, verbose: bool = False):
    """
    Show info about an OMIM diseae

    Parameters
    ----------
    omim_id: int
        The OMIM ID
    verbose: bool, default False
        Show associated HPO term IDs

    Returns
    -------
    array
        OMIM Disease

    """
    try:
        res = Omim.get(omim_id).toJSON(verbose=verbose)
    except AttributeError:
        raise HTTPException(status_code=404, detail="OMIM disease does not exist")
    try:
        res['hpo'] = [Ontology[x].toJSON() for x in res['hpo']]
    except KeyError:
        pass
    return res


@app.get(
    '/gene/{gene_id}',
    tags=['genes'],
    response_description='Gene'
)
async def gene(gene_id, verbose: bool = False):
    """
    Show info about an OMIM diseae

    Parameters
    ----------
    omim_id: int or str
        The HGNC gene-id or gene-symbol
    verbose: bool, default False
        Show associated HPO term IDs

    Returns
    -------
    array
        Gene

    """
    try:
        res = Gene.get(gene_id).toJSON(verbose=verbose)
    except AttributeError:
        raise HTTPException(status_code=404, detail="Gene does not exist")
    try:
        res['hpo'] = [Ontology[x].toJSON() for x in res['hpo']]
    except KeyError:
        pass
    return res


@app.get(
    '/terms/similarity',
    tags=['terms', 'similarity'],
    response_description='Similarity score'
)
async def terms_similarity(
    set1: str = Query(..., example='HP:0001537,HP:0000002,HP:0004097'),
    set2: str = Query(..., example='HP:0100360,HP:0001547,HP:0002060'),
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
    set1 = HPOSet.from_queries([get_hpo_id(x) for x in set1.split(',')])
    set2 = HPOSet.from_queries([get_hpo_id(x) for x in set2.split(',')])

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


@app.get(
    '/enrichment/genes',
    tags=['terms', 'enrichment'],
    response_description='Enrichment scores'
)
async def gene_enrichment(
    set1: str = Query(..., example='HP:0001537,HP:0000002,HP:0004097'),
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
    set1 = HPOSet.from_queries([get_hpo_id(x) for x in set1.split(',')])
    res = gene_model.enrichment(method, set1)
    return [{
        'gene:': x['item'].toJSON(),
        'count': x['count'],
        'enrichment': x['enrichment']
    } for x in res[offset:(limit+offset)]]


@app.get(
    '/enrichment/omim',
    tags=['terms', 'enrichment'],
    response_description='Enrichment scores'
)
async def omim_enrichment(
    set1: str = Query(..., example='HP:0001537,HP:0000002,HP:0004097'),
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
    set1 = HPOSet.from_queries([get_hpo_id(x) for x in set1.split(',')])
    res = omim_model.enrichment(method, set1)
    return [{
        'omim:': x['item'].toJSON(),
        'count': x['count'],
        'enrichment': x['enrichment']
    } for x in res[offset:(limit+offset)]]


@app.get(
    '/terms/suggest/',
    tags=['terms', 'enrichment'],
    response_description='HPOTerm list'
)
async def hpo_suggest(
    set1: str = Query(..., example='HP:0001537,HP:0000002,HP:0004097'),
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

    set1 = HPOSet.from_queries([get_hpo_id(x) for x in set1.split(',')])

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