package cscg.user;

import java.io.*;
import java.io.IOException;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class UserConfigCustomize extends UserConfig {

    private boolean debugMode;
    private int language;
    private User user;

    public static void main() throws JsonProcessingException {
        UserConfigCustomize configCustomize = new UserConfigCustomize();
        ObjectMapper mapper = new ObjectMapper();
        String jsonString = mapper.writeValueAsString(configCustomize);
        System.out.println(jsonString);
    }

    public UserConfigCustomize() {
        this.debugMode = false;
        this.language = 0;
        this.user = null;
    }

    public boolean isDebugMode() {
        return debugMode;
    }

    public User getUser() {
        return null;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public int getLanguage() {
        return language;
    }

    public void setLanguage(int language) {
        this.language = language;
    }

    public void setDebugMode(boolean debugMode) {
        this.debugMode = debugMode;
    }
}
