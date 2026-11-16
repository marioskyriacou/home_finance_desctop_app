"""
Data shapes coming in and out of API
"""

from datetime import datetime
from pydantic import BaseModel,ConfigDict, Field


class ItemCreate(BaseModel):
	# ItemCreate is what the API accepts when you add an item
	name: str = Field(min_length=1, max_length=100)
	description: str = Field(default="", max_length=2000)

class ItemOut(BaseModel):
	# ItemOut is what the API sends back
	model_config = ConfigDict(from_attributes=True)
	id:int
	name:str
	description:str
	created_at:datetime

class Token(BaseModel):
	access_token: str
	token_type: str = 'bearer'

class UserOut(BaseModel):
	# only id, username/ password is not leaked to the API
	model_config = ConfigDict(from_attributes=True)
	id:int
	username:str