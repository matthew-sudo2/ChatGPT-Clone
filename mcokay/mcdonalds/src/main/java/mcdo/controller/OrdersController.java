package mcdo.controller;

import java.io.IOException;
import java.net.URL;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ResourceBundle;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.Button;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import mcdo.App;
import mcdo.model.OrderItem;
import mcdo.model.Product;
import mcdo.util.Constants;

public class OrdersController implements Initializable {

    @FXML private ImageView logoImage;
    @FXML private TableView<OrderItem> orderTable;
    @FXML private TableColumn<OrderItem, String> productNameCol;
    @FXML private TableColumn<OrderItem, Integer> quantityCol;
    @FXML private TableColumn<OrderItem, Double> priceCol;
    @FXML private TableColumn<OrderItem, String> timestampCol;
    
    @FXML private TextField productNameField;
    @FXML private TextField quantityField;
    @FXML private TextField priceField;
    
    @FXML private Button btncreate;
    @FXML private Button btnupdate;
    @FXML private Button btndelete;
    @FXML private Button btnback;

    private ObservableList<OrderItem> orderList = FXCollections.observableArrayList();

    @Override
    public void initialize(URL url, ResourceBundle rb) {
        // Set up logo
        logoImage.setImage(new Image(App.class.getResource("/images/mcdonalds-png-logo-2772.png").toExternalForm()));
        
        // Initialize table columns
        productNameCol.setCellValueFactory(new PropertyValueFactory<>("productName"));
        quantityCol.setCellValueFactory(new PropertyValueFactory<>("quantity"));
        priceCol.setCellValueFactory(new PropertyValueFactory<>("price"));
        timestampCol.setCellValueFactory(new PropertyValueFactory<>("timestamp"));
        
        // Set up table
        orderTable.setItems(orderList);
        
        // Add listener for table selection
        orderTable.getSelectionModel().selectedItemProperty().addListener((obs, oldSelection, newSelection) -> {
            if (newSelection != null) {
                productNameField.setText(newSelection.getProduct().getName());
                quantityField.setText(String.valueOf(newSelection.getQuantity()));
                priceField.setText(String.valueOf(newSelection.getProduct().getPrice()));
            }
        });
        
        // Set up back button
        btnback.setOnAction(event -> {
            try {
                App.setRoot(Constants.MENU_FXML);
            } catch (IOException e) {
                showError("Failed to return to menu");
            }
        });
        
        // Load initial data
        loadOrders();
    }

    @FXML
    private void createOrder() {
        try {
            String productName = productNameField.getText().trim();
            int quantity = Integer.parseInt(quantityField.getText().trim());
            double price = Double.parseDouble(priceField.getText().trim());
            
            if (productName.isEmpty()) {
                showError("Please enter a product name");
                return;
            }
            
            if (quantity <= 0) {
                showError("Quantity must be greater than 0");
                return;
            }
            
            if (price <= 0) {
                showError("Price must be greater than 0");
                return;
            }
            
            Product product = new Product(productName, price, "", Product.Category.BURGER);
            OrderItem orderItem = new OrderItem(product);
            orderItem.setQuantity(quantity);
            
            orderList.add(orderItem);
            clearFields();
            
            // Save to orders.txt
            saveOrderToFile(orderItem);
            
            showSuccess("Order added successfully");
        } catch (NumberFormatException e) {
            showError("Please enter valid numbers for quantity and price");
        }
    }

    @FXML
    private void updateOrder() {
        OrderItem selectedItem = orderTable.getSelectionModel().getSelectedItem();
        if (selectedItem == null) {
            showError("Please select an order to update");
            return;
        }
        
        try {
            String productName = productNameField.getText().trim();
            int quantity = Integer.parseInt(quantityField.getText().trim());
            double price = Double.parseDouble(priceField.getText().trim());
            
            if (productName.isEmpty()) {
                showError("Please enter a product name");
                return;
            }
            
            if (quantity <= 0) {
                showError("Quantity must be greater than 0");
                return;
            }
            
            if (price <= 0) {
                showError("Price must be greater than 0");
                return;
            }
            
            // Create new product and order item
            Product product = new Product(productName, price, "", Product.Category.BURGER);
            OrderItem newOrderItem = new OrderItem(product);
            newOrderItem.setQuantity(quantity);
            
            // Replace the old item with the new one
            int index = orderList.indexOf(selectedItem);
            orderList.set(index, newOrderItem);
            
            clearFields();
            
            // Update orders.txt
            updateOrderInFile(newOrderItem);
            
            showSuccess("Order updated successfully");
        } catch (NumberFormatException e) {
            showError("Please enter valid numbers for quantity and price");
        }
    }

    @FXML
    private void deleteOrder() {
        OrderItem selectedItem = orderTable.getSelectionModel().getSelectedItem();
        if (selectedItem == null) {
            showError("Please select an order to delete");
            return;
        }
        
        orderList.remove(selectedItem);
        clearFields();
        
        // Update orders.txt
        deleteOrderFromFile(selectedItem);
        
        showSuccess("Order deleted successfully");
    }

    private void loadOrders() {
        orderList.clear();
        // Load orders from file
        // This will be handled by OrderManager
    }

    private void saveOrderToFile(OrderItem order) {
        // This will be handled by OrderManager
    }

    private void updateOrderInFile(OrderItem order) {
        // This will be handled by OrderManager
    }

    private void deleteOrderFromFile(OrderItem order) {
        // This will be handled by OrderManager
    }

    private void clearFields() {
        productNameField.clear();
        quantityField.clear();
        priceField.clear();
        orderTable.getSelectionModel().clearSelection();
    }

    private void showError(String message) {
        Alert alert = new Alert(AlertType.ERROR);
        alert.setTitle("Error");
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }

    private void showSuccess(String message) {
        Alert alert = new Alert(AlertType.INFORMATION);
        alert.setTitle("Success");
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }
} 