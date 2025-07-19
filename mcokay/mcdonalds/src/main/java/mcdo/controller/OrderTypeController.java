package mcdo.controller;

import java.io.IOException;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import mcdo.App;
import mcdo.util.Constants;

public class OrderTypeController {

    @FXML
    private Button dineIn;

    @FXML
    private Button takeOut;

    @FXML
    private Button backButton;

    @FXML
    private void initialize() {
        // When "Dine In" is clicked
        dineIn.setOnAction(event -> {
            App.setOrderType(Constants.ORDER_TYPE_DINE_IN);
            System.out.println("Order type selected: " + Constants.ORDER_TYPE_DINE_IN);
            goToMenu();
        });

        // When "Take Out" is clicked
        takeOut.setOnAction(event -> {
            App.setOrderType(Constants.ORDER_TYPE_TAKE_OUT);
            System.out.println("Order type selected: " + Constants.ORDER_TYPE_TAKE_OUT);
            goToMenu();
        });

        // When back button is clicked
        backButton.setOnAction(event -> {
            try {
                App.setRoot(Constants.LOGIN_FXML);
            } catch (IOException e) {
                System.err.println("Error navigating to login: " + e.getMessage());
                e.printStackTrace();
            }
        });
    }

    private void goToMenu() {
        try {
            App.setRoot(Constants.MENU_FXML);
        } catch (IOException e) {
            System.err.println("Error navigating to menu: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
