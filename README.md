facets
======

A place to test some facet server ideas.

Using port scan data from [scans.io(https://scans.io/study/sonar.cio)] and the code is tied to that schema for now. Obviously the next version won't do that, and will support specified and auto detected schemas.

Python version
==============
This uses a simple [Tornado(http://www.tornadoweb.org/en/stable/)] app to server queries. 

Run the app as such, and pass it some data:

```
python src/python/facet_server.py -i sample_data.json -p 8888
```

To query, use a web browser and go to http://localhost:8888, or use cURL:


```
curl -XGET "http://localhost:18888/query/?q=port:22&size=1000&facets=geo_c"

{"facets": {"geo_c": {"LBN": 1, "ARG": 1}}, "num_results": 2, "results": [{"name": "ssh", "proto": "tcp", "ip": "95.129.2.233", "banner": "SSH-2.0-ROSSSH\r\n\\x00\\x00\\x01d\\x08\\x147\\xcaMm|\\x97?2\\xa0odQ\\xc7\\xb7\\x995\\x00\\x00\\x00~diffie-hellman-group-exchange-sha256,diffie-hellman-group-exchange-sha1,diffie-hellman-group14-sha1,diffie-hellman-group1-sha1\\x00\\x00\\x00\\x07ssh-dss\\x00\\x00\\x006aes192-cbc,aes128-cbc,aes256-cbc,blowfish-cbc,3des-cbc\\x00\\x00\\x006aes192-cbc,aes128-cbc,aes256-cbc,blowfish-cbc,3des-cbc\\x00\\x00\\x00\\x12hmac-sha1,hmac-md5\\x00\\x00\\x00\\x12hmac-sha1,hmac-md5\\x00\\x00\\x00\\x04none\\x00\\x00\\x00\\x04none\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x8d\\xa3e\\x81\\x93\\xfdf\\xa8", "t": {"$date": 1359698404000}, "_id": {"ip": "95.129.2.233", "h": "ccac4d77de93e7e120835a04a164be11", "p": 22}, "geo": {"city": "Beirut", "c": "LBN", "reg": "04", "loc": [33.87189865112305, 35.50970077514648]}, "port": 22}, {"name": "ssh", "proto": "tcp", "ip": "190.105.145.67", "banner": "SSH-2.0-OpenSSH_4.3\n\\x00\\x00\\x02\\xbc\\x07\\x14p\\xca3\\xed\\xc5h/7WUzm\\x1f\\xd1\\xc4\\x15\\x00\\x00\\x00Ydiffie-hellman-group-exchange-sha1,diffie-hellman-group14-sha1,diffie-hellman-group1-sha1\\x00\\x00\\x00\\x0fssh-rsa,ssh-dss\\x00\\x00\\x00\\x9daes128-ctr,aes192-ctr,aes256-ctr,arcfour256,arcfour128,aes128-cbc,3des-cbc,blowfish-cbc,cast128-cbc,aes192-cbc,aes256-cbc,arcfour,rijndael-cbc@lysator.liu.se\\x00\\x00\\x00\\x9daes128-ctr,aes192-ctr,aes256-ctr,arcfour256,arcfour128,aes128-cbc,3des-cbc,blowfish-cbc,cast128-cbc,aes192-cbc,aes256-cbc,arcfour,rijndael-cbc@lysator.liu.se\\x00\\x00\\x00Uhmac-md5,hmac-sha1,hmac-ripemd160,hmac-ripemd160@openssh.com,hmac-sha1-96,hmac-md5-96\\x00\\x00\\x00Uhmac-md5,hmac-sha1,hmac-ripemd160,hmac-ripemd160@openssh.com,hmac-sha1-96,hmac-md5-96\\x00\\x00\\x00\\x15none,zlib@openssh.com\\x00\\x00\\x00\\x15none,zlib@openssh.com\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00", "t": {"$date": 1359698422000}, "_id": {"ip": "190.105.145.67", "h": "84d653bd31e77e899d05bf21e7c07eb4", "p": 22}, "geo": {"loc": [-34, -64], "c": "ARG"}, "port": 22}]}

```

You can do multiple comma-separated query terms:

```
curl -XGET "http://localhost:18888/query/?q=geo_c:USA,port:22&size=5&facets=geo_c"

{"facets": {"geo_c": {"USA": 2}}, "num_results": 2, "results": [{"name": "ssh", "proto": "tcp", "ip": "173.254.69.102", "banner": "SSH-2.0-OpenSSH_5.3\r\n\\x00\\x00\\x03\\x0c\n\\x14\\xf3Q\\xd5\\x81\\xa9#*\\x96\\x04\\x8b`\\x04zp\\xe3\\x94\\x00\\x00\\x00~diffie-hellman-group-exchange-sha256,diffie-hellman-group-exchange-sha1,diffie-hellman-group14-sha1,diffie-hellman-group1-sha1\\x00\\x00\\x00\\x0fssh-rsa,ssh-dss\\x00\\x00\\x00\\x9daes128-ctr,aes192-ctr,aes256-ctr,arcfour256,arcfour128,aes128-cbc,3des-cbc,blowfish-cbc,cast128-cbc,aes192-cbc,aes256-cbc,arcfour,rijndael-cbc@lysator.liu.se\\x00\\x00\\x00\\x9daes128-ctr,aes192-ctr,aes256-ctr,arcfour256,arcfour128,aes128-cbc,3des-cbc,blowfish-cbc,cast128-cbc,aes192-cbc,aes256-cbc,arcfour,rijndael-cbc@lysator.liu.se\\x00\\x00\\x00ihmac-md5,hmac-sha1,umac-64@openssh.com,hmac-ripemd160,hmac-ripemd160@openssh.com,hmac-sha1-96,hmac-md5-96\\x00\\x00\\x00ihmac-md5,hmac-sha1,umac-64@openssh.com,hmac-ripemd160,hmac-ripemd160@openssh.com,hmac-sha1-96,hmac-md5-96\\x00\\x00\\x00\\x15none,zlib@openssh.com\\x00\\x00\\x00\\x15none,zlib@openssh.com\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00", "t": {"$date": 1359698414000}, "_id": {"ip": "173.254.69.102", "h": "440ac8ebaa6ea38e2a542d54fe1065e8", "p": 22}, "geo": {"city": "Provo", "c": "USA", "reg": "UT", "loc": [40.21810150146484, -111.6132965087891]}, "port": 22}, {"name": "ssh", "proto": "tcp", "ip": "70.232.4.145", "banner": "SSH-2.0-RomCliSecure_4.12\r\n\\x00\\x00\\x00\\x94\n\\x14\\xeb\\xc3<\\xce\\xb2\\x00\\xfd\\xb6\\x95\\x93\\x86*\\xd6\\x14Q\\x94\\x00\\x00\\x00\\x1adiffie-hellman-group1-sha1\\x00\\x00\\x00\\x07ssh-dss\\x00\\x00\\x00\\x083des-cbc\\x00\\x00\\x00\\x083des-cbc\\x00\\x00\\x00\thmac-sha1\\x00\\x00\\x00\thmac-sha1\\x00\\x00\\x00\\x04none\\x00\\x00\\x00\\x04none\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x7f\\xd0\\xcay\\xabe\\xf0+\\xb7V", "t": {"$date": 1359698414000}, "_id": {"ip": "70.232.4.145", "h": "85d5c055f46f7ba4d7f8280b8369cc9e", "p": 22}, "geo": {"loc": [38, -97], "c": "USA"}, "port": 22}]}
```




