package com.oremj.client;

import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.ClickListener;
import com.google.gwt.user.client.ui.DockPanel;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.RootPanel;
import com.google.gwt.user.client.ui.SimplePanel;
import com.google.gwt.user.client.ui.VerticalPanel;
import com.google.gwt.user.client.ui.Widget;


public class Game {
	private Shoe shoe;
	private Player player;
	private Dealer dealer;
	private HorizontalPanel button_panel;
	private DockPanel dock_panel;
	private final SimplePanel player_status;
	private boolean in_game;
	public Game() {
		shoe = new Shoe(6);
		in_game = false;
		dealer = new Dealer();
		player = new Player("Test");
		button_panel = new HorizontalPanel();
		dock_panel = new DockPanel();
		player_status = new SimplePanel();
		player_status.add(player.getBankrollLabel());
		
		
		VerticalPanel vert_panel = new VerticalPanel();
		vert_panel.add(dealer.getNameLabel());
		vert_panel.add(dealer.getPanel());
		vert_panel.add(player.getNameLabel());
		vert_panel.add(player.getPanel());
		dock_panel.add(vert_panel, DockPanel.CENTER);
		dock_panel.add(player_status, DockPanel.EAST);
		RootPanel.get().add(dock_panel);
		RootPanel.get().add(button_panel);
	}
	
	public void playRound() {
		if ( ! in_game  ) {
			in_game = true;
			initHands();
		}
	}
	
	public void endRound() {
		player.endHand();
		dealer.endHand();
		button_panel.clear();
		in_game = false;
	}
	private void initHands() {
		player.getCard(shoe.deal());
		dealer.getCard(shoe.deal()).flip();
		player.getCard(shoe.deal());
		dealer.getCard(shoe.deal());
		dealer.displayHand();
		player.displayHand();
		if (isBlackjack(dealer)) {
			player_lose();
			return;
		}
		if (isBlackjack(player)) {
			player_win(3/2);
			return;
		}
		addHitStand();
	}
	private boolean isBlackjack( Player p ) {
		if (p.handValue() == 21) {
			return true;
		}
		return false;
	}
	private boolean isBust( Player p ) {
		if (p.handValue() > 21) {
			return true;
		}
		return false;
	}
	private void hit() {
		player.getCard(shoe.deal());
		player.displayHand();
		if (isBust(player)) {
			player_lose();
		}
	}
	
	private void stay() {
		button_panel.clear();
		dealOutDealer();
	}
	private void dealOutDealer() {
		while (dealer.handValue() < 17) {
			dealer.getCard(shoe.deal());
			dealer.displayHand();
		}
		checkHands();
	}
	
	private void player_lose( ) {
		player.takeMoney(10);
		endRound();
	}
	private void player_win( float multiplier) {
		player.giveMoney(10 * multiplier);
		endRound();
	}
	private void player_push() {
		endRound();;
	}
	private void checkHands() {
		if (dealer.handValue() > player.handValue() ) {
			player_lose();
		} else if (player.handValue() > dealer.handValue() ) {
			player_win(1);
		} else {
			player_push();
		}
	}
	private void addHitStand() {
		Button hit = new Button("Hit");
		Button stay = new Button("Stay");
		hit.addClickListener(new ClickListener() {
			public void onClick(Widget sender) {
				hit();
			}
		});
		stay.addClickListener(new ClickListener() {
		
			public void onClick(Widget sender) {
				stay();
			}
		
		});
		button_panel.add(hit);
		button_panel.add(stay);
	}
	
}
