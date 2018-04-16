# WargamingOpenID - The Wargaming OpenID 2.0 implementation

WargamingOpenID is a Python library for implementing the unified login system of Wargaming Games (World of Tanks, World of Warplanes, World of Warships) on your web/mobile apps and on secure way based on [OpenID 2.0](https://en.wikipedia.org/wiki/OpenID).

OpenID is an open standard and decentralized authentication protocol.

You could use this library to authenticate your users with another external entity like Wargaming.
I mean, if you'll go on having your own user database (profile, avatar, ...) but your users won't have to remember two usernames and two passwords. Theirs World of Tanks username and password will be valid on your web. WoW!

Obviously, it makes sense that your web or app is related to Wargaming World or their games ;).

## Requirements

* Python>=3.6

## Overview
This OpenID implementation consists on three steps:

### Step 1 - Requesting Authentication (authentication.py)
This first call only requires three parameters:

* **OpenID EndPoint**. It's needed to send basic information about our request. Wargaming: https://eu.wargaming.net/id/openid/
* **Unique Identifier**. You will be create on your own or let library generate automatically (request_id).
* **Callback URL (a.k.a. return url)**. This will be the web url endpoint where the OpenID Athentication Process will finish. This callback url will receive extra information that you'll have to manage.

You'll receive one URL Location on your Python program from the library. This URL must be send to the User's browser.

Then, the User's browser will open the Wargaming login page. He/she will write his/her username and password and if everything is ok, he/she will be redirect to the **callback url (a.k.a. return url)**.

### Step 2 - Verification (verification.py)

You'll develop a web mechanism to parse this callback destination url. You could use Flask, Django, TornadoWeb or something like that to catch the callback.

You'll be able to play with https://requestb.in/ on this library by default but this is a temporary solution to check and understand this library.

This step does the next checks:
* Verify if it is a possitive assertion. It is a field value inside the callback url.
* Verify if the callback url is the same that the return_url sent on the Step 1.
* Check a nonce value to avoid Replay Attack.
* Verify OpenID signatures. This is a server-to-server verification and the most important to avoid phising and other attacks.

### Step 3 - Getting User Info and Save on Your System (verification.py)

You'll have got on secure way the identity of the user on this step. Fields:

* identity
* claimed_id

Wargaming uses this kind of identity/claimed_id:

``https://eu.wargaming.net/id/<account_id>-<nickname>/'``

<account_id>: It is a numeric identifier.
<nickname>: It is the player nickname used in the game.

After getting this information, you'll have to parse it to extract the player_id and player_nickname data.

Extraction example:

    Example Identifier:
    https://eu.wargaming.net/id/0000000-JohnDoe/

    Regex to extract:
    https://eu.wargaming.net/id/([0-9]+)-(\w+)/

    Group 1: 0000000
    Group 2: JohnDoe

It would be interesting if you send the login sucessfully on this step. It usually consists on send a secure cookie, create an user on your datebase, save intial profile data on your database, ...

## Dependencies
* requests

## Installation

```
python setup.py
```

## Usage

### Step 1
```python
from openid_wargaming.authentication import Authentication

auth = Authentication()
url = auth.authenticate('https://eu.wargaming.net/id/openid/')

# Send this URL to the web browser location
some_redirect_function(url)
```

### Step 2 and Step 3
```python
import re
from openid_wargaming.verification import Verification

current_url = some_function_to_gather_current_url()
regex = r'https://eu.wargaming.net/id/([0-9]+)-(\w+)/'

verify = Verification(current_url)
identities = verify.verify()

match = re.search(regex, identities['identity'])
account_id = match.group(1)
nickname = match.group(2)

# Log in the system
some_login_function(nickname)

# Set Session Cookie
some_cookie_session_setter()

# Send this URL to the web browser location
some_redirect_to_successfully_url()
```


## Examples

File example.py contains a full example of the Wargaming OpenID redirections using a SimpleHTTPServer using Python3.
You'll have to open or click on the link printed on your screen.

```
##################
# Open this url: #
------------------
https://eu.wargaming.net/id/signin/?next=/id/openid/770470869069588087/&trust_root=http%3A//localhost%3A8000/
------------------

...
```


The program will output the Wargaming nickname just logged in on your Internet Browser.

```
...

### Wargaming nickname authenticated: <nickname>
```

You'll be able to execute when you install the package.

## TODO
* Unit Tests
* More examples

## Links
* [Project Home Page (GitHub)](https://github.com/mac-developer/openid-wargaming)
* [Wargaming](http://wargaming.net)
* [OpenID 2.0 Standard](https://openid.net/specs/openid-authentication-2_0.html)
* [Python Requests Library](http://docs.python-requests.org/en/master/)
* [HTTP Request and Response Service](https://httpbin.org/)
