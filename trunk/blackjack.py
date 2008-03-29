#!/usr/bin/python
import random


DOUBLE = 1
SPLIT  = 2
HIT    = 3
STAY   = 4

class Strategy:
	def __init__(self):
		pass
	
	def always(self,always_range,action):
		tmp_dict = {}
		for i in always_range:
			tmp_dict[i] = action
		return tmp_dict

class SimpleStrategy(Strategy):
	def __init__(self):
		Strategy.__init__(self)
	def action(self,hand,upcard):
		if hand.value() < 17:
			return HIT
		else: return STAY
class BasicStrategy(Strategy):
	def __init__(self):
		Strategy.__init__(self)
		self.strategy_table = {}
		for i in range(17,22):
			self.strategy_table[i] = self.always(range(2,12),STAY)
		for i in range(13,17):
			self.strategy_table[i] = self.always(range(2,7),STAY) 
			self.strategy_table[i].update(self.always(range(7,12),HIT))
		self.strategy_table[12] = { 2: HIT , 3: HIT } 
		self.strategy_table[12].update(self.always(range(4,7),STAY)) 
		self.strategy_table[12].update(self.always(range(7,12),HIT))
		for i in range(2,12):
			self.strategy_table[i] = self.always(range(2,12),HIT)
			
	def action(self,hand,upcard):
		try:
			return self.strategy_table[hand.value()][upcard]
		except KeyError:
			print "upcard: " + str(upcard)
			print "hand value: " + str(hand.value())
			raise

class BetterBasicStrategy(BasicStrategy):
	def __init__(self):
		BasicStrategy.__init__(self)
		self.strategy_table[11] = self.always(range(2,12), DOUBLE)


class Hand:
	def __init__(self):
		self.bet = 0
		self.cards = []
		self.sum = 0
	def card_value(self,card):
		if ( self.sum + card )  > 21 and card == 11:
			return 1
		else: return card 
	def value(self):
		return self.sum
	def deal_card(self,card):
		new_card = self.card_value(card)
		self.cards.append(self.card_value(card))
		self.sum += new_card
	def place_bet(self,bet):
		self.bet = bet
	def clear_cards(self):
		self.bet = 0
		self.cards = [] 
		self.sum = 0
class Player:
	def __init__(self,name,bankroll,playhands,strategy):
		self.name = name
		self.bankroll = bankroll
		self.strategy = strategy
		self.hands = []
		self.blackjacks = 0
		self.wins = 0
		self.losses = 0
		self.pushes = 0
		self.print_actions = False
		self.num_hands = playhands
	def print_action(self,action):
		if self.print_actions:
			print self.name + " " + action
	def clear_cards(self):
		for hand in self.hands:
			self.destroy_hand(hand)
	def bet_hands(self):
		for i in range(0,self.num_hands):
			self.bet_hand(Hand())
	def bet_hand(self,hand):
		self.bankroll -= 10
		hand.place_bet(10)
		self.print_action("bets " + str(10))
		self.hands.append(hand)

	def action(self,hand,upcard):
		return self.strategy.action(hand,upcard)
	def destroy_hand(self,hand):
		del self.hands[self.hands.index(hand)]
	def lose_all_hands(self):
		for h in self.hands:
			self.lose_hand(h)
	def win_all_hands(self):
		for h in self.hands:
			self.win_hand(h)
	def lose_hand(self,hand):
		if not hand.value():
			return
		self.print_action("loses hand")
		self.losses += 1
		self.destroy_hand(hand)
	def win_hand(self,hand):
		if not hand.value():
			return
		self.print_action("wins hand")
		self.wins += 1
		self.bankroll += hand.bet * 2
		self.destroy_hand(hand)
	def push_hand(self,hand):
		self.print_action("pushes")
		self.pushes += 1
		self.bankroll += hand.bet
		self.destroy_hand(hand)
	def blackjack_hand(self,hand):
		self.print_action("Blackjack!!")
		self.blackjacks += 1
		self.bankroll += hand.bet + hand.bet * (3./2.)
		self.destroy_hand(hand)
	def deal_card(self,hand,card):
		self.print_action("dealt " + str(card))
		hand.deal_card(card)

