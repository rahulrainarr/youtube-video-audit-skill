# Training Tracker - Workflows & Security
## Authentication, Password Management, Ticket Support, and Recommendation Flows

---

## 1. AUTHENTICATION & LOGIN WORKFLOW

### 1.1 Local Username/Password Login

```
User                              Application                    Backend
  │                                 │                               │
  ├─ Enters credentials ────────────>│                               │
  │                                 │                               │
  │                                 ├─ Validate input format ──────>│
  │                                 │                               │
  │                                 │<─ Input valid ────────────────┤
  │                                 │                               │
  │                                 ├─ Query user by username ─────>│
  │                                 │                               │
  │                                 │<─ User found? ────────────────┤
  │                                 │    (NO)                       │
  │                                 │                               │
  │                                 ├─ Check failed login count ───>│
  │                                 │                               │
  │                                 │<─ Account locked? ────────────┤
  │                                 │    (YES - increment counter)  │
  │                                 │                               │
  │<─ Invalid credentials ──────────┤ Lock after 5 attempts       │
  │   Error message                 │ Lock duration: 30 minutes     │
  │                                 │                               │
  │ (User found, not locked)        │                               │
  │                                 ├─ Verify password ────────────>│
  │                                 │  (bcrypt.compare)             │
  │                                 │                               │
  │                                 │<─ Password valid? ────────────┤
  │                                 │    (YES)                      │
  │                                 │                               │
  │                                 ├─ Check MFA enabled ─────────>│
  │                                 │                               │
  │                                 │<─ MFA required? ──────────────┤
  │                                 │    (NO)                       │
  │                                 │                               │
  │                                 ├─ Clear failed login count ───>│
  │                                 │                               │
  │                                 ├─ Create JWT/Session ────────>│
  │                                 │  - Payload: user_id, roles    │
  │                                 │  - Expiry: 24 hours           │
  │                                 │                               │
  │                                 ├─ Log login event ────────────>│
  │                                 │  (audit_logs table)           │
  │                                 │                               │
  │<─ JWT Token + User Info ────────┤ Set Secure HttpOnly Cookie   │
  │   Redirect to dashboard         │                               │
  │                                 │                               │
```

### 1.2 SSO Integration (Azure AD / OAuth2)

```
User                    Application                 Azure AD / SSO Provider
  │                        │                              │
  ├─ Click "Sign in ─────────>│                              │
  │   with Azure AD"         │                              │
  │                          ├─ Redirect to ─────────────────>│
  │                          │  Azure AD login               │
  │                          │  (with client_id, redirect_uri)
  │                          │                              │
  │<─ Redirect to Azure AD ──┤                              │
  │  login page              │                              │
  │                          │                              │
  ├─ Authenticate on ──────────────────────────────────────>│
  │   Azure AD (2FA if set)  │                              │
  │                          │                              │
  │<──────────────────────────────── Auth code ────────────┤
  │  Redirects with auth code
  │                          │
  │                          ├─ Exchange code for token ──>│
  │                          │  (backend to backend)        │
  │                          │  client_id + secret          │
  │                          │                              │
  │                          │<─ Access Token + ID Token ──┤
  │                          │                              │
  │                          ├─ Get user info ────────────>│
  │                          │  (claims: email, name, etc.)
  │                          │                              │
  │                          │<─ User claims ───────────────┤
  │                          │                              │
  │                          ├─ Find/Create user ────────────┤
  │                          │  Match by email or SSO ID    │
  │                          │  Mark as SSO authenticated   │
  │                          │                              │
  │                          ├─ Create app JWT ────────────┤
  │                          │  Expiry: 24 hours            │
  │                          │                              │
  │<─ JWT Token + Redirect ──┤                              │
  │   to dashboard           │                              │
  │                          │                              │
```

### 1.3 Multi-Factor Authentication (MFA)

