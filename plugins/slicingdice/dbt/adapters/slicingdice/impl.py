from dbt.adapters.sql import SQLAdapter
from dbt.adapters.slicingdice import SlicingDiceAdapterConnectionManager


class SlicingDiceAdapterAdapter(SQLAdapter):
    ConnectionManager = SlicingDiceAdapterConnectionManager

    @classmethod
    def date_function(cls):
        return 'CURRENT_TIMESTAMP()'
