# Weather Analytics Pipeline

Production-grade end-to-end batch data pipeline built with ~4 years of real-world data engineering experience.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Technical Design Decisions](#technical-design-decisions)
- [Data Flow](#data-flow)
- [Monitoring & Quality](#monitoring--quality)
- [Development](#development)
- [Trade-offs](#trade-offs)

## Overview

This project implements a production-ready data pipeline that ingests weather data from OpenWeatherMap API, transforms it using dbt-style SQL models, and stores it in a PostgreSQL data warehouse. The pipeline is orchestrated with Apache Airflow and runs entirely in Docker containers.

### Key Features

- **Scalable Ingestion**: Asynchronous API calls with configurable batch sizes and rate limiting
- **Transform Layer**: dbt-style SQL transformations with clear staging and mart models
- **Data Quality**: Automated validation checks on completeness, freshness, and value ranges
- **Orchestration**: Airflow DAGs with proper dependency management and failure handling
- **Observability**: Comprehensive logging at each pipeline stage
- **Containerization**: Full Docker Compose setup for reproducible local development

## Architecture

### High-Level Design

```
┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│   Weather API    │────────▶│   Airflow DAG    │────────▶│   PostgreSQL     │
│ (OpenWeatherMap) │         │  (Orchestration) │         │  (Data Warehouse)│
└──────────────────┘         └──────────────────┘         └──────────────────┘
                                      │
                                      │
                         ┌────────────┼────────────┐
                         │            │            │
                    Extract      Transform    Quality Check
                 (Python Module) (SQL Models)  (Validation)
```

### Components

1. **Data Source**: OpenWeatherMap API (REST)
2. **Orchestration**: Apache Airflow 2.x with LocalExecutor
3. **Storage**: PostgreSQL 13 with separate raw/transformed schemas
4. **Transform Engine**: Custom SQL runner implementing dbt-style patterns
5. **Quality Framework**: Python-based validation with configurable thresholds

## Quick Start

### Prerequisites

- Docker & Docker Compose
- OpenWeatherMap API key ([Get one here](https://openweathermap.org/api))
- 2GB+ available RAM

### Setup

```bash
# Clone repository
git clone https://github.com/JaswanthR1007/weather-analytics-pipeline.git
cd weather-analytics-pipeline

# Configure environment
cp .env.example .env
# Edit .env and add your WEATHER_API_KEY

# Start services
docker-compose up -d

# Wait for Airflow initialization (~30 seconds)
docker-compose logs -f airflow-init

# Access Airflow UI
open http://localhost:8080
# Login: admin / admin
```

### Running the Pipeline

1. Navigate to Airflow UI at http://localhost:8080
2. Enable the `weather_data_pipeline` DAG
3. Trigger a manual run or wait for scheduled execution (every 2 hours)
4. Monitor task execution in the Graph or Grid view

## Project Structure

```
weather-analytics-pipeline/
├── airflow/
│   ├── dags/
│   │   └── weather_pipeline.py          # Main orchestration logic
│   └── logs/                             # Airflow execution logs
├── config/
│   └── pipeline_config.yaml              # Centralized configuration
├── docker/
│   └── postgres/
│       └── init.sql                      # Schema initialization
├── docs/
│   └── ARCHITECTURE.md                   # Detailed architecture docs
├── src/
│   ├── extract/
│   │   └── weather_api.py                # API client with retry logic
│   ├── transform/
│   │   ├── sql/
│   │   │   ├── staging/
│   │   │   │   └── stg_weather_raw.sql   # Raw data cleanup
│   │   │   └── marts/
│   │   │       └── weather_daily_agg.sql # Business metrics
│   │   └── runner.py                     # SQL execution engine
│   ├── quality/
│   │   └── checks.py                     # Data validation framework
│   └── utils/
│       └── db.py                         # Database connection manager
├── tests/
│   ├── unit/                             # Unit tests
│   └── integration/                      # Integration tests
├── .env.example                          # Environment variables template
├── docker-compose.yml                    # Container orchestration
└── README.md                             # This file
```

## Technical Design Decisions

### 1. Why Apache Airflow?

**Decision**: Use Airflow over alternatives (Luigi, Prefect, Dagster)

**Rationale**:
- Industry-standard with strong community support
- Rich UI for monitoring and debugging
- Native support for complex dependencies
- Battle-tested in production environments

**Trade-off**: Higher resource overhead vs. simpler alternatives

### 2. Transformation Approach

**Decision**: Implement dbt-style SQL transformations without full dbt

**Rationale**:
- SQL as transformation language keeps logic accessible
- Layered approach (staging → marts) enforces clean architecture
- Custom runner provides learning opportunity while maintaining patterns
- Easier to debug than heavy framework abstractions

**Trade-off**: Manual dependency management vs. dbt's automatic lineage

### 3. Database Schema Design

**Decision**: Separate schemas for raw and transformed data

**Rationale**:
- Clear data lineage (raw → staging → marts)
- Ability to re-run transformations without re-ingesting
- Follows modern data warehouse patterns (bronze/silver/gold)

**Trade-off**: Additional storage overhead vs. data reliability

### 4. API Rate Limiting

**Decision**: Implement exponential backoff with configurable retry limits

**Rationale**:
- Respects API provider's rate limits
- Handles transient network failures gracefully
- Configurable for different API tiers

**Trade-off**: Slower initial runs vs. system stability

## Data Flow

### Stage 1: Extract (Raw Zone)

```python
# Fetches data from OpenWeatherMap API
# Stores in raw.weather_observations table
# No transformations applied
```

**Schema**: `raw.weather_observations`
- Preserves API response structure
- Includes ingestion metadata (timestamp, pipeline_id)
- Uses JSONB for flexible schema evolution

### Stage 2: Transform (Staging Layer)

```sql
-- Cleans and standardizes raw data
-- Handles nulls, type casting, unit conversions
-- Creates: staging.stg_weather_raw
```

**Transformations**:
- Temperature conversion (Kelvin → Celsius)
- Timestamp standardization to UTC
- Null handling and default values
- Deduplication logic

### Stage 3: Transform (Mart Layer)

```sql
-- Aggregates data for analytical queries
-- Calculates daily statistics
-- Creates: marts.weather_daily_agg
```

**Business Metrics**:
- Daily min/max/avg temperature
- Precipitation totals
- Weather condition frequencies
- Data quality scores

### Stage 4: Quality Checks

```python
# Validates data completeness and accuracy
# Checks for anomalies and outliers
# Logs results to quality.check_results table
```

**Checks**:
- Completeness: Row counts, null percentages
- Freshness: Maximum data age
- Accuracy: Value range validations
- Consistency: Cross-table comparisons

## Monitoring & Quality

### Logging Strategy

- **Application Logs**: Structured JSON logs with correlation IDs
- **Airflow Logs**: Task-level execution details
- **Database Logs**: Query performance and errors

### Data Quality Framework

```python
# Example quality check
{
    "check_name": "temperature_range",
    "check_type": "accuracy",
    "threshold": ">= 0.95",
    "actual_value": 0.97,
    "status": "passed"
}
```

### Alerting

- Airflow email alerts on task failures
- Quality check violations logged for review
- Configurable severity levels (warning/critical)

## Development

### Running Tests

```bash
# Unit tests
docker-compose exec airflow pytest tests/unit/

# Integration tests
docker-compose exec airflow pytest tests/integration/

# Code coverage
docker-compose exec airflow pytest --cov=src tests/
```

### Adding New Transformations

1. Create SQL file in appropriate directory:
   - `src/transform/sql/staging/` for cleaning/standardization
   - `src/transform/sql/marts/` for aggregations/metrics

2. Update `config/pipeline_config.yaml` with transformation order

3. Add data quality checks in `src/quality/checks.py`

4. Create unit tests in `tests/unit/`

### Local Database Access

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U airflow -d weather_db

# View raw data
SELECT * FROM raw.weather_observations LIMIT 10;

# Check transformed data
SELECT * FROM marts.weather_daily_agg;
```

## Trade-offs

### What I Would Change for Production

1. **Secrets Management**
   - Current: Environment variables
   - Production: AWS Secrets Manager / HashiCorp Vault
   - Reason: Centralized rotation, audit logging

2. **Orchestration**
   - Current: Airflow LocalExecutor
   - Production: Airflow with CeleryExecutor or Kubernetes Executor
   - Reason: Horizontal scaling, resource isolation

3. **Storage**
   - Current: Single PostgreSQL instance
   - Production: Separate OLTP/OLAP databases (RDS + Redshift/Snowflake)
   - Reason: Optimized for different workload patterns

4. **Monitoring**
   - Current: Airflow UI + logs
   - Production: DataDog/Prometheus + Grafana
   - Reason: Centralized observability, proactive alerting

5. **Testing**
   - Current: Unit + integration tests
   - Production: + End-to-end tests, data quality SLAs
   - Reason: Production confidence, SLA enforcement

6. **Infrastructure**
   - Current: Docker Compose
   - Production: Terraform/Kubernetes
   - Reason: Infrastructure as code, multi-environment support

### Scalability Considerations

- **Current**: Handles ~100 API calls/hour
- **Scale to 10x**: Add connection pooling, batch API requests
- **Scale to 100x**: Implement async workers, distributed task queue
- **Scale to 1000x**: Move to streaming architecture (Kafka + Flink)

## License

MIT License - See LICENSE file for details

## Contact

- GitHub: [@JaswanthR1007](https://github.com/JaswanthR1007)
- Portfolio: [Your Portfolio URL]

---

**Note**: This project showcases my experience building production-ready data pipelines. While this implementation is functional and follows best practices, enterprise deployment would benefit from additional monitoring, security hardening, and infrastructure automation as outlined in the trade-offs section.
