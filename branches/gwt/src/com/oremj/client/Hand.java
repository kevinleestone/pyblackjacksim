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
	public void allFaceUp() {
		Card tmp_card; 
		for ( int i = 0; i < cards.size(); i++) {
			tmp_card = (Card) cards.get(i);
			if (tmp_card.isFacedown()) {
				tmp_card.flip();
			}
		}
	}
	public int handValue() {
		int hand_value = 0;
		Card tmp_card;
		for ( int i = 0; i < cards.size(); i++) {
			tmp_card = (Card) cards.get(i);
			hand_value += tmp_card.value();
		}
		return hand_value;
	}
}
