from contextlib import contextmanager

import pyodbc
import dbt.exceptions
from dbt.adapters.base import Credentials
from dbt.adapters.sql import SQLConnectionManager
from dbt.logger import GLOBAL_LOGGER as logger


SLICINGDICE_CREDENTIALS_CONTRACT = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'database': {
            'type': 'string',
        },
        'host': {
            'type': 'string'
        },
        'schema': {
            'type': 'string'
        }
    },
    'required': ['database'],
}

CONNECTION_STRING_TEMPLATE = "Driver=CData ODBC Driver for SlicingDice;" \
                             "Logfile=/tmp/slicingdice.log;Verbosity=3;" \
                             "APIKeys='%s';" \
                             "APIEndpoint='%s/v1'"


class SlicingDiceAdapterCredentials(Credentials):
    SCHEMA = SLICINGDICE_CREDENTIALS_CONTRACT
    ALIASES = {
        'database_key': 'database',
    }

    @property
    def type(self):
        return 'slicingdice'

    def _connection_keys(self):
        # return an iterator of keys to pretty-print in 'dbt debug'
        raise ('database', 'schema')


class SlicingDiceAdapterConnectionManager(SQLConnectionManager):
    TYPE = 'slicingdice'

    @contextmanager
    def exception_handler(self, sql):
        try:
            yield
        except Exception as e:
            logger.debug("Error running SQL: %s", sql)
            logger.debug("Rolling back transaction.")
            self.release()
            if isinstance(e, dbt.exceptions.RuntimeException):
                # during a sql query, an internal to dbt exception was raised.
                # this sounds a lot like a signal handler and probably has
                # useful information, so raise it without modification.
                raise

            raise dbt.exceptions.RuntimeException(e)

    @classmethod
    def open(cls, connection):
        if connection.state == 'open':
            logger.debug('Connection is already open, skipping open.')

        credentials = cls.get_credentials(connection.credentials.incorporate())
        try:
            connection_string = CONNECTION_STRING_TEMPLATE % (
                credentials.database, credentials.host)
            handle = pyodbc.connect(connection_string)

            connection.handle = handle
            connection.state = 'open'
        except Exception as e:
            logger.debug("Got an error when attempting to open a slicingdice "
                         "connection: '{}'"
                         .format(e))

            connection.handle = None
            connection.state = 'fail'

            raise dbt.exceptions.FailedToConnectException(str(e))

        return connection

    @classmethod
    def get_credentials(cls, credentials):
        return credentials

    def cancel(self, connection):
        pass

    @classmethod
    def get_status(cls, cursor):
        return "SUCCESS {}".format(cursor.rowcount)
