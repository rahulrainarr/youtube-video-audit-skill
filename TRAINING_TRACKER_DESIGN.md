# Enterprise Learning Portal - Training Tracker
## Complete Architecture & Design Document

---

## 1. EXECUTIVE SUMMARY

**Application Name:** Training Tracker / Enterprise Learning Portal

**Purpose:** A web-based learning management system enabling organizations to deliver, track, and manage employee training across cloud and on-premises environments.

**Key Value Propositions:**
- Centralized training delivery and progress tracking
- Role-based access control for learners, managers, trainers, admins, and support agents
- Secure authentication with optional SSO integration
- AI-ready recommendation engine with rules-based foundation
- Integrated ticket support system
- Comprehensive reporting and compliance tracking
- Multi-deployment model support (cloud, on-prem, hybrid)

**Target Users:** Organizations with 100-10,000+ employees requiring enterprise-grade training management.

**Success Metrics:**
- User adoption rate >80% within first 90 days
- Course completion rate improvement by 30%
- Support ticket resolution <24 hours for 95% of issues
- System uptime >99.5%
- User satisfaction score >4.5/5

---

## 2. APPLICATION OVERVIEW & CORE FEATURES

### 2.1 Core Feature Categories

| Feature Area | Description | Key Components |
|---|---|---|
| **Authentication** | Secure sign-in with optional SSO, MFA, password management | Login, SSO (Azure AD/Okta/Google), MFA, password reset, session management |
| **Courses & Learning** | Course lifecycle management, content delivery, progress tracking | Catalog, enrollment, modules, lessons, quizzes, assignments |
| **Progress Tracking** | Real-time monitoring of user learning journey | Score tracking, completion %, time spent, certificates |
| **Recommendations** | Course suggestions based on role, skills, and compliance | Rules-based engine, future ML-based capability |
| **Support** | Ticket system and live support channels | Ticket creation, status tracking, chat, email integration |
| **Administration** | User, course, and system management | User CRUD, role management, bulk uploads, configuration |
| **Reporting** | Analytics and compliance dashboards | Real-time dashboards, scheduled reports, export (Excel/PDF/CSV) |

### 2.2 Key Characteristics

- **Responsive Design:** Desktop, tablet, mobile support
- **Accessibility:** WCAG 2.1 AA compliance
- **Scalability:** Support 10,000+ concurrent users
- **Security:** HTTPS, encryption, audit logging, OWASP compliance
- **Multi-Language:** Internationalization ready (future phase)
- **Customizable:** Configurable email templates, workflows, branding

---

## 3. USER ROLES & PERMISSION MATRIX

### 3.1 Role Definitions

| Role | Primary Responsibility | Key Permissions |
|---|---|---|
| **Learner** | Complete assigned training, track progress | View assigned/recommended courses, enroll optional courses, submit quizzes, download certs, raise tickets |
| **Trainer/Instructor** | Create and manage course content | Create/edit courses, upload content, view course analytics, grade assignments |
| **Manager** | Monitor team training compliance | View team progress, assign courses, view reports, approve learning plans |
| **Admin** | System-wide configuration and user management | Manage users/roles/departments, manage courses, configure system, view all reports, audit logs |
| **Support Agent** | Resolve user tickets and issues | View/assign/resolve tickets, respond to chat, view user profile, send notifications |

### 3.2 Permission Matrix

```
┌─────────────────┬──────────┬─────────┬────────┬───────┬──────────┐
│ Feature         │ Learner  │ Trainer │Manager │ Admin │ Support  │
├─────────────────┼──────────┼─────────┼────────┼───────┼──────────┤
│ View Courses    │    ✓     │    ✓    │   ✓    │   ✓   │    ✓     │
│ Enroll Courses  │    ✓     │    ✗    │   ✗    │   ✓   │    ✗     │
│ Create Course   │    ✗     │    ✓    │   ✗    │   ✓   │    ✗     │
│ View Progress   │ Own Only │  Dept   │  Team  │  All  │  Own+As  │
│ View Reports    │    ✗     │  Owned  │  Team  │  ALL  │  Tickets │
│ Manage Users    │    ✗     │    ✗    │   ✗    │   ✓   │    ✗     │
│ View Tickets    │ Own      │    ✗    │   ✗    │   ✓   │   ALL    │
│ Create Ticket   │    ✓     │    ✗    │   ✗    │   ✓   │ On behalf│
│ Close Ticket    │    ✗     │    ✗    │   ✗    │   ✓   │    ✓     │
└─────────────────┴──────────┴─────────┴────────┴───────┴──────────┘
```

