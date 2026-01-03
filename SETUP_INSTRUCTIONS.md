# Weather Analytics Pipeline - Complete Project Setup

**Production-Grade Data Engineering Project**  
*Demonstrates ~4 years of real-world data engineering experience*

---

## Project Overview

This is an end-to-end batch data pipeline that:
- Ingests weather data from OpenWeatherMap API
- Transforms data using dbt-style SQL modeling
- Orchestrates with Apache Airflow
- Loads into PostgreSQL data warehouse
- Includes comprehensive logging and data quality checks
- Fully containerized with Docker

---

## Quick Start

```bash
# 1. Clone the repository (if you haven't already)
git clone https://github.com/JaswanthR1007/weather-analytics-pipeline.git
cd weather-analytics-pipeline

# 2. Run the automated setup script
chmod +x generate_complete_project.sh
./generate_complete_project.sh

# 3. Configure environment variables
cp .env.example .env
# Edit .env and add your WEATHER_API_KEY from openweathermap.org

# 4. Start the services
docker-compose up -d

# 5. Access Airflow UI
# URL: http://localhost:8080
# Username: admin
# Password: admin
```

---

## Architecture

```
┌─────────────────┐         ┌──────────────┐         ┌───────────────┐
│  OpenWeather    │────────▶│   Airflow    │────────▶│   Postgres    │
│      API        │         │   Pipeline   │         │  Data Warehouse│
└─────────────────┘         └──────────────┘         └───────────────┘
                                   │
                                   ├─── Data Ingestion (Python)
                                   ├─── Transformations (SQL)
                                   └─── Quality Checks (Python)
```

### Data Flow:
1. **Extract**: Python ingestion layer pulls weather data from API
2. **Stage**: Raw JSON loaded to `staging.weather_raw`
3. **Transform**: dbt-style SQL models create dimension and fact tables
4. **Validate**: Data quality checks run on final tables
5. **Monitor**: Comprehensive logging at every step

---

## Project Structure

```
weather-analytics-pipeline/
├── airflow/                    # Airflow configuration
│   ├── dags/                  # DAG definitions
│   │   └── weather_data_pipeline.py
│   ├── plugins/               # Custom operators
│   │   └── custom_operators/
│   │       └── data_quality_operator.py
│   ├── config/
│   └── logs/
├── src/                       # Source code
│   ├── ingestion/            # Data extraction layer
│   │   ├── api_client.py     # API wrapper
│   │   ├── extractors.py     # Extract logic
│   │   └── loaders.py        # Load to staging
│   ├── transformations/       # SQL transformations
│   │   ├── sql/
│   │   │   ├── staging/      # Staging models
│   │   │   ├── intermediate/ # Business logic
│   │   │   └── marts/        # Final dim/fact tables
│   │   └── transform_runner.py
│   ├── utils/                # Shared utilities
│   │   ├── db_connector.py   # Database connections
│   │   ├── logger.py         # Logging setup
│   │   └── config_loader.py  # Config management
│   └── data_quality/         # Data validation
│       ├── checks.py
│       └── validators.py
├── tests/                    # Test suite
│   ├── unit/
│   └── integration/
├── docker/                   # Docker configurations
│   ├── airflow/
│   │   └── Dockerfile
│   └── postgres/
│       └── init.sql
├── config/                   # Configuration files
│   ├── pipeline_config.yaml
│   └── logging_config.yaml
├── scripts/                  # Utility scripts
│   ├── generate_complete_project.sh  # Main setup script
│   └── init_db.sh
├── docs/                     # Documentation
│   ├── architecture.md
│   └── data_dictionary.md
├── .env.example              # Environment template
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── setup.py
└── README.md
```

---

## Technology Stack

- **Orchestration**: Apache Airflow 2.7.3
- **Data Warehouse**: PostgreSQL 14
- **Programming**: Python 3.10
- **Containerization**: Docker & Docker Compose
- **Data Modeling**: dbt-style SQL transformations
- **API**: OpenWeatherMap REST API
- **Logging**: Python logging module with structured logs
- **Testing**: pytest, unittest

---

## Key Features Demonstrating Senior Experience

### 1. **Production-Ready Code Organization**
- Clear separation of concerns (extraction, transformation, loading)
- Reusable utility modules
- Configuration-driven design
- Environment-based settings

### 2. **Data Modeling Best Practices**
- Staging → Intermediate → Marts layered approach
- Dimensional modeling (star schema)
- Slowly Changing Dimensions (SCD Type 2) ready
- Incremental processing patterns

### 3. **Error Handling & Resilience**
- Retry logic with exponential backoff
- Dead letter queues for failed records
- Graceful degradation
- Comprehensive error logging

### 4. **Data Quality & Monitoring**
- Custom data quality checks
- Null/duplicate detection
- Freshness validations
- Anomaly detection thresholds

### 5. **Scalability Considerations**
- Parameterized queries
- Batch processing with configurable chunk sizes
- Connection pooling
- Efficient SQL with proper indexing

### 6. **DevOps Integration**
- Fully Dockerized
- Environment variable management
- CI/CD ready (GitHub Actions template included)
- Infrastructure as Code patterns

---

## Getting Started - Detailed Steps

