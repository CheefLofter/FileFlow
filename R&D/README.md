# PLAN SO FAR

the tool will use flask to make a server that accept the  file (zip only) from the user and encripts it with AES-256-GCM and send it through a cloudflare tunnel. there url will have a fragment that will be uded to decrypt yhe file on client side. 

### encryption

AES-256-GCM is gold standard fro file encription and it can encrypt and decrypt files using same keys. 
the the key will be generated right befor encryption and will be only available through url fragment. the sending server will forget everything after shutdown.

befor initializing the server. the files will be encrypted using cryptograpghy module and will the blobe will be rent to the server 

in future specif flies like images etc will be allowed with freatures like metadata striping etc

### tunneling

cloudflared will be used to setup a tunnel to mask server ip. it can only see the encrypted files not the fragment with key

### user interface

there will be two ver clients at / for the reciver and at /send for the server side ui fro the sender. 