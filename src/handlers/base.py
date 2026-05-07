from abc import ABC, abstractmethod
from playwright.sync_api import Page
from src.models.question import Question

class BaseHandler(ABC):
    @abstractmethod
    def execute(self, page: Page, question: Question):
        pass