#!/usr/bin/python
import random


DOUBLE = 1
SPLIT  = 2
HIT    = 3
STAY   = 4

class Strategy:
	def __init__(self):
		pass
class BasicStrategy(Strategy):
	def __init__(self):
		Strategy.__init__(self)

class Hand:
	def __init__(self):
		self.bet = 0
		self.cards = []
	def deal_card(self,card):
		self.cards.append(card)
	def place_bet(self,bet):
		self.bet = bet
	def clear_cards(self):
		self.bet = 0
		self.cards = [] 
class Player:
	def __init__(self,name,bankroll):
		self.name = name
		self.bankroll = bankroll
		self.strategy = BasicStrategy()
		self.hands = [Hand()]
		self.blackjacks = 0
		self.wins = 0
		self.losses = 0
	def clear_cards(self):
		self.hand = []
		self.bet = 0
	def bet_hands(self):
		for h in self.hands:
			self.bet_hand(h)
	def bet_hand(self,hand):
		self.bankroll -= 10
		hand.place_bet(10)

	def ask(self,upcard):
		return HIT
	def lose_all_hands(self):
		for h in self.hands:
			self.lose_hand(h)
	def win_all_hands(self):
		for h in self.hands:
			self.win_hand(h)
	def lose_hand(self,hand):
		self.losses -= 1
		hand.clear_cards()
	def win_hand(self,hand):
		self.wins += 1
		self.bankroll += hand.bet
		hand.clear_cards()
	def blackjack_hand(self,hand):
		print "Blackjack!!"
		self.blackjack += 1
		self.bankroll += hand.bet * (3./2.)
		hand.clear_cards()

class Rules:
	def __init__(self):
		pass
	def blackjack(self,hand):
		return sum(hand.cards) == 21
	def bust(self,hand):
		return sum(hand.cards) > 21

class Blackjack:
	def __init__(self,dealer,players,rules,decks,minbet):
		self.decks = decks
		self.deck = []
		self.rules = rules
		self.minbet = minbet
		self.players = players
		self.dealer = dealer
	def play_hand(self):
		self.take_bets()
		self.deal_cards()
		if self.rules.blackjack(dealer.hands[0]):
			self.everybody_loses()
			return
		self.for_all_hands(self.check_blackjacks)

	def for_all_hands(self,func,*args,**kwargs):
		for p in players:
			for h in p.hands:
				func(p,h,*args,**kwargs)
	def check_blackjacks(self,player,hand):
		if self.rules.blackjack(hand):
			player.blackjack_hand(hand)

	def everybody_loses(self):
		for p in players:
			p.lose_all_hands()

		
	def take_bets(self):
		for p in self.players:
			p.bet_hands()
	def draw_card(self):
		try:
			card = self.deck.pop()
		except IndexError: 
			self.shuffle()
			card = self.deck.pop()
		return card
	def deal_card(self,player,hand):
		hand.deal_card(self.draw_card())
	def deal_cards(self):
		for i in range(0,2):
			self.for_all_hands(self.deal_card)
			dealer.hands[0].deal_card(self.draw_card())
	def get_new_deck(self):
		return (range(2,10) * 4 + [10] * (4 * 4) + [11] * 4) * self.decks
	def shuffle(self):
		print "Shuffling Deck"
		self.deck = self.get_new_deck()	
		random.shuffle(self.deck)
		
class Dealer(Player):
	def __init__(self):
		Player.__init__(self,"Dealer",10000000000000000000)	
	
	def play_hands(self,players):
		for p in players:
			self.play_hand(p)
	def show_upcard(self):
		return self.hand[0]

	
	
players = [ Player("jballs",1000) ] 
dealer = Dealer()
decks = 6

dealer = Dealer()

bj = Blackjack(dealer,players,Rules(),decks,10)
bj.play_hand()






