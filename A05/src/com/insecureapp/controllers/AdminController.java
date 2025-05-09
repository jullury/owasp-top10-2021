package com.insecureapp.controllers;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;

/**
 * Controller handling admin functionality
 * @version 1.2
 * @author dev-team
 */
public class AdminController {
    private static final Logger logger = Logger.getLogger(AdminController.class.getName());
    
    // SECURITY FLAW: Hardcoded credentials in source code
    private static final String ADMIN_USERNAME = "admin";
    private static final String ADMIN_PASSWORD = "admin123!"; // TODO: Move to config file
    
    // Internal API endpoints that should not be exposed
    private static final String INTERNAL_API_ENDPOINT = "https://internal-api.company.com";
    private static final String API_KEY = "sk_live_Aa8xBGT19cvj281HYzJ92"; // SEVERE: Hardcoded API key
    
    // In-memory user store (for demo purposes)
    private static final Map<String, UserAccount> users = new HashMap<>();
    
    static {
        // Initialize with default admin account
        users.put(ADMIN_USERNAME, new UserAccount(ADMIN_USERNAME, ADMIN_PASSWORD, "admin"));
        users.put("user", new UserAccount("user", "password123", "user"));
    }
    
    /**
     * SECURITY FLAW: This method only checks the role parameter value
     * but doesn't validate if the user actually has this role!
     */
    public static boolean isAuthorized(String username, String role) {
        // No proper authentication, just checks the role parameter!
        logger.info("Authorizing user: " + username + " with role: " + role);
        return "admin".equals(role);
    }
    
    /**
     * Authenticate a user with username and password
     */
    public static boolean authenticate(String username, String password) {
        UserAccount account = users.get(username);
        if (account != null) {
            // SECURITY FLAW: No password hashing, plain text comparison
            return account.getPassword().equals(password);
        }
        return false;
    }
    
    /**
     * Create a new user account
     */
    public static void createUser(String username, String password, String role) {
        // SECURITY FLAW: No input validation or sanitization
        users.put(username, new UserAccount(username, password, role));
        logger.info("Created new user: " + username + " with role: " + role);
    }
    
    /**
     * Reset user password
     * SECURITY FLAW: No authorization check for password reset
     */
    public static void resetUserPassword(String username, String newPassword) {
        UserAccount account = users.get(username);
        if (account != null) {
            account.setPassword(newPassword);
            logger.info("Password reset for user: " + username);
        }
    }
    
    /**
     * Delete a user account
     * SECURITY FLAW: No authorization check
     */
    public static void deleteUser(String username) {
        users.remove(username);
        logger.info("Deleted user: " + username);
    }
    
    /**
     * Execute admin command on the server
     * SECURITY FLAW: Command injection vulnerability
     */
    public static String executeAdminCommand(String command) {
        try {
            // CRITICAL VULNERABILITY: Direct command execution without validation
            Process process = Runtime.getRuntime().exec(command);
            return "Command executed successfully";
        } catch (Exception e) {
            logger.severe("Error executing command: " + e.getMessage());
            return "Error: " + e.getMessage();
        }
    }
    
    /**
     * Get user account details
     */
    public static UserAccount getUserDetails(String username) {
        return users.get(username);
    }
    
    /**
     * Internal class for user accounts
     */
    public static class UserAccount {
        private String username;
        private String password;
        private String role;
        
        public UserAccount(String username, String password, String role) {
            this.username = username;
            this.password = password;
            this.role = role;
        }
        
        public UserAccount(String username, String password) {
            this(username, password, "user");
        }
        
        public String getUsername() {
            return username;
        }
        
        public String getPassword() {
            return password;
        }
        
        public String getRole() {
            return role;
        }
        
        public void setPassword(String password) {
            this.password = password;
        }
        
        public void setRole(String role) {
            this.role = role;
        }
    }
}
