#  H!pster Startup
tags: web

## Description

>Our [on-campus start-up](http://cyberai.uni.hctf.fun/) was hacked.<br>
The hacker somehow deleted the only admin user... Can you login to the admin interface and revert it?


## Solution

As we probably need to login to complete the task, trying with `/admin` is a simple, but correct, guess for a login portal.

After trying some base credentials, I tried to find out if the form suffer of SQL injection. Sending `'` as username showed an error message that also includes the vulnerable query:

```SQL
FOR u IN users FILTER u.user == 'username' && u.passwd == 'password' RETURN u
```

The error message also helps identifying the database: "*AQL: syntax error*". It's a NoSQL database called *ArangoDB*.

Trying to bypass the login sending `' or 1 == 1 RETURN u //` as username results in `The user's 'role' is not 'admin'!` error.

On the other end trying to filtering by `u.role == 'admin'` prompt another error: `User/Password combination does not exist!`. Probably this error is shown when the query doesn't return any user.

This mean I need to setup a more complex query, so I checked out the ArangoDB documentation. I found the command `UPDATE` that can update (and save) in-place the returned documents, but returned out the query has read-only permission on the database.

After a deeper search in the documentation I found the command `MERGE` that can, obviously, merge two documents, and actually change the returned documents without saving them in the database. So the right query to insert in the username field is: `' || 1 == 1 LET newitem = MERGE(u, {'role': 'admin' }) RETURN newitem //`, that finally provide the wanted result: `Nothing here. Meanwhile: flag{1_l0v3_a_g00d_1nj3ct10n}`.

Nice one!
