# 🔐 Nginx Secure Reverse Proxy with HTTPS & Python Backend

## 📌 Project Overview

This project demonstrates how to configure a **secure production-like web server** using **Nginx** on Linux.

The system includes:

* Static website hosting using Nginx
* HTTPS setup using self-signed SSL (OpenSSL)
* Automatic HTTP → HTTPS redirection
* Reverse proxy to a Python backend server (port 3000)

---

## 🏗️ Architecture

```id="arch001"
Client (Browser)
       ↓
HTTP (Port 80) → Redirect
       ↓
HTTPS (Port 443, SSL)
       ↓
Nginx Web Server
       ├── /        → Static Frontend (HTML, CSS, JS)
       └── /api/    → Python Backend (Port 3000)
```

---

## ⚙️ Technologies Used

* Nginx (Web Server & Reverse Proxy)
* OpenSSL (SSL Certificate Generation)
* Python (Backend Server using HTTPServer)

---

## 📁 Project Structure

```id="struct001"
nginx-secure-reverse-proxy/
├── backend/
│   └── server.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── nginx/
│   └── secure-app.conf
├── screenshots/
└── README.md
```

---

## 🚀 Setup Instructions

### 🔹 Step 1: Install Required Packages

```bash
sudo apt update
sudo apt install nginx openssl python3 -y
```

---

### 🔹 Step 2: Setup Static Website

```bash
sudo mkdir -p /var/www/secure-app
sudo cp frontend/* /var/www/secure-app/
sudo chown -R www-data:www-data /var/www/secure-app
```

---

### 🔹 Step 3: Generate Self-Signed SSL Certificate

```bash
sudo mkdir -p /etc/nginx/ssl

sudo openssl req -x509 -nodes -days 365 \
-newkey rsa:2048 \
-keyout /etc/nginx/ssl/nginx.key \
-out /etc/nginx/ssl/nginx.crt
```

> Enter your server IP as the Common Name (CN)

---

### 🔹 Step 4: Configure Nginx

Edit config file:

```bash
sudo nano /etc/nginx/sites-available/secure-app
```

Paste:

```nginx
server {
    listen 80;
    server_name localhost;

    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name localhost;

    ssl_certificate /etc/nginx/ssl/nginx.crt;
    ssl_certificate_key /etc/nginx/ssl/nginx.key;

    root /var/www/secure-app;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:3000/api/;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

### 🔹 Step 5: Enable Configuration

```bash
sudo ln -s /etc/nginx/sites-available/secure-app /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
```

---

### 🔹 Step 6: Test & Restart Nginx

```bash
sudo nginx -t
sudo systemctl restart nginx
```

---

### 🔹 Step 7: Run Python Backend

```bash
cd backend
python3 server.pyr
```

---

## 🧪 Testing

### ✅ 1. HTTP → HTTPS Redirect

```bash
curl -I http://localhost
```

Expected:

```id="out001"
301 Moved Permanently
Location: https://...
```

---

### ✅ 2. HTTPS Working

Open in browser:

```id="test002"
https://<your-server-ip>
```

> Browser may show "Not Secure" (self-signed certificate)

---

### ✅ 3. Backend via Reverse Proxy

```bash
curl -k https://localhost/api/tasks
```

Expected output:

```json
[]
```

---

## 📸 Screenshots

Screenshots included in `/screenshots`:
<img width="963" height="113" alt="nginx_setup" src="https://github.com/user-attachments/assets/159a58fa-c270-4abe-9d4c-22034916f59b" />
<img width="963" height="113" alt="nginx_setup" src="https://github.com/user-attachments/assets/0d2836b2-c643-4c33-8de8-4c87b5f7f6e9" />
<img width="877" height="126" alt="Backend_Working_via_Nginx" src="https://github.com/user-attachments/assets/50303443-65a2-4626-a1d4-512dff419e8d" />
<img width="878" height="245" alt="File_Structure" src="https://github.com/user-attachments/assets/345caa39-1572-4975-86f1-3426595dc131" />
<img width="940" height="174" alt="HTTP-HTTPS_Redirect" src="https://github.com/user-attachments/assets/a3386a76-4916-457c-ae22-5182f78261e9" />
<img width="1000" height="1030" alt="HTTPS_Working_on_browser" src="https://github.com/user-attachments/assets/eb235192-004d-467b-9d86-24e2518103dd" />

---

## ⚠️ Common Issues & Fixes

| Problem         | Cause               | Solution                               |
| --------------- | ------------------- | -------------------------------------- |
| 502 Bad Gateway | Backend not running | Start Python server                    |
| CSS not loading | Files not copied    | Copy frontend to `/var/www/secure-app` |
| SSL error       | Wrong path          | Check `/etc/nginx/ssl/`                |
| 404 on /api     | Wrong proxy_pass    | Use correct `/api/` mapping            |

---

## 🧠 Key Concepts Learned

* Reverse Proxy using Nginx
* SSL/TLS encryption (HTTPS)
* HTTP to HTTPS redirection
* Separation of frontend and backend
* Production-style web server architecture

---

## ✅ Conclusion

This project successfully demonstrates a **secure Nginx web server setup** with HTTPS and reverse proxy integration. The architecture reflects real-world DevOps practices where Nginx handles traffic routing and security, while backend services handle application logic.

---
