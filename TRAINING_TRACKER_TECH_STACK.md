# Training Tracker - Technology Stack & Deployment
## Recommended Stack, Architecture Options, and Deployment Models

---

## 1. RECOMMENDED TECHNOLOGY STACK

### 1.1 Frontend Stack (Presentation Layer)

| Component | Recommendation | Alternatives | Rationale |
|---|---|---|---|
| **Framework** | React 18+ (Vite) | Vue 3, Angular 17+ | React ecosystem, large community, component reusability |
| **State Management** | Redux Toolkit or Zustand | Context API, Jotai | Predictable state, time-travel debugging, middleware support |
| **UI Component Library** | Material-UI v5 | Shadcn/ui, Chakra UI | Professional components, accessibility, theming |
| **Styling** | Tailwind CSS | SASS/SCSS | Utility-first, rapid development, consistency |
| **Form Handling** | React Hook Form | Formik | Light weight, excellent validation integration |
| **HTTP Client** | axios | fetch API | Interceptors, retry logic, request/response transformation |
| **Real-time Chat** | Socket.io | Pusher, AWS AppSync | WebSocket support, fallback mechanisms |
| **Video Player** | HLS.js + React Video Player | JW Player, Vimeo API | Open-source, adaptive bitrate streaming |
| **PDF/Export** | PDFKit / ReportLab backend | jsPDF | Server-side generation for quality control |
| **Testing** | Jest + React Testing Library | Vitest, Playwright | Industry standard, excellent coverage |
| **Build Tool** | Vite | Webpack, Parcel | Fast development server, optimized builds |
| **Type Safety** | TypeScript | PropTypes | Compile-time error detection |
| **Code Quality** | ESLint + Prettier | Standard JS | Consistent formatting, rule enforcement |

### 1.2 Backend Stack (Application Logic Layer)

#### Option A: Node.js + Express (Recommended for faster MVPs)

| Component | Recommendation | Rationale |
|---|---|---|
| **Runtime** | Node.js 20+ LTS | JavaScript across stack, vast package ecosystem |
| **Framework** | Express.js + middleware | Lightweight, middleware-based, highly customizable |
| **ORM** | Sequelize or TypeORM | SQL abstraction, migrations, relationships |
| **Authentication** | Passport.js + JWT | Flexible, supports 300+ SSO strategies |
| **Validation** | Joi or Zod | Schema validation, custom rules |
| **Testing** | Jest + Supertest | Full integration testing, mocking |
| **Logging** | Winston | Structured logging, multiple transports |
| **Caching** | Redis + ioredis | Session storage, rate limiting, recommendations |
| **Job Queue** | Bull/BullMQ | Background tasks (email, PDF generation) |
| **API Docs** | Swagger/OpenAPI + Swagger UI | Auto-generated documentation |

**Pros:**
- Single language (JavaScript/TypeScript) across stack
- Fast prototyping and MVP development
- Large npm ecosystem
- WebSocket support with Socket.io

**Cons:**
- CPU-heavy operations should offload to worker threads
- Single-threaded nature (mitigated with clustering)

#### Option B: Python + FastAPI (Recommended for AI integration)

| Component | Recommendation | Rationale |
|---|---|---|
| **Framework** | FastAPI | Modern, async, auto-documentation |
| **ORM** | SQLAlchemy | Powerful, supports multiple databases |
| **Authentication** | FastAPI Security + JWT | Dependency injection, flexible |
| **Validation** | Pydantic | Data validation, type hints |
| **Testing** | pytest | Comprehensive, fixtures, mocking |
| **Logging** | Python logging + structlog | Structured logging |
| **Caching** | Redis + aioredis | Async support |
| **Job Queue** | Celery + Redis | Distributed task processing |
| **ML/AI** | Scikit-learn, TensorFlow | Future ML recommendations |
| **API Docs** | Auto-generated Swagger | Built into FastAPI |

**Pros:**
- Excellent for ML/AI features (recommendation engine, future)
- Strong data science ecosystem
- Async-first (better performance)
- Great for computational tasks

**Cons:**
- Requires Python deployment infrastructure
- Larger team ramp-up if JS-heavy organization

#### Option C: Java + Spring Boot (Enterprise, if org uses Java)

