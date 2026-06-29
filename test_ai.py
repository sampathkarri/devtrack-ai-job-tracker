from services.ai_service import calculate_match_score

resume = """
Python
FastAPI
SQL
Git
Docker
"""

job_description = """
Python
FastAPI
SQL
"""

score = calculate_match_score(
    resume,
    job_description
)

print("Match Score:", score)