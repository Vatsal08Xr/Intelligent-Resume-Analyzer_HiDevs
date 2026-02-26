from dataclasses import dataclass, asdict


@dataclass
class Candidate:
    name: str
    email: str
    phone: str
    location: str
    education: list
    roles: list
    certifications: list
    skills: dict
    experience_years: int
    quality_assessment: dict

    def to_dict(self):
        return asdict(self)