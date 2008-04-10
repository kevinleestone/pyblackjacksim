package com.oremj.client;

import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.ClickListener;
import com.google.gwt.user.client.ui.Hyperlink;
import com.google.gwt.user.client.ui.Image;
import com.google.gwt.user.client.ui.KeyboardListener;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.RootPanel;
import com.google.gwt.user.client.ui.TextBox;
import com.google.gwt.user.client.ui.Widget;

/**
 * Entry point classes define <code>onModuleLoad()</code>.
 */
public class BlackJackApplication implements EntryPoint {

  /**
   * This is the entry point method.
   */
  public void onModuleLoad() {
	Hyperlink link = new Hyperlink("Deal","deal");
	

    final Game game = new Game();
	link.addClickListener(new ClickListener() {
		
		public void onClick(Widget sender) {
			// TODO Auto-generated method stub
			game.playRound();
		}
	
	});
	RootPanel.get().add(link);
	
    game.playRound();
  }
  
}
