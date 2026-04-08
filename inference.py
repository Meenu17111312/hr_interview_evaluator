import os
from openai import OpenAI
from env import HRInterviewEnv


def get_llm_score(client, model, question, answer):
    prompt = f"""
    Evaluate this answer for the question.

    Question: {question}
    Answer: {answer}

    Give a score between 0 and 1.
    Only return a number.
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )

        score = float(response.choices[0].message.content.strip())
        return max(0.0, min(score, 1.0))

    except:
        return 0.5  # fallback


def run():
    client = OpenAI(
        base_url=os.environ["API_BASE_URL"],
        api_key=os.environ["API_KEY"]
    )

    model = "gpt-4o-mini"

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
            score = get_llm_score(
                client,
                model,
                obs["question"],
                obs["answer"]
            )

            obs, reward, done, info = env.step({"score": score})

            steps += 1
            total_score += score

            print(f"[STEP] step={steps} reward={score}", flush=True)

        final_score = round(total_score / steps, 4)

        print(f"[END] task={task_id} score={final_score} steps={steps}", flush=True)


if __name__ == "__main__":
    run()
