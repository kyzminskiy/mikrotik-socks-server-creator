## Microtik socks-server creator in SSH

Цей скрипт дозволяє автоматично створювати проксі-сервери SOCKS на роутерах MikroTik за допомогою SSH.

## Використання

1. Встановіть залежності
```sh
pip install -r requirements.txt
```

2. Додайте до файлу ssh.txt сервери у форматі
```sh
ip:username:password
```

## Запуск
```sh
python create_socks_proxy.py
```
