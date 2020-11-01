from fastapi import APIRouter, Path
from typing import List

from pyhpo.set import HPOSet
from api.helpers import get_hpo_term
from api import models

router = APIRouter()


@router.get(
    '/{term_id}',
    response_description='HPOTerm object',
    response_model=models.HPO
)
async def HPO_term(
        term_id=Path(..., example='HP:0000822'),
        verbose: bool = False
):
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
    return get_hpo_term(term_id).toJSON(bool(verbose))


@router.get(
    '/{term_id}/parents',
    response_description='HPOTerm object',
    response_model=List[models.HPO]
)
async def parent_terms(
    term_id=Path(..., example='HP:0000822'),
    verbose: bool = False
):
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
    return [
        t.toJSON(verbose)
        for t in get_hpo_term(term_id).parents
        ]


@router.get(
    '/{term_id}/children',
    response_description='HPOTerm object',
    response_model=List[models.HPO]

)
async def child_terms(
    term_id=Path(..., example='HP:0000822'),
    verbose: bool = False
):
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
    return [
        t.toJSON(verbose)
        for t in get_hpo_term(term_id).children
        ]


@router.get(
    '/{term_id}/neighbours',
    response_description='HPOTerm object',
    response_model=models.HPONeighbours
)
async def neighbour_terms(
    term_id=Path(..., example='HP:0000822'),
    verbose: bool = False
):
    """
    Get all surrounding terms of an HPOterm

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
        Dict with the following keys:

        * **parents**: Array of parent HPOTerms
        * **children**: Array of child HPOTerms
        * **neighbours**: Array of 'sibling' HPOTerms

    """
    term = get_hpo_term(term_id)
    parents = HPOSet(term.parents)
    children = HPOSet(term.children)
    neighbours = HPOSet([])
    for parent in parents:
        for t in parent.children:
            if t != term and t not in parents and t not in children:
                neighbours.add(t)

    for child in children:
        for t in child.parents:
            if t != term and t not in parents and t not in children:
                neighbours.add(t)

    res = {
        'parents': [t.toJSON(verbose) for t in parents],
        'children': [t.toJSON(verbose) for t in children],
        'neighbours': [t.toJSON(verbose) for t in neighbours]
    }
    return res


@router.get(
    '/{term_id}/genes',
    tags=['annotations'],
    response_description='List of Genes',
    response_model=List[models.Gene]

)
async def term_associated_genes(
    term_id=Path(..., example='HP:0000822')
):
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
    return [
        g.toJSON()
        for g in get_hpo_term(term_id).genes
    ]


@router.get(
    '/{term_id}/omim',
    tags=['annotations'],
    response_description='List of OMIM Diseases',
    response_model=List[models.Omim]
)
async def term_associated_OMIM_diseases(
    term_id=Path(..., example='HP:0000822')
):
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
    return [
        d.toJSON()
        for d in get_hpo_term(term_id).omim_diseases
    ]
