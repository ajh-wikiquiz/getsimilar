import graphene
from pydantic import BaseModel

from typing import Optional, List, Union


class SimilarRequestPOST(BaseModel):
  text: str
  topn: int = 10


class SimilarResponseREST(BaseModel):
  text: str
  similarity: Union[float, None]


class SimilarResponseGraphQL(graphene.ObjectType):
  text = graphene.String(required=True)
  similarity = graphene.Float()