```
Step 1: After valid username/password
User                    Application                    Backend
  │                        │                              │
  │<─ Show MFA method ─────┤                              │
  │   options              │                              │
  │   [Email OTP]          │                              │
  │   [Authenticator]      │                              │
  │   [SMS OTP]            │                              │
  │                        │                              │
  ├─ Select method ────────>│                              │
  │   (e.g., Email OTP)    │                              │
  │                        ├─ Generate 6-digit OTP ─────>│
  │                        │  Expiry: 10 minutes          │
  │                        │                              │
  │                        ├─ Send via email ────────────>│
  │                        │  (SendGrid, AWS SES, etc.)   │
  │                        │                              │
  │<─ Enter OTP code ──────┤                              │
  │   from email           │                              │
  │                        │                              │
  │                        ├─ Validate OTP ──────────────>│
  │                        │  Check: exists, not expired  │
  │                        │                              │
  │                        │<─ OTP valid? ────────────────┤
  │                        │    (YES)                     │
  │                        │                              │
  │                        ├─ Mark OTP as used ─────────>│
  │                        │  (used_at = now)             │
  │                        │                              │
  │                        ├─ Create final JWT ─────────>│
  │                        │  Full access token           │
  │                        │                              │
  │<─ JWT Token ──────────┤                              │
  │   Redirect to dashboard
  │                        │                              │
```

---

## 2. PASSWORD RESET & CHANGE WORKFLOWS

### 2.1 Forgot Password Workflow

```
User                    Application                    Backend (Email Service)
  │                        │                              │
  ├─ Click "Forgot ───────>│                              │
  │   Password"            │                              │
  │                        │                              │
  │<─ Enter email form ────┤                              │
  │                        │                              │
  ├─ Enter registered ────>│                              │
  │   email                │ ├─ Input validation ────────>│
  │                        │ │  - Format check            │
  │                        │ │  - Rate limiting           │
  │                        │ │  (3 requests/hour/IP)      │
  │                        │ │                            │
  │                        │ ├─ Query user by email ─────>│
  │                        │ │                            │
  │                        │ │<─ User found? ────────────┤
  │                        │ │                            │
  │                        │ ├─ Generate reset token ───>│
  │                        │ │  - 32-byte random string   │
  │                        │ │  - Hash with SHA256        │
  │                        │ │  - Expiry: 30 minutes      │
  │                        │ │                            │
  │                        │ ├─ Store in DB ────────────>│
  │                        │ │  (password_reset_tokens)   │
  │                        │ │                            │
  │                        │ ├─ Send email ─────────────>│
  │                        │ │  Reset URL with token      │
  │                        │ │  Token in link or form     │
  │                        │ │                            │
  │<─ Generic message: ───┤                              │
  │   "If the email exists"│                              │
  │   "we sent a link"     │                              │
  │   (Safe response:      │                              │
  │    No user enumeration)│                              │
  │                        │                              │
  │ User clicks link in ───>│                              │
  │ email or opens reset   │                              │
  │ form with token        │                              │
  │                        │                              │
  ├─ Submits new ────────>│                              │
  │   password             │ ├─ Validate token ────────────>│
  │                        │ │  - Exists in DB?            │
  │                        │ │  - Not expired?             │
  │                        │ │  - Not already used?        │
  │                        │ │                            │
  │                        │ │<─ Token valid? ────────────┤
  │                        │ │    (YES)                   │
  │                        │ │                            │
  │                        │ ├─ Validate password ──────>│
  │                        │ │  - 12+ characters          │
  │                        │ │  - Uppercase, lowercase    │
  │                        │ │  - Number, special char    │
  │                        │ │  - Not in previous 5       │
  │                        │ │                            │
  │                        │ │<─ Password valid? ────────┤
  │                        │ │    (YES)                   │
  │                        │ │                            │
  │                        │ ├─ Hash new password ──────>│
  │                        │ │  (bcrypt, cost=12)         │
  │                        │ │                            │
  │                        │ ├─ Update user record ─────>│
  │                        │ │  - Set password_hash       │
  │                        │ │  - password_changed_at     │
  │                        │ │  - Invalidate old tokens   │
  │                        │ │                            │
  │                        │ ├─ Mark token as used ─────>│
  │                        │ │  (used_at = now)           │
  │                        │ │                            │
  │                        │ ├─ Send confirmation ──────>│
  │                        │ │  email (security alert)    │
  │                        │ │                            │
  │                        │ ├─ Log action ─────────────>│
  │                        │ │  (audit_logs table)        │
  │                        │ │                            │
  │<─ Success message ────┤                              │
  │   "Password reset"    │                              │
  │   "Sign in again"     │                              │
  │                        │                              │
  ├─ Redirect to login ───>│                              │
  │                        │                              │
```

### 2.2 Change Password (Logged-In User)

