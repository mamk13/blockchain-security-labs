"""Fixed-cost work units, not EVM gas. Immutable append-only job sequence."""
class Batch:
    def __init__(self, jobs):
        if any(type(x) is not int or x < 0 for x in jobs):
            raise ValueError('nonnegative integer jobs required')
        self.jobs=tuple(jobs)
        self.cursor=0
        self.total=0

    def all_at_once(self, budget):
        if len(self.jobs)-self.cursor > budget:
            raise ValueError('transaction budget exceeded')
        self.total += sum(self.jobs[self.cursor:])
        self.cursor=len(self.jobs)

    def step(self, limit, budget, fail_at=None):
        if type(limit) is not int or type(budget) is not int or limit <= 0 or budget <= 0:
            raise ValueError('positive integer bounds required')
        end=min(len(self.jobs),self.cursor+limit,self.cursor+budget)
        subtotal=0
        for i in range(self.cursor,end):
            if i == fail_at: raise ValueError('injected failure')
            subtotal += self.jobs[i]
        # Commit only after the entire chosen chunk succeeds.
        self.total += subtotal
        self.cursor=end

