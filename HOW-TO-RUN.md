# How to Run the Portfolio Web Application

## Easiest way (no MySQL or Redis needed)

1. **Open a terminal** in this folder:  
   `c:\Users\Administrator\Portfolio_Application\asset-architects_01`

2. **Run with the standalone profile** (uses in-memory database only):
   ```cmd
   .\mvnw.cmd spring-boot:run "-Dspring-boot.run.profiles=standalone"
   ```

3. **Wait** until you see:
   ```text
   Tomcat started on port 8081
   Started PortfolioManagerApplication in ... seconds
   ```

4. **Open your browser** and go to:
   ```text
   http://localhost:8081
   ```
   Do **not** open the `index.html` file directly (file://). It must be loaded from the server.

5. **Keep the terminal open** while you use the app. Closing it stops the server.

---

## If it still doesn’t work

| Problem | What to do |
|--------|------------|
| **"Port 8081 already in use"** | Another instance is running. Close that terminal or run: `netstat -ano \| findstr :8081` then `taskkill /PID <number> /F` |
| **"Connection refused" in browser** | Make sure you use **http://localhost:8081** (not file://). Start the server first, then open the URL. |
| **"Failed to fetch" or blank Dashboard** | You are likely on file://. Open **http://localhost:8081** in the address bar. |
| **MySQL error when not using standalone** | Use the standalone profile (step 2 above), or install/start MySQL and create database `portfolio_db`. |

---

## Full setup (MySQL + Redis)

If you want to use MySQL and optional Redis:

1. Install and start **MySQL**. Create database: `CREATE DATABASE portfolio_db;`
2. Update `src/main/resources/application.properties` if your MySQL username/password differ.
3. (Optional) Start **Redis** on port 6379.
4. Run **without** a profile:
   ```cmd
   .\mvnw.cmd spring-boot:run
   ```
5. Open **http://localhost:8081** in your browser.

---

## Features

- **Market Dashboard**: Stocks, Mutual Funds, and Gold with live (dummy) prices. Click a stock row to see price trend graph; use **Buy** to place orders.
- **My Holdings**: Your assets by category. Click a row for purchase/sale history and holding details; use **Sell** for quick sell.
- **Portfolio Insights**: Total invested, net P&L, P&L % per asset, and asset allocation by industry (pie chart).
- **Theme**: Use the sun/moon icon in the header to switch light/dark theme.
- **Language**: Use the dropdown to switch between English and Hindi (हिंदी).

## AI Assistant (Flask + Groq)

The ◆ AI Assistant uses a **Flask** server that calls the **Groq API**. Do this once:

1. **Get a Groq API key**  
   Sign up at [https://console.groq.com](https://console.groq.com) and create an API key.

2. **Set the API key** (choose one):
   - **Option A (recommended):** In this folder, copy `.env.example` to `.env` and set:
     ```text
     GROQ_API_KEY=gsk_your_actual_key_here
     ```
   - **Option B:** In a terminal before running `server.py`:
     - Windows: `set GROQ_API_KEY=gsk_your_actual_key_here`
     - Linux/Mac: `export GROQ_API_KEY=gsk_your_actual_key_here`

3. **Install Python dependencies** (in this folder):
   ```cmd
   pip install -r requirements-server.txt
   ```

4. **Start the AI server** in a **second terminal** (keep it open):
   ```cmd
   python server.py
   ```
   You should see: `AI Assistant (Flask + Groq) starting on http://0.0.0.0:5000`

5. **Start the Portfolio app** (IntelliJ or `mvnw spring-boot:run`) and open the app in the browser (e.g. http://localhost:8082). Click **◆ AI Assistant** and type a question.

The Spring Boot app proxies chat requests to `http://localhost:5000/api/chat`. If the Flask server is not running, the app falls back to a simple built-in finance Q&A.
