"""
Demo script for PDF Text Summarizer
Shows the application in action with a sample text.
"""

import sys
from text_summarizer import TextSummarizer
from utils import format_duration, format_word_count


def demo_with_sample_text():
    """Demonstrate the summarizer with sample text."""
    print("PDF TEXT SUMMARIZER - DEMO")
    print("=" * 50)
    
    # Sample text (simulating extracted PDF content)
    sample_text = """
    Artificial Intelligence and Machine Learning: A Comprehensive Overview
    
    Introduction
    
    Artificial Intelligence (AI) and Machine Learning (ML) represent two of the most transformative 
    technologies of the 21st century. These fields have revolutionized numerous industries, from 
    healthcare and finance to transportation and entertainment. This document provides a comprehensive 
    overview of AI and ML, exploring their history, current applications, and future potential.
    
    Historical Development
    
    The concept of artificial intelligence dates back to ancient times, with myths and stories about 
    artificial beings. However, the modern field of AI began in the 1950s with the work of pioneers 
    like Alan Turing, who proposed the Turing Test as a measure of machine intelligence. The term 
    "artificial intelligence" was first coined by John McCarthy in 1956 at the Dartmouth Conference.
    
    Machine learning, as a subset of AI, emerged from the field of statistics and computer science. 
    Early developments included perceptrons in the 1950s and neural networks in the 1980s. The 
    breakthrough came with the advent of big data and increased computational power in the 2000s, 
    enabling the development of deep learning algorithms.
    
    Core Concepts and Technologies
    
    Artificial Intelligence encompasses several key areas:
    
    1. Machine Learning: Algorithms that learn from data without explicit programming
    2. Deep Learning: Neural networks with multiple layers for complex pattern recognition
    3. Natural Language Processing: Understanding and generating human language
    4. Computer Vision: Interpreting and analyzing visual information
    5. Robotics: Creating machines that can interact with the physical world
    
    Machine Learning Types
    
    Supervised Learning: Uses labeled training data to learn mapping functions
    Unsupervised Learning: Finds hidden patterns in data without labeled examples
    Reinforcement Learning: Learns through interaction with an environment and feedback
    
    Current Applications
    
    Healthcare: AI is transforming medical diagnosis, drug discovery, and personalized treatment plans. 
    Machine learning algorithms can analyze medical images, predict patient outcomes, and assist in 
    surgical procedures.
    
    Finance: Financial institutions use AI for fraud detection, algorithmic trading, credit scoring, 
    and risk assessment. These systems can process vast amounts of data in real-time to make 
    informed decisions.
    
    Transportation: Autonomous vehicles represent one of the most visible applications of AI. 
    Self-driving cars use computer vision, sensor fusion, and machine learning to navigate roads 
    safely.
    
    Technology Industry: Tech companies leverage AI for search engines, recommendation systems, 
    virtual assistants, and content moderation. These applications improve user experience and 
    automate routine tasks.
    
    Challenges and Limitations
    
    Despite significant progress, AI and ML face several challenges:
    
    Data Quality: Machine learning models depend heavily on high-quality, representative data
    Bias and Fairness: AI systems can perpetuate or amplify human biases present in training data
    Interpretability: Many AI models, especially deep learning, are "black boxes" that are difficult to interpret
    Privacy Concerns: AI systems often require large amounts of personal data
    Computational Requirements: Training sophisticated models requires significant computational resources
    
    Ethical Considerations
    
    The rapid advancement of AI raises important ethical questions about privacy, employment, 
    decision-making autonomy, and the potential for misuse. Organizations must consider these 
    implications when developing and deploying AI systems.
    
    Future Directions
    
    The future of AI and ML looks promising, with several emerging trends:
    
    Explainable AI: Developing models that can explain their decisions
    Edge Computing: Running AI models on local devices rather than cloud servers
    Quantum Machine Learning: Leveraging quantum computing for enhanced ML capabilities
    AI for Scientific Discovery: Using AI to accelerate research in various scientific fields
    
    Conclusion
    
    Artificial Intelligence and Machine Learning continue to evolve rapidly, offering unprecedented 
    opportunities for innovation and improvement across all sectors. While challenges remain, the 
    potential benefits of these technologies are immense. As we move forward, it will be crucial 
    to develop AI systems that are not only powerful but also ethical, fair, and beneficial to 
    humanity as a whole.
    
    The key to successful AI implementation lies in understanding both the technical capabilities 
    and the human implications of these technologies. By fostering collaboration between 
    technologists, ethicists, policymakers, and end-users, we can ensure that AI serves as a 
    force for positive change in our increasingly connected world.
    """
    
    print("Sample Text Analysis:")
    print(f"Original word count: {format_word_count(len(sample_text.split()))}")
    print(f"Character count: {len(sample_text):,}")
    
    # Initialize summarizer
    print("\nInitializing text summarizer...")
    print("Note: This demo requires an OpenAI API key.")
    print("Set your OPENAI_API_KEY environment variable or the demo will fail.")
    
    try:
        summarizer = TextSummarizer()
        print("✓ OpenAI client initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize OpenAI client: {str(e)}")
        print("Please set your OPENAI_API_KEY environment variable.")
        return
    
    # Create summary for 15-minute video
    print("Creating summary for 15-minute video...")
    result = summarizer.summarize_for_video(sample_text, target_duration_minutes=15)
    
    # Display results
    print("\n" + "=" * 50)
    print("SUMMARY RESULTS")
    print("=" * 50)
    
    print(f"Summary word count: {format_word_count(result['word_count'])}")
    print(f"Target word count: {format_word_count(result['target_word_count'])}")
    print(f"Estimated duration: {format_duration(result['estimated_duration_minutes'])}")
    print(f"Summarization method: {result.get('summarization_method', 'openai').upper()}")
    print(f"Compression ratio: {result['original_word_count'] / result['word_count']:.1f}:1")
    
    print("\nSUMMARY:")
    print("-" * 30)
    print(result['summary'])
    
    print("\nKEY POINTS:")
    print("-" * 30)
    for i, point in enumerate(result['key_points'], 1):
        print(f"{i}. {point}")
    
    print("\nKEY TOPICS:")
    print("-" * 30)
    for topic, count in result['key_topics']:
        print(f"• {topic} (mentioned {count} times)")
    
    if result['reading_metrics']:
        print("\nREADING METRICS:")
        print("-" * 30)
        metrics = result['reading_metrics']
        print(f"Flesch Reading Ease: {metrics.get('flesch_reading_ease', 'N/A'):.2f}")
        print(f"Flesch-Kincaid Grade: {metrics.get('flesch_kincaid_grade', 'N/A'):.2f}")
        print(f"Automated Readability Index: {metrics.get('automated_readability_index', 'N/A'):.2f}")
        print(f"Coleman-Liau Index: {metrics.get('coleman_liau_index', 'N/A'):.2f}")
    
    print("\n" + "=" * 50)
    print("DEMO COMPLETED")
    print("=" * 50)
    print("This demonstrates how the PDF Text Summarizer works.")
    print("To use with actual PDF files, run: python main.py your_document.pdf")


if __name__ == "__main__":
    try:
        demo_with_sample_text()
    except Exception as e:
        print(f"Demo failed: {str(e)}")
        sys.exit(1)
