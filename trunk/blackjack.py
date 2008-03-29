#!/usr/bin/python
import random

class Strategy:
	def __init__(self):
		pass
class BasicStrategy(Strategy):
	def __init__(self):
		Strategy.__init__(self)
class Player:
	def __init__(self,name):
		self.name = name
		self.wins = 0
		self.losses = 0
		self.strategy = BasicStrategy()
		self.hand = []
	def deal_card(self,card):
		print self.name + " dealt: " + str(card)
		self.hand.append(card)
	def clear_cards(self):
		self.hand = []
	def ask(self,upcard):
		return True

class Rules:
	def __init__(self):
		pass
	def blackjack(self,hand):
		return sum(hand) == 21
	def bust(self,hand):
		return sum(hand) > 21

class Blackjack:
	def __init__(self,dealer,players,rules,decks):
		self.decks = decks
		self.deck = []
		self.rules = rules
	def play_hand(self):
		self.deal_cards()
	def draw_card(self):
		try:
			card = self.deck.pop()
		except IndexError: 
			self.shuffle()
			card = self.deck.pop()
		return card
	def deal_cards(self):
		for i in range(0,2):
			for p in self.players:
				p.deal_card(self.draw_card())
			dealer.deal_card(self.draw_card())
	def get_new_deck(self):
		return (range(2,10) * 4 + [10] * (4 * 4) + [11] * 4) * self.decks
	def shuffle(self):
		print "Shuffling Deck"
		self.deck = self.get_new_deck()	
		random.shuffle(self.deck)
		
class Dealer(Player):
	def __init__(self,decks):
		Player.__init__(self,"Dealer")	
		self.shuffle()
	def deal_cards(self,players):
		for i in range(0,2):
			for p in players:
				p.deal_card(self.draw_card())
			self.deal_card(self.draw_card())
	def clear_all_cards(self,players):
		for p in players:
			p.clear_cards()
		self.clear_cards()
	
	def play_hands(self,players):
		for p in players:
			self.play_hand(p)
	def player_wins(self,player):
		print "Player Wins"
		player.wins += 1
		dealer.losses += 1
		player.clear_cards()
	def player_loses(self,player):
		print "Player Loses"
		player.losses += 1
		dealer.wins += 1
		player.clear_cards()
	def show_upcard(self):
		return self.hand[0]
	def play_hand(self,player):
		if self.rules.blackjack(player.hand):
			self.player_wins(player)
		while not self.rules.bust(player.hand):
			if player.ask(self.show_upcard):
				player.deal_card(self.draw_card())
			else:
				return
		self.player_loses(player)

	
	
players = [ Player("jballs") ] 
decks = 6

dealer = Dealer(decks)


dealer.deal_cards(players)

dealer.play_hands(players)

dealer.deal_self()

dealer.check_hands(players)

dealer.clear_all_cards(players)