class Rules:
	def __init__(self):
		pass
			
	def blackjack(self,hand):
		return hand.value() == 21
	def bust(self,hand):
		return hand.value() > 21

class Blackjack:
	def __init__(self,dealer,players,rules,decks,minbet):
		self.decks = decks
		self.deck = []
		self.rules = rules
		self.minbet = minbet
		self.players = players
		self.dealer = dealer
		self.shuffles = 0
	def play_hand(self):
		self.dealer.hands.append(Hand())
		self.take_bets()
		self.deal_cards()
		if self.rules.blackjack(dealer.hands[0]):
			dealer.print_action("blackjack everyone loses")
			self.everybody_loses()
			return
		self.for_all_hands(self.check_blackjacks)
		self.for_all_hands(self.hand_actions)
		self.play_dealer()
		if self.rules.bust(self.dealer.hands[0]):
			self.everybody_wins()
			return
		self.for_all_hands(self.eval_hand)
	def clear_all_cards(self):
		for p in self.players:
			p.clear_cards()
		dealer.clear_cards()
		
	def eval_hand(self,player,hand):
		if hand.value() > dealer.hands[0].value():
			player.win_hand(hand)
		elif hand.value() < dealer.hands[0].value():
			player.lose_hand(hand)
		else: 
			player.push_hand(hand)
	def play_dealer(self):
		hand = self.dealer.hands[0]
		while not self.rules.bust(hand):
			if hand.value() < 17:
				dealer.print_action("hits")
				self.deal_card(self.dealer,hand)
			else: return
			
	def hand_actions(self,player,hand):
		while not self.rules.bust(hand):
			action = player.action(hand,dealer.show_upcard())
			if action == HIT:
				player.print_action("hits")
				self.deal_card(player,hand)
			elif action == STAY:
				return
			elif action == DOUBLE:
				hand.bet *= 2
				self.deal_card(player,hand)
				return
		player.lose_hand(hand)
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
	def everybody_wins(self):
		for p in players:
			p.win_all_hands()
		
	def take_bets(self):
		for p in self.players:
			p.bet_hands()
	def draw_card(self):
		try:
			card = self.deck.pop()
		except IndexError: 
			self.shuffle()
			self.shuffles += 1
			#print "Shuffling for the " + str(self.shuffles) + " time"
			card = self.deck.pop()
		return card
	def deal_card(self,player,hand):
		player.deal_card(hand,self.draw_card())
	def deal_cards(self):
		for i in range(0,2):
			self.for_all_hands(self.deal_card)
			self.deal_card(dealer,dealer.hands[0])
	def get_new_deck(self):
		return (range(2,10) * 4 + [10] * (4 * 4) + [11] * 4) * self.decks
	def shuffle(self):
		self.deck = self.get_new_deck()	
		random.shuffle(self.deck)
		
class Dealer(Player):
	def __init__(self):
		Player.__init__(self,"Dealer",10000000000000000000,1,Strategy())	
	def show_upcard(self):
		return self.hands[0].cards[0]

	
	
players = [ Player("jballs",1000,1,BetterBasicStrategy()), Player("woo",1000,1,SimpleStrategy()) ] 
dealer = Dealer()
decks = 6

dealer = Dealer()

bj = Blackjack(dealer,players,Rules(),decks,10)

for i in range(0,10):
#	print
	bj.play_hand()
	bj.clear_all_cards()

for p in players:
	print "=============== " + p.name + " ==============="
	print "Strategy: " + p.strategy.__class__.__name__
	print "Blackjacks: " + str(p.blackjacks)
	print "Wins: " + str(p.wins)
	print "Losses: " + str(p.losses)
	print "Pushes: " + str(p.pushes)
	print "Bankroll: " + str(p.bankroll)