| Component | Recommendation | Rationale |
|---|---|---|
| **Framework** | Spring Boot 3+ | Mature, enterprise-grade |
| **ORM** | JPA/Hibernate | Robust, cacheable |
| **Authentication** | Spring Security + OAuth2 | Battle-tested security |
| **Testing** | JUnit 5 + Mockito | Comprehensive testing |
| **Caching** | Redis + Spring Cache | Abstraction, annotation-based |
| **Job Queue** | Spring Batch / Quartz | Enterprise job scheduling |

**Recommendation:** Choose Java if your organization standardizes on it; otherwise Node.js or Python for faster development.

### 1.3 Database Stack

#### Primary Database: PostgreSQL 15+

```
Rationale:
✓ ACID compliance (data integrity)
✓ Advanced features: JSON support, full-text search, arrays
✓ Excellent performance at scale (10K+ users)
✓ Rich type system
✓ Proven in production (banking, telecom)
✓ Open-source, no licensing costs
✓ Strong backup/replication tools (Patroni, pg_basebackup)

Configuration:
- Connection pooling: PgBouncer (3 connections per app instance)
- Replication: Streaming replication for HA
- Backups: WAL archiving + daily snapshots
```

#### Cache Layer: Redis 7+

```
Rationale:
✓ Sub-millisecond response times
✓ Session storage (JWT/session tokens)
✓ Rate limiting (token bucket)
✓ Pub/Sub for notifications
✓ Sorted sets for leaderboards/rankings

Use Cases:
- Recommendation cache (5-minute TTL)
- Session cache (1-day TTL)
- Rate limit counters (per-minute)
- Real-time notifications (pub/sub)
- Course progress updates (debounced to DB every 30s)
```

#### Search (Optional, for large deployments): Elasticsearch 8+

```
Rationale:
✓ Full-text search across courses, documents
✓ Advanced filtering on course metadata
✓ Aggregations for analytics

Implementation:
- Index courses, lessons, documents
- Update index asynchronously via message queue
- TTL: keep last 6 months indexed
- Use for: course search, audit log search
```

### 1.4 File Storage & CDN

| Service | Use Case | Details |
|---|---|---|
| **AWS S3 / Azure Blob / GCS** | Course content, assignments, certificates | Versioning, encryption, lifecycle policies |
| **CloudFront / Azure CDN / GCS CDN** | Video delivery, PDF downloads | 30-day cache, gzip compression |
| **Internal File Server** | On-prem deployment | NFS mount or SMB share, local caching |

**Video Delivery:**
- Store .mp4 / .webm in object storage
- Serve via CDN with HLS/DASH for adaptive streaming
- Backup: 2 regions minimum (replication)

### 1.5 Email Service

| Service | Use Case | Details |
|---|---|---|
| **SendGrid** (Cloud) | Transactional emails | 100K free/month tier, webhook tracking |
| **AWS SES** (Cloud) | High-volume, cost-sensitive | $0.10 per 1000 emails |
| **Microsoft Exchange** (On-prem) | Enterprise SMTP | Integrated with Active Directory |
| **SMTP Relay** (Internal) | On-prem alternative | Use internal mail server |

**Features:**
- Email templates (Handlebars/Liquid syntax)
- Unsubscribe management
- Bounce handling
- DKIM/SPF signing

### 1.6 Real-time Communication

| Feature | Technology | Details |
|---|---|---|
| **Chat Support** | Socket.io + Redis adapter | Room-based, user presence, message history |
| **Notifications** | Socket.io + browser push | In-app alerts, optional desktop push |
| **Teams Integration** | Microsoft Graph API | Send messages to Teams channels |
| **Slack Integration** | Incoming Webhooks | Ticket notifications |

---

## 2. DEPLOYMENT ARCHITECTURE - OPTION A: CLOUD-NATIVE

