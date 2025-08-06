FROM python:3.11-slim

# =============================
# 1. Install dependencies
# =============================
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    curl \
    unzip \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libasound2 \
    libatk1.0-0 \
    libcups2 \
    libdrm2 \
    libxss1 \
    libxtst6 \
    libappindicator3-1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# =============================
# 2. Set working directory
# =============================
WORKDIR /app

# =============================
# 3. Copy files
# =============================
COPY . /app

# =============================
# 4. Install Python deps
# =============================
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# =============================
# 5. Env untuk chromium headless
# =============================
ENV CHROMIUM_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/lib/chromium/chromedriver

# =============================
# 6. Jalankan Flask
# =============================
# CMD ["python", "server.py"]
