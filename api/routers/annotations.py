from fastapi import APIRouter, HTTPException, Path


from pyhpo.ontology import Ontology
from pyhpo.annotations import Gene, Omim

router = APIRouter()


@router.get(
    '/omim/{omim_id}',
    tags=['disease'],
    response_description='OMIM Disease'
)
async def omim_disease(
    omim_id: int = Path(..., example=230800),
    verbose: bool = False
):
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


@router.get(
    '/gene/{gene_id}',
    tags=['gene'],
    response_description='Gene'
)
async def gene(
    gene_id=Path(..., example='GBA'),
    verbose: bool = False
):
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
