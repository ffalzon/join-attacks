class PSU:
	def __init__(self, X):
		X = set(X)
		self.X = X
		self._invocations = 0
		self.query_budget = None
		
	def set_query_budget(self, query_budget: int):
		self.query_budget = query_budget

	def PSU(self, Y):
		if self.query_budget is not None and self._invocations >= self.query_budget:
			return None
		
		Y = set(Y)
		self._invocations += 1
		return Y.union(self.X)

	def PSU_CA(self, Y):
		u = self.PSU(Y)
		if u is None:
			return None
		return len(u)
	
	def invocations(self):
		return self._invocations
	
	def reset(self):
		self._invocations = 0