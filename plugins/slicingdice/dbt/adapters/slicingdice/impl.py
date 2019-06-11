import requests
import dbt.exceptions

from dbt.adapters.base import available
from dbt.adapters.slicingdice import SlicingDiceAdapterConnectionManager
from dbt.adapters.slicingdice import SlicingDiceRelation
from dbt.adapters.sql import SQLAdapter
from dbt.logger import GLOBAL_LOGGER as logger


class SlicingDiceAdapterAdapter(SQLAdapter):
    Relation = SlicingDiceRelation
    ConnectionManager = SlicingDiceAdapterConnectionManager

    RELATION_TYPES = {
        'TABLE': SlicingDiceRelation.Table,
        'VIEW': SlicingDiceRelation.View
    }

    @classmethod
    def date_function(cls):
        return 'CURRENT_TIMESTAMP()'

    @available
    def list_schemas(self, database):
        return ['default']

    def list_relations_without_caching(self, information_schema, schema):
        connection = self.connections.get_thread_connection()
        client = connection.handle
        cursor = client.cursor()

        return [self._sd_table_to_relation(table) for table in cursor.tables()]

    def _sd_table_to_relation(self, sd_table):
        if sd_table is None:
            return None

        return self.Relation.create(
            database=sd_table[0],
            schema=sd_table[1],
            identifier=sd_table[2],
            quote_policy={
                'schema': True,
                'identifier': True
            },
            type=self.RELATION_TYPES.get(sd_table[3]))

    def drop_relation(self, relation):
        host = self.connections.get_thread_connection().credentials.get('host')
        database = self.connections.get_thread_connection().credentials.get(
            'database')
        host = host + '/v1/dimension'

        relation = relation.name
        relation = relation.replace("_", "-")
        relation = relation.replace("--dbt-tmp", "")

        headers = {
            "Content-Type": "application/json",
            "Authorization": database
        }

        r = requests.delete(host, json={'api-name': relation}, headers=headers)
        if r.status_code != 200:
            raise dbt.exceptions.FailedToConnectException(str(e))

    def rename_relation(self, from_relation, to_relation):
        pass
