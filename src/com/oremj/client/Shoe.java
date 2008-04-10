package com.oremj.client;

import java.util.ArrayList;

import com.google.gwt.user.client.Random;

public class Shoe {
	private int num_decks;
	private ArrayList deck;
	private String[] suits;
	private String[] idents;
	public Shoe(int decks) {
		num_decks = decks;
		deck = new ArrayList();
		String[] suits_init = { "spades", "hearts", "clubs", "diamonds" };
		String[] idents_init = {"2", "3", "4","5","6","7","8","9","10","j","q","k","a"};
		this.suits = suits_init;
		this.idents = idents_init;
		shuffle();
	}
	
	public void shuffle() {
		for ( int i = 0; i < suits.length; i++) {
			for ( int j = 0; j < idents.length; j++) {
				deck.add(new Card(suits[i],idents[j]));
			}
		}
	}
	
	public Card deal() {
		int random_index;
		if (! cardsInDeck()) {
			shuffle();
		}
		random_index = Random.nextInt(deck.size());

		return (Card) deck.remove(random_index);
	}
	
	
	private boolean cardsInDeck() {
		if (deck.size() == 0) return false;
		
		return true;
	}
}
