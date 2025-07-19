package mcdo;

import java.io.IOException;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import mcdo.util.Constants;
import mcdo.controller.CartController;

/**
 * Main entry-point for the McDonald's kiosk.
 */
public class App extends Application {

    /* ───────────  singletons  ─────────── */
    private static Stage primaryStage;   // kept for global navigation
    private static Scene scene;          // current scene (always non-null after start)
    private static String orderType;     // "Dine-in" | "Take-out"
    private static String currentUser;   // currently logged in user

    /* ───────────  JavaFX life-cycle  ─────────── */
    @Override
    public void start(Stage stage) throws IOException {
        /* 1️⃣  cache the stage reference immediately */
        primaryStage = stage;

        /* 2️⃣  load first view ("welcome.fxml") */
        scene = new Scene(loadFXML(Constants.WELCOME_FXML), 
                         Constants.WINDOW_WIDTH, 
                         Constants.WINDOW_HEIGHT);

        /* 3️⃣  normal stage plumbing */
        primaryStage.setScene(scene);
        primaryStage.setTitle(Constants.APP_TITLE);
        primaryStage.setResizable(false); // Fixed size for kiosk
        primaryStage.centerOnScreen();
        primaryStage.show();
    }

    @Override
    public void stop() {
        // Clear orders.txt when application closes
        CartController.clear();
    }

    /* ───────────  navigation helpers  ─────────── */

    /** Switch the root to another FXML (found under /mcdo/fxml/). */
    public static void setRoot(String fxml) throws IOException {
        scene.setRoot(loadFXML(fxml));
    }

    /** Convenience for controllers that need the *live* scene. */
    public static Scene getCurrentScene() {
        return scene;          // always valid after start()
    }

    /** Expose the stage only if you truly need it (e.g. dialogs). */
    public static Stage getPrimaryStage() {
        return primaryStage;
    }

    /* ───────────  order-type (Dine-in / Take-out)  ─────────── */
    public static void   setOrderType(String type) { orderType = type; }
    public static String getOrderType()            { return orderType; }

    /* ───────────  current user  ─────────── */
    public static void   setCurrentUser(String user) { currentUser = user; }
    public static String getCurrentUser()            { return currentUser; }

    /* ───────────  helpers  ─────────── */

    /** Loads an FXML from the class-path location "/mcdo/fxml/<n>.fxml". */
    private static Parent loadFXML(String name) throws IOException {
        String resourcePath = "/mcdo/fxml/" + name + ".fxml";
        System.out.println("Loading FXML from: " + resourcePath);
        FXMLLoader loader = new FXMLLoader(App.class.getResource(resourcePath));
        if (loader.getLocation() == null) {
            throw new IOException("Could not find FXML file: " + resourcePath);
        }
        return loader.load();
    }

    public static void main(String[] args) { launch(args); }
}