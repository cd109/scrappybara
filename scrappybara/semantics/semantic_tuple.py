class SemanticTuple(object):
    """N-tuple extracted from text"""

    def __init__(self, *args):
        self.__args = args

    def __str__(self):
        return self.flatten()

    def __repr__(self):
        return self.flatten()

    def __iter__(self):
        return iter(self.__args)

    def __len__(self):
        return len(self.__args)

    @property
    def code(self):
        """Concatenates all argument's codes"""
        return ''.join([arg.code for arg in self.__args])

    def flatten(self, with_decorators=True):
        """Returns the string representation"""
        return self.code + '(' + ', '.join([arg.flatten(with_decorators) for arg in self.__args]) + ')'

    def arg(self, idx):
        """Returns argument at 0-idx"""
        return self.__args[idx]

    def has_any_arg_with_code(self, arg_code):
        return any([arg.code == arg_code for arg in self.__args])