```
User                    Application                    Backend
  │                        │                              │
  ├─ Navigate to ────────>│                              │
  │   Settings/Account    │                              │
  │                        │                              │
  │<─ Change password ────┤                              │
  │   form                 │                              │
  │   [Current Password]   │                              │
  │   [New Password]       │                              │
  │   [Confirm Password]   │                              │
  │                        │                              │
  ├─ Fill and submit ────>│                              │
  │   form                 │ ├─ Validate JWT ────────────>│
  │                        │ │  (User authenticated?)     │
  │                        │ │                            │
  │                        │ │<─ JWT valid? ─────────────┤
  │                        │ │    (YES)                   │
  │                        │ │                            │
  │                        │ ├─ Input validation ────────>│
  │                        │ │  - Field lengths           │
  │                        │ │  - Passwords match         │
  │                        │ │                            │
  │                        │ │<─ Input valid? ───────────┤
  │                        │ │    (YES)                   │
  │                        │ │                            │
  │                        │ ├─ Fetch user from DB ─────>│
  │                        │ │  (Use user_id from JWT)    │
  │                        │ │                            │
  │                        │ ├─ Verify current password ─>│
  │                        │ │  (bcrypt.compare)          │
  │                        │ │                            │
  │                        │ │<─ Password correct? ──────┤
  │                        │ │    (YES)                   │
  │                        │ │                            │
  │                        │ ├─ Validate new password ───>│
  │                        │ │  - 12+ characters          │
  │                        │ │  - Complexity rules        │
  │                        │ │  - Not in history (last 5) │
  │                        │ │  - Different from current  │
  │                        │ │                            │
  │                        │ │<─ New password valid? ────┤
  │                        │ │    (YES)                   │
  │                        │ │                            │
  │                        │ ├─ Hash new password ──────>│
  │                        │ │  (bcrypt, cost=12)         │
  │                        │ │                            │
  │                        │ ├─ Store old password hash ─>│
  │                        │ │  (password history table)   │
  │                        │ │  Keep last 5 hashes        │
  │                        │ │                            │
  │                        │ ├─ Update user record ─────>│
  │                        │ │  - password_hash           │
  │                        │ │  - password_changed_at     │
  │                        │ │  - Invalidate all sessions │
  │                        │ │  (force re-login)          │
  │                        │ │                            │
  │                        │ ├─ Send notification ──────>│
  │                        │ │  email (security alert)    │
  │                        │ │                            │
  │                        │ ├─ Log action ─────────────>│
  │                        │ │  (audit_logs table)        │
  │                        │ │                            │
  │<─ Success message ────┤                              │
  │   "Password changed"  │                              │
  │   "Re-login required" │                              │
  │                        │                              │
  ├─ Logout and login ───>│                              │
  │   with new password   │                              │
  │                        │                              │
```

### 2.3 Password Policy Requirements