---

## 4. LOGICAL ARCHITECTURE

### 4.1 Layered Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                         │
│  Web UI (React/Vue) │ Mobile Responsive │ Admin Dashboard    │
└──────────────────────────────────────────────────────────────┘
                              ▲
                              │ HTTPS / WSS
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                        │
│  REST/GraphQL │ Rate Limiting │ Auth Validation │ Logging    │
└──────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                       │
│ ┌─────────────┐ ┌──────────┐ ┌──────────┐ ┌─────────────┐   │
│ │ Auth        │ │ Learning │ │ Progress │ │ Support     │   │
│ │ Service     │ │ Service  │ │ Service  │ │ Service     │   │
│ └─────────────┘ └──────────┘ └──────────┘ └─────────────┘   │
│ ┌─────────────┐ ┌──────────┐ ┌──────────┐ ┌─────────────┐   │
│ │Recommend    │ │Notifi-   │ │ Reporting│ │ Admin       │   │
│ │Service      │ │cation    │ │ Service  │ │ Service     │   │
│ └─────────────┘ └──────────┘ └──────────┘ └─────────────┘   │
└──────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                      DATA ACCESS LAYER                        │
│  ORM (Sequelize/Hibernate) │ Query Builder │ Connection Pool  │
└──────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    DATABASE & STORAGE LAYER                   │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│ │PostgreSQL│ │ Redis    │ │ S3/Blob  │ │File      │         │
│ │MySQL     │ │ Cache    │ │ Storage  │ │ Server   │         │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘         │
└──────────────────────────────────────────────────────────────┘
                              ▲
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
    ┌─────────┐          ┌─────────┐        ┌──────────┐
    │Azure AD/│          │Email    │        │Monitoring│
    │SSO      │          │Service  │        │System    │
    └─────────┘          └─────────┘        └──────────┘
