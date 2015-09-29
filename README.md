# HTTP-authentication-brute-force
You should install nscd if you are on Linux for dns cache or using the website IP instead of the domain.

```
sudo apt-get install nscd
```

#How to install and run

```
virtualenv -p /usr/bin/python2.7 env
source env/bin/activate
pip install --upgrade pip
pip install -R requirements.txt
python http_bruteforce.py
```
