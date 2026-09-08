# Contact API deployment

The public form should only be pointed at this API **after** the health check and a real Telegram delivery both succeed.

## 1. Create a virtual environment

```bash
cd /home/kianirad2020/kianirad.website
python3 -m venv .venv-contact
.venv-contact/bin/pip install -r server/requirements-contact.txt
```

## 2. Store secrets outside Git

Create `/etc/kianirad-contact.env` as root:

```text
TELEGRAM_BOT_TOKEN=TODO_REAL_BOT_TOKEN
TELEGRAM_CHAT_ID=TODO_REAL_CHAT_ID
CONTACT_RATE_LIMIT=5
CONTACT_RATE_WINDOW_SECONDS=600
```

Then:

```bash
sudo chmod 600 /etc/kianirad-contact.env
```

Do not put the token or chat ID in this repository.

## 3. systemd service

Create `/etc/systemd/system/kianirad-contact.service`:

```ini
[Unit]
Description=Kianirad contact form API
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=kianirad2020
WorkingDirectory=/home/kianirad2020/kianirad.website
EnvironmentFile=/etc/kianirad-contact.env
ExecStart=/home/kianirad2020/kianirad.website/.venv-contact/bin/uvicorn server.contact_api:app --host 127.0.0.1 --port 8042 --workers 1
Restart=on-failure
RestartSec=3
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Enable it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now kianirad-contact.service
curl -fsS http://127.0.0.1:8042/health
```

Expected response:

```json
{"ok":true}
```

## 4. Nginx proxy

Inside the `www.kianirad.website` HTTPS server block:

```nginx
location = /api/contact {
    proxy_pass http://127.0.0.1:8042/contact;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header CF-Connecting-IP $http_cf_connecting_ip;
}
```

Then:

```bash
sudo nginx -t && sudo systemctl reload nginx
```

Keep the origin protected so arbitrary direct traffic cannot spoof Cloudflare's visitor-IP header.

## 5. Test before activating the form

```bash
curl -i https://www.kianirad.website/api/contact \
  -H 'Content-Type: application/json' \
  --data '{"name":"Deploy test","contact":"server test","need":"Contact API","message":"If you see this in Telegram, delivery works.","lang":"en","page":"deploy-test","website":""}'
```

Only after that message arrives in the intended Telegram chat should `formEndpoint` in `assets/site.js` be changed from an empty string to:

```text
/api/contact
```

Until then the existing mailto fallback remains active.

## 6. Honeypot

The frontend includes a hidden `website` field. Normal visitors leave it blank; submissions that fill it are silently discarded by the API.