| Rule | Details |
|---|---|
| **Length** | Minimum 12 characters |
| **Complexity** | Must contain: uppercase (A-Z), lowercase (a-z), number (0-9), special char (!@#$%^&*) |
| **History** | Cannot reuse last 5 passwords |
| **Expiry** | Configurable by admin (optional, default: no expiry) |
| **Format** | No repeating characters (e.g., "aaa"), no sequential (e.g., "abc", "123") |
| **Not Allow** | Username in password, dictionary words |

---

## 3. SUPPORT TICKET WORKFLOW

### 3.1 Ticket Lifecycle

```
┌──────────────────────────────────────────────────────────────┐
│                      TICKET LIFECYCLE                         │
└──────────────────────────────────────────────────────────────┘

  User Creates                Support Reviews            Support Resolves
  Ticket                       & Assigns                  & Closes
    │                               │                          │
    ▼                               ▼                          ▼
┌─────────┐    ┌─────────┐    ┌──────────┐    ┌────────┐   ┌────────┐
│   NEW   │───>│ ASSIGNED│───>│IN PROGRESS│───>│ PENDING│──>│RESOLVED│
└─────────┘    └─────────┘    └──────────┘    │ USER   │   └────────┘
                                              └────────┘        │
                                                  ▲             │
                                                  │             │
                                                  └─────────────┘
                                                   (User responds)
                                                        │
                                                        ▼
                                                   ┌────────┐
                                                   │ CLOSED │
                                                   └────────┘

SLA Tracking by Priority:
  ├─ CRITICAL:  Response in 1 hour,   Resolution in 4 hours
  ├─ HIGH:      Response in 2 hours,  Resolution in 8 hours
  ├─ MEDIUM:    Response in 4 hours,  Resolution in 24 hours
  └─ LOW:       Response in 8 hours,  Resolution in 48 hours
```

### 3.2 Ticket Creation Flow

```
User                         Application                    Backend
  │                             │                              │
  ├─ Navigate to ───────────────>│                              │
  │   Support/Tickets            │                              │
  │                              │                              │
  │<─ Create ticket form ────────┤                              │
  │   [Category dropdown]        │                              │
  │   [Subject field]            │                              │
  │   [Description]              │                              │
  │   [Attachments optional]     │                              │
  │   [Priority auto-set]        │                              │
  │                              │                              │
  ├─ Fill form and submit ──────>│                              │
  │                              ├─ Validate input ───────────>│
  │                              │  - Required fields          │
  │                              │  - Subject length           │
  │                              │  - Description length       │
  │                              │  - File size limits         │
  │                              │                            │
  │                              │<─ Input valid? ─────────────┤
  │                              │    (YES)                    │
  │                              │                            │
  │                              ├─ Generate ticket number ───>│
  │                              │  Format: TKT-YYYY-000001    │
  │                              │                            │
  │                              ├─ Create ticket record ─────>│
  │                              │  - ticket_id (UUID)         │
  │                              │  - user_id (from JWT)       │
  │                              │  - status: 'new'            │
  │                              │  - created_at: now()        │
  │                              │                            │
  │                              ├─ Store attachments ────────>│
  │                              │  Cloud storage (S3/Blob)    │
  │                              │                            │
  │                              ├─ Send notification ────────>│
  │                              │  Email to user:             │
  │                              │  "Ticket created"           │
  │                              │  Ticket number              │
  │                              │  Tracking link              │
  │                              │                            │
  │                              ├─ Notify support team ──────>│
  │                              │  Internal notification      │
  │                              │  (Teams/Slack webhook)      │
  │                              │                            │
  │                              ├─ Log action ──────────────>│
  │                              │  (audit_logs table)         │
  │                              │                            │
  │                              ├─ Rate limit check ────────>│
  │                              │  (5 tickets/day per user)   │
  │                              │  Update counter             │
  │                              │                            │
  │<─ Success message ───────────┤                              │
  │   Ticket number: TKT-2026-001│                              │
  │   Track your ticket: [link]  │                              │
  │                              │                              │
  ├─ Redirect to ticket ────────>│                              │
  │   detail page                │                              │
  │                              │                              │
```

### 3.3 Ticket Assignment & Resolution Flow

```
Support Agent                Application                    Backend
  │                            │                              │
  ├─ View pending tickets ────>│                              │
  │   (status = 'new')        │                              │
  │                            │                              │
  │<─ Ticket list ────────────┤                              │
  │   Sorted by:               │                              │
  │   - Priority (desc)        │                              │
  │   - Created time (asc)     │                              │
  │   - SLA risk (asc)         │                              │
  │                            │                              │
  ├─ Select ticket ───────────>│                              │
  │                            ├─ Fetch ticket details ─────>│
  │                            │                            │
  │                            │<─ Full ticket data ────────┤
  │                            │                            │
  │<─ Ticket detail view ─────┤                              │
  │   [Category]               │                              │
  │   [Subject]                │                              │
  │   [Description]            │                              │
  │   [SLA info]               │                              │
  │   [Comments section]       │                              │
  │   [Assign button]          │                              │
  │   [Status dropdown]        │                              │
  │   [Response box]           │                              │
  │                            │                              │
  ├─ Click "Assign to me" ───>│                              │
  │                            ├─ Update ticket ────────────>│
  │                            │  - assigned_to: agent_id    │
  │                            │  - status: 'assigned'       │
  │                            │  - assigned_at: now()       │
  │                            │                            │
  │                            ├─ Send notification ────────>│
  │                            │  Email to user:             │
  │                            │  "Ticket assigned"          │
  │                            │  Agent name                 │
  │                            │                            │
  │                            ├─ Log action ──────────────>│
  │                            │  (audit_logs)               │
  │                            │                            │
  ├─ Type response ───────────>│                              │
  │                            ├─ Validate comment ────────>│
  │                            │  - Non-empty               │
  │                            │  - Max 5000 chars          │
  │                            │                            │
  │                            │<─ Valid? ─────────────────┤
  │                            │    (YES)                   │
  │                            │                            │
  │                            ├─ Create comment record ───>│
  │                            │  - ticket_id               │
  │                            │  - commented_by (agent)    │
  │                            │  - comment_text            │
  │                            │  - created_at: now()       │
  │                            │                            │
  ├─ Change status ───────────>│                              │
  │   to "In Progress"         │                              │
  │                            ├─ Update status ───────────>│
  │                            │  - status: 'in_progress'   │
  │                            │                            │
  │                            ├─ Send notification ────────>│
  │                            │  Email to user:             │
  │                            │  "We're working on it"     │
  │                            │                            │
  │ (Agent resolves issue)     │                              │
  │                            │                              │
  ├─ Change status ───────────>│                              │
  │   to "Pending User"        │                              │
  │   (awaiting feedback)      │                              │
  │                            ├─ Update status ───────────>│
  │                            │  - status: 'pending_user'  │
  │                            │                            │
  │                            ├─ Set reminder ────────────>│
  │                            │  Auto-close after 7 days   │
  │                            │  if no response             │
  │                            │                            │
  │ (User confirms resolution) │                              │
  │                            │                              │
  │                            ├─ Send notification ────────>│
  │                            │  Email to user:             │
  │                            │  "Please confirm resolution"
  │                            │  Rating & feedback form     │
  │                            │                            │
  ├─ Final comment + ────────>│                              │
  │   Change status            │                              │
  │   to "Resolved"            │                              │
  │                            ├─ Update status ───────────>│
  │                            │  - status: 'resolved'      │
  │                            │  - resolved_at: now()      │
  │                            │  - resolution_time (mins)  │
  │                            │                            │
  │                            ├─ Send notification ────────>│
  │                            │  Confirmation email         │
  │                            │  Survey/feedback link      │
  │                            │                            │
  │                            ├─ Calculate SLA ───────────>│
  │                            │  Met? Yes/No               │
  │                            │  Response time vs SLA      │
  │                            │  Resolution time vs SLA    │
  │                            │                            │
  │                            ├─ Log action ──────────────>│
  │                            │  (audit_logs)              │
  │                            │                            │
  │<─ Confirmation ───────────┤                              │
  │   "Ticket resolved"       │                              │
  │                            │                              │
  ├─ Manual close (admin) ───>│                              │
  │   after 7 days or         │                              │
  │   manually click "Close"   │                              │
  │                            ├─ Update status ───────────>│
  │                            │  - status: 'closed'        │
  │                            │  - closed_at: now()        │
  │                            │                            │
  │                            ├─ Final notification ──────>│
  │                            │  Ticket closed              │
  │                            │  Reference number          │
  │                            │                            │
  │                            ├─ Log action ──────────────>│
  │                            │  (audit_logs)              │
  │                            │                            │
```

---

## 4. RECOMMENDATION ENGINE WORKFLOW

### 4.1 Rules-Based Recommendation Logic

```
User Profile                    Recommendation Engine              Recommendations
                                                                  Output
    │
    ├─ Role ID  ────────────┐
    │                       │
    ├─ Department ID ───────┤
    │                       ├──> [Rule Engine] ──────> [Scored Courses]
    ├─ Completed ───────────┤
    │   Courses             ├──> [Filter]  ────────> [Top 5-10]
    │                       │
    └─ Skill Level ────────┘
                            ├──> [Ranking by Score]
                            │
                            └──> [Add Reason Text]


RULES APPLIED:

1. MANDATORY COMPLIANCE RULES
   IF role = "Manager" AND department = "Finance"
   THEN recommend "Compliance & Ethics" (High Priority)
   Reason: "Mandatory for Finance role"

2. ROLE-BASED RECOMMENDATIONS
   IF role = "Project Manager"
   AND completed_courses.includes("Agile Basics")
   THEN recommend "Advanced Agile", "Risk Management"
   Reason: "Recommended for Project Manager role"

3. SKILL GAP RECOMMENDATIONS
   IF (skill_level < 3) AND
   (role_requirements.includes(skill))
   THEN recommend "skill_course"
   Reason: "Recommended to develop skills for your role"

4. PREREQUISITE-BASED
   IF course.prerequisites.all_completed_by(user)
   THEN recommend course
   Reason: "Recommended because you completed prerequisites"

5. POPULAR COURSES
   IF course.completion_rate > 80%
   AND NOT user.completed(course)
   THEN recommend_low_priority
   Reason: "Popular course in your organization"

6. DEPARTMENT LEARNING PATH
   IF manager_assigned_path.includes(course)
   THEN recommend_high_priority
   Reason: "Recommended by your manager"
```

### 4.2 Recommendation Display & Dismissal

```
User Dashboard                   Application                    Backend
  │                                │                              │
  ├─ View dashboard ──────────────>│                              │
  │                                ├─ Fetch recommendations ────>│
  │                                │  Query: SELECT * FROM        │
  │                                │  recommendations             │
  │                                │  WHERE user_id = ?           │
  │                                │  AND dismissed_at IS NULL    │
  │                                │  ORDER BY score DESC         │
  │                                │  LIMIT 10                    │
  │                                │                             │
  │                                │<─ Recommendations list ──────┤
  │                                │                             │
  │<─ Recommendations shown ───────┤                              │
  │   Card 1: "Cloud Fundamentals" │                              │
  │     Reason: Recommended for    │                              │
  │     your Project Manager role  │                              │
  │     [Enroll] [Dismiss]         │                              │
  │                                │                              │
  │   Card 2: "AWS Security"       │                              │
  │     Reason: Mandatory for your │                              │
  │     department                 │                              │
  │     [Enroll] [Dismiss]         │                              │
  │                                │                              │
  ├─ Click [Enroll] ──────────────>│                              │
  │                                ├─ Create enrollment ────────>│
  │                                │  (course_assignments)        │
  │                                │                             │
  │                                ├─ Create progress record ───>│
  │                                │  status = 'not_started'      │
  │                                │                             │
  │                                ├─ Send notification ────────>│
  │                                │  "Enrolled in Cloud Fund"   │
  │                                │                             │
  │<─ Enrolled success ────────────┤                              │
  │                                │                              │
  ├─ Click [Dismiss] ─────────────>│                              │
  │                                ├─ Update recommendation ────>│
  │                                │  dismissed_at = now()        │
  │                                │                             │
  │                                ├─ Log action ──────────────>│
  │                                │  (audit_logs)               │
  │                                │                             │
  │<─ Card removed from display ──┤                              │
  │                                │                              │
```

---

## 5. SECURITY ARCHITECTURE

### 5.1 Authentication & Authorization

| Component | Technology | Details |
|---|---|---|
| **Password Storage** | bcrypt | Cost factor: 12, salt auto-generated |
| **Session Management** | JWT or Secure Cookies | JWT: 24-hour expiry, refresh tokens for 30 days |
| **MFA** | Email OTP, Authenticator, SMS | 10-minute OTP expiry, rate-limited to 3 attempts |
| **SSO** | OAuth2 / OpenID Connect | Azure AD, Okta, Google Workspace support |
| **Token Storage** | HttpOnly Secure Cookies | No localStorage (XSS protection) |
| **CORS** | Whitelist trusted origins | Credentials: include |
| **CSRF Protection** | SameSite=Strict + CSRF tokens | For state-changing operations |

### 5.2 API Security

| Layer | Mechanism | Details |
|---|---|---|
| **Transport** | HTTPS/TLS 1.3 | All communications encrypted |
| **Authentication** | Bearer JWT | Every request must include valid JWT |
| **Authorization** | Role-Based Access Control | Middleware checks user roles before processing |
| **Rate Limiting** | Token bucket algorithm | Login: 5 attempts/min, API: 100 req/min per user |
| **Input Validation** | Schema validation | ZOD or JOI for request body validation |
| **SQL Injection** | Parameterized queries | ORM + prepared statements, no raw SQL |
| **XSS Protection** | HTML sanitization | DOMPurify on user input, CSP headers |
| **IDOR Prevention** | Resource ownership check | Verify user_id from JWT matches resource |

### 5.3 Data Protection

| Aspect | Approach | Details |
|---|---|---|
| **Encryption at Rest** | AES-256 | Database encryption, file storage encryption |
| **Encryption in Transit** | TLS 1.3 | All data over HTTPS/WSS |
| **PII Handling** | Encryption + minimal storage | Only store necessary PII, encrypt phone/SSN |
| **Audit Logging** | Immutable logs | All user actions logged, cannot be modified |
| **Backup** | Encrypted backups | Daily incremental, weekly full backups |
| **Secrets Management** | Vault (HashiCorp/Azure Key Vault) | API keys, DB passwords, encryption keys |

### 5.4 Compliance & Privacy

| Standard | Implementation |
|---|---|
| **GDPR** | Data minimization, user consent, right to deletion, data export |
| **CCPA** | User data access, deletion, opt-out mechanisms |
| **HIPAA** | (If healthcare data) Audit logs, encryption, access control |
| **SOC 2** | Logging, monitoring, incident response, access reviews |
| **PCI DSS** | (If storing payments) Tokenization, no plain card storage |

---

(Continues with UI/UX flows in next section...)
