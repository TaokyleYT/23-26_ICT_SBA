from typing import Any
import types

types_tuple = (
    type,
    types.GenericAlias,
    types.UnionType,
)

def type_check(instance: Any,
               _type: type | types.GenericAlias | types.UnionType) -> bool:

    if not isinstance(_type, types_tuple):
        raise TypeError("typ must be a type")

    if isinstance(_type, types.UnionType):
        return any(type_check(instance, t) for t in _type.__args__)

    #check if typ is sth like list[int] or tuple[str,int]
    if isinstance(_type, types.GenericAlias):
        if hasattr(_type, '__origin__') and hasattr(_type, '__args__'):
            if not isinstance(instance, _type.__origin__):
                return False
            if isinstance(instance, tuple):
                if len(_type.__args__) != len(instance):
                    return False
                return all((type_check(instance[i], _type.__args__[i]))
                           for i in range(len(_type.__args__)))
            return all(
                type_check(item, _type.__args__[0]) for item in instance)
        else:
            raise AssertionError("GenericAlias should always have __origin__ and __args__")

    # normal check
    # check if instance is a subclass of typ
    if isinstance(instance, _type):
        return True
    return False


if __name__ == "__main__":
    print(f"{type_check(1, int) = }")
    print(f"{type_check(1, float) = }")
    print(f"{type_check(True, bool) = }")
    print(f"{type_check([1, 2, 3], list[int]) = }")
    print(f"{type_check([1, 'A', 3], list[int]) = }")
    print(f"{type_check((1,2,3,4,5), tuple[int, ...]) = }")
    print(
        f"{type_check((1, 'A', [0.1, 0.2]), tuple[int, str, list[float]]) = }")
    print(f"{type_check(1, int|bool) = }")