### Prerequisites
- Docker Desktop installed
- OpenWeatherMap API key (free tier: https://openweathermap.org/api)
- 8GB RAM minimum
- macOS, Linux, or Windows with WSL2

### Step 1: Generate Project Files

Run the comprehensive setup script that creates all necessary files:

```bash
chmod +x generate_complete_project.sh
./generate_complete_project.sh
```

This script will create:
- All directory structures
- Python source files
- SQL transformation models
- Airflow DAGs
- Docker configurations
- Configuration files
- Documentation

### Step 2: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and set:
```env
WEATHER_API_KEY=your_api_key_here
POSTGRES_DW_USER=dataeng
POSTGRES_DW_PASSWORD=dataeng123
POSTGRES_DW_DB=weather_dw
```

### Step 3: Start Services

```bash
# Build and start all containers
docker-compose up -d

# Check logs
docker-compose logs -f

# Verify services are running
docker-compose ps
```

### Step 4: Access Airflow

1. Open browser: http://localhost:8080
2. Login with admin/admin
3. Enable the `weather_data_pipeline` DAG
4. Trigger manually or wait for scheduled run (daily at 2 AM UTC)

### Step 5: Monitor Pipeline

```bash
# View Airflow scheduler logs
docker-compose logs -f airflow-scheduler

# View pipeline logs
docker-compose exec airflow-webserver cat /opt/airflow/logs/dag_id=weather_data_pipeline/run_id=<run_id>/task_id=<task_id>/attempt=1.log

# Connect to Postgres to view data
docker-compose exec postgres-dw psql -U dataeng -d weather_dw
```

```sql
-- Check staging data
SELECT * FROM staging.weather_raw LIMIT 10;

-- Check dimension tables
SELECT * FROM marts.dim_location;

-- Check fact table
SELECT * FROM marts.fact_weather_daily 
ORDER BY date DESC LIMIT 10;
```

---

## Data Model

### Staging Layer
- `staging.weather_raw`: Raw JSON from API

### Marts Layer (Star Schema)
- `marts.dim_location`: City dimension (SCD Type 2 ready)
- `marts.dim_date`: Date dimension
- `marts.fact_weather_daily`: Daily weather metrics

### Sample Query
```sql
SELECT 
    d.date,
    l.city_name,
    l.country,
    f.temperature_avg,
    f.humidity_avg,
    f.wind_speed_avg
FROM marts.fact_weather_daily f
JOIN marts.dim_location l ON f.location_key = l.location_key
JOIN marts.dim_date d ON f.date_key = d.date_key
WHERE d.date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY d.date DESC, l.city_name;
```

---

## Development Workflow

### Running Tests
```bash
# Install dev dependencies
pip install -r requirements.txt

# Run unit tests
pytest tests/unit/

# Run integration tests  
pytest tests/integration/

# Run with coverage
pytest --cov=src tests/
```

### Code Quality
```bash
# Format code
black src/

# Lint
flake8 src/
pylint src/

# Type checking
mypy src/
```

### Adding New Data Sources
1. Create new extractor in `src/ingestion/extractors.py`
2. Add staging SQL model in `src/transformations/sql/staging/`
3. Update transformation runner
4. Add to Airflow DAG
5. Write tests

---

## Production Deployment Considerations

### Security
- [ ] Use secrets manager (AWS Secrets Manager, HashiCorp Vault)
- [ ] Rotate credentials regularly
- [ ] Enable SSL/TLS for database connections
- [ ] Implement role-based access control
- [ ] Scan Docker images for vulnerabilities

### Monitoring
- [ ] Integrate with Datadog/New Relic
- [ ] Set up PagerDuty alerts
- [ ] Configure Airflow email alerts
- [ ] Add Slack notifications
- [ ] Implement custom metrics dashboards

### Scalability
- [ ] Use Kubernetes instead of Docker Compose
- [ ] Implement Celery Executor for Airflow
- [ ] Add Redis for caching
- [ ] Partition large tables by date
- [ ] Implement data archiving strategy

### Cost Optimization
- [ ] Use spot instances where possible
- [ ] Implement data retention policies
- [ ] Compress older data
- [ ] Use read replicas for analytics
- [ ] Monitor and optimize query performance

---

## Troubleshooting

### Services won't start
```bash
# Check Docker resources
docker system df

# Clean up
docker system prune -a

# Rebuild
docker-compose down -v
docker-compose up --build
```

### Airflow DAG not appearing
```bash
# Check for Python syntax errors
docker-compose exec airflow-scheduler python /opt/airflow/dags/weather_data_pipeline.py

# Refresh DAGs
docker-compose restart airflow-scheduler
```

### Database connection issues
```bash
# Test Postgres connection
docker-compose exec postgres-dw psql -U dataeng -d weather_dw -c "SELECT 1;"

# Check network
docker network inspect weather-analytics-pipeline_default
```

---

## API Rate Limits

OpenWeatherMap Free Tier:
- 60 calls/minute
- 1,000,000 calls/month

The pipeline is configured to:
- Query 5 cities per run
- Run once daily (30 calls/day)
- Well within free tier limits

To monitor multiple cities, edit `config/pipeline_config.yaml`

---

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## License

MIT License - See LICENSE file for details

---

## Contact

Project maintainer: Data Engineering Team
Repository: https://github.com/JaswanthR1007/weather-analytics-pipeline

---

## Acknowledgments

- OpenWeatherMap API for weather data
- Apache Airflow community
- dbt Labs for modeling inspiration

---

**Note**: This project is designed as a portfolio piece to demonstrate production-grade data engineering skills. It can be extended for real-world use cases with additional data sources, more complex transformations, and advanced monitoring.