package mcdo.controller;

import java.io.IOException;
import javafx.fxml.FXML;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.Button;
import mcdo.App;
import mcdo.util.Constants;

public class AdminChoiceController {
    
    @FXML
    private Button placeOrderButton;
    
    @FXML
    private Button manageAccountsButton;
    
    @FXML
    private void initialize() {
        // Set up button actions
        placeOrderButton.setOnAction(event -> {
            try {
                handlePlaceOrder();
            } catch (IOException e) {
                showErrorAlert("Navigation Error", "Could not navigate to order type page: " + e.getMessage());
            }
        });
        
        manageAccountsButton.setOnAction(event -> {
            try {
                handleManageAccounts();
            } catch (IOException e) {
                showErrorAlert("Navigation Error", "Could not navigate to admin page: " + e.getMessage());
            }
        });
    }
    
    @FXML
    private void handlePlaceOrder() throws IOException {
        // Navigate to order type page
        App.setRoot(Constants.ORDER_TYPE_FXML);
    }
    
    @FXML
    private void handleManageAccounts() throws IOException {
        // Navigate to admin page
        App.setRoot(Constants.ADMIN_FXML);
    }
    
    private void showErrorAlert(String title, String content) {
        Alert alert = new Alert(AlertType.ERROR);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(content);
        alert.showAndWait();
    }
} 