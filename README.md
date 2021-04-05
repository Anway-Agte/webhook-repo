# Dev Assessment - Webhook Receiver


* The endpoint is at:

```bash
POST http://127.0.0.1:5000/webhook/receiver
```

* The UI is at:

```bash
GET <ngrok-link>/webhook/io 
```

*** File Structure *** 
```bash 
app/webhook/routes.py
```
All the routes and endpoints of the application . Data handling and processing modules . 
 
```bash 
 app/static/scripts.js 
``` 
Javascript calls from client side to server for continuous data receiving . 
  
 ```bash 
app/templates/
```
HTML templates for UI

*******************