```
┌─────────────────────────────────────────────────────────────────────┐
│                           USERS (Internet)                           │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         CDN (CloudFront/CDN)                        │
│                 Static assets, video streaming                       │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      WAF (Web Application Firewall)                 │
│                        DDoS Protection                               │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Load Balancer (ALB/NLB)                          │
│              Health checks, sticky sessions, SSL offload             │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
        ┌────────────┐  ┌────────────┐  ┌────────────┐
        │ App Server │  │ App Server │  │ App Server │
        │  Instance  │  │  Instance  │  │  Instance  │
        │  (ECS/EKS) │  │  (ECS/EKS) │  │  (EKS)     │
        │ Container  │  │ Container  │  │ Container  │
        └────────────┘  └────────────┘  └────────────┘
                │              │              │
                └──────────────┼──────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
    ┌─────────┐           ┌────────┐           ┌──────────┐
    │PostgreSQL│           │ Redis  │           │    S3    │
    │ Primary  │           │ Cache  │           │ Storage  │
    │ RDS/AKS  │           │Cluster │           │ (Media)  │
    └─────────┘           └────────┘           └──────────┘
        │
        ▼
    ┌─────────────────────┐
    │ Read Replica        │
    │ (Multi-region)      │
    └─────────────────────┘

Background Services:
┌─────────────────────────────────────────────────────────────────────┐
│                     Message Queue (SQS/RabbitMQ)                    │
│   - Email delivery                                                   │
│   - PDF generation                                                   │
│   - Certificate issuance                                             │
│   - Notification sending                                             │
└─────────────────────────────────────────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
    ┌─────────┐          ┌──────────┐          ┌──────────┐
    │ Email   │          │ PDF      │          │Notification│
    │ Worker  │          │ Worker   │          │ Worker   │
    └─────────┘          └──────────┘          └──────────┘

Monitoring & Logging:
┌─────────────────────────────────────────────────────────────────────┐
│                                                                      │
│   CloudWatch / Datadog / Prometheus/Grafana │ Elasticsearch/ELK    │
│   - Performance metrics                      │ - Log aggregation    │
│   - Alerts & alarms                          │ - Audit logs         │
│   - Dashboards                               │ - Analysis           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.1 Cloud Providers & Services

#### AWS Option

| Component | Service | Details |
|---|---|---|
| **Compute** | ECS (Fargate) or EKS | Containerized apps, auto-scaling |
| **Database** | RDS PostgreSQL | Managed, automated backups, replication |
| **Cache** | ElastiCache (Redis) | Fully managed, cluster mode |
| **Storage** | S3 + CloudFront | Object storage + CDN |
| **Load Balancing** | Application Load Balancer | Layer 7, health checks |
| **Email** | SES | Transactional email |
| **Message Queue** | SQS | Managed queue, FIFO + standard |
| **Job Scheduling** | EventBridge + Lambda | Cron jobs, scheduled tasks |
| **Monitoring** | CloudWatch | Logs, metrics, alarms |
| **Secrets** | Secrets Manager | API keys, DB passwords |

#### Azure Option

| Component | Service | Details |
|---|---|---|
| **Compute** | App Service / AKS | Managed containers, auto-scale |
| **Database** | Azure SQL / PostgreSQL Flexible | Managed relational DB |
| **Cache** | Azure Cache for Redis | Fully managed Redis |
| **Storage** | Blob Storage + CDN | Object storage + edge delivery |
| **Load Balancing** | Application Gateway | WAF, path routing |
| **Email** | SendGrid (partner) | Transactional email |
| **Message Queue** | Service Bus | Enterprise messaging |
| **Job Scheduling** | Logic Apps / Functions | Serverless scheduling |
| **Monitoring** | Application Insights | APM, logging, analytics |
| **Secrets** | Key Vault | Secret management |
| **Auth** | Azure AD B2C | SSO, MFA, SAML |

#### GCP Option

| Component | Service | Details |
|---|---|---|
| **Compute** | Cloud Run / GKE | Serverless or Kubernetes |
| **Database** | Cloud SQL (PostgreSQL) | Managed relational DB |
| **Cache** | Cloud Memorystore (Redis) | Fully managed cache |
| **Storage** | Cloud Storage + CDN | Object storage + edge |
| **Load Balancing** | Cloud Load Balancing | Global, multi-region |
| **Email** | SendGrid (partner) | Transactional email |
| **Message Queue** | Cloud Pub/Sub | Event streaming |
| **Job Scheduling** | Cloud Scheduler | Cron jobs |
| **Monitoring** | Cloud Monitoring | Metrics, logs, traces |
| **Secrets** | Secret Manager | Sensitive data |

### 2.2 High Availability Setup

```
Region: us-east-1 (Primary)
  ├─ Availability Zone 1a
  │  ├─ App Server (ECS)
  │  ├─ PostgreSQL Primary
  │  └─ Redis Master
  │
  └─ Availability Zone 1b
     ├─ App Server (ECS)
     ├─ PostgreSQL Standby (streaming replication)
     └─ Redis Replica

