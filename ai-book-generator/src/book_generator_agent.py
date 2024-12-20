import os
import json
from langchain.agents import initialize_agent, Tool
from langchain.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

class BookGeneratorAgent:
    def __init__(self, config_path='../config.json'):
        # Load configuration
        with open(config_path, 'r') as config_file:
            self.config = json.load(config_file)
        
        # Configure Ollama LLM
        ollama_config = self.config['ollama']
        self.llm = Ollama(
            model=ollama_config.get('model', 'llama2'),
            base_url=ollama_config.get('url', 'http://localhost:11434')
        )
        
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        
        # Define tools for book generation workflow
        self.tools = [
            Tool(
                name="narrative_generator",
                func=self.generate_narrative,
                description="Generates book narrative based on user input and art style"
            ),
            Tool(
                name="chapter_expander",
                func=self.expand_chapter,
                description="Expands individual book chapters with more detail"
            )
        ]
        
        self.agent = initialize_agent(
            self.tools, 
            self.llm, 
            memory=self.memory,
            agent="conversational-react-description"
        )
    
    def generate_narrative(self, user_description: str, art_style: str):
        """Generate initial book narrative"""
        prompt = f"""
        Create a book narrative based on:
        - User Description: {user_description}
        - Art Style: {art_style}
        
        Generate a compelling story outline with:
        1. Main Characters
        2. Plot Structure
        3. Thematic Elements
        """
        return self.llm(prompt)
    
    def expand_chapter(self, chapter_outline: str):
        """Expand chapter with more narrative details"""
        prompt = f"""
        Expand this chapter outline into a detailed narrative:
        {chapter_outline}
        
        Add rich descriptions, dialogue, and character development.
        """
        return self.llm(prompt)
    
    def generate_book(self, user_description: str, art_style: str):
        """Complete book generation workflow"""
        narrative = self.generate_narrative(user_description, art_style)
        chapters = self.split_narrative_to_chapters(narrative)
        
        expanded_chapters = [
            self.expand_chapter(chapter) for chapter in chapters
        ]
        
        return {
            "narrative": narrative,
            "chapters": expanded_chapters
        }
    
    def split_narrative_to_chapters(self, narrative: str):
        """Split narrative into chapter outlines"""
        max_chapters = self.config['generation_settings'].get('max_chapters', 10)
        # Implement intelligent chapter splitting logic
        chapters = narrative.split('\n\n')[:max_chapters]
        return chapters

    def get_art_style_prompt(self, genre: str = None, custom_style: str = None):
        """
        Retrieve art style prompt based on genre or custom style
        
        Args:
            genre (str, optional): Book genre
            custom_style (str, optional): Custom art style
        
        Returns:
            str: Art style prompt
        """
        art_styles = self.config['art_styles']
        
        if custom_style and custom_style in art_styles['custom_styles']:
            return art_styles['custom_styles'][custom_style]
        
        if genre and genre.lower() in art_styles['genres']:
            genre_styles = art_styles['genres'][genre.lower()]
            return genre_styles[0]  # Return first style for the genre
        
        # Fallback to a default style
        return "Watercolor illustration with soft, blended colors"

# Example usage
if __name__ == "__main__":
    agent = BookGeneratorAgent()
    book = agent.generate_book(
        "A young programmer's journey", 
        agent.get_art_style_prompt(genre="sci-fi")
    )
    print(book)
