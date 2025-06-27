import pytest
from imut import ImmutableList
from imut.immutable_list import _TRIE_WIDTH

@pytest.mark.parametrize(
        'arg, expected',
        (
            ([1, '2', 3.0, {4: 5}, None], (1, '2', 3.0, {4: 5}, None)),
            ((i + 10 for i in range(50)), tuple(i + 10 for i in range(50))),
            ({1, 2}, (1, 2)),
            ({1: 2, '3': '4'}, (1, '3')),
            ([i for i in range(1000)], tuple(i for i in range(1000)))
        )
)
def test_get_item(arg, expected):
    l = ImmutableList(arg)

    for i, j in enumerate(expected):
        assert j == l[i]

def test_iter():
    data = tuple(i for i in range(_TRIE_WIDTH + 1))
    l = ImmutableList(data)

    index = 0
    for i in l:
        assert data[index] == i
        index += 1

def test_slice():
    data = [i for i in range(64 ** 3)]
    assert ImmutableList(data)[:100] == ImmutableList(range(100))
    assert ImmutableList(data)[100:500] == ImmutableList(range(100, 500))
    assert ImmutableList(data)[500:9000:4] == ImmutableList(range(500, 9000, 4))

def test_append():
    l = ImmutableList([1,2])
    to_append = (i for i in range(3, 64 ** 2))
    new_list = l
    for i in to_append:
        new_list = new_list.append(i)
    assert new_list == ImmutableList((i for i in range(1, 64 ** 2)))
    assert l == ImmutableList([1,2])

def test_extend():
    l = ImmutableList([1,2])
    assert l.extend((i for i in range(3, 64 ** 2))) == ImmutableList((i for i in range(1, 64 ** 2)))
    assert l == ImmutableList([1,2])

def test_add():
    l = ImmutableList([1,2])
    assert l + ImmutableList((i for i in range(3, 64 ** 2))) == ImmutableList((i for i in range(1, 64 ** 2)))
    assert l == ImmutableList([1,2])

def test_insert():
    l = ImmutableList([2])
    new_l = l.insert(10, 4).insert(0, 1).insert(2, 3)
    for i in range(64 ** 2):
        if i == 61:
            print(1)
        new_l = new_l.insert(64 ** 2, 64000)
    assert new_l == ImmutableList((1,2,3,4) + tuple(64000 for _ in range(64 ** 2)))
    assert l == ImmutableList([2])

def test_remove():
    l = ImmutableList([1, 3, 2, 3])
    assert l.remove(3) == ImmutableList([1,2,3])
    assert l == ImmutableList([1, 3, 2, 3])

def test_remove_should_raise_ValueError_when_value_not_found():
    l = ImmutableList([1, 2, 3])
    with pytest.raises(ValueError):
        l.remove(4)

def test_index():
    l = ImmutableList((i for i in range(64 ** 2)))
    assert l.index(1) == 1
    assert l.index(2, 1) == 2
    assert l.index(3, 1, 999) == 3

@pytest.mark.parametrize(
    'args',
    (
        ((4,),),
        ((1, 1, 0),),
        ((1, 2, 10),)
    )
)
def test_index_should_raise_ValueError_when_value_not_found(args):
    l = ImmutableList([1, 2, 3])
    with pytest.raises(ValueError):
        l.index(*args)

@pytest.mark.parametrize(
    'arg, expected',
    (
        (4, 0),
        (1, 1),
        (2, 2)
    )
)
def test_count(arg, expected):
    l = ImmutableList([1, 2, 3, 2])
    assert l.count(arg) == expected
