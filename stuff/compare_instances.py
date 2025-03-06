from typing import Any


def compare_class_instances(typ:type, 
                            *, length_limit:int|None=20, hide_private=True, 
                            **instances: Any) -> None:
    """
    Compares the attributes of multiple instances of the same class and prints the results.
    \n
    Args:
        typ (type): The type of the class to compare.
        length_limit (int|None, optional): The maximum length of the string representation of each attribute. (If None, no limit is applied. Defaults to 20.)
        hide_private (bool, optional): Whether to hide private attributes. Defaults to True.
        **instances (Any): Keyword arguments representing the instances to compare.
            The key of each argument should be the name of the instance.
    \n
    Raises:
        AssertionError: If any of the provided instances is not an instance of the given class.
    """
    instances_name = []
    instances_vars_lst = []
    for instance_name, instance in instances.items():
        if not isinstance(instance, typ):
            raise AssertionError(f"{instance_name} not in the same type {typ}")
        instances_name.append(instance_name)
        instances_vars_lst.append(vars(instance))
    for instance_name in instances_name:
        print(f"{instance_name} | self: {instances[instance_name]}")
    input()
    keys = list(instances_vars_lst[0].keys())
    for i in range(len(instances_vars_lst[0])):
        for j in range(len(instances)):
            key = keys[i]
            if hide_private and (f"_{typ.__name__}__" in key):
                break
            obj = instances_vars_lst[j][key]
            _obj = str(obj)
            if length_limit:
                _obj = _obj[:length_limit]

            print(
                f"{instances_name[j]} | {key}: {obj}, id:{id(obj)}, type:{obj.__class__.__name__}")
        else: #loop finished normally not by break
            _ = input("")
    print("end")

if __name__ == "__main__":
    class sth:
        def __init__(self) -> None:
            self.attr1 = 1
            self.attr2 = []
            self.attr3 = True
            self.__attr4 = None
            self.__attr5 = []
            self.attr6 = 3142857314159265358979
    a = sth()
    b = sth()
    b.attr6 = 3142857314159265358979
    compare_class_instances(sth, hide_private=True, a=a, b=b)