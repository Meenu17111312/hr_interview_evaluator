# hr_interview_evaluator
OpenEnv-compatible reinforcement learning environment that simulates real-world HR interview evaluation.
---
title: HR Interview Evaluator
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_file: inference.py
pinned: false
🎓 HR Interview Evaluator — OpenEnv
An OpenEnv-compatible reinforcement learning environment that simulates real-world HR interview evaluation.
This system uses a multi-factor reward modeling approach to evaluate candidate responses based on relevance, completeness, reasoning depth, and clarity — mimicking human interviewer judgment.
---
📁 Project Structure
```
hr_env/
├── env.py          # HRInterviewEnv — reset / step / state API
├── tasks.py        # 3 tasks: Easy / Medium / Hard
├── grader.py       # Keyword + Explanation + Clarity scorer
├── inference.py    # inference.py    # AI agent runner (hybrid scoring, no external API)
├── openenv.yaml    # Environment metadata
├── Dockerfile      # Container definition
└── README.md
```
---
🎮 Game Loop
```
reset()  →  state { question, answer }
               ↓
        AI predicts score
               ↓
step({ score })  →  reward + grader breakdown
```
---
⚙️ Environment API
`reset(task_id=None)`
Start a new episode. Returns a state dict:
```json
{
  "task_id":    1,
  "difficulty": "easy",
  "question":   "What is Python?",
  "answer":     "Python is a high-level..."
}
```
`step(action)`
Submit the AI's score prediction. `action = {"score": 0.85}`
Returns:
```json
{
  "reward":     0.96,
  "done":       true,
  "info": {
    "ai_score":      0.85,
    "ground_truth":  0.81,
    "error":         0.04,
    "grader_detail": "..."
  },
  "next_state": null
}
```
`state()`
Returns current state dict without consuming a step.
---
🏆 Reward Function
---
🧠 Advanced Reward Design
This environment uses a multi-factor reward modeling system to simulate realistic human evaluation.
Factors considered:
Keyword Relevance → Measures alignment with expected concepts
Answer Completeness → Based on response length and coverage
Explanation Depth → Detects reasoning (e.g., "because", "example")
Clarity → Ensures structured and readable responses
Anti-cheating Mechanisms:
Penalizes overly long answers (verbosity exploitation)
Penalizes keyword stuffing without meaningful explanation
Penalizes extremely short or incomplete responses
Normalization:
Scores are normalized using a baseline to reflect human evaluation bias.
---
---
🧪 Grader Logic
Multi-factor reward system:
Keyword relevance (semantic match)
Answer completeness (length-based scaling)
Explanation depth (reasoning detection)
Clarity (structure & readability)
🟢🟡🔴 Tasks
#	Difficulty	Question
1	🟢 Easy	What is Python?
2	🟡 Medium	Explain Machine Learning
3	🔴 Hard	Describe a challenging project you worked on
---
🚀 Quick Start
Python
```bash
cd hr_env
python inference.py
```
Docker
```bash
docker build -t hr-eval .
docker run --rm hr-eval
```
Use the env directly
```python
from env import HRInterviewEnv

env = HRInterviewEnv()
state = env.reset(task_id=1)
print(state["question"])

result = env.step({"score": 0.80})
print(result["reward"])
```
---
📊 Sample Output
```
══════════════════════════════════════════════════════════════
  🎓  HR INTERVIEW EVALUATOR — AI Agent Run
══════════════════════════════════════════════════════════════

📊 Example (Hybrid Scoring Output):

Task 1 (Easy) Score: 0.62  
→ keyword:0.33, length:0.47, depth:0.00  

Task 2 (Medium) Score: 0.77  
→ keyword:0.67, length:0.79, depth:0.17  

Final Average Score: 0.68
```
---
---
💡 Key Insight
Unlike traditional black-box evaluation, this system provides transparent and explainable scoring, making it suitable for real-world HR automation and AI evaluation pipelines.
---
📄 License
MIT
