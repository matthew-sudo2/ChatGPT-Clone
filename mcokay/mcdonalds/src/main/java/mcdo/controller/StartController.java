package mcdo.controller;

import java.io.File;
import java.io.IOException;
import java.util.Scanner;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import mcdo.App;
import mcdo.model.User;
import mcdo.util.Constants;

public class StartController {

    @FXML
    private Label usernamelabel;

    @FXML
    private Label passwordlabel;

    @FXML
    private TextField usernametextfield;

    @FXML
    private PasswordField passwordfield;

    @FXML
    private Button loginbutton;

    @FXML
    private Button signupbutton;

    @FXML
    private void initialize() {
        // Set up sign up button action
        signupbutton.setOnAction(event -> {
            try {
                App.setRoot(Constants.SIGNUP_FXML);
            } catch (IOException e) {
                showErrorAlert(Constants.NAVIGATION_ERROR_TITLE, "Could not open sign up page: " + e.getMessage());
            }
        });
    }

    @FXML
    public void loginbuttonHandler(ActionEvent event) throws IOException {
        String username = usernametextfield.getText();
        String password = passwordfield.getText();

        if (username.isEmpty() || password.isEmpty()) {
            showErrorAlert(Constants.LOGIN_ERROR_TITLE, "Please enter both username and password");
            return;
        }

        User user = new User(username, password, "", "");

        File accountsfile = new File("accounts.txt");
        boolean loginSuccessful = false;

        if (accountsfile.exists()) {
            try (Scanner filescanner = new Scanner(accountsfile)) {
                while (filescanner.hasNextLine()) {
                    String data = filescanner.nextLine();
                    String[] parts = data.split(",");
                    
                    if (parts.length < 4) continue; // Skip invalid lines
                    
                    String fileuname = parts[0];
                    String filepword = parts[1];
                    String filestatus = parts[3];

                    if (fileuname.equals(user.getUsername()) && filepword.equals(user.getPassword())) {
                        loginSuccessful = true;
                        if (filestatus.equals("customer")) {
                            System.out.println(Constants.LOGIN_SUCCESS_MSG + username);
                            goOrderType();
                        } else if (filestatus.equals("admin")) {
                            System.out.println(Constants.LOGIN_SUCCESS_MSG + username);
                            goAdminChoice();
                        }
                        break;
                    }
                }
            }
        }

        if (!loginSuccessful) {
            showErrorAlert(Constants.LOGIN_FAILED_TITLE, Constants.ERROR_INVALID_CREDENTIALS);
        }
    }

    private void goOrderType() {
        try {
            App.setRoot(Constants.ORDER_TYPE_FXML);
        } catch (IOException e) {
            showErrorAlert(Constants.NAVIGATION_ERROR_TITLE, "Could not navigate to order type page: " + e.getMessage());
        }
    }

    private void goAdminChoice() {
        try {
            App.setRoot(Constants.ADMIN_CHOICE_FXML);
        } catch (IOException e) {
            showErrorAlert(Constants.NAVIGATION_ERROR_TITLE, "Could not navigate to admin choice page: " + e.getMessage());
        }
    }

    private void showErrorAlert(String title, String message) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }
}