from dataclasses import dataclass


@dataclass
class Job:
    skills: list
    min_experience: int
    weights: dict