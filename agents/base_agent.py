from abc import ABC, abstractmethod
import openai
import os

class BaseAgent(ABC):
    def __init__(self):
        self.system_prompt = self._get_system_prompt()
    
    @abstractmethod
    def _get_system_prompt(self):
        """Return the specific system prompt for this agent type"""
        pass
    
    def query(self, context):
        """Query GPT with agent-specific system prompt and context"""
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"{self.system_prompt}\n\nInclude a section at the end titled '# Tasks' with a bullet-point list of specific, actionable tasks that need to be completed."},
                {"role": "user", "content": context}
            ],
            max_tokens=1000,
            temperature=0.7,
        )
        return response['choices'][0]['message']['content'].strip()