Region: us-west-2 (Disaster Recovery)
  ├─ PostgreSQL Read Replica (1-hour lag)
  └─ S3 Cross-Region Replication (real-time)

Failover:
- If primary AZ fails: ALB routes to backup AZ
- If primary region fails: Manual failover to DR region
  (or automated with Route 53 health checks)

RTO: 5 minutes (within region)
RPO: 15 minutes (across regions)
```

---

## 3. DEPLOYMENT ARCHITECTURE - OPTION B: ON-PREMISES / HYBRID

```
┌──────────────────────────────────────────────────────────────────────┐
│                        USERS (Intranet)                               │
└──────────────────────────┬───────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    VPN / Reverse Proxy (Nginx)                       │
│            DDoS Protection, SSL, Access Control                       │
└──────────────────────────┬───────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│              Load Balancer (Nginx, HAProxy, F5)                      │
│         Health checks, session persistence, rate limiting             │
└──────────────────────────┬───────────────────────────────────────────┘
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │ App Server │  │ App Server │  │ App Server │
    │  VM/Bare   │  │  VM/Bare   │  │  VM/Bare   │
    │  Metal     │  │  Metal     │  │  Metal     │
    │ (Node/Java)│  │(Node/Java) │  │(Python)    │
    └────────────┘  └────────────┘  └────────────┘
            │              │              │
            └──────────────┼──────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    ┌─────────────┐   ┌──────────┐      ┌──────────┐
    │ SQL Server/ │   │  Redis   │      │File Server│
    │ PostgreSQL  │   │ (Memory) │      │(NFS/SMB)  │
    │ (VM/Bare)   │   │ Cluster  │      │  Shares   │
    └─────────────┘   └──────────┘      └──────────┘
            │
            ▼
        ┌──────────────┐
        │ SAN/Storage  │
        │ (Backup)     │
        └──────────────┘

Background Services (Separate VM Cluster):
┌──────────────────────────────────────────────────────────────────────┐
│           Message Queue (RabbitMQ / Apache Kafka)                    │
│                  Email, PDF, Notifications                            │
└──────────────────────────────────────────────────────────────────────┘
            │
    ┌───────┼───────┐
    ▼       ▼       ▼
┌─────┐┌──────┐┌──────────┐
│Email││ PDF  ││Notification│
│Svc  ││Svc   ││Service   │
└─────┘└──────┘└──────────┘

Monitoring & Backup:
┌──────────────────────────────────────────────────────────────────────┐
│  Prometheus/Grafana (Metrics) │ ELK Stack (Logs) │ Backup Storage   │
│  - Custom dashboards           │ - Centralized    │ - Daily snapshots│
│  - Alerting rules              │ - Audit logs     │ - Offsite copy  │
│  - Performance trends          │ - Search/filter  │ - Retention: 90d│
└──────────────────────────────────────────────────────────────────────┘

