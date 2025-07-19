module com.example {
    requires javafx.controls;
    requires javafx.fxml;
    requires java.logging;

    opens mcdo to javafx.graphics;
    opens mcdo.controller to javafx.fxml;
    opens mcdo.util to javafx.fxml;
    opens mcdo.model to javafx.fxml;

    exports mcdo;
    exports mcdo.util;
    exports mcdo.model;
}
