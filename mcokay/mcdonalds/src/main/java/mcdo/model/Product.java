package mcdo.model;

public class Product {
    public enum Category { BURGER, DRINK, CHICKEN, FRIES, RICEBOWLS, BREAKFAST, MCCAFE }

    private final String   name;
    private final double   price;
    private final String   imagePath;    // e.g. "/images/fooditems/bigmac.png"
    private final Category category;
    private final String   description;

    public Product(String name, double price, String imagePath, Category cat) {
        this(name, price, imagePath, cat, "");
    }

    public Product(String name, double price, String imagePath, Category cat, String description) {
        this.name = name;
        this.price = price;
        this.imagePath = imagePath;
        this.category = cat;
        this.description = description;
    }

    /* ---- getters ---- */
    public String   getName()        { return name;        }
    public double   getPrice()       { return price;       }
    public String   getImagePath()   { return imagePath;   }
    public Category getCategory()    { return category;    }
    public String   getDescription() { return description; }
}
