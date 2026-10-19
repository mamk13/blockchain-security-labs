"""Upgrade-state transition policy with explicit modeled rollback."""
from copy import deepcopy


class Proxy:
    def __init__(self, atomic=True):
        self.state = {'implementation': 'v1', 'version': 1, 'owner': 'alice',
                      'balances': {'alice': 70, 'bob': 30}, 'total': 100}
        self.atomic = atomic

    def upgrade(self, caller, implementation, version, migrate):
        if caller != 'governance':
            raise ValueError('unauthorized')
        if implementation != 'v2' or version != 2 or self.state['version'] != 1:
            raise ValueError('unexpected transition')
        before = deepcopy(self.state)
        try:
            self.state['implementation'] = implementation
            migrate(self.state)
            if (self.state.get('version') != version
                    or self.state.get('owner') != before['owner']
                    or self.state.get('balances') != before['balances']
                    or self.state.get('total') != before['total']
                    or self.state.get('implementation') != implementation
                    or self.state.get('limit') != before['total']):
                raise ValueError('migration postcondition')
        except Exception:
            if self.atomic:
                self.state = before
            raise


def migrate_v2(state):
    state['limit'] = state['total']
    state['version'] = 2


class SplitUpgrade(Proxy):
    """Negative control: installed code remains changed after migration failure."""
    def __init__(self):
        super().__init__(atomic=False)
