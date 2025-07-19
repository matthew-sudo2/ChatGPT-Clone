package mcdo.controller;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.net.URL;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.ResourceBundle;
import java.util.Scanner;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.Button;
import javafx.scene.control.ChoiceBox;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import javafx.scene.control.cell.PropertyValueFactory;
import mcdo.App;
import mcdo.model.User;
import mcdo.util.Constants;

public class AdminController implements Initializable {

    ObservableList<User> mylist = FXCollections.observableArrayList();

    @FXML
    private Button btncreate;

    @FXML
    private Button btndelete;

    @FXML
    private Button btnupdate;

    @FXML
    private Button btnback;

    @FXML
    private TableColumn<User, String> usernamecol;

    @FXML
    private TableColumn<User, String> passwordcol;

    @FXML
    private TableColumn<User, String> statuscol;

    @FXML
    private TableColumn<User, String> accountcreatedcol;

    @FXML
    private TableView<User> mytable;

    @FXML
    TextField usernametextfield;

    @FXML
    TextField passwordtextfield;

    @FXML
    ChoiceBox<String> statuschoicebox;

    String filename = "accounts.txt";

    @Override
    public void initialize(URL url, ResourceBundle rb) {
        initializeCol();
        loadData();

        // Add items to the choice box to match your original code
        statuschoicebox.getItems().addAll("admin", "customer");

        // Listener to update text fields when a row is selected
        mytable.getSelectionModel().selectedItemProperty().addListener((obs, oldSelection, newSelection) -> {
            if (newSelection != null) {
                usernametextfield.setText(newSelection.getUsername());
                passwordtextfield.setText(newSelection.getPassword());
                statuschoicebox.setValue(newSelection.getAccountstatus());
            } else {
                // Clear fields when no row is selected
                clearFields();
            }
        });
        btnback.setOnAction(event -> {
            try {
                App.setRoot(Constants.WELCOME_FXML);
            } catch (IOException e) {
                Alert alert = new Alert(AlertType.ERROR);
                alert.setContentText("failed to go back");
            }
        });
    }

    private void initializeCol() {
        usernamecol.setCellValueFactory(new PropertyValueFactory<>("username"));
        passwordcol.setCellValueFactory(new PropertyValueFactory<>("password"));
        accountcreatedcol.setCellValueFactory(new PropertyValueFactory<>("accountcreated"));
        statuscol.setCellValueFactory(new PropertyValueFactory<>("accountstatus"));

        // Set column widths
        usernamecol.setPrefWidth(200);
        passwordcol.setPrefWidth(200);
        accountcreatedcol.setPrefWidth(200);
        statuscol.setPrefWidth(150);

        // Make columns resizable
        usernamecol.setResizable(true);
        passwordcol.setResizable(true);
        accountcreatedcol.setResizable(true);
        statuscol.setResizable(true);
    }

    private void loadData() {
        System.out.println("Starting loadData()...");
        mylist.clear();
        System.out.println("Cleared mylist");

        try {
            File myFile = new File("accounts.txt");
            System.out.println("Looking for file: " + myFile.getAbsolutePath());

            if (myFile.exists()) {
                System.out.println("File exists, size: " + myFile.length() + " bytes");
                Scanner filescanner = new Scanner(myFile);

                while (filescanner.hasNextLine()) {
                    String data = filescanner.nextLine();
                    System.out.println("Raw line from file: " + data);
                    
                    if (data.trim().isEmpty()) {
                        System.out.println("Skipping empty line");
                        continue;
                    }
                    
                    String[] parts = data.split(",");
                    System.out.println("Split into " + parts.length + " parts");
                    
                    if (parts.length >= 4) {
                        String username = parts[0].trim();
                        String password = parts[1].trim();
                        String dcreated = parts[2].trim();
                        String status = parts[3].trim();
                        
                        System.out.println("Creating user with:");
                        System.out.println("  Username: " + username);
                        System.out.println("  Password: " + password);
                        System.out.println("  Date Created: " + dcreated);
                        System.out.println("  Status: " + status);
                        
                        User user = new User(username, password, dcreated, status);
                        mylist.add(user);
                        System.out.println("Added user to list. Current list size: " + mylist.size());
                    } else {
                        System.out.println("Invalid data format, skipping line");
                    }
                }
                filescanner.close();
                
                System.out.println("Setting table items. List size: " + mylist.size());
                mytable.setItems(mylist);
                System.out.println("Refreshing table");
                mytable.refresh();
                System.out.println("Table refresh complete");
            } else {
                System.out.println("File does not exist, creating new file");
                myFile.createNewFile();
            }
        } catch (Exception e) {
            System.out.println("Error in loadData: " + e.getMessage());
            e.printStackTrace();
        }
        System.out.println("loadData() completed");
    }

