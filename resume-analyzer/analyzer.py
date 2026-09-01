"""
Resume Analyzer - Score and analyze resumes against Sales & BD metrics
"""

import re
from typing import Dict, List, Tuple
from models import ResumeData, ResumeAnalysis
from metrics import SALES_BD_METRICS, SCORE_THRESHOLDS, JOB_READINESS_LEVELS


class ResumeAnalyzer:
    def __init__(self):
        self.metrics = SALES_BD_METRICS
        self.thresholds = SCORE_THRESHOLDS
        self.resume_text = ""

    def analyze(self, resume_data: ResumeData) -> ResumeAnalysis:
        """Perform comprehensive analysis of resume"""
        self.resume_text = resume_data.raw_text.lower()

        # Score each metric
        metric_scores = self._score_all_metrics(resume_data)

        # Calculate overall score
        overall_score = self._calculate_overall_score(metric_scores)
        match_percentage = overall_score

        # Generate insights
        strengths = self._identify_strengths(resume_data, metric_scores)
        gaps = self._identify_gaps(resume_data, metric_scores)
        recommendations = self._generate_recommendations(gaps)

        # Industry alignment
        industry_alignment = self._assess_industry_alignment(resume_data)

        # Job readiness
        job_readiness = self._determine_job_readiness(overall_score)

        return ResumeAnalysis(
            resume_name=resume_data.name,
            overall_score=overall_score,
            match_percentage=match_percentage,
            matched=overall_score >= 80,
            metric_scores=metric_scores,
            strengths=strengths,
            gaps=gaps,
            recommendations=recommendations,
            industry_alignment=industry_alignment,
            job_readiness=job_readiness
        )

    def _score_all_metrics(self, resume_data: ResumeData) -> Dict[str, float]:
        """Score all defined metrics"""
        scores = {}
        for metric_name, metric_config in self.metrics.items():
            score = self._score_metric(metric_name, metric_config, resume_data)
            scores[metric_name] = round(score, 1)
        return scores

    def _score_metric(self, metric_name: str, metric_config: dict, resume_data: ResumeData) -> float:
        """Score a single metric"""
        if metric_name == "sales_revenue_generation":
            return self._score_revenue_generation(resume_data)
        elif metric_name == "business_development":
            return self._score_business_development(resume_data)
        elif metric_name == "account_management":
            return self._score_account_management(resume_data)
        elif metric_name == "leadership_experience":
            return self._score_leadership(resume_data)
        elif metric_name == "industry_expertise":
            return self._score_industry_expertise(resume_data)
        elif metric_name == "product_technical_knowledge":
            return self._score_technical_knowledge(resume_data)
        elif metric_name == "communication_skills":
            return self._score_communication(resume_data)
        elif metric_name == "negotiation_closing":
            return self._score_negotiation(resume_data)
        elif metric_name == "relevant_certifications":
            return self._score_certifications(resume_data)
        elif metric_name == "analytics_data_driven":
            return self._score_analytics(resume_data)
        return 0.0

    def _score_revenue_generation(self, resume_data: ResumeData) -> float:
        """Score sales revenue generation"""
        experience_years = sum(exp.duration_years for exp in resume_data.experiences)

        if experience_years >= 5:
            base_score = 100
        elif experience_years >= 3:
            base_score = 80
        elif experience_years >= 1:
            base_score = 60
        elif experience_years > 0:
            base_score = 40
        else:
            base_score = 0

        # Boost if revenue metrics mentioned
        revenue_keywords = ["revenue", "sales", "quota", "close", "deal", "pipeline"]
        keywords_found = sum(1 for keyword in revenue_keywords if keyword in self.resume_text)

        if keywords_found >= 3:
            base_score = min(100, base_score + 10)

        return base_score

    def _score_business_development(self, resume_data: ResumeData) -> float:
        """Score business development experience"""
        bd_keywords = ["business development", "new business", "market expansion", "partnership", "strategic account"]
        keyword_count = sum(1 for keyword in bd_keywords if keyword in self.resume_text)

        if keyword_count >= 3:
            return 100
        elif keyword_count >= 2:
            return 85
        elif keyword_count >= 1:
            return 70
        else:
            # Check if they have relevant experience
            if resume_data.experiences:
                return 50
            return 0

    def _score_account_management(self, resume_data: ResumeData) -> float:
        """Score account/client management experience"""
        am_keywords = ["account management", "client", "retention", "relationship", "enterprise", "portfolio"]
        keyword_count = sum(1 for keyword in am_keywords if keyword in self.resume_text)

        if keyword_count >= 3:
            return 100
        elif keyword_count >= 2:
            return 85
        elif keyword_count >= 1:
            return 70
        else:
            return 0

    def _score_leadership(self, resume_data: ResumeData) -> float:
        """Score leadership and management experience"""
        leadership_keywords = ["managed", "led", "team", "director", "manager", "leader", "head of"]
        keyword_count = sum(1 for keyword in leadership_keywords if keyword in self.resume_text)

        # Count team mentions
        team_size_pattern = r'(\d+)\+?\s*(?:direct|reports|team|members)'
        team_matches = re.findall(team_size_pattern, self.resume_text)
        max_team_size = max([int(m) for m in team_matches], default=0)

        if max_team_size >= 10:
            return 100
        elif max_team_size >= 5:
            return 85
        elif max_team_size >= 1:
            return 70
        elif keyword_count >= 2:
            return 60
        elif keyword_count >= 1:
            return 40
        else:
            return 0

    def _score_industry_expertise(self, resume_data: ResumeData) -> float:
        """Score industry-specific knowledge"""
        # Check if same companies appear multiple times
        companies = [exp.company for exp in resume_data.experiences]
        company_counts = {}
        for company in companies:
            company_counts[company] = company_counts.get(company, 0) + 1

        # Check for same industry
        industries = [exp.industry for exp in resume_data.experiences if exp.industry]

        total_years = sum(exp.duration_years for exp in resume_data.experiences)

        if total_years >= 5:
            if len(industries) > 0:
                return 100
            else:
                return 85
        elif total_years >= 3:
            return 70
        elif total_years >= 2:
            return 60
        else:
            return 40

    def _score_technical_knowledge(self, resume_data: ResumeData) -> float:
        """Score technical and product knowledge"""
        tech_keywords = ["saas", "technical", "product", "api", "crm", "salesforce", "tools", "software"]
        keyword_count = sum(1 for keyword in tech_keywords if keyword in self.resume_text)

        skill_count = len(resume_data.skills)

        if keyword_count >= 3 and skill_count >= 5:
            return 100
        elif keyword_count >= 2 and skill_count >= 3:
            return 80
        elif keyword_count >= 1 or skill_count >= 2:
            return 60
        else:
            return 0

    def _score_communication(self, resume_data: ResumeData) -> float:
        """Score communication and presentation skills"""
        comm_keywords = ["presentation", "communication", "speaking", "negotiation", "persuasion", "articulate"]
        keyword_count = sum(1 for keyword in comm_keywords if keyword in self.resume_text)

        if keyword_count >= 3:
            return 100
        elif keyword_count >= 2:
            return 75
        elif keyword_count >= 1:
            return 60
        else:
            return 0

    def _score_negotiation(self, resume_data: ResumeData) -> float:
        """Score negotiation and deal closing"""
        neg_keywords = ["close", "negotiation", "deal", "contract", "terms", "closing"]
        keyword_count = sum(1 for keyword in neg_keywords if keyword in self.resume_text)

        if keyword_count >= 3:
            return 100
        elif keyword_count >= 2:
            return 85
        elif keyword_count >= 1:
            return 70
        else:
            return 0

    def _score_certifications(self, resume_data: ResumeData) -> float:
        """Score relevant certifications"""
        cert_count = len(resume_data.certifications)

        if cert_count >= 3:
            return 100
        elif cert_count >= 2:
            return 80
        elif cert_count >= 1:
            return 60
        else:
            return 0

    def _score_analytics(self, resume_data: ResumeData) -> float:
        """Score analytics and data-driven approach"""
        analytics_keywords = ["analytics", "dashboard", "metrics", "reporting", "data-driven", "bi", "forecasting"]
        keyword_count = sum(1 for keyword in analytics_keywords if keyword in self.resume_text)

        if keyword_count >= 3:
            return 100
        elif keyword_count >= 2:
            return 85
        elif keyword_count >= 1:
            return 70
        else:
            return 0

    def _calculate_overall_score(self, metric_scores: Dict[str, float]) -> float:
        """Calculate weighted overall score"""
        total_weighted_score = 0
        for metric_name, score in metric_scores.items():
            if metric_name in self.metrics:
                weight = self.metrics[metric_name].get("weight", 0)
                total_weighted_score += score * weight

        return round(total_weighted_score, 1)

    def _identify_strengths(self, resume_data: ResumeData, metric_scores: Dict[str, float]) -> List[str]:
        """Identify top strengths"""
        strengths = []
        threshold = 80

        for metric_name, score in metric_scores.items():
            if score >= threshold:
                metric_config = self.metrics.get(metric_name, {})
                description = metric_config.get("description", metric_name)
                strengths.append(f"{description.capitalize()} ({score}%)")

        # Add specific strengths from resume
        if resume_data.experiences:
            years = sum(exp.duration_years for exp in resume_data.experiences)
            strengths.append(f"Extensive experience: {years:.1f} years in relevant roles")

        if len(resume_data.certifications) > 0:
            strengths.append(f"Professional certifications: {', '.join(resume_data.certifications)}")

        return strengths[:5]  # Top 5 strengths

    def _identify_gaps(self, resume_data: ResumeData, metric_scores: Dict[str, float]) -> List[str]:
        """Identify skill gaps"""
        gaps = []
        threshold = 60

        for metric_name, score in metric_scores.items():
            if score < threshold:
                metric_config = self.metrics.get(metric_name, {})
                description = metric_config.get("description", metric_name)
                gaps.append(f"Limited {description.lower()} (Current: {score}%)")

        return gaps[:5]  # Top 5 gaps

    def _generate_recommendations(self, gaps: List[str]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        if "revenue" in str(gaps).lower():
            recommendations.append("Develop or showcase concrete sales metrics and revenue achievements")

        if "leadership" in str(gaps).lower():
            recommendations.append("Gain leadership experience through mentoring or team management roles")

        if "certification" in str(gaps).lower():
            recommendations.append("Pursue relevant industry certifications (e.g., Salesforce, HubSpot)")

        if "communication" in str(gaps).lower():
            recommendations.append("Enhance presentation and communication skills through training")

        if "technical" in str(gaps).lower():
            recommendations.append("Build technical product knowledge through hands-on experience")

        recommendations.append("Develop case studies highlighting successful deals and client relationships")

        return recommendations[:5]

    def _assess_industry_alignment(self, resume_data: ResumeData) -> str:
        """Assess alignment with Sales & BD industry"""
        sales_bd_keywords = [
            "sales", "business development", "account management", "revenue",
            "quota", "pipeline", "client", "deal", "closing"
        ]

        keyword_count = sum(1 for keyword in sales_bd_keywords if keyword in self.resume_text)
        experience_count = len(resume_data.experiences)

        if keyword_count >= 5 and experience_count >= 2:
            return "High"
        elif keyword_count >= 3 or experience_count >= 2:
            return "Medium"
        else:
            return "Low"

    def _determine_job_readiness(self, overall_score: float) -> str:
        """Determine job readiness level"""
        if overall_score >= 90:
            return "Ready - Immediate deployment"
        elif overall_score >= 80:
            return "Ready - Minor onboarding needed"
        elif overall_score >= 70:
            return "Developing - Requires targeted development"
        elif overall_score >= 60:
            return "Developing - Significant gaps to address"
        else:
            return "Needs Work - Substantial preparation required"
