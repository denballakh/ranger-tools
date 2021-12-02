from abc import ABCMeta


def C3(cls, getancestors=lambda c: c.__bases__, root=object):
    if cls is root:
        return [root]

    def merge(mros):
        if not any(mros):
            return []
        for candidate, *_ in mros:
            if all(candidate not in tail for _, *tail in mros):
                return [candidate] + merge(
                    [tail if head is candidate else [head, *tail] for head, *tail in mros]
                )

        raise TypeError('No legal mro')

    return [cls] + merge(
        [C3(base, getancestors=getancestors, root=root) for base in getancestors(cls)]
    )


class SingletonMeta(ABCMeta):
    def __new__(mcls, clsname, bases, clsdict):
        cls = super().__new__(mcls, clsname, bases, clsdict)
        cls.__instance__ = None
        return cls

    def __call__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            cls.__instance__ = super().__call__(*args, **kwargs)
        return cls.__instance__


class Singleton(metaclass=SingletonMeta):
    pass
