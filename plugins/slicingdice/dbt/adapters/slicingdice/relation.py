from dbt.adapters.base.relation import BaseRelation


class SlicingDiceRelation(BaseRelation):
    DEFAULTS = {
        'metadata': {
            'type': 'SlicingDiceRelation'
        },
        'quote_character': '"',
        'quote_policy': {
            'database': False,
            'schema': False,
            'identifier': False,
        },
        'include_policy': {
            'database': False,
            'schema': False,
            'identifier': False,
        }
    }
