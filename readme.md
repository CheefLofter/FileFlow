*FileFlow V2 is under development and will use encryptions and tunnels to send files securely across the globe . you can see V1 [here](/V-1/)*



<div align="center">

# FILE FLOW 
## A Zero Knowledge file sharing tool

![logo](Assets/logo.jpg)

</div>

<div align="center">


File-Flow is a zero knowledge file sharing tool. it hides sender using a cloud flare tunnel that masks the sender ip and uses a clowdflare server ip. it also encrypts the files using AES-256-GCM encryption which is considered gold standard for genral purpose encryptions. 

it is written in python version 3.13.5 and will run a flask server to accept user input through a web ui on localhost:3000 it will then encrypt the file usinga onettime 32bit key that is generated during encryption and will not be sent to the server. 

it automaticall opens a cloudflare tunnel and exposes localhost to it and also gives the reciver url back to be sent to reciver.

the private key is embedded into the url as a fragment which is encodded to base64 (url_safe) to make the process automatic fro reciver. the key is never sent to the server and is kept by the browser for decription.

the decryption is done on client side in the browser by extracting key from fragment and using Javascript to decrypt the files before downloading



![Block Diagram](Assets/block-diagram.png)

</div>