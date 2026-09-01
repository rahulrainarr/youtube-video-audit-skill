# 📊 Metrics Reference Guide

## Overview

The Resume Analyzer uses **10 industry-standard metrics** weighted to evaluate Sales & Business Development candidates. Total weight = 100%.

---

## Metric Details & Scoring

### 1️⃣ Sales Revenue Generation (15% weight)

**Category:** Experience
**Description:** Demonstrated ability to generate revenue and close deals

**Scoring Criteria:**
| Experience | Points |
|-----------|--------|
| 5+ years | 100 |
| 3-4 years | 80 |
| 1-2 years | 60 |
| <1 year | 40 |
| None | 0 |

**Bonus:** +10 points if 3+ revenue-related keywords found

**Keywords Detected:**
- revenue, sales, quota, close, deal, pipeline

**Example:**
- "Generated $5M in revenue over 3 years" → 80-100 points
- "Exceeded sales quota by 25%" → Bonus points

---

### 2️⃣ Business Development (12% weight)

**Category:** Experience
**Description:** New market identification, client acquisition, partnership development

**Scoring Criteria:**
| Achievement | Points |
|-----------|--------|
| Strategic account development | 100 |
| Market expansion | 90 |
| New business acquisition | 85 |
| Partner development | 75 |
| None | 0 |

**Keywords Detected:**
- business development, new business, market expansion, partnership, strategic account

**Example:**
- "Expanded into 3 new markets generating $2M" → 85-90 points
- "Developed 5 strategic partnerships" → 75-85 points

---

### 3️⃣ Account Management (12% weight)

**Category:** Experience
**Description:** Management and retention of existing client accounts

**Scoring Criteria:**
| Achievement | Points |
|-----------|--------|
| Enterprise account management | 100 |
| Account growth | 90 |
| Client retention | 85 |
| Relationship management | 75 |
| None | 0 |

**Keywords Detected:**
- account management, client, retention, relationship, enterprise, portfolio

**Example:**
- "Managed $10M portfolio with 95% retention" → 100 points
- "Grew existing accounts by 40% annually" → 85-90 points

---

### 4️⃣ Leadership Experience (10% weight)

**Category:** Experience
**Description:** Leading and managing sales/BD teams

**Scoring Criteria:**
| Team Size | Points |
|-----------|--------|
| 10+ direct reports | 100 |
| 5-9 direct reports | 85 |
| 1-4 direct reports | 70 |
| Leadership projects | 60 |
| None | 0 |

**Keywords Detected:**
- managed, led, team, director, manager, leader, head of

**Calculation:**
- Team size extracted from resume
- Multiple mentions increase score
- Leadership project keywords count as 60 points baseline

**Example:**
- "Led team of 15 sales professionals" → 100 points
- "Managed 3 business development managers" → 70-85 points

---

### 5️⃣ Industry Expertise (10% weight)

**Category:** Experience
**Description:** Deep knowledge of target industry (Sales & Business Development)

**Scoring Criteria:**
| Experience | Points |
|-----------|--------|
| 5+ years same industry | 100 |
| 3-4 years same industry | 85 |
| 2-3 years same industry | 70 |
| Diverse experience | 60 |
| None | 0 |

**Keywords Detected:**
- industry, domain, sector, vertical, market

**Calculation:**
- Total years in sales/BD roles
- Same company/industry = higher score
- Industry-specific keywords boost score

**Example:**
- "8 years in SaaS sales" → 100 points
- "5 years in enterprise software, 3 in tech startups" → 85-100 points

---

### 6️⃣ Product & Technical Knowledge (8% weight)

**Category:** Technical
**Description:** Understanding of SaaS, CRM, product, and technical concepts

**Scoring Criteria:**
| Level | Points |
|-----------|--------|
| Advanced (3+ keywords, 5+ skills) | 100 |
| Intermediate (2 keywords, 3+ skills) | 80 |
| Basic (1 keyword, 2 skills) | 60 |
| None | 0 |

**Keywords Detected:**
- SaaS, technical, product, API, CRM, Salesforce, tools, software

