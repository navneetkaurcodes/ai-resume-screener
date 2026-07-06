from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import (
    Resume,
    JobDescription,
    CandidateScore,
    SkillGap
)

from app.services.scoring_service import (
    calculate_tfidf_score,
    calculate_skill_match,
    calculate_experience_match,
    calculate_final_score
)

router = APIRouter(
    prefix="/scoring",
    tags=["AI Scoring"]
)

@router.post("/score_candidate/{resume_id}/{job_id}")
def score_resume(
    resume_id: int,
    job_id: int,
    db: Session = Depends(get_db)
):

    resume = db.query(Resume).filter(
        Resume.id == resume_id
    ).first()

    if not resume:
        raise HTTPException(404, "Resume not found")

    job = db.query(JobDescription).filter(
        JobDescription.id == job_id
    ).first()

    if not job:
        raise HTTPException(404, "Job Description not found")

    tfidf_score = calculate_tfidf_score(
        job.description,
        resume.raw_text
    )

    skill_percent, matched, missing = calculate_skill_match(
        job.required_skills,
        resume.extracted_skills
    )

    experience_score = calculate_experience_match(
        job.min_experience,
        resume.experience_years
    )

    final_score = calculate_final_score(
        tfidf_score,
        skill_percent,
        experience_score
    )

    score = CandidateScore(
        resume_id=resume.id,
        jd_id=job.id,
        tfidf_score=float(tfidf_score),
        skill_match_percent=float(skill_percent),
        final_score=float(final_score),
    )

    db.add(score)

    gap = SkillGap(
        resume_id=resume.id,
        jd_id=job.id,
        matched_skills=matched,
        missing_skills=missing,
        match_percent=skill_percent
    )

    db.add(gap)

    db.commit()

    return {
        "resume_id": resume.id,
        "job_id": job.id,
        "tfidf_score": tfidf_score,
        "skill_match": skill_percent,
        "experience_score": experience_score,
        "final_score": final_score,
        "matched_skills": matched,
        "missing_skills": missing
    }

@router.get("/ranking/{job_id}")
def get_candidate_ranking(
    job_id: int,
    db: Session = Depends(get_db)
):

    rankings = (
        db.query(CandidateScore)
        .filter(CandidateScore.jd_id == job_id)
        .order_by(CandidateScore.rank)
        .all()
    )

    return rankings
