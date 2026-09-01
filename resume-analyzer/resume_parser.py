"""
Resume Parser - Extract structured data from resume files
Supports PDF, DOCX, and TXT formats
"""

import re
import os
from pathlib import Path
from typing import Optional, Dict, List
from pypdf import PdfReader
from docx import Document
from models import ResumeData, Experience, Education


class ResumeParser:
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}'

    def parse_file(self, file_path: str) -> Optional[ResumeData]:
        """Parse resume file based on extension"""
        file_ext = Path(file_path).suffix.lower()

        if file_ext == '.pdf':
            return self.parse_pdf(file_path)
        elif file_ext in ['.docx', '.doc']:
            return self.parse_docx(file_path)
        elif file_ext == '.txt':
            return self.parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")

    def parse_pdf(self, file_path: str) -> Optional[ResumeData]:
        """Extract text from PDF resume"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return self._extract_resume_data(text, file_path)
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return None

    def parse_docx(self, file_path: str) -> Optional[ResumeData]:
        """Extract text from DOCX resume"""
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return self._extract_resume_data(text, file_path)
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
            return None

    def parse_txt(self, file_path: str) -> Optional[ResumeData]:
        """Extract text from TXT resume"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return self._extract_resume_data(text, file_path)
        except Exception as e:
            print(f"Error parsing TXT: {e}")
            return None

    def _extract_resume_data(self, text: str, file_path: str) -> ResumeData:
        """Extract structured data from resume text"""
        name = self._extract_name(text)
        email = self._extract_email(text)
        phone = self._extract_phone(text)
        location = self._extract_location(text)
        summary = self._extract_summary(text)
        experiences = self._extract_experiences(text)
        education = self._extract_education(text)
        certifications = self._extract_certifications(text)
        skills = self._extract_skills(text)

        return ResumeData(
            name=name,
            email=email or "not_found@example.com",
            phone=phone,
            location=location,
            professional_summary=summary,
            experiences=experiences,
            education=education,
            certifications=certifications,
            skills=skills,
            raw_text=text
        )

    def _extract_name(self, text: str) -> str:
        """Extract candidate name from text"""
        lines = text.split('\n')
        # First line is often the name
        if lines:
            name = lines[0].strip()
            if name and len(name) < 50:  # Sanity check
                return name
        return "Unknown"

    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email address"""
        match = re.search(self.email_pattern, text)
        return match.group(0) if match else None

    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number"""
        match = re.search(self.phone_pattern, text)
        return match.group(0) if match else None

    def _extract_location(self, text: str) -> Optional[str]:
        """Extract location (basic extraction)"""
        # Look for common location patterns
        location_keywords = ["location", "based in", "located in"]
        for keyword in location_keywords:
            pattern = f"{keyword}[:|]?\\s*([^\\n,]+)"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    def _extract_summary(self, text: str) -> str:
        """Extract professional summary"""
        # Look for sections with keywords
        keywords = ["professional summary", "objective", "about", "profile"]
        for keyword in keywords:
            pattern = f"{keyword}[:|]?\\s*([^\\n]{{50,}}?)(?:\\n\\n|\\n[A-Z])"
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:500]
        # Return first 500 chars if no summary found
        return text[:500] if len(text) > 500 else text

    def _extract_experiences(self, text: str) -> List[Experience]:
        """Extract work experiences"""
        experiences = []

        # Look for experience sections
        experience_section = self._find_section(text, ["experience", "work experience", "employment"])
        if not experience_section:
            return experiences

        # Split by common patterns (company names, job titles)
        job_blocks = re.split(r'\n(?=[A-Z][^a-z]|\d{4})', experience_section)

        for block in job_blocks:
            if len(block.strip()) < 20:
                continue

            company = self._extract_company(block)
            position = self._extract_position(block)
            duration = self._extract_duration(block)
            achievements = self._extract_achievements(block)

            if company and position:
                experiences.append(Experience(
                    company=company,
                    position=position,
                    duration_years=duration,
                    key_achievements=achievements[:5],  # Limit to 5
                    sales_metrics=self._extract_sales_metrics(block)
                ))

        return experiences[:10]  # Limit to 10 experiences

    def _extract_company(self, text: str) -> Optional[str]:
        """Extract company name from job block"""
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        if lines:
            return lines[0]
        return None

    def _extract_position(self, text: str) -> Optional[str]:
        """Extract job position/title"""
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        if len(lines) > 1:
            return lines[1]
        return None

    def _extract_duration(self, text: str) -> float:
        """Calculate experience duration in years"""
        years = re.findall(r'(\d+)\s*(?:years?|yrs?)', text, re.IGNORECASE)
        if years:
            return float(years[0])
        # Try to extract dates
        dates = re.findall(r'(?:19|20)\d{2}', text)
        if len(dates) >= 2:
            try:
                return float(int(dates[-1]) - int(dates[0])) / 12
            except:
                pass
        return 0.0

    def _extract_achievements(self, text: str) -> List[str]:
        """Extract key achievements/responsibilities"""
        achievements = []
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if any(x in line.lower() for x in ['•', '-', '*', 'achieved', 'increased', 'improved', 'developed']):
                if len(line) > 10:
                    achievements.append(line.lstrip('•-* '))
        return achievements

    def _extract_sales_metrics(self, text: str) -> Optional[Dict[str, str]]:
        """Extract sales-specific metrics"""
        metrics = {}
        # Look for revenue, quota, etc.
        patterns = {
            'revenue': r'\$\d+[MK]?',
            'quota_achievement': r'(\d+)%\s*(?:quota|target)',
            'clients': r'(\d+)\+?\s*(?:clients|accounts)',
        }
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                metrics[key] = match.group(0)
        return metrics if metrics else None

    def _extract_education(self, text: str) -> List[Education]:
        """Extract education details"""
        education = []
        education_section = self._find_section(text, ["education", "academic"])

        if not education_section:
            return education

        degrees = ['bachelor', 'master', 'phd', 'mba', 'bs', 'ms', 'ba', 'ma']
        for degree in degrees:
            pattern = rf'{degree}[^\.]*(?:in|of)\s*([^,\.]+)'
            matches = re.finditer(pattern, education_section, re.IGNORECASE)
            for match in matches:
                field = match.group(1).strip()
                # Extract institution name
                institution = "Unknown Institution"
                lines = education_section.split('\n')
                for i, line in enumerate(lines):
                    if degree.lower() in line.lower():
                        if i + 1 < len(lines):
                            institution = lines[i + 1].strip()
                        break

                education.append(Education(
                    degree=degree.capitalize(),
                    field=field,
                    institution=institution
                ))

        return education

    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        certifications = []
        cert_section = self._find_section(text, ["certification", "certifications", "credentials"])

        if not cert_section:
            return certifications

        # Common sales/BD certifications
        cert_keywords = [
            'salesforce', 'HubSpot', 'Google Analytics', 'Six Sigma', 'SCRUM',
            'Coursera', 'LinkedIn Learning', 'Certified', 'AWS', 'Azure'
        ]

        for keyword in cert_keywords:
            if keyword.lower() in cert_section.lower():
                certifications.append(keyword)

        return certifications

    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills"""
        skills = []
        skills_section = self._find_section(text, ["skills", "technical skills", "core competencies"])

        if skills_section:
            # Remove common punctuation and split
            text_to_parse = skills_section.replace(',', '\n').replace(';', '\n')
            for line in text_to_parse.split('\n'):
                skill = line.strip().lstrip('•-* ')
                if skill and len(skill) > 2:
                    skills.append(skill)

        return skills[:20]  # Limit to 20 skills

    def _find_section(self, text: str, keywords: List[str]) -> Optional[str]:
        """Find and extract a section by keywords"""
        for keyword in keywords:
            pattern = rf'(?i){keyword}[:|]?(.*?)(?:\n[A-Z][^a-z]|\Z)'
            match = re.search(pattern, text, re.DOTALL)
            if match:
                return match.group(1)
        return None
