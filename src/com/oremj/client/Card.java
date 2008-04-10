package com.oremj.client;

import com.google.gwt.user.client.ui.Image;

public class Card {
	private String suit;
	private String ident;
	public Card(String suit, String ident) {
		this.suit = suit;
		this.ident = ident;
	}
		
	public String toURL() {
		return "img/" + suit + "-" + ident + "-150.png";
	}
	
	public Image getImage() {
		return new Image(toURL());
	}
}
