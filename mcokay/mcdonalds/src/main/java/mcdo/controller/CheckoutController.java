package mcdo.controller;

import java.io.IOException;

import javafx.beans.property.ReadOnlyObjectWrapper;
import javafx.beans.property.ReadOnlyStringWrapper;
import javafx.collections.ListChangeListener;
import javafx.fxml.FXML;
import javafx.geometry.Pos;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TableCell;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Region;
import mcdo.App;
import mcdo.controller.CartController;
import mcdo.model.OrderItem;
import mcdo.util.Constants;

public class CheckoutController {

    @FXML private TableView<OrderItem>          table;
    @FXML private TableColumn<OrderItem,String> colName;
    @FXML private TableColumn<OrderItem,Integer>colQty;
    @FXML private TableColumn<OrderItem,Double> colPrice;
    @FXML private TableColumn<OrderItem,Double> colLineTot;
    @FXML private TableColumn<OrderItem,Void>   colAction;
    @FXML private Label grandTotal;

    @FXML private void initialize() {
        table.setItems(CartController.getItems());

        colName.setCellValueFactory(d -> new ReadOnlyStringWrapper(
                                            d.getValue().getProduct().getName()));
        colQty.setCellValueFactory(d -> new ReadOnlyObjectWrapper<>(
                                            d.getValue().getQuantity()));
        colPrice.setCellValueFactory(d -> new ReadOnlyObjectWrapper<>(
                                            d.getValue().getProduct().getPrice()));
        colLineTot.setCellValueFactory(d -> new ReadOnlyObjectWrapper<>(
                                            d.getValue().getLineTotal()));

        /* Plus/Minus buttons and X button in last column */
        colAction.setCellFactory(tc -> new TableCell<>() {
            final Button minusBtn = new Button("−");
            final Button plusBtn = new Button("+");
            final Button removeBtn = new Button("✕");
            final HBox buttonBox = new HBox(5);
            
            {
                minusBtn.setStyle("-fx-background-color: #ff6b6b; -fx-text-fill: white; -fx-font-weight: bold; -fx-min-width: 30px;");
                plusBtn.setStyle("-fx-background-color: #51cf66; -fx-text-fill: white; -fx-font-weight: bold; -fx-min-width: 30px;");
                removeBtn.setStyle("-fx-background-color: #868e96; -fx-text-fill: white; -fx-font-weight: bold; -fx-min-width: 30px;");
                
                buttonBox.setAlignment(Pos.CENTER);
                buttonBox.getChildren().addAll(minusBtn, plusBtn, removeBtn);
                
                minusBtn.setOnAction(e -> {
                    OrderItem item = getTableView().getItems().get(getIndex());
                    CartController.decrementItem(item);
                    table.refresh();
                    updateGrandTotal();
                });
                
                plusBtn.setOnAction(e -> {
                    OrderItem item = getTableView().getItems().get(getIndex());
                    CartController.incrementItem(item);
                    table.refresh();
                    updateGrandTotal();
                });
                
                removeBtn.setOnAction(e -> {
                    CartController.remove(getTableView().getItems().get(getIndex()));
                    updateGrandTotal();
                });
            }
            
            @Override protected void updateItem(Void v, boolean empty) {
                super.updateItem(v, empty);
                setGraphic(empty ? null : buttonBox);
            }
        });

        CartController.getItems().addListener(
            (ListChangeListener<? super OrderItem>) c ->
                updateGrandTotal()
        );
        updateGrandTotal();
    }
    
    public void updateGrandTotal() {
        grandTotal.setText(String.format("₱ %.2f", CartController.getTotal()));
    }

    @FXML private void backToMenu() throws IOException { App.setRoot("menu"); }

    @FXML private void completeOrder() throws IOException {
        if (CartController.isEmpty()) {
            javafx.scene.control.Alert alert = new javafx.scene.control.Alert(javafx.scene.control.Alert.AlertType.WARNING);
            alert.setTitle("Empty Cart");
            alert.setHeaderText(null);
            alert.setContentText("Your cart is empty. Please add items before completing the order.");
            alert.showAndWait();
            return;
        }
        App.setRoot(Constants.PAYMENT_CHOICE_FXML);
    }
}
