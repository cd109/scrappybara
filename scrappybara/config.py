import pathlib

# ###############################################################################
# FILES
# ###############################################################################

ENCODING = 'utf-8'
DATA_DIR = pathlib.Path(__file__).parent / 'data'

# ###############################################################################
# MACHINE LEARNING
# ###############################################################################

MAX_WORD_LENGTH = 20
MAX_SENT_LENGTH = 50
WORD_VECTOR_SIZE = 100

PADDED_SENT_LENGTH = MAX_SENT_LENGTH + 2
PADDED_WORD_LENGTH = MAX_WORD_LENGTH + 2

# ###############################################################################
# TRIPLE ARGUMENT
# ###############################################################################

COMPOUND_JOIN = ' '
EXIST = 'EXIST'
NEGATION = 'NOT'
NULL = 'NULL'