from app.lib.custom_redis_connection import CustomConnection as RedisCustomConnection
from app.lib.getsimilar import get_similar
from app.lib.models import Request, MostSimilarREST, MostSimilarGraphQL

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
import graphene
import orjson
import redis
from starlette.graphql import GraphQLApp

from os import environ
from typing import Dict, List

# Cache
cache = None
env_var = None
if 'FLY_REDIS_CACHE_URL' in environ:
	env_var = 'FLY_REDIS_CACHE_URL'
elif 'REDIS_URL' in environ:
	env_var = 'REDIS_URL'
if env_var:
	try:
		redis_connection_pool = redis.ConnectionPool.from_url(
			url=environ.get('REDIS_URL'),
			db=0,
			connection_class=RedisCustomConnection
		)
		redis_connection_pool.timeout = 1.0
		redis_connection_pool.max_connections = 19
		cache = redis.Redis(
			connection_pool=redis_connection_pool,
		)
	except redis.exceptions.ConnectionError:
		pass

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


def get_similar_cache(text: str) -> list:
	"""Returns the most similar results from the cache first if found.
	"""
	if cache:
		try:
			cached_value = cache.get(text)
			if cached_value:
				results = orjson.loads(cached_value.decode())
			else:  # value is not cached yet
				results = get_similar(text)
				cache.set(text, orjson.dumps(results))
		except (
			redis.exceptions.ConnectionError,
			redis.exceptions.TimeoutError,
			redis.exceptions.ResponseError,
			orjson.JSONDecodeError
		):
			results = get_similar(text)
	else:  # no cache available
		results = get_similar(text)
	return results


# Routes
@app.get('/similar', response_model=Dict[str, Dict[str, List[MostSimilarREST]]], response_class=ORJSONResponse)
@app.get('/similar/{text}', response_model=Dict[str, Dict[str, List[MostSimilarREST]]], response_class=ORJSONResponse)
async def similar_text(text: str):
	return {'data': {'similar': get_similar_cache(text)}}


# GraphQL
class Query(graphene.ObjectType):
	most_similar = graphene.List(MostSimilarGraphQL, text=graphene.String(required=True))

	def resolve_most_similar(parent, info, text):
		return get_similar_cache(text)


app.add_route('/graphql', GraphQLApp(schema=graphene.Schema(query=Query)))