    @FXML
    private boolean createuser(ActionEvent event) {
        String username = usernametextfield.getText().trim();
        String password = passwordtextfield.getText().trim();
        String status = statuschoicebox.getValue();
        
        if (status != null) {
            status = status.trim();
        }

        if (username.isEmpty()) {
            Alert alert = new Alert(AlertType.ERROR);
            alert.setContentText("No username provided");
            alert.showAndWait();
            return false;
        }

        if (password.isEmpty()) {
            Alert alert = new Alert(AlertType.ERROR);
            alert.setContentText("No password provided");
            alert.showAndWait();
            return false;
        }

        if (status == null || status.isEmpty()) {
            Alert alert = new Alert(AlertType.ERROR);
            alert.setContentText("Please select a status");
            alert.showAndWait();
            return false;
        }

        // Get current date
        LocalDate today = LocalDate.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("MM-dd-yyyy");
        String formattedDate = today.format(formatter);

        try {
            File file = new File("CCOBJPGL_PROJECT_COM246/mcokay/accounts.txt");
            boolean isNewFile = !file.exists();
            
            BufferedWriter myWriter = new BufferedWriter(new FileWriter(file, true));
            
            if (!isNewFile && file.length() > 0) {
                myWriter.newLine();
            }
            
            myWriter.write(username + "," + password + "," + formattedDate + "," + status);
            myWriter.close();

            Alert alert = new Alert(AlertType.INFORMATION);
            alert.setTitle("Success");
            alert.setHeaderText("User created successfully");
            alert.setContentText("Welcome " + username + "! You can now use this username to log in.");
            alert.showAndWait();
            
            // Clear fields and reload data
            clearFields();
            loadData();
            return true;

        } catch (IOException e) {
            Alert alert = new Alert(AlertType.ERROR);
            alert.setTitle("Error");
            alert.setHeaderText("Failed to create user");
            alert.setContentText("An error occurred while creating the user: " + e.getMessage());
            alert.showAndWait();
            return false;
        }
    }
    

