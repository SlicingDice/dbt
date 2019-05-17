from dbt.adapters.slicingdice.connections import SlicingDiceAdapterConnectionManager
from dbt.adapters.slicingdice.connections import SlicingDiceAdapterCredentials
from dbt.adapters.slicingdice.impl import SlicingDiceAdapterAdapter

from dbt.adapters.base import AdapterPlugin
from dbt.include import slicingdice


Plugin = AdapterPlugin(
    adapter=SlicingDiceAdapterAdapter,
    credentials=SlicingDiceAdapterCredentials,
    include_path=slicingdice.PACKAGE_PATH)
