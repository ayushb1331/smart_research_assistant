from transformers import pipeline
import re

class QASystem:
    def __init__(self, document_text):
        self.document_text = document_text
        self.qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
        self.questions = []

    def get_answer(self, question):
        result = self.qa_pipeline(question=question, context=self.document_text)
        answer = result['answer']
        return answer, f"Justified from context: \"{answer}\""

    def generate_questions(self, count=3):
        sentences = re.split(r'(?<=[.!?]) +', self.document_text)
        selected = sentences[:10]
        questions = []
        for i, sent in enumerate(selected[:count]):
            questions.append(f"What does the author mean by: '{sent[:80]}...' ?")
        self.questions = questions
        return questions