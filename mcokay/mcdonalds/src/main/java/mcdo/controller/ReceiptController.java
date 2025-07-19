package mcdo.controller;

import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.io.File;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Priority;
import javafx.scene.layout.Region;
import javafx.scene.layout.VBox;
import mcdo.App;
import mcdo.controller.CartController;
import mcdo.model.OrderItem;
import mcdo.util.Constants;

public class ReceiptController {
    
    @FXML private Label orderNumberLabel;
    @FXML private Label dateTimeLabel;
    @FXML private Label cashierLabel;
    @FXML private Label orderTypeLabel;
    @FXML private Label customerNameLabel;
    @FXML private Label printStatusLabel;
    @FXML private VBox itemsContainer;
    @FXML private Label subtotalLabel;
    @FXML private Label taxLabel;
    @FXML private Label totalLabel;
    @FXML private Label amountPaidLabel;
    @FXML private Label changeLabel;
    @FXML private Button saveToFileButton;
    
    private List<OrderItem> completedOrder;
    
    @FXML private void initialize() {
        // Store the current cart items before clearing
        completedOrder = new ArrayList<>(CartController.getItems());
        System.out.println("Cart has " + CartController.getItems().size() + " items");
        System.out.println("Completed order size: " + completedOrder.size());
        
        // Generate order number
        Random random = new Random();
        int orderNumber = 1000 + random.nextInt(9000);
        orderNumberLabel.setText(String.valueOf(orderNumber));
        
        // Set current date/time
        LocalDateTime now = LocalDateTime.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("MM/dd/yyyy HH:mm:ss");
        dateTimeLabel.setText(now.format(formatter));
        
        // Set cashier
        cashierLabel.setText("Kiosk #01");
        
        // Set customer name
        String currentUser = App.getCurrentUser();
        customerNameLabel.setText(currentUser != null && !currentUser.isEmpty() ? currentUser : "Guest");
        
        // Set order type
        String orderType = App.getOrderType();
        orderTypeLabel.setText(orderType != null && !orderType.isEmpty() ? orderType : "Dine In");
        
        // Populate items list
        populateItemsList();
        
        // Calculate totals
        calculateTotals();
        
        // Set up save to file button
        saveToFileButton.setOnAction(e -> handleSaveToFile());
    }
    
    private void populateItemsList() {
        itemsContainer.getChildren().clear();
        
        for (OrderItem item : completedOrder) {
            // Create main container for each item with better styling
            VBox itemBox = new VBox(6);
            itemBox.setStyle("-fx-padding: 16 0; -fx-border-color: #f0f0f0; -fx-border-width: 0 0 1 0;");
            
            // Top row: Product name and line total
            HBox topRow = new HBox();
            topRow.setStyle("-fx-alignment: center-left;");
            
            Label nameLabel = new Label(item.getProduct().getName());
            nameLabel.setStyle("-fx-font-weight: bold; -fx-font-size: 16px; -fx-text-fill: #333333;");
            
            Region spacer = new Region();
            HBox.setHgrow(spacer, Priority.ALWAYS);
            
            Label lineTotalLabel = new Label(String.format("%s %.2f", Constants.CURRENCY_SYMBOL, item.getLineTotal()));
            lineTotalLabel.setStyle("-fx-font-weight: bold; -fx-font-size: 16px; -fx-text-fill: #DA291C;");
            
            topRow.getChildren().addAll(nameLabel, spacer, lineTotalLabel);
            
            // Bottom row: Quantity and unit price with better formatting
            HBox bottomRow = new HBox();
            bottomRow.setStyle("-fx-alignment: center-left; -fx-spacing: 16;");
            
            Label qtyLabel = new Label("Qty: " + item.getQuantity());
            qtyLabel.setStyle("-fx-font-size: 14px; -fx-text-fill: #666666; -fx-font-weight: bold;");
            
            Label priceLabel = new Label(String.format("@ %s%.2f each", Constants.CURRENCY_SYMBOL, item.getProduct().getPrice()));
            priceLabel.setStyle("-fx-font-size: 14px; -fx-text-fill: #666666;");
            
            bottomRow.getChildren().addAll(qtyLabel, priceLabel);
            
            itemBox.getChildren().addAll(topRow, bottomRow);
            itemsContainer.getChildren().add(itemBox);
        }
        
        // Add a summary line if multiple items
        if (completedOrder.size() > 1) {
            VBox summaryBox = new VBox(8);
            summaryBox.setStyle("-fx-padding: 16 0 8 0; -fx-border-color: #DA291C; -fx-border-width: 2 0 0 0;");
            
            Label summaryLabel = new Label("Order Summary");
            summaryLabel.setStyle("-fx-font-weight: bold; -fx-font-size: 14px; -fx-text-fill: #DA291C;");
            
            int totalItems = completedOrder.stream().mapToInt(OrderItem::getQuantity).sum();
            Label itemCountLabel = new Label(String.format("Total Items: %d", totalItems));
            itemCountLabel.setStyle("-fx-font-size: 14px; -fx-text-fill: #666666;");
            
            summaryBox.getChildren().addAll(summaryLabel, itemCountLabel);
            itemsContainer.getChildren().add(summaryBox);
        }
    }
    
    private void calculateTotals() {
        double total = completedOrder.stream()
            .mapToDouble(OrderItem::getLineTotal)
            .sum();
        
        // Calculate subtotal and tax more accurately
        double subtotal = total / (1 + Constants.VAT_RATE); // Remove VAT to get subtotal
        double tax = total - subtotal;
        
        subtotalLabel.setText(String.format("%s %.2f", Constants.CURRENCY_SYMBOL, subtotal));
        taxLabel.setText(String.format("%s %.2f", Constants.CURRENCY_SYMBOL, tax));
        totalLabel.setText(String.format("%s %.2f", Constants.CURRENCY_SYMBOL, total));
        amountPaidLabel.setText(String.format("%s %.2f", Constants.CURRENCY_SYMBOL, total));
        changeLabel.setText(String.format("%s 0.00", Constants.CURRENCY_SYMBOL));
    }
    
    @FXML private void handleSaveToFile() {
        String filename = "order_" + orderNumberLabel.getText() + "_" + 
                         LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
        if (CartController.saveToFile(filename)) {
            System.out.println("Order saved to: resources/receipts/" + filename + ".txt");
            // Clear the cart after successful save
            CartController.clear();
        } else {
            System.out.println("Failed to save order to file");
        }
    }
    
    @FXML private void handlePrint() {
        printStatusLabel.setText("Print receipt feature coming soon!");
        printStatusLabel.setStyle("-fx-text-fill: #ff9800;");
    }
    
    @FXML private void handleNewOrder() throws IOException {
        // Clear the cart before starting a new order
        CartController.clear();
        // Navigate directly to the menu
        App.setRoot("menu");
    }
}
