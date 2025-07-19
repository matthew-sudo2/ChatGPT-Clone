package mcdo.controller;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Scanner;
import java.util.regex.Pattern;

import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import javafx.scene.paint.Color;
import mcdo.App;
import mcdo.util.Constants;

public class SignUpController {
    
    @FXML
    private TextField newusername;
    
    @FXML
    private PasswordField newpassword;
    
    @FXML
    private PasswordField confirmpassword;
    
    @FXML
    private Button signupbutton;
    
    @FXML
    private Button backbutton;
    
    @FXML
    private Label statuslabel;
    
    @FXML
    private Label passwordStrengthLabel;
    
    @FXML
    private Label passwordMatchLabel;
    
    @FXML
    private Label usernameStatusLabel;

    private static final Pattern HAS_UPPER = Pattern.compile("[A-Z]");
    private static final Pattern HAS_NUMBER = Pattern.compile("\\d");
    private static final Pattern HAS_SPECIAL = Pattern.compile("[!@#$%^&*(),.?\":{}|<>]");
    
    @FXML
    private void initialize() {
        // Set up button actions
        signupbutton.setOnAction(event -> {
            try {
                handleSignUp();
            } catch (FileNotFoundException ex) {
                Alert alert = new Alert(AlertType.ERROR);
                alert.setContentText("sign up button not working");
            }
        });
        backbutton.setOnAction(event -> {
            try {
                App.setRoot(Constants.WELCOME_FXML);
            } catch (IOException e) {
                Alert alert = new Alert(AlertType.ERROR);
                alert.setContentText("failed to go back");
            }
        });
        
        // Clear status label initially
        statuslabel.setText("");
        
        // Add password strength listener
        newpassword.textProperty().addListener((observable, oldValue, newValue) -> {
            updatePasswordStrength(newValue);
        });
        
        // Add password match listener
        confirmpassword.textProperty().addListener((observable, oldValue, newValue) -> {
            updatePasswordMatch(newValue);
        });
        
        // Add username availability checker
        newusername.textProperty().addListener((observable, oldValue, newValue) -> {
            checkUsernameAvailability(newValue);
        });
    }

    private void checkUsernameAvailability(String username) {
        if (username == null || username.trim().isEmpty()) {
            usernameStatusLabel.setText("");
            usernameStatusLabel.setTextFill(Color.GRAY);
            return;
        }
        
        if (isUsernameTaken(username.trim())) {
            usernameStatusLabel.setText("Username is already taken");
            usernameStatusLabel.setTextFill(Color.RED);
        } else {
            usernameStatusLabel.setText("Username is available");
            usernameStatusLabel.setTextFill(Color.GREEN);
        }
    }

    private void updatePasswordMatch(String confirmPass) {
        String password = newpassword.getText();
        
        if (confirmPass == null || confirmPass.isEmpty()) {
            passwordMatchLabel.setText("");
            passwordMatchLabel.setTextFill(Color.GRAY);
            return;
        }
        
        if (password.equals(confirmPass)) {
            passwordMatchLabel.setText("Passwords match");
            passwordMatchLabel.setTextFill(Color.GREEN);
        } else {
            passwordMatchLabel.setText("Passwords do not match");
            passwordMatchLabel.setTextFill(Color.RED);
        }
    }

