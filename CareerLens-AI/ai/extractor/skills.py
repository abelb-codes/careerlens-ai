# ai/extractor/skills.py
"""
Skills extraction utilities for resume text.

This module identifies technical, professional, and soft skills using a
curated vocabulary with canonical output names.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SkillDefinition:
    """A skill label and the text variants that should map to it."""

    canonical_name: str
    aliases: tuple[str, ...]
    case_sensitive: bool = False


SKILL_DEFINITIONS: tuple[SkillDefinition, ...] = (
    SkillDefinition("Python", ("python",)),
    SkillDefinition("JavaScript", ("javascript",)),
    SkillDefinition("TypeScript", ("typescript",)),
    SkillDefinition("Java", ("java",)),
    SkillDefinition("C++", ("c++",)),
    SkillDefinition("C#", ("c#",)),
    SkillDefinition("Ruby", ("ruby",)),
    SkillDefinition("PHP", ("php",)),
    SkillDefinition("Swift", ("swift",)),
    SkillDefinition("Kotlin", ("kotlin",)),
    SkillDefinition("Go", ("Go",), case_sensitive=True),
    SkillDefinition("Go", ("golang",)),
    SkillDefinition("Rust", ("rust",)),
    SkillDefinition("R", ("R",), case_sensitive=True),
    SkillDefinition("SQL", ("sql",)),
    SkillDefinition("HTML", ("html",)),
    SkillDefinition("CSS", ("css",)),
    SkillDefinition("Bash", ("bash",)),
    SkillDefinition("Shell", ("shell",)),
    SkillDefinition("Django", ("django",)),
    SkillDefinition("Flask", ("flask",)),
    SkillDefinition("FastAPI", ("fastapi",)),
    SkillDefinition("React", ("react", "react.js")),
    SkillDefinition("Angular", ("angular",)),
    SkillDefinition("Vue", ("vue", "vue.js")),
    SkillDefinition("Next.js", ("next.js",)),
    SkillDefinition("Nuxt.js", ("nuxt.js",)),
    SkillDefinition("Svelte", ("svelte",)),
    SkillDefinition("Express", ("express", "express.js")),
    SkillDefinition("Node.js", ("node.js", "nodejs")),
    SkillDefinition("Spring", ("spring",)),
    SkillDefinition("Spring Boot", ("spring boot",)),
    SkillDefinition("Laravel", ("laravel",)),
    SkillDefinition("Ruby on Rails", ("rails", "ruby on rails")),
    SkillDefinition("jQuery", ("jquery",)),
    SkillDefinition("Bootstrap", ("bootstrap",)),
    SkillDefinition("Tailwind CSS", ("tailwind", "tailwindcss")),
    SkillDefinition("PostgreSQL", ("postgresql", "postgres")),
    SkillDefinition("MySQL", ("mysql",)),
    SkillDefinition("SQLite", ("sqlite",)),
    SkillDefinition("MongoDB", ("mongodb",)),
    SkillDefinition("Redis", ("redis",)),
    SkillDefinition("Elasticsearch", ("elasticsearch",)),
    SkillDefinition("Cassandra", ("cassandra",)),
    SkillDefinition("MariaDB", ("mariadb",)),
    SkillDefinition("DynamoDB", ("dynamodb",)),
    SkillDefinition("Firebase", ("firebase",)),
    SkillDefinition("AWS", ("aws", "amazon web services")),
    SkillDefinition("Azure", ("azure",)),
    SkillDefinition("GCP", ("gcp", "google cloud", "google cloud platform")),
    SkillDefinition("Docker", ("docker",)),
    SkillDefinition("Kubernetes", ("kubernetes",)),
    SkillDefinition("Jenkins", ("jenkins",)),
    SkillDefinition("Terraform", ("terraform",)),
    SkillDefinition("Ansible", ("ansible",)),
    SkillDefinition("CI/CD", ("ci/cd",)),
    SkillDefinition("GitHub Actions", ("github actions",)),
    SkillDefinition("GitLab CI", ("gitlab ci",)),
    SkillDefinition("Heroku", ("heroku",)),
    SkillDefinition("Linux", ("linux",)),
    SkillDefinition("Nginx", ("nginx",)),
    SkillDefinition("Apache", ("apache",)),
    SkillDefinition("Machine Learning", ("machine learning",)),
    SkillDefinition("Deep Learning", ("deep learning",)),
    SkillDefinition("Artificial Intelligence", ("artificial intelligence",)),
    SkillDefinition("Data Science", ("data science",)),
    SkillDefinition("NLP", ("nlp", "natural language processing")),
    SkillDefinition("Computer Vision", ("computer vision",)),
    SkillDefinition("TensorFlow", ("tensorflow",)),
    SkillDefinition("PyTorch", ("pytorch",)),
    SkillDefinition("Keras", ("keras",)),
    SkillDefinition("scikit-learn", ("scikit-learn", "sklearn")),
    SkillDefinition("Pandas", ("pandas",)),
    SkillDefinition("NumPy", ("numpy",)),
    SkillDefinition("SciPy", ("scipy",)),
    SkillDefinition("Seaborn", ("seaborn",)),
    SkillDefinition("Matplotlib", ("matplotlib",)),
    SkillDefinition("Tableau", ("tableau",)),
    SkillDefinition("Power BI", ("power bi",)),
    SkillDefinition("LLM", ("llm",)),
    SkillDefinition("OpenAI", ("openai",)),
    SkillDefinition("LangChain", ("langchain",)),
    SkillDefinition("Git", ("git",)),
    SkillDefinition("GitHub", ("github",)),
    SkillDefinition("GitLab", ("gitlab",)),
    SkillDefinition("Bitbucket", ("bitbucket",)),
    SkillDefinition("Jira", ("jira",)),
    SkillDefinition("Confluence", ("confluence",)),
    SkillDefinition("Trello", ("trello",)),
    SkillDefinition("Slack", ("slack",)),
    SkillDefinition("Figma", ("figma",)),
    SkillDefinition("Postman", ("postman",)),
    SkillDefinition("Docker Compose", ("docker-compose", "docker compose")),
    SkillDefinition("Agile", ("agile",)),
    SkillDefinition("Scrum", ("scrum",)),
    SkillDefinition("Kanban", ("kanban",)),
    SkillDefinition("OOP", ("oop", "object-oriented programming")),
    SkillDefinition("REST API", ("rest api", "restful api")),
    SkillDefinition("GraphQL", ("graphql",)),
    SkillDefinition("gRPC", ("grpc",)),
    SkillDefinition("Microservices", ("microservices",)),
    SkillDefinition("System Design", ("system design",)),
    SkillDefinition("TDD", ("test-driven development", "tdd")),
    SkillDefinition("MVC", ("mvc",)),
    SkillDefinition("Project Management", ("project management",)),
    SkillDefinition("Product Management", ("product management",)),
    SkillDefinition("Business Analysis", ("business analysis",)),
    SkillDefinition("Scrum Master", ("scrum master",)),
    SkillDefinition("Marketing", ("marketing",)),
    SkillDefinition("SEO", ("seo",)),
    SkillDefinition("Sales", ("sales",)),
    SkillDefinition("Finance", ("finance",)),
    SkillDefinition("Accounting", ("accounting",)),
    SkillDefinition("HR", ("hr",)),
    SkillDefinition("Recruiting", ("recruiting",)),
    SkillDefinition("Communication", ("communication",)),
    SkillDefinition("Leadership", ("leadership",)),
    SkillDefinition("Teamwork", ("teamwork",)),
    SkillDefinition("Problem Solving", ("problem solving",)),
    SkillDefinition("Critical Thinking", ("critical thinking",)),
    SkillDefinition("Time Management", ("time management",)),
    SkillDefinition("Adaptability", ("adaptability",)),
    SkillDefinition("Creativity", ("creativity",)),
    SkillDefinition("Collaboration", ("collaboration",)),
    SkillDefinition("Negotiation", ("negotiation",)),
)


def extract_skills(text: str) -> list[str]:
    """
    Extract known skills from resume text.

    Parameters
    ----------
    text:
        Plain resume text returned by the parser module.

    Returns
    -------
    list[str]
        Alphabetically sorted canonical skill names. Returns an empty list
        when no skills are found.
    """
    if not isinstance(text, str):
        logger.warning("Skills extraction received non-string input.")
        return []

    matched_skills: set[str] = set()

    for skill_definition in SKILL_DEFINITIONS:
        if _definition_matches(text, skill_definition):
            matched_skills.add(skill_definition.canonical_name)

    return sorted(matched_skills, key=str.lower)


def _definition_matches(text: str, skill_definition: SkillDefinition) -> bool:
    """Return True when any alias for the skill appears in the text."""
    flags = 0 if skill_definition.case_sensitive else re.IGNORECASE

    for alias in skill_definition.aliases:
        if re.search(_skill_pattern(alias), text, flags=flags):
            return True

    return False


def _skill_pattern(alias: str) -> str:
    """Build a regex pattern that matches a skill alias as a standalone token."""
    escaped_alias = re.escape(alias)
    return rf"(?<![A-Za-z0-9]){escaped_alias}(?![A-Za-z0-9])"
