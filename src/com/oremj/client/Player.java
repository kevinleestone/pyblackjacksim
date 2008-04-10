package com.oremj.client;

import com.google.gwt.user.client.ui.HTML;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.RootPanel;

public class Player {
	private String name;
	private Hand hand;
	final private HorizontalPanel hand_panel;
	public Player(String name) {
		this.name = name;
		this.hand = new Hand();
		hand_panel = new HorizontalPanel();
		RootPanel.get().add(new Label(name));
		RootPanel.get().add(hand_panel);
	}
	
	public void endHand() {
		hand.destroyHand();
	}
	public void getCard(Card card) {
		hand.addCard(card);
	}
	
	public void displayHand() {
		hand.displayHand(hand_panel);
	}
}
