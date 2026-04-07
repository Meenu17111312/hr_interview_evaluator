"""
grader.py — HR Answer Grading Engine

Scoring formula (per rubric weights):
    score = keyword_score * kw_weight
          + explanation_score * exp_weight
          + clarity_score * clar_weight

All sub-scores are 0.0–1.0; final score clamped to [0.0, 1.0].
"""

import re
from typing import Dict, List


# ─────────────────────────────────────────────────────────────
# Sub-scorer: KEYWORDS
# ─────────────────────────────────────────────────────────────

def keyword_score(answer: str, keywords: List[str]) -> float:
    """Return fraction of expected keywords found in the answer (case-insensitive)."""
    if not keywords:
        return 0.0
    answer_lower = answer.lower()
    hits = sum(1 for kw in keywords if kw.lower() in answer_lower)
    return hits / len(keywords)


# ─────────────────────────────────────────────────────────────
# Sub-scorer: EXPLANATION QUALITY
# ─────────────────────────────────────────────────────────────

def explanation_score(answer: str, difficulty: str) -> float:
    """
    Heuristic scoring based on answer length, sentence variety, and depth signals.
    Thresholds scale with difficulty.
    """
    word_count = len(answer.split())
    sentence_count = len(re.findall(r'[.!?]+', answer)) or 1

    # Thresholds per difficulty
    thresholds = {
        "easy":   {"min_words": 30,  "good_words": 60,  "great_words": 100},
        "medium": {"min_words": 60,  "good_words": 100, "great_words": 160},
        "hard":   {"min_words": 100, "good_words": 160, "great_words": 220},
    }
    t = thresholds.get(difficulty, thresholds["medium"])

    # Length score
    if word_count < t["min_words"]:
        length_score = 0.3
    elif word_count < t["good_words"]:
        length_score = 0.6
    elif word_count < t["great_words"]:
        length_score = 0.85
    else:
        length_score = 1.0

    # Depth signals: examples, numbers, named concepts
    depth_signals = [
        r'\b(for example|such as|like|e\.g\.)\b',
        r'\b\d+[\%]?\b',                             # numbers / percentages
        r'\b(because|therefore|as a result|thus)\b', # causal reasoning
        r'\b(first|second|third|finally|additionally)\b',  # structure
    ]
    depth_hits = sum(1 for p in depth_signals if re.search(p, answer, re.I))
    depth_score = min(depth_hits / len(depth_signals), 1.0)

    return 0.6 * length_score + 0.4 * depth_score


# ─────────────────────────────────────────────────────────────
# Sub-scorer: CLARITY
# ─────────────────────────────────────────────────────────────

def clarity_score(answer: str) -> float:
    """
    Penalise very long sentences and excessive filler words.
    Reward consistent sentence length variation (sign of good writing).
    """
    sentences = re.split(r'[.!?]+', answer)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return 0.0

    word_counts = [len(s.split()) for s in sentences]
    avg_words = sum(word_counts) / len(word_counts)

    # Penalty for run-on sentences (avg > 35 words)
    if avg_words > 35:
        length_penalty = 0.5
    elif avg_words > 25:
        length_penalty = 0.8
    else:
        length_penalty = 1.0

    # Filler words penalty
    fillers = ["um", "uh", "basically", "literally", "you know", "like,", "stuff"]
    filler_count = sum(answer.lower().count(f) for f in fillers)
    filler_penalty = max(0.0, 1.0 - filler_count * 0.1)

    return 0.6 * length_penalty + 0.4 * filler_penalty


# ─────────────────────────────────────────────────────────────
# MAIN GRADER
# ─────────────────────────────────────────────────────────────

def grade(answer: str, task: Dict) -> Dict:
    """
    Grade a candidate answer against a task definition.

    Returns
    -------
    dict with keys:
        score        – final float [0.0, 1.0]
        breakdown    – sub-scores dict
        detail       – human-readable explanation
    """
    rubric     = task["rubric"]
    keywords   = task.get("keywords", [])
    difficulty = task.get("difficulty", "medium")

    kw_score   = keyword_score(answer, keywords)
    exp_score  = explanation_score(answer, difficulty)
    clar_score = clarity_score(answer)

    final = (
        kw_score   * rubric["keyword_weight"] +
        exp_score  * rubric["explanation_weight"] +
        clar_score * rubric["clarity_weight"]
    )
    final = round(min(max(final, 0.0), 1.0), 4)

    breakdown = {
        "keyword_score":     round(kw_score,   4),
        "explanation_score": round(exp_score,  4),
        "clarity_score":     round(clar_score, 4),
        "weights": rubric,
    }

    # Human-readable verdict
    if final >= 0.85:
        verdict = "Excellent answer ✅"
    elif final >= 0.70:
        verdict = "Good answer ⚠️  (room for improvement)"
    elif final >= 0.50:
        verdict = "Acceptable but weak ⚠️"
    else:
        verdict = "Poor answer ❌"

    detail = (
        f"{verdict}\n"
        f"  Keywords matched : {kw_score*100:.1f}%  "
        f"({sum(1 for kw in keywords if kw.lower() in answer.lower())}/{len(keywords)})\n"
        f"  Explanation depth: {exp_score*100:.1f}%\n"
        f"  Clarity          : {clar_score*100:.1f}%\n"
        f"  ─────────────────────────────\n"
        f"  FINAL SCORE      : {final:.4f}"
    )

    return {"score": final, "breakdown": breakdown, "detail": detail}
