"""
env.py — HR Interview Evaluator Environment (OpenEnv-compliant)

OpenEnv strict format:
    reset() → observation (dict)
    step()  → (observation, reward, done, info)   ← standard RL tuple
    state() → current observation
"""

import random
from typing import Dict, Optional, Tuple

from pydantic import BaseModel, Field, field_validator

from tasks import TASKS
from grader import grade


# ── Pydantic Models ───────────────────────────────────────────

class Observation(BaseModel):
    task_id:    int
    difficulty: str
    question:   str
    answer:     str


class Action(BaseModel):
    score: float = Field(..., ge=0.0, le=1.0, description="AI quality score [0.0-1.0]")

    @field_validator("score")
    @classmethod
    def clamp(cls, v: float) -> float:
        return round(min(max(float(v), 0.0), 1.0), 4)


class StepInfo(BaseModel):
    task_id:        int
    difficulty:     str
    ai_score:       float
    ground_truth:   float
    expected_score: float
    error:          float
    grader_detail:  str
    breakdown:      dict


# ── Environment ───────────────────────────────────────────────

class HRInterviewEnv:
    """
    OpenEnv-compliant RL environment for HR interview answer evaluation.

    Observation : Observation model  (question + answer + metadata)
    Action      : Action model       (score: float 0.0-1.0)
    Reward      : float 0.0-1.0      (1 - |ai_score - ground_truth|)
    Episode     : single-step        (one Q&A pair per episode)
    """

    env_id      = "HRInterviewEvaluator-v1"
    version     = "1.0.0"
    action_space      = {"score": "float [0.0, 1.0]"}
    observation_space = {"task_id": "int", "difficulty": "str",
                         "question": "str", "answer": "str"}

    def __init__(self, shuffle: bool = False):
        self._tasks:        list           = TASKS.copy()
        self._shuffle:      bool           = shuffle
        self._task_index:   int            = 0
        self._current_task: Optional[Dict] = None
        self._done:         bool           = False
        self._episode:      int            = 0

    # ── OpenEnv Core API ──────────────────────────────────────

    def reset(self, task_id: Optional[int] = None) -> Dict:
        """Start a new episode. Returns observation dict."""
        if task_id is not None:
            task = next((t for t in self._tasks if t["id"] == task_id), None)
            if task is None:
                raise ValueError(f"No task with id={task_id}")
        elif self._shuffle:
            task = random.choice(self._tasks)
        else:
            task = self._tasks[self._task_index % len(self._tasks)]
            self._task_index += 1

        self._current_task = task
        self._done         = False
        self._episode     += 1

        return self._build_obs().model_dump()

    def step(self, action: Dict) -> Tuple[Dict, float, bool, Dict]:
        """
        Submit AI agent's score prediction.

        Parameters
        ----------
        action : {"score": float}

        Returns  -- strict OpenEnv tuple
        -------
        (observation, reward, done, info)
        """
        if self._current_task is None:
            raise RuntimeError("Call reset() before step().")
        if self._done:
            raise RuntimeError("Episode done. Call reset() for a new episode.")

        act          = Action(**action)
        grade_result = grade(self._current_task["answer"], self._current_task)
        ground_truth = grade_result["score"]
        expected     = self._current_task["expected_score"]

        error  = abs(act.score - ground_truth)
        reward = round(max(0.0, 1.0 - error), 4)

        self._done = True

        info = StepInfo(
            task_id        = self._current_task["id"],
            difficulty     = self._current_task["difficulty"],
            ai_score       = act.score,
            ground_truth   = ground_truth,
            expected_score = expected,
            error          = round(error, 4),
            grader_detail  = grade_result["detail"],
            breakdown      = grade_result["breakdown"],
        ).model_dump()

        observation = self._build_obs().model_dump()

        return observation, reward, self._done, info   # strict OpenEnv tuple

    def state(self) -> Dict:
        """Return current observation without stepping."""
        if self._current_task is None:
            return {}
        return self._build_obs().model_dump()

    def _build_obs(self) -> Observation:
        t = self._current_task
        return Observation(
            task_id    = t["id"],
            difficulty = t["difficulty"],
            question   = t["question"],
            answer     = t["answer"],
        )

    def available_tasks(self):
        return [
            {"id": t["id"], "difficulty": t["difficulty"], "question": t["question"]}
            for t in self._tasks
        ]

    def __repr__(self):
        return (f"<HRInterviewEnv env_id={self.env_id!r} "
                f"episode={self._episode} done={self._done}>")
