package com.oremj.client;


public class Game {
	private Shoe shoe;
	private Player player;
	private Dealer dealer;
	public Game() {
		shoe = new Shoe(6);
		dealer = new Dealer();
		player = new Player("Test");
	}
	
	public void playRound() {
		initHands();
	}
	
	public void endRound() {
		player.endHand();
		dealer.endHand();
	}
	private void initHands() {
		dealer.getCard(shoe.deal());
		dealer.getCard(shoe.deal());
		dealer.displayHand();
		player.getCard(shoe.deal());
		player.getCard(shoe.deal());
		player.displayHand();
		
	}
}
