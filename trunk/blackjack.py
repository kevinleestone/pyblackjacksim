#!/usr/bin/python
import random
from optparse import OptionParser
import collections
import lib


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
		self.special_strategy = {}
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
			return self.special_strategy[tuple(hand.cards)][upcard] 
		except KeyError: pass
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
		self.special_strategy[(8,8)] = self.always(range(2,12),SPLIT)


class Hand:
	def __init__(self,player):
		self.bet = 0
		self.cards = []
		self.sum = 0
		self.player = player
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
		self.bet += bet
		self.player.take_money(bet)
	def to_tuple(self):
		return tuple(self.cards)
	def clear_cards(self):
		self.bet = 0
		self.cards = [] 
		self.sum = 0
	def destroy(self):
		self.player.destroy_hand(self)

def handfinisher(fn):
	def new(self,hand,*args):
		fn(self,hand,*args)
		self.destroy_hand(hand)	
		self.hands_played += 1
	return new
class Player:
	def __init__(self,name,bankroll,playhands,strategy):
		self.name = name
		self.bankroll = bankroll
		self.strategy = strategy
		self.hands = []
		self.outcomes = collections.defaultdict(lib.counterdict)
		self.print_actions = False
		self.num_hands = playhands
		self.card_count = 0
		self.hands_played = 0
	def print_action(self,action):
		if self.print_actions:
			print self.name + " " + action
	def round_over(self): 
		self.clear_cards()
	def clear_cards(self):
		for hand in self.hands:
			self.destroy_hand(hand)
	def bet_hands(self,minbet):
		for i in range(0,self.num_hands):
			self.bet_hand(Hand(self),minbet)
	def bet_hand(self,hand,minbet):
		hand.place_bet(minbet)
		self.print_action("bets " + str(minbet))
		self.hands.append(hand)
	def take_money(self,amount):
		self.bankroll -= amount	
	def double_bet(self,hand):
		hand.place_bet(hand.bet)
	def notify_count(self,count):
		self.card_count = count
	def action(self,hand,upcard):
		return self.strategy.action(hand,upcard)
	def destroy_hand(self,hand):
		self.hands.remove(hand)
	def lose_all_hands(self):
		for h in self.hands:
			self.lose_hand(h)
	def win_all_hands(self):
		for h in self.hands:
			self.win_hand(h)
	def split_hand(self,hand):
		self.give_money(hand,0)
		self.destroy_hand(hand)
	def give_money(self,hand,bet_multiplier):
		self.bankroll += hand.bet + ( hand.bet * bet_multiplier )

	def generate_outcome(self,outcome,hand):
		self.outcomes['outcomes'][outcome] += 1
		oc = self.outcomes['counts'].setdefault(self.card_count,lib.OutcomeCounter()).inc(outcome)
		oc = self.outcomes['starting_hands'].setdefault(tuple(sorted(hand.cards[:2])),lib.OutcomeCounter()).inc(outcome)
		
	@handfinisher
	def lose_hand(self,hand):
		if not hand.value():
			return
		self.print_action("loses hand")
		self.generate_outcome("lose",hand)

	@handfinisher
	def win_hand(self,hand):
		if not hand.value():
			return
		self.print_action("wins hand")
		self.generate_outcome("win",hand)
		self.give_money(hand,1)

			
	@handfinisher
	def push_hand(self,hand):
		self.print_action("pushes")
		self.generate_outcome("push",hand)
		self.give_money(hand,0)

	@handfinisher
	def blackjack_hand(self,hand):
		self.print_action("Blackjack!!")
		self.generate_outcome("blackjack",hand)
		self.generate_outcome("win",hand)
		self.give_money(hand,float(3/2))
	def deal_card(self,hand,card):
		self.print_action("dealt " + str(card))
		hand.deal_card(card)
	def print_stats(self):
		print "=============== " + self.name + " ==============="
		print "Strategy: " + self.strategy.__class__.__name__
		print "Blackjacks: " + str(self.outcomes['outcomes']['blackjack']) + " ( " + str(float(self.outcomes['outcomes']['blackjack']) / self.hands_played) + "% )"
		print "Wins: " + str(self.outcomes['outcomes']['win']) + " ( " + str(float(self.outcomes['outcomes']['win']) / self.hands_played) + "% )"
		print "Losses: " + str(self.outcomes['outcomes']['lose']) + " ( " + str(float(self.outcomes['outcomes']['lose']) / self.hands_played) + "% )"
		print "Pushes: " + str(self.outcomes['outcomes']['push']) + " ( " + str(float(self.outcomes['outcomes']['push']) / self.hands_played) + "% )"
		print "Bankroll: $" + str(self.bankroll)
		print "Deck Count Stats"
		self.print_count_stats()
		print "Starting Hand Stats"
		self.print_card_stats()
	def print_count_stats(self):
		columns = ('count', 'blackjack', 'win', 'push' , 'lose', 'win %')
		keys = self.outcomes['counts'].keys()
		keys.sort()
		print ("%10s" * len(columns)) % columns
		for count in keys:
			total_hands = 0
			outcome_counter = self.outcomes['counts'][count]
			print "%10d" % count,
			print "%10d" * 4  % (outcome_counter.blackjack, outcome_counter.win, outcome_counter.push,
							outcome_counter.lose),
			print "%10.2f%%" % (outcome_counter.win / outcome_counter.total() * 100, ) 
	def print_card_stats(self):
		columns = ('count', 'blackjack', 'win', 'push' , 'lose', 'win %')
		keys = self.outcomes['starting_hands'].keys()
		keys.sort(lambda x,y: cmp(sum(x),sum(y)))
		print ("%10s " * len(columns)) % columns
		for count in keys:
			total_hands = 0
			outcome_counter = self.outcomes['starting_hands'][count]
			print "%10s" % str(count),
			print "%10d " * 4 % (outcome_counter.blackjack, outcome_counter.win, outcome_counter.push,
							outcome_counter.lose),
			print "%10.2f%%" % (outcome_counter.win / outcome_counter.total() * 100, ) 


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
		self.count = 0
	def play_hand(self):
		self.dealer.hands.append(Hand(dealer))
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
				player.double_bet(hand)
				self.deal_card(player,hand)
				return
			elif action == SPLIT:
				# Take one of the pair off the current hand
				card = hand.cards.pop()

				player.split_hand(hand)

				# Create and play 2 new hands with starting card "card"
				for i in range(0,2):
				
					#create a new hand and add that card to it
					# FIXME: must not allow new_hand to change up the bet
					new_hand = Hand(player)
					player.bet_hand(new_hand,self.minbet)
					player.deal_card(new_hand,card)	
					
					#deal another card to the new_hand giving it 2
					player.deal_card(new_hand,self.draw_card())
					
					#play new hand
					self.hand_actions(player,new_hand)
				return 	
		player.lose_hand(hand)
	def notify_counts(self):
		for p in players:
			p.notify_count(self.count)
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
			p.bet_hands(self.minbet)
	def draw_card(self):
		try:
			card = self.deck.pop()
		except IndexError: 
			self.shuffle()
			self.shuffles += 1
			#print "Shuffling for the " + str(self.shuffles) + " time"
			card = self.deck.pop()
		if card <= 6: self.count += 1
		elif card >= 10: self.count -= 1
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
		self.count = 0
		
class Dealer(Player):
	def __init__(self):
		Player.__init__(self,"Dealer",10000000000000000000,1,Strategy())	
	def show_upcard(self):
		return self.hands[0].cards[0]

if __name__ == "__main__":	
	option_parser = OptionParser()
	option_parser.add_option("-n", "--hands", dest="hands", help='Number of hands to play', type="int", default=1)
	(options, args) = option_parser.parse_args()

		
	players = [ Player("Player 1",0,1,BetterBasicStrategy()), Player("Player 2",0,1,BasicStrategy()) ] 
	dealer = Dealer()
	decks = 6

	dealer = Dealer()

	bj = Blackjack(dealer,players,Rules(),decks,1)

	for i in range(0,options.hands):
	#	print
		bj.play_hand()
		bj.clear_all_cards()
		bj.notify_counts()

	for p in players:
		p.print_stats()
