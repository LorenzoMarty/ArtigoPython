from pydantic import BaseModel, Field
from typing import List, Optional

class Article(BaseModel):
    title: str
    english_title: str
    authors: List[str]
    advisor: str
    summary: str = Field(max_length=1500)
    keywords: List[str]
    abstract: str
    english_keywords: List[str]
    introduction: str
    materials_and_methods: str
    results_and_discussion: str
    conclusions: str
    acknowledgments: str
    references: List[str]


    @property
    def word_count(self):
        total_text = (
            (self.summary or "")
            + (self.abstract or "")
            + (self.introduction or "")
            + (self.materials_and_methods or "")
            + (self.results_and_discussion or "")
            + (self.conclusions or "")
            + (self.acknowledgments or "")
        )
        return len(total_text.split())
