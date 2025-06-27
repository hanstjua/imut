from collections.abc import Iterable, Reversible, Sequence
from typing import Any, Generator, Optional, Tuple, Union


_TRIE_WIDTH = 64

class _Trie:
    def __init__(self, content: Iterable):
        content_ = tuple(content)
        children = content_
        height = 0
        while len(children) > _TRIE_WIDTH:
            children = tuple(
                _Trie(children[i:min(i+_TRIE_WIDTH, len(content_))])
                for i in range(0, len(children), _TRIE_WIDTH)
            )
            height += 1

        self.__children = children
        self.__height = content_[0].height + 1 if len(content_) > 0 and isinstance(content_[0], _Trie) else height
        self.__size = sum((child.size for child in content_)) if len(content_) > 0 and isinstance(content_[0], _Trie) else len(content_)

    def __getitem__(self, index: int) -> Any:
        i = self.__size - index if index < 0 else index
        if i >= self.__size or i < 0:
            raise IndexError(f'index {index} is out of range for immutable list of length {self.__size}.')
        
        subindices = list(i // (_TRIE_WIDTH ** j) % _TRIE_WIDTH for j in range(self.__height, -1, -1))
        value = self
        for k in subindices:
            value = value.__children[k]

        return value

    @property
    def height(self) -> int:
        return self.__height
    
    @property
    def size(self) -> int:
        return self.__size
    
    def append(self, value: Any, is_root = True) -> Optional['_Trie']:
        if self.__height == 0:
            if len(self.__children) < _TRIE_WIDTH:
                return _Trie(self.__children + (value,))
            else:
                if is_root:
                    return _Trie((self, _Trie((value,))))
                else:
                    return None
        else:
            new_last_child = self.__children[-1].append(value, False)
            if new_last_child is None:
                if is_root:
                    if len(self.__children) < _TRIE_WIDTH:
                        new_child = _Trie((value,))
                        for _ in range(self.__height - 1):
                            new_child = _Trie((new_child,))

                        return _Trie(self.__children + (new_child,))
                    else:
                        new_sibling = _Trie((value,))
                        for _ in range(self.__height):
                            new_sibling = _Trie((new_sibling,))

                        return _Trie((self, new_sibling))
                else:
                    return new_last_child
            else:
                return _Trie(self.__children[:-1] + (new_last_child,))
    
    def replace(self, index: int, value: Any) -> '_Trie':
        if index >= self.__size or index < -self.__size:
            raise IndexError(f'index {index} is out of range for immutable list of length {self.__size}.')
        
        index = index if index >= 0 else self.__size - index
        if self.__height == 0:
            if index == 0:
                return _Trie((value,) + self.__children[1:])
            elif index == _TRIE_WIDTH - 1:
                return _Trie(self.__children[:-1] + (value,))
            else:
                return _Trie(self.__children[:index] + (value,) + self.__children[index+1:])
        
        else:
            subindex = index // _TRIE_WIDTH
            if index % _TRIE_WIDTH == 0:
                return _Trie(self.__children[0].insert(subindex, value) + self.__children[1:])
            elif index % _TRIE_WIDTH == _TRIE_WIDTH - 1:
                return _Trie(self.__children[:-1] + self.__children[-1].insert(subindex, value))
            else:
                return _Trie(self.__children[:index % _TRIE_WIDTH] + self.__children[index % _TRIE_WIDTH].insert(subindex, value) + self.__children[index % _TRIE_WIDTH + 1:])
            
    def insert(self, index: int, value: Any) -> '_Trie':
        index = index if index >= 0 else self.__size + index
        ret = self.slice(0, min(index, self.__size), 1).append(value)
        for i in range(index, self.__size):
            ret = ret.append(self[i])

        return ret

    def slice(self, start: int, stop: int, step: int) -> '_Trie':
        end = stop if stop >= 0 else self.__size - stop
        if end < 0:
            raise IndexError(f'index {stop} is out of range for immutable list of length {self.__size}.')
        
        start = start if start >= 0 else self.__size - start
        if start < 0 or start >= self.__size:
            raise IndexError(f'index {start} is out of range for immutable list of length {self.__size}.')
        
        if start == 0 and end > 1 and step == 1:
            if self.__height == 0:
                return _Trie(self.__children[:end])
            else:
                last_child_index = min(end, self.__size - 1) // (_TRIE_WIDTH ** self.__height) % _TRIE_WIDTH
                new_last_child = self.__children[last_child_index].slice(0, end // _TRIE_WIDTH, step)
                return _Trie(self.__children[:last_child_index] + (new_last_child,))
        else:
            return _Trie((self[i] for i in range(start, end, step)))
        
    def index(self, value: Any, start: int, stop: int) -> int:
        stop = stop if stop >= 0 else self.__size - stop
        if stop < 0:
            raise IndexError(f'index {stop} is out of range for immutable list of length {self.__size}.')
        
        start = start if start >= 0 else self.__size - start
        if start < 0 or start >= self.__size:
            raise IndexError(f'index {start} is out of range for immutable list of length {self.__size}.')
        
        if self.__height == 0:
            start_subindex = max(start, 0) % _TRIE_WIDTH
            stop_subindex = min(stop, self.__size - 1) % _TRIE_WIDTH
            return self.__children.index(value) if value in self.__children[start:stop] else -1
        else:
            start_subindex = max(start, 0) // (_TRIE_WIDTH ** self.__height) % _TRIE_WIDTH
            stop_subindex = min(stop, self.__size - 1) // (_TRIE_WIDTH ** self.__height) % _TRIE_WIDTH
            for i in range(
                start_subindex,
                stop_subindex
            ):
                child = self.__children[i]
                subindex = child.index(
                    value,
                    start,
                    stop
                )
                if subindex > -1:
                    return i * _TRIE_WIDTH + subindex
                
            return -1
        
    def remove(self, value: Any) -> '_Trie':
        index = self.index(value, 0, self.__size)
        if index == -1:
            return None
        else:
            ret = self.slice(0, index, 1)
            for i in range(index + 1, self.__size):
                ret = ret.append(self[i])

            return ret

class ImmutableList(Sequence, Reversible):
    def __new__(cls, content: Iterable) -> 'ImmutableList':
        if isinstance(content, ImmutableList):
            return content
        else:
            inst = super().__new__(cls)

            inst._trie = _Trie(content)

            return inst
        
    def __repr__(self) -> str:
        return f'<{", ".join(str(self._trie[i]) for i in range(self._trie.size))}>'

    def __len__(self) -> int:
        return self._trie.size

    def __getitem__(self, key: Union[int, slice]) -> Any:
        if isinstance(key, slice):
            start = key.start if key.start is not None else 0
            stop = key.stop if key.stop is not None else len(self)
            step = key.step if key.step else 1
            return ImmutableList((self._trie[i] for i in range(start, stop, step)))
        
        return self._trie[key]
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, ImmutableList):
            return False
        
        for i in range(min(len(__value), self.__len__())):
            if __value[i] != self._trie[i]:
                return False
            
        return True
    
    def __add__(self, rhs: object) -> 'ImmutableList':
        if not isinstance(rhs, ImmutableList):
            raise TypeError(f'can only concatenate ImmutableList (not "{type(rhs).__name__}") to ImmutableList')
        
        return self.extend(rhs)
    
    def append(self, value: object) -> 'ImmutableList':
        ret = ImmutableList(())
        ret._trie = self._trie.append(value)
        return ret
    
    def extend(self, value: Iterable) -> 'ImmutableList':
        iter(value)  ## make sure value is iterable

        ret = self
        for i in value:
            ret = ret.append(i)

        return ret
    
    def insert(self, index: int, value: Any) -> 'ImmutableList':
        ret = ImmutableList(())
        ret._trie = self._trie.insert(index, value)
        return ret
    
    def remove(self, value: Any) -> 'ImmutableList':
        trie = self._trie.remove(value)

        if trie is None:
            raise ValueError(f'{value} not in ImmutableList')

        ret = ImmutableList(())
        ret._trie = trie
        return ret
    
    def index(self, value: Any, start: int = None, stop: int = None) -> int:
        ret = self._trie.index(
            value,
            start if start is not None else 0,
            min(stop, self._trie.size) if stop is not None else self._trie.size,
        )
        if ret == -1:
            raise ValueError(f'{value} not in ImmutableList')
        return ret
