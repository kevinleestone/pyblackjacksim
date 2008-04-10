package com.oremj.client;

import java.util.ArrayList;

import com.google.gwt.user.client.ui.HorizontalPanel;

public class Hand {
	private ArrayList cards;
	public Hand() {
		cards = new ArrayList();
	}
	public void addCard(Card card) {
		cards.add(card);
	}
	public void destroyHand() {
		cards = new ArrayList();
	}
	public void displayHand(HorizontalPanel panel) {
		panel.clear();
		for ( int i = 0; i < cards.size(); i++) {
			panel.add(((Card)cards.get(i)).getImage());
		}
		
	}
}
