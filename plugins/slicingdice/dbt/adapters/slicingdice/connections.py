from contextlib import contextmanager

from dbt.adapters.base import Credentials
from dbt.adapters.sql import SQLConnectionManager


SLICINGDICE_CREDENTIALS_CONTRACT = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'database': {
            'type': 'string',
        },
        'schema': {
            'type': 'string',
        },
    },
    'required': ['database', 'schema'],
}


class SlicingDiceAdapterCredentials(Credentials):
    SCHEMA = SLICINGDICE_CREDENTIALS_CONTRACT

    @property
    def type(self):
        return 'slicingdice'

    def _connection_keys(self):
        # return an iterator of keys to pretty-print in 'dbt debug'
        raise NotImplementedError


class SlicingDiceAdapterConnectionManager(SQLConnectionManager):
    TYPE = 'slicingdice'
