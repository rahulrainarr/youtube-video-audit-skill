"""
Sales & Business Development Industry Standard Metrics
Aligned with common industry practices and skill frameworks
"""

SALES_BD_METRICS = {
    # Experience & Track Record
    "sales_revenue_generation": {
        "category": "Experience",
        "weight": 0.15,
        "description": "Demonstrated ability to generate revenue or close deals",
        "criteria": {
            "5+ years": 100,
            "3-4 years": 80,
            "1-2 years": 60,
            "0-1 years": 40,
            "none": 0
        },
        "keywords": ["revenue", "sales", "quota", "close", "deal", "pipeline"]
    },

    # Business Development
    "business_development": {
        "category": "Experience",
        "weight": 0.12,
        "description": "New market identification and client acquisition",
        "criteria": {
            "strategic_account_development": 100,
            "market_expansion": 90,
            "new_business_acquisition": 85,
            "partner_development": 75,
            "none": 0
        },
        "keywords": ["business development", "new business", "market expansion", "partnership", "strategic account"]
    },

    # Client/Account Management
    "account_management": {
        "category": "Experience",
        "weight": 0.12,
        "description": "Management and retention of existing accounts",
        "criteria": {
            "enterprise_accounts": 100,
            "account_growth": 90,
            "client_retention": 85,
            "relationship_management": 75,
            "none": 0
        },
        "keywords": ["account management", "client retention", "relationship", "enterprise", "portfolio"]
    },

    # Team Leadership
    "leadership_experience": {
        "category": "Experience",
        "weight": 0.10,
        "description": "Leading and managing sales/BD teams",
        "criteria": {
            "10+ direct_reports": 100,
            "5-9_direct_reports": 85,
            "1-4_direct_reports": 70,
            "leadership_projects": 60,
            "none": 0
        },
        "keywords": ["managed", "led", "team", "director", "manager", "leader", "head of"]
    },

    # Industry Knowledge
    "industry_expertise": {
        "category": "Technical",
        "weight": 0.10,
        "description": "Deep knowledge of target industry",
        "criteria": {
            "5+_years_same_industry": 100,
            "3-4_years_same_industry": 85,
            "2-3_years_same_industry": 70,
            "diverse_experience": 60,
            "none": 0
        },
        "keywords": ["industry", "domain", "sector", "vertical", "market"]
    },

    # Technical & Product Knowledge
    "product_technical_knowledge": {
        "category": "Technical",
        "weight": 0.08,
        "description": "Understanding of SaaS/Product/Technical concepts",
        "criteria": {
            "advanced": 100,
            "intermediate": 80,
            "basic": 60,
            "none": 0
        },
        "keywords": ["SaaS", "technical", "product", "API", "CRM", "Salesforce", "tools"]
    },

    # Communication Skills
    "communication_skills": {
        "category": "Behavioral",
        "weight": 0.08,
        "description": "Ability to communicate effectively and persuasively",
        "criteria": {
            "executive_presentations": 100,
            "public_speaking": 90,
            "presentations": 75,
            "written_communication": 70,
            "none": 0
        },
        "keywords": ["presentation", "communication", "speaking", "negotiation", "persuasion"]
    },

    # Negotiation & Deal Closing
    "negotiation_closing": {
        "category": "Behavioral",
        "weight": 0.10,
        "description": "Strong negotiation and deal-closing capabilities",
        "criteria": {
            "demonstrated_closing": 100,
            "negotiation_experience": 85,
            "deal_handling": 75,
            "none": 0
        },
        "keywords": ["close", "negotiation", "deal", "contract", "terms", "closing"]
    },

    # Certifications & Training
    "relevant_certifications": {
        "category": "Technical",
        "weight": 0.07,
        "description": "Industry-recognized certifications",
        "criteria": {
            "multiple_certifications": 100,
            "salesforce_certified": 90,
            "sales_certification": 80,
            "none": 0
        },
        "keywords": ["certified", "certification", "training", "credential", "salesforce"]
    },

    # Analytics & Data-Driven
    "analytics_data_driven": {
        "category": "Technical",
        "weight": 0.08,
        "description": "Using data and analytics for decision making",
        "criteria": {
            "advanced_analytics": 100,
            "dashboard_reporting": 85,
            "metrics_driven": 75,
            "none": 0
        },
        "keywords": ["analytics", "dashboard", "metrics", "reporting", "data-driven", "BI", "forecasting"]
    },
}

# Interview Assessment Scoring Guidelines
INTERVIEW_ASSESSMENT_CRITERIA = {
    "technical_competency": {
        "excellent": "Deep understanding of products, markets, and technical concepts",
        "good": "Solid grasp of industry and product knowledge",
        "fair": "Basic understanding with some gaps",
        "poor": "Limited or superficial understanding"
    },

    "communication_clarity": {
        "excellent": "Clear, articulate, executive-ready communication",
        "good": "Effective communication with minor areas for improvement",
        "fair": "Adequate communication but could be clearer",
        "poor": "Unclear or difficult to follow"
    },

    "problem_solving": {
        "excellent": "Demonstrates structured thinking and creative solutions",
        "good": "Sound problem-solving approach",
        "fair": "Basic problem-solving with guidance",
        "poor": "Struggles with problem-solving"
    },

    "cultural_fit": {
        "excellent": "Strong alignment with company values and culture",
        "good": "Good fit with some minor considerations",
        "fair": "Acceptable fit with some differences",
        "poor": "Questionable cultural alignment"
    },

    "enthusiasm_motivation": {
        "excellent": "Highly motivated and genuinely interested",
        "good": "Demonstrates good interest and motivation",
        "fair": "Shows adequate interest",
        "poor": "Limited enthusiasm or engagement"
    }
}

# Score thresholds
SCORE_THRESHOLDS = {
    "exceptional": 90,
    "strong": 80,
    "moderate": 70,
    "developing": 60,
    "needs_improvement": 0
}

# Job readiness levels
JOB_READINESS_LEVELS = {
    "90_100": "Ready - Immediate deployment",
    "80_89": "Ready - Minor onboarding needed",
    "70_79": "Developing - Requires targeted development",
    "60_69": "Developing - Significant gaps to address",
    "0_59": "Needs Work - Substantial preparation required"
}

def get_metric_config(metric_name: str) -> dict:
    """Get configuration for a specific metric"""
    return SALES_BD_METRICS.get(metric_name, {})

def get_all_metrics() -> dict:
    """Get all defined metrics"""
    return SALES_BD_METRICS

def calculate_total_weight() -> float:
    """Verify total weights sum to 1.0"""
    total = sum(m.get("weight", 0) for m in SALES_BD_METRICS.values())
    return total
