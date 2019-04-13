# Generic Development Libraries

Here is a set of libraries I use in my projects.
For now I am starting with two of them: A set of useful mixings
and a progress reporting library.


## genmixin

Helper mixings which do similar things you may find in [dataclasses]
library (implemented in [Python 3.7][dataclass]).
My mixings are ligher, simpler and more general.
May be injected into any class. 

### ReprMixin

Dynamic `__repr__` method, the method generates the object's
constructor call with fields as constructor's arguments.
Fields to display have to be specified by including them in
`_attrs_filter` list property (use `repr_add_attr()` class method).

Only fields defined directly in the object are considered to be printed.
Optionally set `_attrs_ignore_empty` (`repr_ignore_empty_attr()`)
to avoid printing empty/`None` values.

    Fields:                 Methods
    _attrs_filter        =  repr_add_attr(str or iterable)
    _attrs_ignore_empty  =  repr_ignore_empty_attrs(bool)

Example:

    class MyReprClass(ReprMixin):
        name: str = None
        age: int = None
        spouse: 'MyReprClass' = None
        ReprMixin.repr_add_attr('name age spouse'.split())
        ReprMixin.repr_ignore_empty_attrs()
    
        def __init__(self, name: str, age: int = None,
                     spouse: 'MyReprClass' = None) -> None:
            self.name = name
            self.age = age
            self.spouse = spouse
        
    husband = MyReprClass('Terry', 45)
    wife = MyReprClass('Tracy', 49, husband)
    
    print(husband)
    print(wife)
    
Do not set back `husband.spouse = wife` for it throws
`RecursionError`. I don't have clear idea yet how to approach it.
    
### EqualityMixin

Implements `__eq__` in a class by comparing its object's fields value.
The `__eq__` compares only fields as defined by `self._compare_fields`
property.

If `ReprMixin` has been used, you may make usage of its field
`_attrs_filter` and then optionally add/remove fields of your choice.

    _compare_fields = copy.copy(_attrs_filter)
    _compare_fields.remove('name')

It does not compare fields when the other object has it it set to
`None` or `undefined`.
    
## Progress

Progress reporting class. I used it to feedback about download/upload
process. It expects values in bytes, feedback is in human format
(kb/mb/gb). 

Example:

    from jxa.Progress import Progress
    from time import sleep
    p = Progress(frequency=4)
    max = 9000_000
    for i in range(0,max,1000):
        sleep(1/300)
        p.print(i,max)
    p.print_final()

If it is not what you are searching I suggest to look into other
progress reporting libraries:
* https://pypi.org/project/progress/
* https://github.com/niltonvolpato/python-progressbar/
    
    
[dataclasses]: https://pypi.org/project/dataclasses/
[dataclass]: https://docs.python.org/3/library/dataclasses.html