```

### 4.2 Service Components

| Service | Responsibility | Key Functions |
|---|---|---|
| **Authentication Service** | User authentication, session management, MFA | Login, logout, SSO integration, token validation, password reset |
| **Learning Service** | Course and content management | Course CRUD, content upload, module management, enrollment |
| **Progress Service** | Track user learning journey | Record progress, calculate scores, issue certificates |
| **Recommendation Service** | Course suggestions | Rule-based matching, compliance mapping, AI-ready design |
| **Support Service** | Ticket lifecycle management | Create, assign, resolve tickets, chat integration |
| **Notification Service** | Multi-channel communications | Email, in-app alerts, Teams/Slack webhooks |
| **Reporting Service** | Analytics and reporting | Generate dashboards, export reports, compliance tracking |
| **Admin Service** | System configuration | User management, role management, email templates, settings |

---

## 5. CORE FUNCTIONAL MODULES

### 5.1 Module Breakdown

#### A. Authentication & Access Control Module

**Flows:**
- Local login with username/password
- Forgot password workflow
- SSO integration (Azure AD, Okta, Google)
- Multi-factor authentication (email OTP, authenticator app, SMS)
- Session management with JWT or session cookies
- Account lockout after 5 failed attempts
- Password policy enforcement (12+ chars, complexity, history)

**Key Features:**
- Secure password hashing (bcrypt/Argon2)
- Single-use password reset tokens
- Token expiry (15-30 minutes)
- Rate limiting on login attempts
- Comprehensive audit logging

#### B. Course Management Module

**Flows:**
- Create course (admin/trainer)
- Define course structure (modules → lessons)
- Upload course content (videos, documents, PDFs)
- Set course properties (category, difficulty, duration, mandatory/optional)
- Publish/archive courses
- Define completion criteria and prerequisites

**Key Features:**
- Hierarchical course structure
- Content versioning
- Draft and published states
- Metadata management (tags, department, skill level)
- Bulk course upload (CSV/Excel)

#### C. Enrollment & Progress Module

**Flows:**
- Admin assigns courses to users/groups
- Learner enrolls in optional courses
- Learner starts and resumes courses
- Complete lessons, take quizzes, submit assignments
- System tracks completion % and time spent
- Award certificates on completion

**Key Features:**
- Enrollment by user, department, role, or location
- Progress synchronization across devices
- Automatic progress calculation
- Certificate generation and download
- Completion notifications

#### D. Recommendation Engine Module

**Flows:**
- Rules-based recommendations (role, department, compliance)
- Display recommended courses on dashboard
- Show recommendation reason
- Track recommendation acceptance rate
- AI-ready design for future ML integration

**Key Features:**
- Role-based recommendations
- Compliance-required courses
- Prerequisite-based suggestions
- Popular courses ranking
- Manager-assigned learning paths

#### E. Support Ticket Module

**Flows:**
- User creates ticket (in-app form)
- Ticket categorized and assigned to support agent
- Support agent responds and updates status
- Ticket workflow: New → Assigned → In Progress → Pending User → Resolved → Closed
- SLA tracking (Low/Medium/High/Critical)
- Email notifications at each step

**Key Features:**
- Multiple ticket categories
- Priority-based SLA
- Ticket reassignment
- Comment history
- Optional integration with ServiceNow, Jira, Zendesk
- Optional chatbot support (Azure Bot, Dialogflow)

#### F. Reporting & Analytics Module

**Flows:**
- Admin/Manager views dashboards
- Generate reports by user, department, course
- Export to Excel, CSV, PDF
- Schedule automated email reports
- View audit logs

**Key Features:**
- Real-time dashboards
- Historical trend analysis
- Compliance reporting
- SLA performance tracking
- Customizable report templates

#### G. Admin Portal Module

**Flows:**
- Manage users (create, edit, deactivate)
- Assign roles and permissions
- Manage departments and locations
- Configure system settings
- Bulk user import (CSV/Excel)
- Email template management

**Key Features:**
- User CRUD operations
- Role management
- Department management
- Configuration UI
- Audit log viewer

---

## 6. DATABASE SCHEMA DESIGN

### 6.1 Core Tables

#### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  password_hash VARCHAR(255),
  department_id UUID REFERENCES departments(id),
  manager_id UUID REFERENCES users(id),
  status ENUM('active', 'inactive', 'suspended'),
  sso_provider VARCHAR(50),
  sso_id VARCHAR(255),
  mfa_enabled BOOLEAN DEFAULT false,
  mfa_method ENUM('email', 'authenticator', 'sms'),
  last_login TIMESTAMP,
  password_changed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_email (email),
  INDEX idx_department_id (department_id),
  INDEX idx_status (status)
);
```

#### Roles & Permissions
```sql
CREATE TABLE roles (
  id UUID PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE permissions (
  id UUID PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  description TEXT,
  resource VARCHAR(100),
  action VARCHAR(50)
);

CREATE TABLE role_permissions (
  role_id UUID REFERENCES roles(id),
  permission_id UUID REFERENCES permissions(id),
  PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE user_roles (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  role_id UUID REFERENCES roles(id),
  assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id, role_id)
);
```

