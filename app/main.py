from app.lib.cache import cache, get_cache
from app.lib.getsimilar import get_similar
from app.lib.models import SimilarRequestPOST, SimilarResponseREST, SimilarResponseGraphQL

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
import graphene
from starlette.graphql import GraphQLApp

from typing import Dict, List

# Initialization
app = FastAPI()

# Allow CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)


# Routes
@app.get('/similar', response_model=Dict[str, Dict[str, List[SimilarResponseREST]]], response_class=ORJSONResponse)
@app.get('/similar/{text}', response_model=Dict[str, Dict[str, List[SimilarResponseREST]]], response_class=ORJSONResponse)
async def similar_get(text: str, topn: int = 10):
  return {'data': {'similar': get_cache(get_similar, text, topn)}}


@app.post('/similar', response_model=Dict[str, Dict[str, List[SimilarResponseREST]]], response_class=ORJSONResponse)
async def similar_post(request: SimilarRequestPOST):
  return {'data': {'similar': get_cache(get_similar, request.text, request.topn)}}


# GraphQL
class Query(graphene.ObjectType):
  similar = graphene.List(
    SimilarResponseGraphQL,
    text=graphene.String(required=True),
    topn=graphene.Int(default_value=10),
  )

  def resolve_similar(parent, info, text, topn):
    return get_cache(get_similar, text, topn)


app.add_route('/graphql', GraphQLApp(schema=graphene.Schema(query=Query)))
