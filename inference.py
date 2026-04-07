"""
inference.py — HR Interview Evaluator Agent Runner (Hackathon-compliant)
"""

import os
from openai import OpenAI

from env import HRInterviewEnv


# ── Scoring Function ─────────────────────────────────────────

def get_ai_score(client, model, question: str, answer: str):
    """Advanced hybrid scoring (hackathon-ready)"""

    answer_lower = answer.lower()
    question_words = set(question.lower().split())
    answer_words = set(answer_lower.split())

    # --- KEYWORD MATCH ---
    common = question_words.intersection(answer_words)
    keyword_score = len(common) / len(question_words) if question_words else 0

    # --- LENGTH SCORE ---
    word_count = len(answer.split())
    length_score = min(word_count / 80, 1.0)

    # --- DEPTH SCORE ---
    depth_words = ["because", "example", "explain", "process", "method", "approach"]
    depth_score = sum(1 for w in depth_words if w in answer_lower) / len(depth_words)

    # --- CLARITY ---
    clarity_score = 1.0 if "." in answer else 0.7

    # --- BASE SCORE ---
    score = (
        0.5 * keyword_score +
        0.2 * length_score +
        0.2 * depth_score +
        0.1 * clarity_score
    )

    # --- ANTI-CHEATING ---
    if word_count > 200:
        score -= 0.1

    if keyword_score > 0.9 and length_score < 0.2:
        score -= 0.2

    # --- NORMALIZATION ---
    score = 0.4 + (0.6 * score)

    # --- FINAL ---
    score = round(min(max(score, 0.0), 1.0), 4)

    return score, keyword_score, length_score, depth_score


# ── Main Runner ─────────────────────────────────────────────

def run():
    client = OpenAI(
    api_key=os.getenv("HF_TOKEN", ""),
    base_url=os.getenv("API_BASE_URL", "https://api-inference.huggingface.co/v1"),
)

    model = os.getenv("MODEL_NAME", "meta-llama/Meta-Llama-3-8B-Instruct")

    env = HRInterviewEnv(shuffle=False)
    task_ids = [t["id"] for t in env.available_tasks()]
    diff_name = {1: "Easy", 2: "Medium", 3: "Hard"}

    print("Running HR Interview Evaluator...\n")

    total_score = 0.0

    for task_id in task_ids:
        obs = env.reset(task_id=task_id)

        # ✅ Get score + breakdown
        ai_score, keyword_score, length_score, depth_score = get_ai_score(
            client, model, obs["question"], obs["answer"]
        )

        _obs, reward, done, info = env.step({"score": ai_score})

        label = diff_name.get(task_id, f"Task {task_id}")

        # ✅ Debug print (now works)
        print(f"Task {task_id} ({label}) Score: {ai_score:.2f}")
        print(f" → keyword:{keyword_score:.2f}, length:{length_score:.2f}, depth:{depth_score:.2f}\n")

        total_score += ai_score

    final = total_score / len(task_ids)
    print(f"Final Average Score: {final:.2f}")


# ── Entry Point ─────────────────────────────────────────────

if __name__ == "__main__":
    run()
