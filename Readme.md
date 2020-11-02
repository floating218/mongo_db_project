## 설치하기(우분투 18 기준)

### MongoDB 설치,실행

```bash
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
$ echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org
$ sudo service mongod start
```

### PyMongo 설치

```bash
$ pip3 install pymongo
```

## 실행하기

```bash
$ python3 main.py
```

## 메인 메뉴
<img src="img/main.png">

## 2→ 회원가입(Sign Up)
<img src="img/sign_up.png">

## 1 → 로그인(Sign In)
<img src="img/sign_in.png">

## 로그인 후 유저메뉴
<img src="img/usermenu.png">
