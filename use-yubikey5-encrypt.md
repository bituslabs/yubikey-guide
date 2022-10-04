- [准备工作](#准备工作)
- [GPG 密钥](#GPG密钥)
- [yubikey 操作](#yubikey操作)
- [加解密的使用](#加解密的使用)

# 使用 yubikey 5 openpgp 加密数据

YubiKey 是由 Yubico 生产的身份认证设备，支持一次性密码（OTP）、公钥加密和身份认证，以及由FIDO联盟（FIDO U2F）开发的通用第二因素（U2F）等协议。

## 准备工作

### 安装 gpg

```
https://gnupg.org/download/
```

可以选择比较友好的 GPG Suite

```
https://gpgtools.org/
```

本文选择安装 2.3.x 版本的 GPG


### 安装 yubikey manager

```
https://www.yubico.com/support/download/yubikey-manager/
```

TODO


## GPG密钥


### 创建主密钥

```
gpg --expert --full-generate-key
```

```
gpg (GnuPG) 2.3.7; Copyright (C) 2021 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Please select what kind of key you want:
   (1) RSA and RSA
   (2) DSA and Elgamal
   (3) DSA (sign only)
   (4) RSA (sign only)
   (7) DSA (set your own capabilities)
   (8) RSA (set your own capabilities)
   (9) ECC (sign and encrypt) *default*
  (10) ECC (sign only)
  (11) ECC (set your own capabilities)
  (13) Existing key
  (14) Existing key from card
Your selection? 8

Possible actions for this RSA key: Sign Certify Encrypt Authenticate
Current allowed actions: Sign Certify Encrypt

   (S) Toggle the sign capability
   (E) Toggle the encrypt capability
   (A) Toggle the authenticate capability
   (Q) Finished

Your selection? s

Possible actions for this RSA key: Sign Certify Encrypt Authenticate
Current allowed actions: Certify Encrypt

   (S) Toggle the sign capability
   (E) Toggle the encrypt capability
   (A) Toggle the authenticate capability
   (Q) Finished

Your selection? e

Possible actions for this RSA key: Sign Certify Encrypt Authenticate
Current allowed actions: Certify

   (S) Toggle the sign capability
   (E) Toggle the encrypt capability
   (A) Toggle the authenticate capability
   (Q) Finished

Your selection? q
RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (3072) 4096
Requested keysize is 4096 bits
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 0
Key does not expire at all
Is this correct? (y/N) y

GnuPG needs to construct a user ID to identify your key.

Real name: HelloWorld
Email address: hello.world@bituslabs.com
Comment:
You selected this USER-ID:
    "HelloWorld <hello.world@bituslabs.com>"

Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? O
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
gpg: revocation certificate stored as '/Users/hello/.gnupg/openpgp-revocs.d/F3846BD341BC7A6B0392D3E07D187EED23E32758.rev'
public and secret key created and signed.

pub   rsa4096 2022-10-04 [C]
      F3846BD341BC7A6B0392D3E07D187EED23E32758
uid                      HelloWorld <hello.world@bituslabs.com>
```

### 创建子证书

```
export KEYID=F3846BD341BC7A6B0392D3E07D187EED23E32758
```

```
gpg --expert --edit-key $KEYID
```

```
gpg (GnuPG) 2.3.7; Copyright (C) 2021 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Secret key is available.

sec  rsa4096/7D187EED23E32758
     created: 2022-10-04  expires: never       usage: C
     trust: ultimate      validity: ultimate
[ultimate] (1). HelloWorld <hello.world@bituslabs.com>

// 创建签名证书
gpg> addkey
Please select what kind of key you want:
   (3) DSA (sign only)
   (4) RSA (sign only)
   (5) Elgamal (encrypt only)
   (6) RSA (encrypt only)
   (7) DSA (set your own capabilities)
   (8) RSA (set your own capabilities)
  (10) ECC (sign only)
  (11) ECC (set your own capabilities)
  (12) ECC (encrypt only)
  (13) Existing key
  (14) Existing key from card
Your selection? 4
RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (3072) 4096
Requested keysize is 4096 bits
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 1y
Key expires at Mon 10/ 3 20:25:27 2023 PDT
Is this correct? (y/N) y
Really create? (y/N) y
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.

sec  rsa4096/7D187EED23E32758
     created: 2022-10-04  expires: never       usage: C
     trust: ultimate      validity: ultimate
ssb  rsa4096/0B5A607575288C62
     created: 2022-10-04  expires: 2023-10-04  usage: S
[ultimate] (1). HelloWorld <hello.world@bituslabs.com>

// 创建加密证书
gpg> addkey
Please select what kind of key you want:
   (3) DSA (sign only)
   (4) RSA (sign only)
   (5) Elgamal (encrypt only)
   (6) RSA (encrypt only)
   (7) DSA (set your own capabilities)
   (8) RSA (set your own capabilities)
  (10) ECC (sign only)
  (11) ECC (set your own capabilities)
  (12) ECC (encrypt only)
  (13) Existing key
  (14) Existing key from card
Your selection? 6
RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (3072) 4096
Requested keysize is 4096 bits
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 1y
Key expires at Mon 10/ 3 20:26:28 2023 PDT
Is this correct? (y/N) y
Really create? (y/N) y
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.

sec  rsa4096/7D187EED23E32758
     created: 2022-10-04  expires: never       usage: C
     trust: ultimate      validity: ultimate
ssb  rsa4096/0B5A607575288C62
     created: 2022-10-04  expires: 2023-10-04  usage: S
ssb  rsa4096/4E39157293C4AD7C
     created: 2022-10-04  expires: 2023-10-04  usage: E
[ultimate] (1). HelloWorld <hello.world@bituslabs.com>

// 创建认证证书
gpg> addkey
Please select what kind of key you want:
   (3) DSA (sign only)
   (4) RSA (sign only)
   (5) Elgamal (encrypt only)
   (6) RSA (encrypt only)
   (7) DSA (set your own capabilities)
   (8) RSA (set your own capabilities)
  (10) ECC (sign only)
  (11) ECC (set your own capabilities)
  (12) ECC (encrypt only)
  (13) Existing key
  (14) Existing key from card
Your selection? 8

Possible actions for this RSA key: Sign Encrypt Authenticate
Current allowed actions: Sign Encrypt

   (S) Toggle the sign capability
   (E) Toggle the encrypt capability
   (A) Toggle the authenticate capability
   (Q) Finished

Your selection? s

Possible actions for this RSA key: Sign Encrypt Authenticate
Current allowed actions: Encrypt

   (S) Toggle the sign capability
   (E) Toggle the encrypt capability
   (A) Toggle the authenticate capability
   (Q) Finished

Your selection? e

Possible actions for this RSA key: Sign Encrypt Authenticate
Current allowed actions:

   (S) Toggle the sign capability
   (E) Toggle the encrypt capability
   (A) Toggle the authenticate capability
   (Q) Finished

Your selection? a

Possible actions for this RSA key: Sign Encrypt Authenticate
Current allowed actions: Authenticate

   (S) Toggle the sign capability
   (E) Toggle the encrypt capability
   (A) Toggle the authenticate capability
   (Q) Finished

Your selection? q
RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (3072) 4096
Requested keysize is 4096 bits
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 1y
Key expires at Mon 10/ 3 20:27:16 2023 PDT
Is this correct? (y/N) y
Really create? (y/N) y
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.

sec  rsa4096/7D187EED23E32758
     created: 2022-10-04  expires: never       usage: C
     trust: ultimate      validity: ultimate
ssb  rsa4096/0B5A607575288C62
     created: 2022-10-04  expires: 2023-10-04  usage: S
ssb  rsa4096/4E39157293C4AD7C
     created: 2022-10-04  expires: 2023-10-04  usage: E
ssb  rsa4096/7BB50A0B99FAD612
     created: 2022-10-04  expires: 2023-10-04  usage: A
[ultimate] (1). HelloWorld <hello.world@bituslabs.com>

```


### 备份密钥

```
// 备份主密钥
gpg --armor --export-secret-key --output hello-secret.asc $KEYID 
```

```
// 备份公钥
gpg --armor --export --output hello-public.asc $KEYID 
```

```
// 备份子密钥
gpg --armor --export-secret-subkeys --output hello-secret-sub.asc $KEYID
```

## yubikey操作

### 初始化yubikey

首次插入 yubikey 后修改管理密码

```
gpg --edit-card

// 进入卡管理界面
gpg/card> admin
Admin commands are allowed

// 修改密码
gpg/card> passwd
gpg: OpenPGP card no. D***************************0000 detected

1 - change PIN
2 - unblock PIN
3 - change Admin PIN
4 - set the Reset Code
Q - quit

Your selection?

// 分别选择 1修改使用密码，3修改管理密码
// 默认使用密码是 123456
// 默认管理密码是 12345678

gpg/card> name
Cardholder's surname: Hello
Cardholder's given name: World

gpg/card> lang
Language preferences: en
```


### 将证书写入yubikey

注意：写入 yubikey 之后，本地的密钥将被移除，请确保备份或完全理解其安全逻辑

```
gpg --edit-key $KEYID
```

```
gpg (GnuPG) 2.3.7; Copyright (C) 2021 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Secret key is available.

sec  rsa4096/7D187EED23E32758
     created: 2022-10-04  expires: never       usage: C
     trust: ultimate      validity: ultimate
ssb  rsa4096/0B5A607575288C62
     created: 2022-10-04  expires: 2023-10-04  usage: S
ssb  rsa4096/4E39157293C4AD7C
     created: 2022-10-04  expires: 2023-10-04  usage: E
ssb  rsa4096/7BB50A0B99FAD612
     created: 2022-10-04  expires: 2023-10-04  usage: A
[ultimate] (1). HelloWorld <hello.world@bituslabs.com>

gpg> key 1

sec  rsa4096/7D187EED23E32758
     created: 2022-10-04  expires: never       usage: C
     trust: ultimate      validity: ultimate
ssb* rsa4096/0B5A607575288C62
     created: 2022-10-04  expires: 2023-10-04  usage: S
ssb  rsa4096/4E39157293C4AD7C
     created: 2022-10-04  expires: 2023-10-04  usage: E
ssb  rsa4096/7BB50A0B99FAD612
     created: 2022-10-04  expires: 2023-10-04  usage: A
[ultimate] (1). HelloWorld <hello.world@bituslabs.com>

gpg> keytocard
Please select where to store the key:
   (1) Signature key
   (3) Authentication key
Your selection? 1

Replace existing key? (y/N) y

sec  rsa4096/7D187EED23E32758
     created: 2022-10-04  expires: never       usage: C
     trust: ultimate      validity: ultimate
ssb* rsa4096/0B5A607575288C62
     created: 2022-10-04  expires: 2023-10-04  usage: S
ssb  rsa4096/4E39157293C4AD7C
     created: 2022-10-04  expires: 2023-10-04  usage: E
ssb  rsa4096/7BB50A0B99FAD612
     created: 2022-10-04  expires: 2023-10-04  usage: A
[ultimate] (1). HelloWorld <hello.world@bituslabs.com>

gpg> key 1

sec  rsa4096/7D187EED23E32758
     created: 2022-10-04  expires: never       usage: C
     trust: ultimate      validity: ultimate
ssb  rsa4096/0B5A607575288C62
     created: 2022-10-04  expires: 2023-10-04  usage: S
ssb  rsa4096/4E39157293C4AD7C
     created: 2022-10-04  expires: 2023-10-04  usage: E
ssb  rsa4096/7BB50A0B99FAD612
     created: 2022-10-04  expires: 2023-10-04  usage: A
[ultimate] (1). HelloWorld <hello.world@bituslabs.com>

gpg> key 2

sec  rsa4096/7D187EED23E32758
     created: 2022-10-04  expires: never       usage: C
     trust: ultimate      validity: ultimate
ssb  rsa4096/0B5A607575288C62
     created: 2022-10-04  expires: 2023-10-04  usage: S
ssb* rsa4096/4E39157293C4AD7C
     created: 2022-10-04  expires: 2023-10-04  usage: E
ssb  rsa4096/7BB50A0B99FAD612
     created: 2022-10-04  expires: 2023-10-04  usage: A
[ultimate] (1). HelloWorld <hello.world@bituslabs.com>

gpg> keytocard
Please select where to store the key:
   (2) Encryption key
Your selection? 2

Replace existing key? (y/N) y

sec  rsa4096/7D187EED23E32758
     created: 2022-10-04  expires: never       usage: C
     trust: ultimate      validity: ultimate
ssb  rsa4096/0B5A607575288C62
     created: 2022-10-04  expires: 2023-10-04  usage: S
ssb* rsa4096/4E39157293C4AD7C
     created: 2022-10-04  expires: 2023-10-04  usage: E
ssb  rsa4096/7BB50A0B99FAD612
     created: 2022-10-04  expires: 2023-10-04  usage: A
[ultimate] (1). HelloWorld <hello.world@bituslabs.com>

gpg> key 2

sec  rsa4096/7D187EED23E32758
     created: 2022-10-04  expires: never       usage: C
     trust: ultimate      validity: ultimate
ssb  rsa4096/0B5A607575288C62
     created: 2022-10-04  expires: 2023-10-04  usage: S
ssb  rsa4096/4E39157293C4AD7C
     created: 2022-10-04  expires: 2023-10-04  usage: E
ssb  rsa4096/7BB50A0B99FAD612
     created: 2022-10-04  expires: 2023-10-04  usage: A
[ultimate] (1). HelloWorld <hello.world@bituslabs.com>

gpg> key 3

sec  rsa4096/7D187EED23E32758
     created: 2022-10-04  expires: never       usage: C
     trust: ultimate      validity: ultimate
ssb  rsa4096/0B5A607575288C62
     created: 2022-10-04  expires: 2023-10-04  usage: S
ssb  rsa4096/4E39157293C4AD7C
     created: 2022-10-04  expires: 2023-10-04  usage: E
ssb* rsa4096/7BB50A0B99FAD612
     created: 2022-10-04  expires: 2023-10-04  usage: A
[ultimate] (1). HelloWorld <hello.world@bituslabs.com>

gpg> keytocard
Please select where to store the key:
   (3) Authentication key
Your selection? 3

Replace existing key? (y/N) y

sec  rsa4096/7D187EED23E32758
     created: 2022-10-04  expires: never       usage: C
     trust: ultimate      validity: ultimate
ssb  rsa4096/0B5A607575288C62
     created: 2022-10-04  expires: 2023-10-04  usage: S
ssb  rsa4096/4E39157293C4AD7C
     created: 2022-10-04  expires: 2023-10-04  usage: E
ssb* rsa4096/7BB50A0B99FAD612
     created: 2022-10-04  expires: 2023-10-04  usage: A
[ultimate] (1). HelloWorld <hello.world@bituslabs.com>
``` 

### 上传公钥到 Key Server

```
gpg --send-keys $KEYID
```

去 Key Server 确认上传的公钥

```
https://keys.openpgp.org/search?q=hello.world@bituslabs.com
```

### 在另一台电脑使用yubikey

```
// 找到公钥
gpg --search hello.world@bituslabs.com
```

or

```
// 直接导入备份公钥
gpg --import hello-public.asc 
```

```
// 设置信任
% gpg --edit-key $KEYID
gpg (GnuPG) 2.3.7; Copyright (C) 2021 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.


pub  rsa4096/7D187EED23E32758
     created: 2022-10-04  expires: never       usage: C
     trust: unknown       validity: unknown
sub  rsa4096/0B5A607575288C62
     created: 2022-10-04  expires: 2023-10-04  usage: S
sub  rsa4096/4E39157293C4AD7C
     created: 2022-10-04  expires: 2023-10-04  usage: E
sub  rsa4096/7BB50A0B99FAD612
     created: 2022-10-04  expires: 2023-10-04  usage: A
[ unknown] (1). HelloWorld <hello.world@bituslabs.com>

gpg> trust
pub  rsa4096/7D187EED23E32758
     created: 2022-10-04  expires: never       usage: C
     trust: unknown       validity: unknown
sub  rsa4096/0B5A607575288C62
     created: 2022-10-04  expires: 2023-10-04  usage: S
sub  rsa4096/4E39157293C4AD7C
     created: 2022-10-04  expires: 2023-10-04  usage: E
sub  rsa4096/7BB50A0B99FAD612
     created: 2022-10-04  expires: 2023-10-04  usage: A
[ unknown] (1). HelloWorld <hello.world@bituslabs.com>

Please decide how far you trust this user to correctly verify other users' keys
(by looking at passports, checking fingerprints from different sources, etc.)

  1 = I don't know or won't say
  2 = I do NOT trust
  3 = I trust marginally
  4 = I trust fully
  5 = I trust ultimately
  m = back to the main menu

Your decision? 5
Do you really want to set this key to ultimate trust? (y/N) y

pub  rsa4096/7D187EED23E32758
     created: 2022-10-04  expires: never       usage: C
     trust: ultimate      validity: unknown
sub  rsa4096/0B5A607575288C62
     created: 2022-10-04  expires: 2023-10-04  usage: S
sub  rsa4096/4E39157293C4AD7C
     created: 2022-10-04  expires: 2023-10-04  usage: E
sub  rsa4096/7BB50A0B99FAD612
     created: 2022-10-04  expires: 2023-10-04  usage: A
[ unknown] (1). HelloWorld <hello.world@bituslabs.com>
Please note that the shown key validity is not necessarily correct
unless you restart the program.
```

### 从 yubikey 中同步

```
gpg --edit-card


gpg/card> fetch
gpg: Total number processed: 1
gpg:              unchanged: 1
```

## 加解密的使用

### 加密文件

```
// 需要有 hello.world@bituslabs.com 的公钥
gpg --encrypt --recipient hello.world@bituslabs.com ./demo.txt
```

加密会得到加密文件 ./demo.txt.gpg


### 解密文件

```
// 需要有 hello.world@bituslabs.com 的密钥
gpg --decrypt ./demo.txt.gpg
```


### 使用 python 解密文件或数据

```
pip install python-gnupg
```

```
// 参考文档
https://gnupg.readthedocs.io/en/latest/
```

```
// example
import gnupg

filename = './demo.txt.gpg'

gpg = gnupg.GPG()
with open(filename, 'rb') as f:
    status = gpg.decrypt_file(f)

print('ret: ', status)
print('ok: ', status.ok)
print('status: ', status.status)
print('stderr: ', status.stderr)
```