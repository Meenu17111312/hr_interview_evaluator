from fastapi import FastAPI
from env import HRInterviewEnv
from typing import Optional, Dict

app = FastAPI()

env = HRInterviewEnv()


@app.post("/reset")
def reset(data: Optional[Dict] = None):
    data = data or {}
    task_id = data.get("task_id", None)

    obs = env.reset(task_id=task_id)

    return {
        "state": obs
    }


@app.post("/step")
def step(action: Dict):
    obs, reward, done, info = env.step(action)

    return {
        "state": obs,
        "reward": reward,
        "done": done,
        "info": info
    }


# ✅ VERY IMPORTANT (indent correct ah irukanum)
def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