**Skills Counted:**
- Any relevant technical/product skills from resume

**Example:**
- "Expert in SaaS, proficient with Salesforce and APIs" → 100 points
- "Basic product knowledge, uses CRM tools" → 60-80 points

---

### 7️⃣ Communication Skills (8% weight)

**Category:** Behavioral
**Description:** Ability to communicate effectively and persuasively

**Scoring Criteria:**
| Skill Level | Points |
|-----------|--------|
| Executive presentations | 100 |
| Public speaking experience | 90 |
| Presentations | 75 |
| Written communication | 70 |
| None | 0 |

**Keywords Detected:**
- presentation, communication, speaking, negotiation, persuasion, articulate

**Example:**
- "Delivered 50+ executive presentations" → 90-100 points
- "Strong negotiation and communication skills" → 75 points

---

### 8️⃣ Negotiation & Deal Closing (10% weight)

**Category:** Behavioral
**Description:** Strong negotiation and deal-closing capabilities

**Scoring Criteria:**
| Achievement | Points |
|-----------|--------|
| Demonstrated deal closing | 100 |
| Negotiation experience | 85 |
| Deal handling | 75 |
| None | 0 |

**Keywords Detected:**
- close, negotiation, deal, contract, terms, closing

**Example:**
- "Negotiated and closed multi-million dollar contracts" → 100 points
- "Closed 100+ deals annually" → 100 points
- "Experienced in contract negotiation" → 85 points

---

### 9️⃣ Relevant Certifications (7% weight)

**Category:** Technical
**Description:** Industry-recognized certifications and credentials

**Scoring Criteria:**
| Count | Points |
|-----------|--------|
| 3+ certifications | 100 |
| Salesforce certified | 90 |
| Sales certification | 80 |
| None | 0 |

**Certifications Recognized:**
- Salesforce Certified Sales Cloud Consultant
- HubSpot Sales Certification
- Google Analytics Certified
- LinkedIn Sales Navigator
- SPIN Selling Certification
- Coursera/LinkedIn Learning certificates

**Example:**
- "Salesforce Certified + HubSpot Certified + Google Analytics" → 100 points
- "HubSpot Sales Certified" → 80-90 points

---

### 🔟 Analytics & Data-Driven (8% weight)

**Category:** Technical
**Description:** Using data and analytics for decision making

**Scoring Criteria:**
| Level | Points |
|-----------|--------|
| Advanced analytics (3+ keywords) | 100 |
| Dashboard & reporting (2 keywords) | 85 |
| Metrics-driven (1 keyword) | 70 |
| None | 0 |

**Keywords Detected:**
- analytics, dashboard, metrics, reporting, data-driven, BI, forecasting

**Example:**
- "Implemented analytics dashboard improving forecasting accuracy by 25%" → 100 points
- "Uses metrics-driven approach" → 70 points

---

## Overall Score Calculation

### Formula
```
Overall Score = Σ(Metric Score × Metric Weight)

Example:
= (95 × 0.15) + (85 × 0.12) + (80 × 0.12) + (70 × 0.10) + (85 × 0.10) 
  + (75 × 0.08) + (80 × 0.08) + (85 × 0.10) + (70 × 0.07) + (80 × 0.08)
= 14.25 + 10.2 + 9.6 + 7 + 8.5 + 6 + 6.4 + 8.5 + 4.9 + 6.4
= 81.7%
```

### Matching Threshold
- **80-100%**: ✅ Qualified (Meets threshold)
- **70-79%**: ⚠️ Developing (Targeted development needed)
- **60-69%**: ⚠️ Significant Gaps (Major preparation needed)
- **<60%**: ❌ Not Ready (Substantial work required)

---

## Job Readiness Levels

Based on overall score:

| Score | Readiness | Recommendation |
|-------|-----------|-----------------|
| 90-100% | Ready - Immediate deployment | Fast-track to final round |
| 80-89% | Ready - Minor onboarding needed | Schedule interview immediately |
| 70-79% | Developing - Requires targeted development | Consider for future roles |
| 60-69% | Developing - Significant gaps | Offer training/coaching |
| 0-59% | Needs Work - Substantial preparation | Reject or reassess later |

