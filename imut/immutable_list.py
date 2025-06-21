from collections.abc import Iterable, Reversible, Sequence
from typing import Any, Union





class ImmutableList(Sequence, Reversible):
    def __init__(self, content) -> None:
        if isinstance(content, list):
            self._content = content
        else:
            self._content = list(content)

    def __len__(self) -> int:
        return self._content.__len__()

    def __getitem__(self, key: Union[int, slice]) -> Any:
        if isinstance(key, slice):
            return ImmutableList(self._content[key])
        
        return self._content[key]
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, ImmutableList):
            return False
        
        for i in range(min(len(__value), self.__len__())):
            if __value[i] != self._content[i]:
                return False
            
        return True
    
    def __add__(self, rhs: object) -> 'ImmutableList':
        if not isinstance(rhs, ImmutableList):
            raise TypeError(f'can only concatenate ImmutableList (not "{type(rhs).__name__}") to ImmutableList')
        
        return ImmutableList(self._content + rhs._content)
    
    def append(self, value: object) -> 'ImmutableList':
        return ImmutableList(self._content + [value])
    
    def extend(self, value: Iterable) -> 'ImmutableList':
        iter(value)  ## make sure value is iterable

        return self + ImmutableList(value)
    
    def insert(self, index: int, value: Any) -> 'ImmutableList':
        content = self._content.copy()
        content.insert(index, value)

        return ImmutableList(content)
    
    def remove(self, value: Any) -> 'ImmutableList':
        content = self._content.copy()
        content.remove(value)

        return ImmutableList(content)
    
    def count(self, value: Any) -> int:
        return self._content.count(value)
