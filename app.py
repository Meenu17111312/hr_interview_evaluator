from fastapi import FastAPI
from env import HRInterviewEnv

app = FastAPI()

env = HRInterviewEnv()

@app.post("/reset")
def reset():
    obs = env.reset()
    return obs

@app.post("/step")
def step(action: dict):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }
