from loinclib import NodeAttributeKey


key = NodeAttributeKey.SOME_KEY

print(f'{key} is of type {type(key)}')
print(f'{key.name} is of type {type(key.name)}')
print(f'{key.value} is of type {type(key.value)}')