    @FXML  
    public boolean deleteuser(ActionEvent event) {
        // Check if a user is selected from the table
        User selectedUser = mytable.getSelectionModel().getSelectedItem();
        if (selectedUser == null) {
            Alert alert = new Alert(AlertType.ERROR);
            alert.setTitle("No User Selected");
            alert.setHeaderText("Please select a user from the table to delete");
            alert.setContentText("Click on a row in the table to select a user for deletion.");
            alert.showAndWait();
            return false;
        }

        String username = selectedUser.getUsername();
        System.out.println("Deleting user: " + username);

        String userToDelete = username;

        List<String> updatedLines = new ArrayList<>();

        // Step 1: Read and filter lines
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (!line.trim().isEmpty()) { // skip empty lines
                    String[] parts = line.split(",");
                    if (!parts[0].equalsIgnoreCase(userToDelete)) {
                        updatedLines.add(line);
                    }
                }
            }
        } catch (IOException e) {
            Alert alert = new Alert(AlertType.ERROR);
            alert.setTitle("File Error");
            alert.setHeaderText("Failed to read accounts file");
            alert.setContentText("Error: " + e.getMessage());
            alert.showAndWait();
            e.printStackTrace();
            return false;
        }

        // Step 2: Write back without trailing newline
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
            for (int i = 0; i < updatedLines.size(); i++) {
                writer.write(updatedLines.get(i));
                if (i < updatedLines.size() - 1) {
                    writer.newLine(); // add newline except after the last line
                }
            }
        } catch (IOException e) {
            Alert alert = new Alert(AlertType.ERROR);
            alert.setTitle("File Error");
            alert.setHeaderText("Failed to write to accounts file");
            alert.setContentText("Error: " + e.getMessage());
            alert.showAndWait();
            e.printStackTrace();
            return false;
        }

        Alert alert = new Alert(AlertType.INFORMATION);
        alert.setTitle("Success");
        alert.setHeaderText("User deleted successfully");
        alert.setContentText("User '" + userToDelete + "' has been deleted from the system.");
        alert.showAndWait();
        
        // Clear fields and reload data
        clearFields();
        loadData();
        
        return true;
    }
    
    @FXML
    public boolean updateuser(ActionEvent event) {
        // Check if a user is selected from the table
        User selectedUser = mytable.getSelectionModel().getSelectedItem();
        if (selectedUser == null) {
            Alert alert = new Alert(AlertType.ERROR);
            alert.setTitle("No User Selected");
            alert.setHeaderText("Please select a user from the table to update");
            alert.setContentText("Click on a row in the table to select a user for updating.");
            alert.showAndWait();
            return false;
        }

        String username = usernametextfield.getText();
        String password = passwordtextfield.getText();
        String status = statuschoicebox.getValue();

        // Trim all values
        username = username.trim();
        password = password.trim();
        if (status != null) {
            status = status.trim();
        }

        // Validation
        if (username.isEmpty()) {
            Alert alert = new Alert(AlertType.ERROR);
            alert.setTitle("Validation Error");
            alert.setHeaderText("Username is required");
            alert.setContentText("Please enter a username.");
            alert.showAndWait();
            return false;
        }

        if (password.isEmpty()) {
            Alert alert = new Alert(AlertType.ERROR);
            alert.setTitle("Validation Error");
            alert.setHeaderText("Password is required");
            alert.setContentText("Please enter a password.");
            alert.showAndWait();
            return false;
        }

        if (status == null || status.isEmpty()) {
            Alert alert = new Alert(AlertType.ERROR);
            alert.setTitle("Validation Error");
            alert.setHeaderText("Status is required");
            alert.setContentText("Please select a status (admin or customer).");
            alert.showAndWait();
            return false;
        }

        String targetUsername = selectedUser.getUsername();
        String newPassword = password;
        String newUsername = username;
        String newStatus = status;

        List<String> updatedLines = new ArrayList<>();

        // Step 1: Read and update
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (!line.trim().isEmpty()) {
                    String[] parts = line.split(",");

                    if (parts.length == 4 && parts[0].equalsIgnoreCase(targetUsername)) {
                        // Update the line with new password and status, keep original date
                        updatedLines.add(newUsername + "," + newPassword + "," + selectedUser.getAccountcreated() + "," + newStatus);
                    } else {
                        updatedLines.add(line);
                    }
                }
            }
        } catch (IOException e) {
            Alert alert = new Alert(AlertType.ERROR);
            alert.setTitle("File Error");
            alert.setHeaderText("Failed to read accounts file");
            alert.setContentText("Error: " + e.getMessage());
            alert.showAndWait();
            e.printStackTrace();
            return false;
        }

        // Step 2: Write updated lines back
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
            for (int i = 0; i < updatedLines.size(); i++) {
                writer.write(updatedLines.get(i));
                if (i < updatedLines.size() - 1) {
                    writer.newLine(); // no extra blank line
                }
            }
        } catch (IOException e) {
            Alert alert = new Alert(AlertType.ERROR);
            alert.setTitle("File Error");
            alert.setHeaderText("Failed to write to accounts file");
            alert.setContentText("Error: " + e.getMessage());
            alert.showAndWait();
            e.printStackTrace();
            return false;
        }

        Alert alert = new Alert(AlertType.INFORMATION);
        alert.setTitle("Success");
        alert.setHeaderText("User successfully updated");
        alert.setContentText("User '" + targetUsername + "' has been updated with the new information.");
        alert.showAndWait();
        
        // Clear fields and reload data
        clearFields();
        loadData();
        return true;
    }
        

    private void clearFields() {
        usernametextfield.clear();
        passwordtextfield.clear();
        statuschoicebox.setValue(null);
        mytable.getSelectionModel().clearSelection();
    }
}