from dbt.adapters.sql import SQLAdapter
from dbt.adapters.slicingdice import SlicingDiceAdapterConnectionManager


class SlicingDiceAdapterAdapter(SQLAdapter):
    ConnectionManager = SlicingDiceAdapterConnectionManager
