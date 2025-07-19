package mcdo.controller;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.nio.file.*;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import mcdo.App;
import mcdo.model.OrderItem;
import mcdo.model.Product;

public final class CartController {

    /* Single global list the UI can observe  */
    private static final ObservableList<OrderItem> ITEMS =
            FXCollections.observableArrayList();
    
    private static WatchService watchService;
    private static Thread watchThread;
    private static boolean isWatching = false;

    private CartController() {}   // no instances

    /* --------------- API ---------------- */
    public static ObservableList<OrderItem> getItems() { 
        return ITEMS; 
    }

    /**
     * Start watching orders.txt for changes
     */
    public static void startWatchingOrdersFile() {
        if (isWatching) return;
        
        try {
            watchService = FileSystems.getDefault().newWatchService();
            Path path = Paths.get("orders.txt").getParent();
            path.register(watchService, StandardWatchEventKinds.ENTRY_MODIFY);
            
            watchThread = new Thread(() -> {
                try {
                    while (isWatching) {
                        WatchKey key = watchService.take();
                        for (WatchEvent<?> event : key.pollEvents()) {
                            if (event.context().toString().equals("orders.txt")) {
                                // Reload cart from orders.txt
                                loadFromOrdersFile();
                            }
                        }
                        key.reset();
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            
            isWatching = true;
            watchThread.start();
        } catch (IOException e) {
            System.err.println("Error setting up file watch: " + e.getMessage());
        }
    }

    /**
     * Stop watching orders.txt for changes
     */
    public static void stopWatchingOrdersFile() {
        isWatching = false;
        if (watchService != null) {
            try {
                watchService.close();
            } catch (IOException e) {
                System.err.println("Error closing watch service: " + e.getMessage());
            }
        }
        if (watchThread != null) {
            watchThread.interrupt();
        }
    }

    /**
     * Force refresh the cart from orders.txt
     */
    public static void refreshFromOrdersFile() {
        loadFromOrdersFile();
    }

    public static void add(Product p) {
        if (p == null) {
            System.err.println("Cannot add null product to cart");
            return;
        }
        
        try {
            // Find existing item with the same product name
            ITEMS.stream()
                 .filter(oi -> oi.getProduct().getName().equals(p.getName()))
                 .findFirst()
                 .ifPresentOrElse(
                     orderItem -> {
                         orderItem.increment();
                         // Save to orders.txt
                         saveToOrdersFile();
                     },
                     () -> {
                         OrderItem newItem = new OrderItem(p);
                         ITEMS.add(newItem);
                         // Save to orders.txt
                         saveToOrdersFile();
                     }
                 );
        } catch (Exception e) {
            System.err.println("Error adding product to cart: " + e.getMessage());
        }
    }

    public static void add(OrderItem item) {
        if (item == null) {
            System.err.println("Cannot add null order item to cart");
            return;
        }
        
        try {
            // Find existing item with the same product name
            ITEMS.stream()
                 .filter(oi -> oi.getProduct().getName().equals(item.getProduct().getName()))
                 .findFirst()
                 .ifPresentOrElse(
                     orderItem -> {
                         orderItem.setQuantity(orderItem.getQuantity() + item.getQuantity());
                         // Save to orders.txt
                         saveToOrdersFile();
                         // Notify listeners of the change
                         ITEMS.set(ITEMS.indexOf(orderItem), orderItem);
                     },
                     () -> {
                         ITEMS.add(item);
                         // Save to orders.txt
                         saveToOrdersFile();
                     }
                 );
        } catch (Exception e) {
            System.err.println("Error adding order item to cart: " + e.getMessage());
        }
    }

    public static void updateItemQuantity(OrderItem item, int newQuantity) {
        if (item == null || newQuantity < 0) {
            return;
        }
        
        try {
            int index = ITEMS.indexOf(item);
            if (index != -1) {
                if (newQuantity == 0) {
                    ITEMS.remove(index);
                } else {
                    item.setQuantity(newQuantity);
                    ITEMS.set(index, item);
                }
                // Save to orders.txt
                saveToOrdersFile();
            }
        } catch (Exception e) {
            System.err.println("Error updating item quantity: " + e.getMessage());
        }
    }

    public static void remove(OrderItem oi) { 
        if (oi != null) {
            ITEMS.remove(oi);
            // Update orders.txt
            saveToOrdersFile();
        }
    }

    public static void clear() {
        ITEMS.clear();
        // Clear orders.txt
        try {
            new FileWriter("orders.txt", false).close();
        } catch (IOException e) {
            System.err.println("Error clearing orders file: " + e.getMessage());
        }
    }

    public static double getTotal() {
        try {
            return ITEMS.stream().mapToDouble(OrderItem::getLineTotal).sum();
        } catch (Exception e) {
            System.err.println("Error calculating cart total: " + e.getMessage());
            return 0.0;
        }
    }
    
    public static int getItemCount() {
        return ITEMS.stream().mapToInt(OrderItem::getQuantity).sum();
    }

    public static boolean isEmpty() {
        return ITEMS.isEmpty();
    }

    /**
     * Loads orders from orders.txt into the cart
     * This method should be called when the application starts
     */
    public static void loadFromOrdersFile() {
        ITEMS.clear();
        try {
            File file = new File("orders.txt");
            if (!file.exists()) {
                file.createNewFile();
                return;
            }

            List<OrderItem> loadedItems = new ArrayList<>();
            try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    if (line.trim().isEmpty()) continue;
                    
                    try {
                        String[] parts = line.split(",");
                        if (parts.length >= 4) {
                            String productName = parts[0].trim();
                            int quantity = Integer.parseInt(parts[1].trim());
                            double price = Double.parseDouble(parts[2].trim());
                            String timestamp = parts[3].trim();
                            
                            // Validate data
                            if (quantity <= 0 || price < 0) {
                                System.err.println("Invalid data in orders.txt, skipping line: " + line);
                                continue;
                            }
                            
                            Product product = new Product(productName, price, "", Product.Category.BURGER);
                            OrderItem orderItem = new OrderItem(product);
                            orderItem.setQuantity(quantity);
                            
                            loadedItems.add(orderItem);
                        }
                    } catch (NumberFormatException e) {
                        System.err.println("Invalid number format in orders.txt, skipping line: " + line);
                    }
                }
            }
            
            // Add all valid items to the cart
            ITEMS.addAll(loadedItems);
            
        } catch (IOException e) {
            System.err.println("Error loading orders from file: " + e.getMessage());
        }
    }

    /**
     * Saves current cart contents to orders.txt
     * This method is called whenever the cart is modified
     */
    public static void saveToOrdersFile() {
        try {
            File file = new File("orders.txt");
            // Create backup of current file
            if (file.exists()) {
                File backup = new File("orders.txt.bak");
                if (backup.exists()) {
                    backup.delete();
                }
                file.renameTo(backup);
            }
            
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(file))) {
                for (OrderItem item : ITEMS) {
                    String line = String.format("%s,%d,%.2f,%s",
                        item.getProduct().getName(),
                        item.getQuantity(),
                        item.getProduct().getPrice(),
                        LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
                    writer.write(line);
                    writer.newLine();
                }
            }
            
            // If save was successful, delete backup
            File backup = new File("orders.txt.bak");
            if (backup.exists()) {
                backup.delete();
            }
            
        } catch (IOException e) {
            System.err.println("Error saving orders to file: " + e.getMessage());
            // Try to restore from backup if save failed
            File backup = new File("orders.txt.bak");
            if (backup.exists()) {
                backup.renameTo(new File("orders.txt"));
            }
        }
    }

    /**
     * Saves the current cart contents to a text file in the project's receipts directory
     * @param filename The name of the file to save to (without extension)
     * @return true if the save was successful, false otherwise
     */
    public static boolean saveToFile(String filename) {
        if (isEmpty()) {
            System.err.println("Cannot save empty cart to file");
            return false;
        }

        try {
            // Get the project's root directory
            String projectPath = System.getProperty("user.dir");
            File receiptsDir = new File(projectPath, "receipts");
            
            // Create receipts directory if it doesn't exist
            if (!receiptsDir.exists()) {
                boolean created = receiptsDir.mkdirs();
                if (!created) {
                    System.err.println("Failed to create receipts directory");
                    return false;
                }
            }

            File outputFile = new File(receiptsDir, filename + ".txt");
            System.out.println("Attempting to save to: " + outputFile.getAbsolutePath());

            try (FileWriter writer = new FileWriter(outputFile)) {
                // Write header
                writer.write("==========================================\n");
                writer.write("              MCDONALD'S ORDER            \n");
                writer.write("==========================================\n\n");
                
                // Write date and time
                LocalDateTime now = LocalDateTime.now();
                DateTimeFormatter formatter = DateTimeFormatter.ofPattern("MM/dd/yyyy HH:mm:ss");
                writer.write("Date: " + now.format(formatter) + "\n");
                
                // Write order type
                String orderType = App.getOrderType();
                if (orderType != null && !orderType.isEmpty()) {
                    writer.write("Order Type: " + orderType + "\n");
                } else {
                    writer.write("Order Type: Dine In\n");
                }
                
                // Write user information
                String currentUser = App.getCurrentUser();
                if (currentUser != null && !currentUser.isEmpty()) {
                    writer.write("Ordered by: " + currentUser + "\n");
                }
                writer.write("\n");
                
                // Write items
                writer.write("ITEMS ORDERED:\n");
                writer.write("------------------------------------------\n");
                for (OrderItem item : ITEMS) {
                    writer.write(String.format("%-30s ₱%.2f\n", 
                        item.getProduct().getName(), 
                        item.getProduct().getPrice()));
                    writer.write(String.format("  Quantity: %d\n", item.getQuantity()));
                    writer.write(String.format("  Subtotal: ₱%.2f\n", item.getLineTotal()));
                    writer.write("------------------------------------------\n");
                }
                
                // Write total
                writer.write("\nTOTAL AMOUNT: ₱" + String.format("%.2f", getTotal()) + "\n");
                
                System.out.println("Successfully saved to: " + outputFile.getAbsolutePath());
                
                // Clear the cart and orders.txt after successful save
                clear();
                
                return true;
            }
        } catch (Exception e) {
            System.err.println("Error saving cart to file: " + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }

    /**
     * Increment the quantity of an item by 1, given the OrderItem.
     */
    public static void incrementItem(OrderItem item) {
        if (item == null) return;
        int index = ITEMS.indexOf(item);
        if (index != -1) {
            item.increment();
            ITEMS.set(index, item);
            saveToOrdersFile();
        }
    }

    /**
     * Decrement the quantity of an item by 1, given the OrderItem.
     * If quantity reaches 0, remove the item.
     */
    public static void decrementItem(OrderItem item) {
        if (item == null) return;
        int index = ITEMS.indexOf(item);
        if (index != -1) {
            item.decrement();
            if (item.getQuantity() <= 0) {
                ITEMS.remove(index);
            } else {
                ITEMS.set(index, item);
            }
            saveToOrdersFile();
        }
    }

    /**
     * Update the quantity of a product in the cart by product reference.
     * If newQty is 0, remove the item.
     */
    public static void updateProductQuantity(Product product, int newQty) {
        if (product == null || newQty < 0) return;
        ITEMS.stream()
            .filter(item -> item.getProduct().getName().equals(product.getName()))
            .findFirst()
            .ifPresent(item -> updateItemQuantity(item, newQty));
    }
}
