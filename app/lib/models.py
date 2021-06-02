import graphene
from pydantic import BaseModel

from typing import Optional, List, Union


class SimilarREST(BaseModel):
  text: str
  similarity: Union[float, None]


class SimilarGraphQL(graphene.ObjectType):
  text = graphene.String(required=True)
  similarity = graphene.Float()
