package mcdo.controller;

import java.io.IOException;
import javafx.fxml.FXML;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.paint.Color;
import mcdo.App;
import mcdo.util.Constants;

public class PaymentChoiceController {
    
    @FXML
    private Button payAtCounterButton;
    
    @FXML
    private Button cashlessButton;
    
    @FXML
    private Label cashlessStatusLabel;
    
    @FXML
    private void initialize() {
        // Set up button actions
        payAtCounterButton.setOnAction(event -> {
            try {
                handlePayAtCounter();
            } catch (IOException e) {
                showErrorAlert("Navigation Error", "Could not navigate to receipt page: " + e.getMessage());
            }
        });
        
        cashlessButton.setOnAction(event -> {
            handleCashless();
        });
    }
    
    @FXML
    private void handlePayAtCounter() throws IOException {
        // Navigate to receipt page
        App.setRoot(Constants.RECEIPT_FXML);
    }
    
    @FXML
    private void handleCashless() {
        // Show coming soon message
        cashlessStatusLabel.setText("Cashless payment coming soon!");
        cashlessStatusLabel.setTextFill(Color.ORANGE);
    }
    
    @FXML
    private void handleBack() throws IOException {
        // Return to checkout without clearing anything
        App.setRoot(Constants.CHECKOUT_FXML);
    }
    
    private void showErrorAlert(String title, String content) {
        Alert alert = new Alert(AlertType.ERROR);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(content);
        alert.showAndWait();
    }
} 