import collections


class counterdict(collections.defaultdict):
	def __init__(self):
		collections.defaultdict.__init__(self,int)


class OutcomeCounter():
	def __init__(self):
		self.blackjack = 0
		self.win = 0
		self.lose = 0
		self.push = 0
	def inc(self,outcome, by = 1):
		setattr(self,outcome, getattr(self,outcome) + by)
	def total(self):
		return float(self.win + self.lose + self.push)
	def percentage(self,outcome):
		return getattr(self,outcome) / self.total() * 100
