import graphene
from pydantic import BaseModel

from typing import Optional, List, Union


class Request(BaseModel):
	text: str


class MostSimilarREST(BaseModel):
	text: str
	similarity: Union[float, None]


class MostSimilarGraphQL(graphene.ObjectType):
	text = graphene.String(required=True)
	similarity = graphene.Float()
