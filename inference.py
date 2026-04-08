import os
from openai import OpenAI
from env import HRInterviewEnv


def get_llm_score(client, model, question, answer):
    prompt = f"""
Evaluate the answer for the given question.

Question: {question}
Answer: {answer}

Return ONLY a number between 0 and 1.
Do not return anything else.
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            timeout=20
        )

        text = response.choices[0].message.content.strip()

        # ✅ SAFE PARSING
        score = float(text.split()[0])

        return max(0.0, min(score, 1.0))

    except Exception as e:
        print(f"Error: {e}", flush=True)
        return 0.5


def run():
    client = OpenAI(
        base_url=os.environ["API_BASE_URL"],
        api_key=os.environ["API_KEY"]
    )

    # ✅ SAFE MODEL NAME
    model = os.environ.get("MODEL_NAME", "meta-llama/Meta-Llama-3-8B-Instruct")

    env = HRInterviewEnv(shuffle=False)
    tasks = env.available_tasks()

    for t in tasks:
        task_id = t["id"]

        print(f"[START] task={task_id}", flush=True)

        obs = env.reset(task_id=task_id)

        done = False
        steps = 0
        total_score = 0.0

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

        final_score = round(total_score / max(steps, 1), 4)

        print(f"[END] task={task_id} score={final_score} steps={steps}", flush=True)


if __name__ == "__main__":
    run()
