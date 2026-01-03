# 🚀 QUICKSTART GUIDE - Complete & Run Project

**Complete this production-grade data engineering project in 5 minutes!**

---

## ✅ Prerequisites Check

Before starting, ensure you have:

```bash
# Check Docker
docker --version
# Should show: Docker version 20.10+ or higher

# Check Docker Compose
docker-compose --version
# Should show: Docker Compose version 2.x or higher

# Check Git
git --version
# Should show: git version 2.x or higher
```

**Don't have these installed?**
- **Docker Desktop**: https://www.docker.com/products/docker-desktop
- **Git**: https://git-scm.com/downloads

---

## 📋 Step-by-Step Instructions

### Step 1: Clone the Repository

```bash
# Open Terminal (macOS) or Command Prompt/PowerShell (Windows)

# Clone the repository
git clone https://github.com/JaswanthR1007/weather-analytics-pipeline.git

# Navigate into the directory
cd weather-analytics-pipeline

# Verify files are present
ls -la
# You should see: .env.example, generate_complete_project.sh, requirements.txt, etc.
```

### Step 2: Get OpenWeatherMap API Key (FREE)

1. Go to: https://openweathermap.org/api
2. Click "Sign Up" (top right)
3. Create a free account
4. After signup, go to: https://home.openweathermap.org/api_keys
5. Copy your API key (looks like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

**Note**: API key may take 10-15 minutes to activate after signup.

### Step 3: Generate Complete Project Structure

```bash
# Make the generation script executable
chmod +x generate_complete_project.sh

# Run the generation script
./generate_complete_project.sh

# This will create:
# ✅ airflow/ directory with DAGs and plugins
# ✅ src/ directory with Python modules
# ✅ docker/ directory with Dockerfiles
# ✅ config/ directory with YAML configs
# ✅ tests/ directory with test files
# ✅ docker-compose.yml file
# ✅ All SQL transformation models
# ✅ Documentation files
```

**Expected Output:**
```
========================================
Weather Analytics Pipeline Generator
Production-Grade Data Engineering Project
========================================

[1/10] Creating directory structure...
[2/10] Creating docker-compose.yml...
[3/10] Creating Airflow DAG...
[4/10] Creating Python source files...
[5/10] Creating SQL transformation models...
[6/10] Creating Postgres init script...
[7/10] Creating configuration files...
[8/10] Creating README.md...
[9/10] Creating test files...
[10/10] Creating documentation...

✅ Project generation complete!
```

### Step 4: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file and add your API key
# macOS/Linux:
nano .env

# Windows (use notepad or any text editor):
notepad .env
```

**Replace this line:**
```env
WEATHER_API_KEY=your_api_key_here
```

**With your actual API key:**
```env
WEATHER_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

**Save and close the file**
- nano: Press `Ctrl+X`, then `Y`, then `Enter`
- notepad: File → Save

### Step 5: Start Docker Services

```bash
# Start all services in detached mode
docker-compose up -d

# This will:
# - Pull Docker images (first time only, ~5-10 minutes)
# - Start PostgreSQL (Airflow metadata + Data Warehouse)
# - Initialize Airflow database
# - Create admin user
# - Start Airflow webserver
# - Start Airflow scheduler
```

**Expected Output:**
```
Creating network "weather-analytics-pipeline_default" with the default driver
Creating volume "weather-analytics-pipeline_postgres-airflow-data" with default driver
Creating volume "weather-analytics-pipeline_postgres-dw-data" with default driver
Pulling postgres-airflow (postgres:14)...
Pulling postgres-dw (postgres:14)...
Pulling airflow-webserver (apache/airflow:2.7.3-python3.10)...
Creating postgres-airflow ... done
Creating postgres-dw      ... done
Creating airflow-init     ... done
Creating airflow-webserver ... done
Creating airflow-scheduler ... done
```

### Step 6: Verify Services Are Running

```bash
# Check container status
docker-compose ps

# All services should show "Up" status:
# NAME                  STATUS          PORTS
# airflow-webserver     Up (healthy)    0.0.0.0:8080->8080/tcp
# airflow-scheduler     Up (healthy)    
# postgres-airflow      Up (healthy)    0.0.0.0:5433->5432/tcp
# postgres-dw           Up (healthy)    0.0.0.0:5434->5432/tcp
```

**Troubleshooting:**
```bash
# If any service is not running, check logs:
docker-compose logs airflow-webserver
docker-compose logs airflow-scheduler
docker-compose logs postgres-dw
```

### Step 7: Access Airflow UI

```bash
# Open your browser and go to:
http://localhost:8080

# Or on macOS:
open http://localhost:8080
```

**Login Credentials:**
- **Username**: `admin`
- **Password**: `admin`

### Step 8: Enable and Run the DAG

1. **Find the DAG**: On the Airflow dashboard, look for `weather_data_pipeline`
2. **Enable the DAG**: Toggle the switch on the left from OFF (red) to ON (green/blue)
3. **Trigger the DAG**: Click the "Play" button (▶) on the right
4. **Monitor Execution**: Click on the DAG name to see task execution

**DAG Tasks:**
- `extract_weather_data` - Extracts weather from API
- `transform_data` - Transforms and loads to staging
- `quality_check` - Validates data quality

### Step 9: Verify Data in PostgreSQL

```bash
# Connect to the data warehouse
docker-compose exec postgres-dw psql -U dataeng -d weather_dw

# Once connected, run these SQL queries:

# List all schemas
\dn

# Check staging data
SELECT * FROM staging.weather_raw LIMIT 5;

# Check marts data
SELECT * FROM marts.fact_weather_daily ORDER BY date_key DESC LIMIT 5;

# Exit psql
\q
```

### Step 10: View Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f airflow-scheduler
docker-compose logs -f postgres-dw

# Stop following logs: Press Ctrl+C
```

---

## 🎯 What You've Built

Congratulations! You now have a fully functional production-grade data engineering pipeline:

✅ **Data Ingestion**: Python-based API extraction  
✅ **Orchestration**: Apache Airflow with LocalExecutor  
✅ **Data Warehouse**: PostgreSQL with dimensional model  
✅ **Transformations**: dbt-style SQL (staging → marts)  
✅ **Containerization**: Full Docker Compose setup  
✅ **Monitoring**: Airflow UI with task tracking  
✅ **Logging**: Structured logging throughout  

---

## 📊 Next Steps

### Explore the Project

```bash
# View project structure
tree -L 2

# View Airflow DAG code
cat airflow/dags/weather_data_pipeline.py

# View Python ingestion code
cat src/ingestion/api_client.py

# View SQL transformation
cat src/transformations/sql/marts/fact_weather_daily.sql
```

### Make Modifications

1. **Add more cities**: Edit `config/pipeline_config.yaml`
2. **Change schedule**: Edit DAG in `airflow/dags/weather_data_pipeline.py`
3. **Add transformations**: Create new SQL files in `src/transformations/sql/`
4. **Add data quality checks**: Edit `src/data_quality/checks.py`

### Commit Your Generated Files

```bash
# Stage all generated files
git add .

# Commit with descriptive message
git commit -m "feat: Complete project implementation with all generated files"

# Push to GitHub
git push origin main
```

---

## 🛑 Stopping the Project

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes all data)
docker-compose down -v

# Restart services
docker-compose restart
```

---

## ❓ Troubleshooting

### Issue: "Port 8080 is already allocated"

**Solution**: Another service is using port 8080
```bash
# Find what's using the port
# macOS/Linux:
lsof -i :8080

# Windows:
netstat -ano | findstr :8080

# Kill the process or change the port in docker-compose.yml
```

### Issue: "Cannot connect to Docker daemon"

**Solution**: Start Docker Desktop
- macOS: Open Docker Desktop from Applications
- Windows: Open Docker Desktop from Start Menu

### Issue: "API key is invalid"

**Solution**: 
1. Verify API key is copied correctly in `.env`
2. Wait 10-15 minutes after signup for key activation
3. Check key status at: https://home.openweathermap.org/api_keys

### Issue: "Services won't start"

**Solution**:
```bash
# Clean up everything
docker-compose down -v
docker system prune -a

# Restart Docker Desktop

# Try again
docker-compose up -d
```

---

## 📚 Additional Resources

- **Full Documentation**: See `SETUP_INSTRUCTIONS.md`
- **Project Repository**: https://github.com/JaswanthR1007/weather-analytics-pipeline
- **Airflow Docs**: https://airflow.apache.org/docs/
- **Docker Compose Docs**: https://docs.docker.com/compose/
- **OpenWeatherMap API**: https://openweathermap.org/api

---

## 🎉 Success!

You've successfully deployed a production-grade data engineering pipeline!

**Share your success:**
- ⭐ Star the repository on GitHub
- 📸 Screenshot your Airflow dashboard
- 💼 Add to your LinkedIn/Resume
- 🚀 Extend with your own features

**Happy Data Engineering! 🚀**