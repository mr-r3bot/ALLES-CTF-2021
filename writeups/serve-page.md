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

----------------------------------
`/register`

- Take `username` and `password` parameter
- Get Servelet Context list of User (array)
- Check if username has existed in Array, if yes => Username existed

else:
- Create new user and add to `users` Array
- Store password in `md5` hash
- Add attribute `config` to user's session
- Redirect back to `home.jsp`

--------------------------
`/login`

- Take `usename` and `password` ( in md5 hash) parameters
- Call `checkLogin` function

`checkLogin`
- Loop through array list of Users, find the username, if not found => return invalid email/address
- 


Get the current **session** with the current `UserConfig` and then set to the current user logging in



------------------------
`/config`

- Set user config

Receive 3 params:

```text
debugMode
language
user
```

Back-end read JSON in and deserialize it

```java
ObjectMapper objectMapper = new ObjectMapper();

UserConfig userConfig = objectMapper.readValue(jsonConfig, UserConfig.class);
```

Perform conditional check before update user configuration:
If field `user` is set, return error

```java
  

if (userConfig == null) {

request.setAttribute("message", "Failed to parse user configuration");

request.setAttribute("type", "danger");

}

else if (userConfig.getUser() != null) {

request.setAttribute("type", "danger");

request.setAttribute("message", "Hacking detected!");

}

else {

request.setAttribute("type", "success");

request.setAttribute("message", "User configuration updated");

session.setAttribute("config", userConfig);

}

  

dispatcher.forward(request, response);
```

Web app is using a persistent session and modify the session on the fly, **not change set the session again** 

------------------------------------------