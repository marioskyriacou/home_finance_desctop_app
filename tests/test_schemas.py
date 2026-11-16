from backend.schemas import ItemCreate

print(ItemCreate(name='Pen'))
ItemCreate(name='') # error str should have at least 1 character
