package mcdo.util;

/**
 * Application constants
 */
public final class Constants {
    
    // Application Configuration
    public static final String APP_TITLE = "McDonald's Kiosk";
    public static final double WINDOW_WIDTH = 1280.0;
    public static final double WINDOW_HEIGHT = 720.0;
    
    // Order Types
    public static final String ORDER_TYPE_DINE_IN = "Dine In";
    public static final String ORDER_TYPE_TAKE_OUT = "Take Out";
    
    // Currency
    public static final String CURRENCY_SYMBOL = "₱";
    
    // Tax Configuration
    public static final double VAT_RATE = 0.12; // 12% VAT
    
    // Validation
    public static final int MIN_PASSWORD_LENGTH = 3;
    public static final int MAX_USERNAME_LENGTH = 50;
    public static final int MAX_PASSWORD_LENGTH = 100;
    
    // File Paths
    public static final String ACCOUNTS_FILE = "/accounts.txt";
    public static final String ORDERS_FILE = "/orders.txt";
    public static final String LOGO_IMAGE = "/images/mcdonalds-png-logo-2772.png";
    public static final String FOOD_PLACEHOLDER_IMAGE = "/images/fooditems/pngwing.com.png";
    
    // FXML Files
    public static final String WELCOME_FXML = "welcome";
    public static final String LOGIN_FXML = "welcome";  // Login uses the welcome screen
    public static final String SIGNUP_FXML = "signup";
    public static final String ORDER_TYPE_FXML = "order_type";
    public static final String MENU_FXML = "menu";
    public static final String CHECKOUT_FXML = "checkout";
    public static final String RECEIPT_FXML = "receipt";
    public static final String PAYMENT_CHOICE_FXML = "paymentchoice";
    public static final String ADMIN_FXML = "admin";
    public static final String ADMIN_CHOICE_FXML = "adminchoice";
    
    // CSS Files
    public static final String MENU_CSS = "/mcdo/css/menu.css";
    public static final String MENU_CSS_ALT = "/css/menu.css";
    
    // Messages
    public static final String LOGIN_SUCCESS_MSG = "Login successful for user: ";
    public static final String LOGIN_ERROR_TITLE = "Login Error";
    public static final String LOGIN_FAILED_TITLE = "Login Failed";
    public static final String SIGNUP_ERROR_TITLE = "Sign Up Error";
    public static final String NAVIGATION_ERROR_TITLE = "Navigation Error";
    
    // Error Messages
    public static final String ERROR_EMPTY_USERNAME = "Please enter a username.";
    public static final String ERROR_EMPTY_PASSWORD = "Please enter a password.";
    public static final String ERROR_INVALID_CREDENTIALS = "Invalid username or password. Please try again.";
    public static final String ERROR_PASSWORD_TOO_SHORT = "Password must be at least " + MIN_PASSWORD_LENGTH + " characters long.";
    public static final String ERROR_PASSWORDS_DONT_MATCH = "Passwords do not match.";
    public static final String ERROR_USERNAME_EXISTS = "Username already exists. Please choose a different username.";
    public static final String ERROR_INVALID_CHARACTERS = "Contains invalid characters (commas, line breaks not allowed).";
    
    // Success Messages
    public static final String SUCCESS_REGISTRATION = "Account created successfully! You can now log in.";
    public static final String SUCCESS_USERNAME_AVAILABLE = "Username available ✓";
    public static final String SUCCESS_PASSWORDS_MATCH = "Passwords match ✓";
    
    // Animation
    public static final int FADE_DURATION_MS = 300;
    public static final double CARD_HOVER_SCALE = 1.02;
    public static final double BUTTON_PRESS_SCALE = 0.98;
    
    private Constants() {
        // Prevent instantiation
    }
} 