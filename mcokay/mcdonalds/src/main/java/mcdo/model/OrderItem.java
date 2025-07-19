package mcdo.model;

import javafx.beans.property.IntegerProperty;
import javafx.beans.property.SimpleIntegerProperty;
import mcdo.controller.CartController;
import mcdo.controller.CartController;

/** one line in the shopping cart */
public class OrderItem {

    private final Product product;
    private final IntegerProperty quantity = new SimpleIntegerProperty(1);

    public OrderItem(Product product) {
        this.product = product;
        
        // Add listener to quantity changes
        quantity.addListener((obs, oldVal, newVal) -> {
            // Save to orders.txt whenever quantity changes
            CartController.saveToOrdersFile();
        });
    }

    /* ------------ derived -------------- */
    public double getLineTotal() { return getQuantity() * product.getPrice(); }

    /* ------------ getters / setters ---- */
    public Product getProduct()           { return product; }

    public int getQuantity()              { return quantity.get(); }
    public void setQuantity(int q)        { quantity.set(q);        }
    public IntegerProperty quantityProperty() { return quantity; }

    public void increment() { setQuantity(getQuantity()+1); }
    public void decrement() { 
        if (getQuantity() > 1) setQuantity(getQuantity()-1);
    }
}
