## Enumeration

Goal: Escalate priveledge to admin

- Java web-app
- tomcat:8.5.43-jdk8
- maven:3.6.1-jdk-8


## Code analysis

API endpoints
```java
/config
/register
/login
/logout
```


--------------------------
`/login`

- Take `usename` and `password` ( in md5 hash) parameters
- Call `checkLogin` function

`checkLogin`
- Loop through array list of Users, find the username, if not found => return invalid email/address
- 


Get the current **session** with the current `UserConfig` and then set to the current user logging in

Notice: 
```java
if (userConfig.isDebugMode()) {

String pw1 = new String(Hex.encodeHex(digestStorage.digest()));

String pw2 = password_md5_sha1;

java.util.logging.Logger.getLogger("login")

.info(String.format("Login tried with: %s == %s", pw1, pw2));

}

if (Arrays.equals(passwordBytes, digestStorage.digest())) {

if (userConfig.isDebugMode())

java.util.logging.Logger.getLogger("login").info("Passwords were equal");

return u;

}
```

In **debugMode** , `digest()` got called twice
- First call, digest will read all from the buffer that has been `.update()`
- Second call, digest's buffer will be empty, so it will generate a `null-byte` hash


-------------------------