Active Directory / LDAP Integration:
┌──────────────────────────────────────────────────────────────────────┐
│  SSO with Windows AD / Okta  │ LDAP for user sync & groups          │
│  - User provisioning           │ - Automated deprovisioning          │
│  - Group-based access          │ - MFA via AD FS or Okta            │
└──────────────────────────────────────────────────────────────────────┘
```

### 3.1 On-Premises Requirements

#### Hardware Specifications

| Component | Specs | Quantity |
|---|---|---|
| **App Servers** | 8 vCPU, 32GB RAM, 500GB SSD | 3 (HA) |
| **Database Server** | 16 vCPU, 128GB RAM, 2TB SAS RAID 10 | 2 (Primary + Standby) |
| **Cache Server** | 4 vCPU, 64GB RAM, 100GB SSD | 2 (Cluster) |
| **File Server** | 2 vCPU, 32GB RAM, 10TB RAID 6 | 1 |
| **Backup/NAS** | 4 vCPU, 64GB RAM, 20TB | 1 |
| **Monitoring** | 4 vCPU, 16GB RAM, 500GB SSD | 1 |

#### Network Requirements

- **Firewall rules:**
  - Port 443 (HTTPS) inbound from users
  - Port 3306/5432 (DB) only internal
  - Port 6379 (Redis) only internal
  - Port 5000-6000 (backend) behind LB
  
- **DNS:** Internal DNS resolution for app.internal.com

- **SSL/TLS:** Self-signed or internal CA certificates

- **Backup:** Encrypted offsite backup (SFTP/AWS S3)

#### OS & Virtualization

- **Hypervisor:** VMware vSphere, Hyper-V, or KVM
- **OS:** Ubuntu 22.04 LTS or RHEL 9
- **Container Option:** Docker + Docker Compose or Kubernetes (OpenShift)

### 3.2 Hybrid Deployment

```
Scenario: On-prem app + Cloud storage for training content

┌─────────────────────────┐
│  On-Premises App        │
│  - Authentication       │
│  - User mgmt            │
│  - Progress tracking    │
│  - Ticket system        │
└──────────────┬──────────┘
               │
      ┌────────┴────────┐
      ▼                 ▼
┌──────────────┐  ┌──────────────────┐
│  Internal    │  │  AWS S3 / Azure  │
│  Database    │  │  Blob (Content)  │
│  + Cache     │  │                  │
└──────────────┘  └──────────────────┘
      │                 │
      └────────┬────────┘
               │
        ┌──────▼──────┐
        │   CDN        │
        │ CloudFront   │
        │  Azure CDN   │
        └──────────────┘

Benefits:
✓ User data stays on-prem (compliance)
✓ Training content in cloud (scalability)
✓ Reduced storage costs
✓ Global content delivery
```

---

## 4. CONTAINERIZATION & ORCHESTRATION

### 4.1 Docker Setup

```dockerfile
# Dockerfile for Training Tracker Backend

FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./

ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD node healthcheck.js

CMD ["node", "dist/server.js"]
```

### 4.2 Docker Compose (Development)

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgres://user:pass@db:5432/training_tracker
      REDIS_URL: redis://cache:6379
    depends_on:
      - db
      - cache
    volumes:
      - ./src:/app/src

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: training_tracker
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    environment:
      VITE_API_URL: http://localhost:3000
    depends_on:
      - app

volumes:
  postgres_data:
  redis_data:
```

### 4.3 Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: training-tracker-app
  labels:
    app: training-tracker
spec:
  replicas: 3
  selector:
    matchLabels:
      app: training-tracker
  template:
    metadata:
      labels:
        app: training-tracker
    spec:
      containers:
      - name: app
        image: registry.example.com/training-tracker:1.0.0
        ports:
        - containerPort: 3000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: connection-string
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: training-tracker-service
spec:
  selector:
    app: training-tracker
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
  type: LoadBalancer
```

---

## 5. CI/CD PIPELINE

### 5.1 GitHub Actions Workflow

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '20'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Lint
      run: npm run lint
    
    - name: Run tests
      run: npm run test:coverage
      env:
        DATABASE_URL: postgres://postgres:postgres@localhost:5432/test_db
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Run SAST scan
      uses: github/super-linter@v4
    - name: Dependency check
      run: npm audit --production

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Build Docker image
      run: docker build -t training-tracker:${{ github.sha }} .
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker tag training-tracker:${{ github.sha }} registry.example.com/training-tracker:latest
        docker push registry.example.com/training-tracker:latest

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/develop'
    steps:
    - name: Deploy to staging
      run: |
        kubectl set image deployment/training-tracker \
          app=registry.example.com/training-tracker:latest \
          --namespace=staging

  deploy-production:
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://training-tracker.example.com
    steps:
    - name: Deploy to production
      run: |
        kubectl set image deployment/training-tracker \
          app=registry.example.com/training-tracker:latest \
          --namespace=production
    - name: Smoke tests
      run: npm run test:smoke -- --url https://training-tracker.example.com
```

---

(Continues with MVP scope in next section...)