---

## Industry Alignment Assessment

**Based on:** Keywords and experience relevance to Sales & Business Development

| Level | Criteria | Examples |
|-------|----------|----------|
| **High** | 5+ S&BD keywords + 2+ relevant experiences | VP of Sales, B.D. Manager |
| **Medium** | 3-4 S&BD keywords or 2+ experiences | Account Executive, Sales Manager |
| **Low** | <3 keywords or <2 relevant experiences | New to sales, diverse background |

---

## Examples: Full Candidate Assessments

### Candidate A: Senior Sales Executive
```
Resume Extract:
"VP of Sales with 8 years experience, $12M revenue, 
led 15-person team, 90% client retention, 
Salesforce & HubSpot certified"

Metric Scores:
- Sales Revenue: 95% (8 years experience + keywords)
- Business Development: 85% (strategic accounts mentioned)
- Account Management: 90% (90% retention stated)
- Leadership: 100% (15 direct reports)
- Industry Expertise: 95% (8 years sales)
- Technical Knowledge: 85% (Salesforce + HubSpot)
- Communication: 75% (implied from VP role)
- Negotiation: 85% (deal keywords)
- Certifications: 90% (2 major certifications)
- Analytics: 70% (metrics mentioned)

OVERALL SCORE: 86.5% ✅ QUALIFIED
```

### Candidate B: Junior Sales Representative
```
Resume Extract:
"3 years sales experience, exceeded quota 120%, 
basic CRM skills, some presentation experience"

Metric Scores:
- Sales Revenue: 60% (3 years, quota mentioned)
- Business Development: 40% (no keywords)
- Account Management: 35% (no experience shown)
- Leadership: 0% (no team experience)
- Industry Expertise: 70% (3 years sales)
- Technical Knowledge: 50% (basic CRM)
- Communication: 60% (presentations mentioned)
- Negotiation: 40% (no keywords)
- Certifications: 0% (none mentioned)
- Analytics: 30% (minimal)

OVERALL SCORE: 38.5% ❌ BELOW THRESHOLD
```

---

## Customizing Metrics

### Adjusting Weights
Edit `metrics.py` to change `weight` values. Must total 1.0:

```python
SALES_BD_METRICS = {
    "sales_revenue_generation": {
        "weight": 0.15,  # Change here
```

### Adding New Metrics
1. Add definition to `SALES_BD_METRICS`
2. Create `_score_[metric_name]` method in `analyzer.py`
3. Metric auto-appears in reports

### Changing Keyword Detection
Edit keywords lists in `metrics.py`:

```python
"keywords": ["revenue", "sales", "quota"]  # Add/remove keywords
```

---

## Common Scoring Scenarios

### Multiple Years Stated
- Resume with: "5 years at Company A, 3 years at Company B"
- Total: 8 years
- Score: 100% for revenue generation

### No Dates But Keywords
- Resume states: "Exceeded sales quota, managed accounts"
- Keywords count: Revenue = 2 keywords → 60%
- Account Management = 1 keyword → 35%

### Certifications Listed
- "Salesforce Certified Sales Cloud Consultant" + "HubSpot Certified"
- Count: 2 certifications → 80-90%

### Mixed Experience
- "3 years in sales, 2 years in marketing, 1 year in business development"
- Relevant: 3 years sales + 1 year BD = 4 years
- Score: 80% industry expertise

---

## FAQs

**Q: Why did my score change after minor edits?**
A: Algorithm detects keywords. Small formatting changes can affect detection.

**Q: Can I weight leadership more heavily?**
A: Yes! Edit `weight` values in `metrics.py`. Remember to keep total = 1.0

**Q: What if none of my skills match?**
A: The app tries to extract meaning from context. For best results, use standard terminology.

**Q: How does the app handle gaps in a resume?**
A: No penalty for gaps. Only evaluates information present.

---

**Note:** These metrics are industry standards for Sales & Business Development roles and are regularly updated based on market trends.
