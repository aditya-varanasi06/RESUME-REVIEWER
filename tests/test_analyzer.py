from resume_reviewer import ResumeReviewer


def test_review_scores_strong_resume_with_job_description() -> None:
    resume = """
    Alex Rivera

    Summary
    Senior Python engineer building APIs and data platforms.

    Skills
    Python, FastAPI, PostgreSQL, AWS, Docker, Terraform, Airflow

    Experience
    Senior Engineer | Example Co | 2021 - Present
    - Built FastAPI service processing 20M events daily and reduced latency by 42%.
    - Led AWS migration for 12 services and cut infrastructure cost by 18%.
    - Optimized PostgreSQL indexes for 80M rows and improved report generation by 55%.
    - Automated Docker CI/CD checks and reduced failed releases by 30%.
    - Mentored 5 engineers through design reviews and improved delivery predictability by 20%.
    - Created Airflow data pipelines that processed 4TB monthly for analytics teams.

    Projects
    - Designed backend observability dashboard using Python, PostgreSQL, and AWS for 15 services.

    Education
    B.S. Computer Science, 2017
    """
    job = "Python FastAPI PostgreSQL AWS Docker Terraform Airflow APIs data pipelines"

    report = ResumeReviewer().review(resume, job, role="backend", experience_level="senior")

    assert report.scorecard.overall >= 70
    assert report.role == "Backend Engineer"
    assert report.experience_level == "Senior"
    assert "experience" in report.section_analysis.detected
    assert "skills" in report.section_analysis.section_feedback
    assert report.keyword_match.match_rate > 0.5
    assert report.metrics["quantified_bullet_count"] >= 6


def test_review_flags_missing_sections_and_weak_bullets() -> None:
    resume = """
    Taylor Smith
    Responsible for various tasks.
    - Worked on reports.
    """

    report = ResumeReviewer().review(resume, "Python SQL AWS")

    titles = {finding.title for finding in report.findings}
    assert "Missing experience section" in titles
    assert "Weak or generic phrasing detected" in titles
    assert report.scorecard.overall < 70
