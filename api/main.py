from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pyhpo.ontology import Ontology
from pyhpo.stats import EnrichmentModel, HPOEnrichment

from .routers import term, terms, annotations

app = FastAPI()

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


_ = Ontology()

terms.gene_model = EnrichmentModel('gene')
terms.omim_model = EnrichmentModel('omim')
terms.hpo_model_genes = HPOEnrichment('gene')
terms.hpo_model_omim = HPOEnrichment('omim')


app.include_router(
    term.router,
    prefix='/term',
    tags=['term'],
    responses={404: {'description': 'HPO Term does not exist'}},
)

app.include_router(
    terms.router,
    prefix='/terms',
    tags=['terms'],
    responses={400: {'description': 'Invalid HPO Term identifier in query'}},
)

app.include_router(
    annotations.router,
    tags=['annotations'],
    responses={404: {'description': 'Gene/Disease does not exist'}},

)
