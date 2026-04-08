from env import HRInterviewEnv


def get_ai_score(question: str, answer: str):
    answer_lower = answer.lower()
    question_words = set(question.lower().split())
    answer_words = set(answer_lower.split())

    common = question_words.intersection(answer_words)
    keyword_score = len(common) / len(question_words) if question_words else 0

    word_count = len(answer.split())
    length_score = min(word_count / 80, 1.0)

    depth_words = ["because", "example", "explain", "process", "method", "approach"]
    depth_score = sum(1 for w in depth_words if w in answer_lower) / len(depth_words)

    clarity_score = 1.0 if "." in answer else 0.7

    score = (
        0.5 * keyword_score +
        0.2 * length_score +
        0.2 * depth_score +
        0.1 * clarity_score
    )

    if word_count > 200:
        score -= 0.1

    if keyword_score > 0.9 and length_score < 0.2:
        score -= 0.2

    score = 0.4 + (0.6 * score)
    score = round(min(max(score, 0.0), 1.0), 4)

    return score


def run():
    env = HRInterviewEnv(shuffle=False)
    tasks = env.available_tasks()

    for t in tasks:
        task_id = t["id"]

        print(f"[START] task={task_id}", flush=True)

        obs = env.reset(task_id=task_id)

        done = False
        steps = 0
        total_score = 0

        while not done:
            score = get_ai_score(obs["question"], obs["answer"])

            obs, reward, done, info = env.step({"score": score})

            steps += 1
            total_score += score

            print(f"[STEP] step={steps} reward={score}", flush=True)

        final_score = round(total_score / steps, 4)

        print(f"[END] task={task_id} score={final_score} steps={steps}", flush=True)


if __name__ == "__main__":
    run()
