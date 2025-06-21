import pytest
from imut.immutable_list import ImmutableList

@pytest.mark.parametrize(
        'arg, expected',
        (
            ([1, '2', 3.0, {4: 5}, None], (1, '2', 3.0, {4: 5}, None)),
            ((i + 10 for i in range(5)), (10, 11, 12, 13, 14)),
            ({1, 2}, (1, 2)),
            ({1: 2, '3': '4'}, (1, '3'))
        )
)
def test_get_item(arg, expected):
    l = ImmutableList(arg)

    for i, j in enumerate(expected):
        assert j == l[i]

def test_iter():
    data = (1, 2, 3)
    l = ImmutableList(data)

    index = 0
    for i in l:
        assert data[index] == i
        index += 1

def test_slice():
    assert ImmutableList([1,2,3])[:2] == ImmutableList([1,2])

def test_append():
    l = ImmutableList([1,2])
    assert l.append(3) == ImmutableList([1,2,3])
    assert l == ImmutableList([1,2])

def test_extend():
    l = ImmutableList([1,2])
    assert l.extend([3, 4]) == ImmutableList([1,2,3,4])
    assert l == ImmutableList([1,2])

def test_add():
    l = ImmutableList([1,2])
    assert l + ImmutableList([3,4]) == ImmutableList([1,2,3,4])
    assert l == ImmutableList([1,2])

def test_insert():
    l = ImmutableList([2])
    assert l.insert(10, 4).insert(0, 1).insert(2, 3) == ImmutableList([1,2,3,4])
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
    l = ImmutableList([1, 2, 3])
    assert l.index(1) == 0
    assert l.index(2, 1) == 1
    assert l.index(3, 1, 999) == 2

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