    private void updatePasswordStrength(String password) {
        if (password == null || password.isEmpty()) {
            passwordStrengthLabel.setText("");
            passwordStrengthLabel.setTextFill(Color.GRAY);
            return;
        }

        // Count powers (uppercase, numbers, special characters)
        int powers = 0;
        for (char c : password.toCharArray()) {
            if (Character.isUpperCase(c)) powers++;
            if (Character.isDigit(c)) powers++;
            if (HAS_SPECIAL.matcher(String.valueOf(c)).find()) powers++;
        }

        boolean hasUpper = HAS_UPPER.matcher(password).find();
        boolean hasNumber = HAS_NUMBER.matcher(password).find();
        boolean hasSpecial = HAS_SPECIAL.matcher(password).find();

        // Check if required criteria are met
        boolean hasRequiredCriteria = hasUpper && hasSpecial && hasNumber;

        if (!hasRequiredCriteria) {
            String missing = "";
            if (!hasUpper) missing += "uppercase letter, ";
            if (!hasNumber) missing += "number, ";
            if (!hasSpecial) missing += "special symbol, ";
            missing = missing.substring(0, missing.length() - 2); // Remove last comma and space
            
            passwordStrengthLabel.setText("Missing: " + missing);
            passwordStrengthLabel.setTextFill(Color.RED);
        } else if (powers <= 3) {
            passwordStrengthLabel.setText("Medium Strength");
            passwordStrengthLabel.setTextFill(Color.ORANGE);
        } else if (powers <= 8) {
            passwordStrengthLabel.setText("Strong Password");
            passwordStrengthLabel.setTextFill(Color.GREEN);
        } else {
            passwordStrengthLabel.setText("Very Strong Password");
            passwordStrengthLabel.setTextFill(Color.DARKGREEN);
        }
    }

    private boolean isPasswordStrong(String password) {
        if (password == null || password.isEmpty()) return false;
        
        boolean hasUpper = HAS_UPPER.matcher(password).find();
        boolean hasNumber = HAS_NUMBER.matcher(password).find();
        boolean hasSpecial = HAS_SPECIAL.matcher(password).find();
        
        // Check if required criteria are met
        if (!hasUpper || !hasNumber || !hasSpecial) {
            return false;
        }
        
        // Count powers
        int powers = 0;
        for (char c : password.toCharArray()) {
            if (Character.isUpperCase(c)) powers++;
            if (Character.isDigit(c)) powers++;
            if (HAS_SPECIAL.matcher(String.valueOf(c)).find()) powers++;
        }
        
        return powers > 3; // At least "Medium" password required
    }

    private boolean isUsernameTaken(String username) {
        File accountsfile = new File("accounts.txt");
        if (!accountsfile.exists()) return false;
        
        try (Scanner filescanner = new Scanner(accountsfile)) {
            while (filescanner.hasNextLine()) {
                String data = filescanner.nextLine();
                String fileuname = data.split(",")[0];
                if (fileuname.equals(username)) {
                    return true;
                }
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        return false;
    }

    private void setStatusMessage(String message, Color color) {
        Platform.runLater(() -> {
            statuslabel.setText(message);
            statuslabel.setTextFill(color);
        });
    }
    
    private void handleSignUp() throws FileNotFoundException {
        String username = newusername.getText().trim();
        String password = newpassword.getText();
        String confirmPass = confirmpassword.getText();
        
        // Validate username
        if (username.isEmpty()) {
            setStatusMessage("Please enter a username", Color.RED);
            return;
        }
        
        if (isUsernameTaken(username)) {
            setStatusMessage("Username already exists!", Color.RED);
            return;
        }
        
        // Validate password
        if (password.isEmpty()) {
            setStatusMessage("Please enter a password", Color.RED);
            return;
        }
        
        if (!isPasswordStrong(password)) {
            setStatusMessage("Password is too weak. Please use a stronger password.", Color.RED);
            return;
        }
        
        if (!password.equals(confirmPass)) {
            setStatusMessage("Passwords do not match", Color.RED);
            return;
        }

        // Get current date
        LocalDate today = LocalDate.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("MM-dd-yyyy");
        String formattedDate = today.format(formatter);

        try {
            BufferedWriter myWriter = new BufferedWriter(new FileWriter("accounts.txt", true));
            myWriter.newLine();
            myWriter.write(username + "," + password + "," + formattedDate + "," + "customer");
            myWriter.close();

            Alert alert = new Alert(AlertType.INFORMATION);
            alert.setTitle("Success");
            alert.setHeaderText("Account created successfully");
            alert.setContentText("Welcome " + username + "! You can now use this username to log in.");
            alert.showAndWait();
            
            // Navigate back to welcome page
            App.setRoot(Constants.WELCOME_FXML);
            
        } catch (IOException e) {
            setStatusMessage("Error creating account: " + e.getMessage(), Color.RED);
        }
    }
}