#### Courses & Content
```sql
CREATE TABLE courses (
  id UUID PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  category_id UUID REFERENCES course_categories(id),
  created_by UUID REFERENCES users(id),
  skill_level ENUM('beginner', 'intermediate', 'advanced'),
  duration_hours INT,
  is_mandatory BOOLEAN DEFAULT false,
  validity_days INT,
  status ENUM('draft', 'published', 'archived'),
  published_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_category_id (category_id),
  INDEX idx_status (status)
);

CREATE TABLE course_modules (
  id UUID PRIMARY KEY,
  course_id UUID REFERENCES courses(id),
  title VARCHAR(255),
  sequence_order INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_course_id (course_id)
);

CREATE TABLE lessons (
  id UUID PRIMARY KEY,
  module_id UUID REFERENCES course_modules(id),
  title VARCHAR(255),
  content_type ENUM('video', 'document', 'quiz', 'assignment'),
  content_url VARCHAR(500),
  duration_minutes INT,
  sequence_order INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_module_id (module_id)
);

CREATE TABLE quizzes (
  id UUID PRIMARY KEY,
  lesson_id UUID REFERENCES lessons(id),
  title VARCHAR(255),
  passing_score INT,
  max_attempts INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE quiz_questions (
  id UUID PRIMARY KEY,
  quiz_id UUID REFERENCES quizzes(id),
  question_text TEXT,
  question_type ENUM('multiple_choice', 'true_false', 'short_answer'),
  sequence_order INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Enrollment & Progress
```sql
CREATE TABLE course_assignments (
  id UUID PRIMARY KEY,
  course_id UUID REFERENCES courses(id),
  user_id UUID REFERENCES users(id),
  assigned_by UUID REFERENCES users(id),
  due_date DATE,
  assignment_type ENUM('assigned', 'optional'),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(course_id, user_id)
);

CREATE TABLE user_progress (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  course_id UUID REFERENCES courses(id),
  status ENUM('not_started', 'in_progress', 'completed'),
  start_date TIMESTAMP,
  completion_date TIMESTAMP,
  last_accessed TIMESTAMP,
  completion_percentage INT DEFAULT 0,
  total_time_minutes INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE(user_id, course_id),
  INDEX idx_user_id (user_id),
  INDEX idx_status (status)
);

CREATE TABLE lesson_progress (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  lesson_id UUID REFERENCES lessons(id),
  status ENUM('not_started', 'in_progress', 'completed'),
  completion_date TIMESTAMP,
  time_spent_minutes INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id, lesson_id)
);

CREATE TABLE quiz_attempts (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  quiz_id UUID REFERENCES quizzes(id),
  score INT,
  passed BOOLEAN,
  attempt_number INT,
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_user_id (user_id),
  INDEX idx_quiz_id (quiz_id)
);
```

#### Certificates
```sql
CREATE TABLE certificates (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  course_id UUID REFERENCES courses(id),
  issued_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expiry_date DATE,
  certificate_number VARCHAR(100) UNIQUE,
  certificate_url VARCHAR(500),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE(user_id, course_id),
  INDEX idx_user_id (user_id)
);
```

#### Recommendations
```sql
CREATE TABLE recommendations (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  course_id UUID REFERENCES courses(id),
  reason VARCHAR(255),
  recommendation_type ENUM('role_based', 'compliance', 'skill_gap', 'popular'),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  dismissed_at TIMESTAMP,
  
  INDEX idx_user_id (user_id)
);
```

#### Support Tickets
```sql
CREATE TABLE tickets (
  id UUID PRIMARY KEY,
  ticket_number VARCHAR(20) UNIQUE,
  user_id UUID REFERENCES users(id),
  assigned_to UUID REFERENCES users(id),
  category VARCHAR(100),
  subject VARCHAR(255),
  description TEXT,
  status ENUM('new', 'assigned', 'in_progress', 'pending_user', 'resolved', 'closed'),
  priority ENUM('low', 'medium', 'high', 'critical'),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  resolved_at TIMESTAMP,
  closed_at TIMESTAMP,
  
  INDEX idx_user_id (user_id),
  INDEX idx_status (status),
  INDEX idx_priority (priority)
);

