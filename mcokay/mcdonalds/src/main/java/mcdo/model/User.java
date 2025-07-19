package mcdo.model;

import javafx.beans.property.SimpleStringProperty;
import javafx.beans.property.StringProperty;

public class User {
    private final SimpleStringProperty username;
    private final SimpleStringProperty password;
    private final SimpleStringProperty accountcreated;
    private final SimpleStringProperty accountstatus;

    public User(String uname, String pword, String dcreated, String astatus) {
        this.username = new SimpleStringProperty(uname);
        this.password = new SimpleStringProperty(pword);
        this.accountcreated = new SimpleStringProperty(dcreated);
        this.accountstatus = new SimpleStringProperty(astatus);
    }

    // Username property methods
    public StringProperty usernameProperty() {
        return username;
    }

    public String getUsername() {
        return username.get();
    }

    public void setUsername(String username) {
        this.username.set(username);
    }

    // Password property methods
    public StringProperty passwordProperty() {
        return password;
    }

    public String getPassword() {
        return password.get();
    }

    public void setPassword(String password) {
        this.password.set(password);
    }

    // Account created property methods
    public StringProperty accountcreatedProperty() {
        return accountcreated;
    }

    public String getAccountcreated() {
        return accountcreated.get();
    }

    public void setAccountcreated(String accountcreated) {
        this.accountcreated.set(accountcreated);
    }

    // Account status property methods
    public StringProperty accountstatusProperty() {
        return accountstatus;
    }

    public String getAccountstatus() {
        return accountstatus.get();
    }

    public void setAccountstatus(String accountstatus) {
        this.accountstatus.set(accountstatus);
    }

    @Override
    public String toString() {
        return "User{" +
                "username=" + getUsername() +
                ", password=" + getPassword() +
                ", accountcreated=" + getAccountcreated() +
                ", accountstatus=" + getAccountstatus() +
                '}';
    }
}
