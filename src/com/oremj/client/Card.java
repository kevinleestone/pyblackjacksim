package com.oremj.client;

import com.google.gwt.user.client.ui.Image;

public class Card {
	private String suit;
	private String ident;
	private boolean facedown;
	public Card(String suit, String ident) {
		this.suit = suit;
		this.ident = ident;
		facedown = false;
	}
		
	public String toURL() {
		return "img/" + suit + "-" + ident + "-150.png";
	}
	public void flip() {
		facedown = ! facedown;
	}
	public Image getImage() {
		if (facedown)
			return new Image("img/back-blue-150-3.png");
		return new Image(toURL());
	}
	
	public boolean isFacedown() {
		return facedown;
	}
	
	public int value() {
		if ( ident == "j" ||
				ident == "q" ||
				ident == "k" ) {
			return 10;
		} else if (ident == "a") {
			return 11;
		} else 
			return Integer.parseInt(ident);
	}
}