CREATE TABLE ticket_comments (
  id UUID PRIMARY KEY,
  ticket_id UUID REFERENCES tickets(id),
  commented_by UUID REFERENCES users(id),
  comment_text TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Audit & Security
```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  action VARCHAR(100),
  entity_type VARCHAR(100),
  entity_id VARCHAR(100),
  old_values JSONB,
  new_values JSONB,
  ip_address VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_user_id (user_id),
  INDEX idx_created_at (created_at)
);

CREATE TABLE password_reset_tokens (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  token VARCHAR(500) UNIQUE NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  used_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_user_id (user_id),
  INDEX idx_expires_at (expires_at)
);

CREATE TABLE login_history (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  logout_time TIMESTAMP,
  ip_address VARCHAR(50),
  user_agent VARCHAR(500),
  session_id VARCHAR(255),
  status ENUM('success', 'failed_password', 'locked'),
  
  INDEX idx_user_id (user_id),
  INDEX idx_login_time (login_time)
);

CREATE TABLE notifications (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  type VARCHAR(50),
  title VARCHAR(255),
  message TEXT,
  read_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_user_id (user_id),
  INDEX idx_created_at (created_at)
);
```

#### Additional Tables
```sql
CREATE TABLE departments (
  id UUID PRIMARY KEY,
  name VARCHAR(100) UNIQUE,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE course_categories (
  id UUID PRIMARY KEY,
  name VARCHAR(100) UNIQUE,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE email_templates (
  id UUID PRIMARY KEY,
  name VARCHAR(100) UNIQUE,
  subject VARCHAR(255),
  body TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 7. API DESIGN (REST Endpoints)

### 7.1 Authentication APIs

```
POST /api/v1/auth/login
  Request: { username, password }
  Response: { token, user, roles }
  Auth: None | Rate Limited (5 req/min)

POST /api/v1/auth/logout
  Request: {}
  Response: { success }
  Auth: JWT Required

POST /api/v1/auth/forgot-password
  Request: { email }
  Response: { message: "Password reset link sent (if account exists)" }
  Auth: None | Rate Limited (3 req/hour)

POST /api/v1/auth/reset-password
  Request: { token, new_password, confirm_password }
  Response: { success }
  Auth: None

POST /api/v1/auth/change-password
  Request: { current_password, new_password, confirm_password }
  Response: { success }
  Auth: JWT Required | User Role

POST /api/v1/auth/enable-mfa
  Request: { mfa_method }
  Response: { secret, qr_code }
  Auth: JWT Required

POST /api/v1/auth/verify-mfa
  Request: { code }
  Response: { token, user }
  Auth: Partial JWT (MFA pending)
```

### 7.2 Course APIs

```
GET /api/v1/courses
  Query: { category, skill_level, status, page, limit }
  Response: { courses[], total, page }
  Auth: JWT Required

GET /api/v1/courses/:id
  Response: { course_details, modules[], prerequisites }
  Auth: JWT Required

POST /api/v1/courses
  Request: { title, description, category_id, skill_level, duration_hours }
  Response: { course_id, message }
  Auth: JWT Required | Trainer/Admin Role

PUT /api/v1/courses/:id
  Request: { title, description, ... }
  Response: { success, updated_course }
  Auth: JWT Required | Trainer/Admin Role (owner)

DELETE /api/v1/courses/:id
  Response: { success }
  Auth: JWT Required | Admin Role

POST /api/v1/courses/:id/publish
  Request: {}
  Response: { success, published_at }
  Auth: JWT Required | Trainer/Admin Role

POST /api/v1/courses/:id/modules
  Request: { title, sequence_order }
  Response: { module_id }
  Auth: JWT Required | Trainer/Admin Role

POST /api/v1/modules/:id/lessons
  Request: { title, content_type, content_url, duration_minutes }
  Response: { lesson_id }
  Auth: JWT Required | Trainer/Admin Role

GET /api/v1/courses/:id/students
  Response: { students[], completion_rates }
  Auth: JWT Required | Trainer/Admin Role
```

### 7.3 Enrollment & Progress APIs

```
POST /api/v1/courses/:id/enroll
  Request: {}
  Response: { success, enrollment_id }
  Auth: JWT Required | Learner Role

GET /api/v1/my/courses
  Query: { status, page, limit }
  Response: { courses[], progress_data[] }
  Auth: JWT Required | Learner Role

GET /api/v1/my/progress/:course_id
  Response: { course_info, modules[], progress%, time_spent, certificates }
  Auth: JWT Required | Learner Role

POST /api/v1/lessons/:id/start
  Request: {}
  Response: { success, session_id }
  Auth: JWT Required | Learner Role

POST /api/v1/lessons/:id/complete
  Request: { time_spent_minutes }
  Response: { success, next_lesson_id }
  Auth: JWT Required | Learner Role

POST /api/v1/quizzes/:id/attempt
  Request: { answers[] }
  Response: { score, passed, certificate_issued }
  Auth: JWT Required | Learner Role

GET /api/v1/my/certificates
  Response: { certificates[] }
  Auth: JWT Required | Learner Role

POST /api/v1/courses/:id/assign
  Request: { user_ids[], due_date }
  Response: { success, assigned_count }
  Auth: JWT Required | Manager/Admin Role
```

### 7.4 Recommendation APIs

```
GET /api/v1/recommendations
  Query: { limit, recommendation_type }
  Response: { recommendations[], reasons[] }
  Auth: JWT Required | Learner Role

POST /api/v1/recommendations/:id/dismiss
  Request: {}
  Response: { success }
  Auth: JWT Required | Learner Role
```

### 7.5 Ticket APIs

```
POST /api/v1/tickets
  Request: { category, subject, description }
  Response: { ticket_id, ticket_number, status }
  Auth: JWT Required | Learner Role
  Rate Limit: 5 tickets/day per user

GET /api/v1/my/tickets
  Query: { status, page, limit }
  Response: { tickets[], total }
  Auth: JWT Required | Learner Role

GET /api/v1/tickets/:id
  Response: { ticket, comments[], attachments }
  Auth: JWT Required | Owner/Support/Admin

POST /api/v1/tickets/:id/comments
  Request: { comment_text }
  Response: { comment_id, created_at }
  Auth: JWT Required | Owner/Support/Admin

PUT /api/v1/tickets/:id/status
  Request: { status }
  Response: { success, updated_at }
  Auth: JWT Required | Support/Admin Role

GET /api/v1/tickets
  Query: { status, priority, assigned_to, page }
  Response: { tickets[], sla_compliance }
  Auth: JWT Required | Support/Admin Role
```

### 7.6 Admin APIs

```
GET /api/v1/admin/users
  Query: { role, status, department, page }
  Response: { users[], total }
  Auth: JWT Required | Admin Role

POST /api/v1/admin/users
  Request: { username, email, first_name, last_name, department_id, role_id }
  Response: { user_id }
  Auth: JWT Required | Admin Role

PUT /api/v1/admin/users/:id
  Request: { email, department_id, status }
  Response: { success }
  Auth: JWT Required | Admin Role

POST /api/v1/admin/users/bulk-import
  Request: FormData { csv_file }
  Response: { imported_count, failed_count, errors[] }
  Auth: JWT Required | Admin Role

GET /api/v1/admin/audit-logs
  Query: { user_id, action, entity_type, date_from, date_to }
  Response: { logs[], total }
  Auth: JWT Required | Admin Role

POST /api/v1/admin/email-templates
  Request: { name, subject, body }
  Response: { template_id }
  Auth: JWT Required | Admin Role

GET /api/v1/admin/settings
  Response: { password_policy, mfa_required, session_timeout }
  Auth: JWT Required | Admin Role

PUT /api/v1/admin/settings
  Request: { key, value }
  Response: { success }
  Auth: JWT Required | Admin Role
```

### 7.7 Reporting APIs

```
GET /api/v1/reports/dashboard
  Response: { total_users, active_learners, completion_rate, overdue_count }
  Auth: JWT Required | Manager/Admin Role

GET /api/v1/reports/completion-by-course
  Query: { department, date_from, date_to }
  Response: { course_data[], trends }
  Auth: JWT Required | Manager/Admin Role

GET /api/v1/reports/user-progress
  Query: { user_id, department }
  Response: { user_courses[], completion_data }
  Auth: JWT Required | Manager/Admin Role (own team)

POST /api/v1/reports/export
  Request: { report_type, format, filters }
  Response: { file_url }
  Auth: JWT Required | Manager/Admin Role
```

---

(Document continues in next section...)
