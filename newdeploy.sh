#!/bin/bash

# رنگ‌ها برای خروجی
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# تابع برای نمایش پیام‌ها
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# تنظیم مجوز اجرا برای اسکریپت
print_message "Setting execution permissions..."
chmod +x "$0"

# بررسی وجود Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker not found. Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    print_message "Docker installed successfully"
fi

# بررسی وجود Docker Compose
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose not found. Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    print_message "Docker Compose installed successfully"
fi

# ایجاد دایرکتوری‌های مورد نیاز
print_message "Creating necessary directories..."
mkdir -p data/db
mkdir -p data/static
mkdir -p data/media
mkdir -p logs

# تنظیم مجوزها
print_message "Setting permissions..."
sudo chown -R $USER:$USER data/
sudo chmod -R 755 data/
sudo chown -R $USER:$USER logs/
sudo chmod -R 755 logs/

# ساخت فایل .env
print_message "Creating .env file..."
cat > .env << EOL
DEBUG=False
SECRET_KEY=$(openssl rand -base64 32)
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///data/db/db.sqlite3
STATIC_ROOT=/app/data/static
MEDIA_ROOT=/app/data/media
EOL

# ساخت فایل docker-compose.yml
print_message "Creating docker-compose.yml..."
cat > docker-compose.yml << EOL
version: '3.8'

services:
  web:
    build: .
    restart: always
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - DJANGO_SETTINGS_MODULE=invoice.settings
    env_file:
      - .env
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 30s
      retries: 3
      start_period: 5s
EOL

# ساخت فایل nginx.conf
print_message "Creating nginx configuration..."
sudo mkdir -p /etc/nginx/conf.d
sudo tee /etc/nginx/conf.d/homayoun.conf << EOL
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static/ {
        alias /app/data/static/;
    }

    location /media/ {
        alias /app/data/media/;
    }
}
EOL

# نصب و راه‌اندازی Nginx
if ! command -v nginx &> /dev/null; then
    print_message "Installing Nginx..."
    sudo apt-get update
    sudo apt-get install -y nginx
    sudo systemctl enable nginx
    sudo systemctl start nginx
fi

# ساخت و راه‌اندازی کانتینرها
print_message "Building and starting containers..."
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# بررسی وضعیت سرویس‌ها
print_message "Checking service status..."
if docker-compose ps | grep -q "Up"; then
    print_message "Services are running successfully!"
else
    print_error "Some services failed to start. Check logs with: docker-compose logs"
fi

# نمایش اطلاعات دسترسی
print_message "Deployment completed!"
print_message "Application is available at: http://localhost:8000"
print_message "To view logs: docker-compose logs -f"
print_message "To stop services: docker-compose down"
print_message "To restart services: docker-compose restart"

# اضافه کردن به crontab برای اجرای خودکار
print_message "Setting up automatic restart..."
(crontab -l 2>/dev/null; echo "@reboot cd $(pwd) && ./NEWDEPLOY.sh") | crontab -

print_message "Deployment script completed successfully!" 