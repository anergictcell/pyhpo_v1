from fastapi import FastAPI, HTTPException

from pyhpo.ontology import Ontology
from pyhpo.annotations import Gene, Omim
from pyhpo.set import HPOSet


app = FastAPI()
_ = Ontology()


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
    tags=['terms', 'genes'],
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
    tags=['terms', 'diseases'],
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
    tags=['terms', 'diseases'],
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
    tags=['terms', 'genes'],
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
    tags=['terms', 'diseases'],
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
    tags=['terms', 'genes'],
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
    set1: str,
    set2: str,
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
        See :func:`pyhpo.HPOTerm.similarity_score` for options

        Additional options:

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
