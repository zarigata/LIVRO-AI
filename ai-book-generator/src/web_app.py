import streamlit as st
from book_generator_agent import BookGeneratorAgent
from image_generator import ImageGenerator
import base64

class BookGeneratorApp:
    def __init__(self):
        self.book_agent = BookGeneratorAgent()
        self.image_generator = ImageGenerator()
        
    def run(self):
        st.title("🌟 AI Book Generator")
        
        # Sidebar for user inputs
        st.sidebar.header("Book Configuration")
        
        # Photo upload for art style
        uploaded_file = st.sidebar.file_uploader(
            "Upload Reference Photo", 
            type=['png', 'jpg', 'jpeg']
        )
        
        # Book description input
        book_description = st.sidebar.text_area(
            "Describe Your Book Concept", 
            height=200
        )
        
        # Genre selection with predefined options from config
        genres = list(self.book_agent.config['art_styles']['genres'].keys())
        genre = st.sidebar.selectbox(
            "Select Book Genre", 
            genres
        )
        
        # Art style selection
        custom_styles = list(self.book_agent.config['art_styles']['custom_styles'].keys())
        custom_style = st.sidebar.selectbox(
            "Select Art Style (Optional)", 
            ["None"] + custom_styles
        )
        
        if st.sidebar.button("Generate Book"):
            with st.spinner("Generating your magical book..."):
                # Determine art style
                if uploaded_file:
                    art_style = self.image_generator.analyze_art_style(uploaded_file)
                elif custom_style != "None":
                    art_style = self.book_agent.get_art_style_prompt(custom_style=custom_style)
                else:
                    art_style = self.book_agent.get_art_style_prompt(genre=genre)
                
                # Generate book narrative
                book_data = self.book_agent.generate_book(
                    book_description, 
                    art_style
                )
                
                # Generate illustrations
                illustrations = [
                    self.image_generator.generate_illustration(
                        f"Illustration for chapter about {chapter[:50]}...",
                        art_style
                    ) for chapter in book_data['chapters']
                ]
                
                # Display results
                st.header("📖 Your Generated Book")
                
                # Display narrative
                st.subheader("Book Narrative")
                st.write(book_data['narrative'])
                
                # Display chapters
                st.subheader("Chapters")
                for i, chapter in enumerate(book_data['chapters'], 1):
                    st.markdown(f"### Chapter {i}")
                    st.write(chapter)
                    
                    # Display corresponding illustration
                    if i <= len(illustrations):
                        st.image(
                            illustrations[i-1], 
                            caption=f"Chapter {i} Illustration"
                        )
        
def main():
    app = BookGeneratorApp()
    app.run()

if __name__ == "__main__":
    main()
