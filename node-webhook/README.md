# Kontakt.io Location Engine webhook handler
A sample implementation of a very basic webhook handler for Kontakt.io Location Engine. Written in Node.js, tested on version 8.4.0.

## Usage
Clone this repository (please be aware it contains other tools, not just the webhook handler)

```
$ git clone https://github.com/adrianz/le-examples.git
```

Move to the folder with webhook handler and initialize dependencies

```
$ cd le-examples/node-webhook
$ npm install
```

Start the server

```
$ node server.js
```

*(Optional)* If the server is running locally, behind NAT or firewall, it needs to be exposed to the Internet, either by opening proper ports on your router, by using tools like [ngrok](https://ngrok.com/), or any other means that work best in particular setup.

## Starting a webhook
A webhook is initiated by a call to Kontakt.io Location Engine HTTP API:

```
POST /webhook/subscribe HTTP/1.1
Accept: application/vnd.com.kontakt+json;version=10
Api-Key: yourSuperSecretAPIKey
Content-Type: application/x-www-form-urlencoded; charset=utf-8
Host: ovs.kontakt.io
Connection: close
User-Agent: Paw/3.0.16 (Macintosh; OS X/10.12.3) GCDHTTPRequest
Content-Length: 130

url=https%3A%2F%2Fyour.server.com%2Fyour%endpoint&sourceId=abcde
```

Details are available in [Location Engine monitoring guide](https://developer.kontakt.io/rest-api/api-guides/location-engine-monitoring/#webhooks) and relevant [API references](https://developer.kontakt.io/rest-api/api-reference/earlyaccess/#analytics-location-engine-subscribe-to-a-webhook).