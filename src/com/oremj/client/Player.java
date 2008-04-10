package com.oremj.client;

import com.google.gwt.user.client.ui.HTML;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.RootPanel;

public class Player {
	private String name;
	private Hand hand;
	private float bankroll;
	final private HorizontalPanel hand_panel;
	final private Label bankroll_label;
	public Player(String name) {
		bankroll = 1000;
		bankroll_label = new Label();
		this.name = name;
		this.hand = new Hand();
		hand_panel = new HorizontalPanel();
		refreshBankroll();

	}
	
	private void refreshBankroll() {
		bankroll_label.setText(String.valueOf(bankroll));
	}
	public void endHand() {
		hand.allFaceUp();
		displayHand();
		hand.destroyHand();
	}

	public Card getCard(Card card) {
		hand.addCard(card);
		return card;
	}
	
	public void displayHand() {
		hand.displayHand(hand_panel);
	}
	
	public int handValue() {
		return hand.handValue();
	}
	
	public Label getNameLabel() {
		return new Label(name);
	}
	
	public Label getBankrollLabel() {
		return bankroll_label;
	}
	public HorizontalPanel getPanel() {
		return hand_panel;
	}
	public int takeMoney(int amount) {
		bankroll -= amount;
		refreshBankroll();
		return amount;
	}
	
	public void giveMoney(float amount) {
		bankroll += amount;
		refreshBankroll();
	}
}
