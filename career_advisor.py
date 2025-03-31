import torch
import pandas as pd
import numpy as np
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import requests
import json
import os
from typing import List, Dict, Tuple, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Check for GPU availability
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {device}")

class CareerAdvisorAI:
    def __init__(self):
        logger.info("Initializing Career Advisor AI...")
        
        # Load BERT model and tokenizer
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased').to(device)
        
        # Load datasets
        self.load_datasets()
        
        # Define personality assessment questions
        self.personality_questions = self.generate_personality_questions()
        self.subject_interest_questions = self.generate_subject_interest_questions()
        
        logger.info("Career Advisor AI initialized successfully")
    
    def load_datasets(self):
        """Load and preprocess the required datasets"""
        logger.info("Loading datasets...")
        
        # In a real implementation, you would load the actual datasets
        # For this example, we'll create simplified mock datasets
        
        # Mock O*NET database for career recommendations
        self.onet_data = pd.DataFrame({
            'occupation': ['Software Developer', 'Data Scientist', 'Doctor', 'Teacher', 'Lawyer', 'Accountant'],
            'description': [
                'Develops applications and systems using programming languages',
                'Analyzes data and builds models to extract insights',
                'Diagnoses and treats medical conditions',
                'Educates students in various subjects',
                'Provides legal advice and represents clients',
                'Prepares and examines financial records'
            ],
            'personality_traits': [
                'analytical,creative,detail-oriented',
                'analytical,curious,technical',
                'compassionate,detail-oriented,patient',
                'patient,communicative,organized',
                'analytical,persuasive,detail-oriented',
                'detail-oriented,analytical,organized'
            ],
            'interests': [
                'programming,problem-solving,technology',
                'mathematics,statistics,technology',
                'biology,chemistry,helping others',
                'education,communication,mentoring',
                'debate,research,writing',
                'mathematics,business,organization'
            ],
            'education_required': [
                "Bachelor's degree in Computer Science",
                "Master's degree in Data Science or related field",
                "Medical Degree (MD)",
                "Bachelor's degree in Education",
                "Law Degree (JD)",
                "Bachelor's degree in Accounting"
            ]
        })
        
        # Mock College Scorecard data for university recommendations
        self.college_data = pd.DataFrame({
            'university': ['MIT', 'Stanford', 'Harvard', 'UC Berkeley', 'Georgia Tech', 'University of Michigan'],
            'location': ['Massachusetts', 'California', 'Massachusetts', 'California', 'Georgia', 'Michigan'],
            'programs': [
                'Computer Science,Engineering,Mathematics',
                'Computer Science,Business,Medicine',
                'Law,Business,Medicine',
                'Computer Science,Engineering,Business',
                'Engineering,Computer Science,Mathematics',
                'Engineering,Business,Medicine'
            ],
            'cost': [55000, 57000, 54000, 43000, 33000, 49000],
            'acceptance_rate': [0.07, 0.05, 0.05, 0.16, 0.21, 0.23],
            'graduation_rate': [0.94, 0.96, 0.97, 0.91, 0.87, 0.92]
        })
        
        # Mock study resources data
        self.resources_data = pd.DataFrame({
            'subject': ['Computer Science', 'Data Science', 'Medicine', 'Education', 'Law', 'Accounting'],
            'books': [
                'Introduction to Algorithms by Cormen et al.',
                'Python for Data Analysis by Wes McKinney',
                'Gray\'s Anatomy',
                'Teaching to Transgress by bell hooks',
                'Law 101 by Jay Feinman',
                'Financial Accounting by Warren et al.'
            ],
            'courses': [
                'CS50 (Harvard),Introduction to Computer Science (MIT)',
                'Data Science Specialization (Coursera),Machine Learning (Stanford)',
                'Introduction to Medicine (Coursera),Human Anatomy (edX)',
                'Teaching Methods (Coursera),Educational Psychology (edX)',
                'Introduction to Law (Coursera),Contract Law (edX)',
                'Financial Accounting (Coursera),Taxation Principles (edX)'
            ],
            'videos': [
                'https://www.youtube.com/c/MITOpenCourseWare',
                'https://www.youtube.com/c/3blue1brown',
                'https://www.youtube.com/c/osmosis',
                'https://www.youtube.com/c/edutopia',
                'https://www.youtube.com/c/LexFridman',
                'https://www.youtube.com/c/AccountingStuff'
            ]
        })
        
        logger.info("Datasets loaded successfully")
    
    def generate_personality_questions(self) -> List[Dict[str, Any]]:
        """Generate personality assessment questions"""
        return [
            {
                "id": "analytical",
                "question": "Do you enjoy solving complex problems and puzzles?",
                "trait": "analytical"
            },
            {
                "id": "creative",
                "question": "Do you often come up with unique ideas or solutions?",
                "trait": "creative"
            },
            {
                "id": "detail_oriented",
                "question": "Do you pay close attention to details and notice small errors?",
                "trait": "detail-oriented"
            },
            {
                "id": "patient",
                "question": "Are you patient when dealing with challenging situations?",
                "trait": "patient"
            },
            {
                "id": "communicative",
                "question": "Do you enjoy explaining concepts to others?",
                "trait": "communicative"
            },
            {
                "id": "organized",
                "question": "Do you prefer to have a structured plan for your activities?",
                "trait": "organized"
            },
            {
                "id": "persuasive",
                "question": "Are you good at convincing others of your point of view?",
                "trait": "persuasive"
            },
            {
                "id": "curious",
                "question": "Do you often seek to learn new things out of curiosity?",
                "trait": "curious"
            },
            {
                "id": "technical",
                "question": "Do you enjoy working with technology and learning how things work?",
                "trait": "technical"
            },
            {
                "id": "compassionate",
                "question": "Do you feel strongly about helping others in need?",
                "trait": "compassionate"
            }
        ]
    
    def generate_subject_interest_questions(self) -> List[Dict[str, Any]]:
        """Generate subject interest assessment questions"""
        return [
            {
                "id": "programming",
                "question": "How much do you enjoy programming or coding?",
                "subject": "programming"
            },
            {
                "id": "mathematics",
                "question": "How interested are you in mathematics and statistical analysis?",
                "subject": "mathematics"
            },
            {
                "id": "biology",
                "question": "How interested are you in biology and life sciences?",
                "subject": "biology"
            },
            {
                "id": "chemistry",
                "question": "How interested are you in chemistry and chemical processes?",
                "subject": "chemistry"
            },
            {
                "id": "education",
                "question": "How much do you enjoy teaching or explaining concepts to others?",
                "subject": "education"
            },
            {
                "id": "business",
                "question": "How interested are you in business and entrepreneurship?",
                "subject": "business"
            },
            {
                "id": "writing",
                "question": "How much do you enjoy writing and communication?",
                "subject": "writing"
            },
            {
                "id": "technology",
                "question": "How interested are you in technology and its applications?",
                "subject": "technology"
            },
            {
                "id": "helping_others",
                "question": "How important is it for you to directly help others in your career?",
                "subject": "helping others"
            },
            {
                "id": "research",
                "question": "How much do you enjoy conducting research and investigation?",
                "subject": "research"
            }
        ]
    
    def get_bert_embedding(self, text: str) -> np.ndarray:
        """Get BERT embedding for a given text"""
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Use the [CLS] token embedding as the sentence representation
        embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
        return embeddings[0]
    
    def assess_personality(self, answers: Dict[str, int]) -> Dict[str, float]:
        """
        Assess personality traits based on answers
        
        Args:
            answers: Dictionary mapping question IDs to scores (1-5)
        
        Returns:
            Dictionary mapping traits to scores
        """
        traits = {}
        for question in self.personality_questions:
            qid = question["id"]
            trait = question["trait"]
            if qid in answers:
                if trait not in traits:
                    traits[trait] = []
                traits[trait].append(answers[qid])
        
        # Average the scores for each trait
        trait_scores = {trait: sum(scores)/len(scores) for trait, scores in traits.items()}
        return trait_scores
    
    def assess_interests(self, answers: Dict[str, int]) -> Dict[str, float]:
        """
        Assess subject interests based on answers
        
        Args:
            answers: Dictionary mapping question IDs to scores (1-5)
        
        Returns:
            Dictionary mapping subjects to scores
        """
        interests = {}
        for question in self.subject_interest_questions:
            qid = question["id"]
            subject = question["subject"]
            if qid in answers:
                if subject not in interests:
                    interests[subject] = []
                interests[subject].append(answers[qid])
        
        # Average the scores for each interest
        interest_scores = {interest: sum(scores)/len(scores) for interest, scores in interests.items()}
        return interest_scores
    
    def recommend_careers(self, trait_scores: Dict[str, float], interest_scores: Dict[str, float], top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Recommend careers based on personality traits and interests
        
        Args:
            trait_scores: Dictionary mapping traits to scores
            interest_scores: Dictionary mapping interests to scores
            top_n: Number of top recommendations to return
            
        Returns:
            List of recommended careers with details
        """
        logger.info("Generating career recommendations...")
        
        # Calculate match scores for each occupation
        scores = []
        for _, row in self.onet_data.iterrows():
            occupation = row['occupation']
            traits = row['personality_traits'].split(',')
            interests = row['interests'].split(',')
            
            # Calculate trait match score
            trait_match = 0
            for trait in traits:
                if trait in trait_scores:
                    trait_match += trait_scores[trait]
            trait_match = trait_match / len(traits) if traits else 0
            
            # Calculate interest match score
            interest_match = 0
            for interest in interests:
                if interest in interest_scores:
                    interest_match += interest_scores[interest]
            interest_match = interest_match / len(interests) if interests else 0
            
            # Combined score (weighted average)
            combined_score = 0.4 * trait_match + 0.6 * interest_match
            
            scores.append({
                'occupation': occupation,
                'description': row['description'],
                'education_required': row['education_required'],
                'score': combined_score
            })
        
        # Sort by score and return top N
        scores.sort(key=lambda x: x['score'], reverse=True)
        return scores[:top_n]
    
    def recommend_universities(self, career_recommendations: List[Dict[str, Any]], top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Recommend universities based on career recommendations
        
        Args:
            career_recommendations: List of recommended careers
            top_n: Number of top recommendations to return
            
        Returns:
            List of recommended universities with details
        """
        logger.info("Generating university recommendations...")
        
        # Extract relevant fields from career recommendations
        recommended_fields = set()
        for career in career_recommendations:
            education = career['education_required']
            if "Computer Science" in education:
                recommended_fields.add("Computer Science")
            elif "Data Science" in education:
                recommended_fields.add("Data Science")
            elif "Medical" in education:
                recommended_fields.add("Medicine")
            elif "Education" in education:
                recommended_fields.add("Education")
            elif "Law" in education:
                recommended_fields.add("Law")
            elif "Accounting" in education:
                recommended_fields.add("Accounting")
            elif "Engineering" in education:
                recommended_fields.add("Engineering")
            elif "Business" in education:
                recommended_fields.add("Business")
        
        # Calculate match scores for each university
        scores = []
        for _, row in self.college_data.iterrows():
            university = row['university']
            programs = set(row['programs'].split(','))
            
            # Calculate program match score
            program_match = len(programs.intersection(recommended_fields)) / len(recommended_fields) if recommended_fields else 0
            
            # Other factors (could be weighted based on user preferences)
            cost_score = 1 - (row['cost'] / 60000)  # Normalize cost (lower is better)
            acceptance_score = row['acceptance_rate']  # Higher acceptance rate is better for accessibility
            graduation_score = row['graduation_rate']  # Higher graduation rate is better
            
            # Combined score (weighted average)
            combined_score = 0.5 * program_match + 0.2 * cost_score + 0.1 * acceptance_score + 0.2 * graduation_score
            
            scores.append({
                'university': university,
                'location': row['location'],
                'programs': row['programs'],
                'cost': row['cost'],
                'acceptance_rate': row['acceptance_rate'],
                'graduation_rate': row['graduation_rate'],
                'score': combined_score
            })
        
        # Sort by score and return top N
        scores.sort(key=lambda x: x['score'], reverse=True)
        return scores[:top_n]
    
    def generate_study_plan(self, major: str) -> Dict[str, Any]:
        """
        Generate a study plan for a given major
        
        Args:
            major: The major to generate a study plan for
            
        Returns:
            Dictionary containing study plan details
        """
        logger.info(f"Generating study plan for {major}...")
        
        # Find the closest matching subject in our resources data
        major_embedding = self.get_bert_embedding(major)
        subject_embeddings = {}
        
        for subject in self.resources_data['subject']:
            subject_embedding = self.get_bert_embedding(subject)
            subject_embeddings[subject] = subject_embedding
        
        # Calculate similarity scores
        similarities = {}
        for subject, embedding in subject_embeddings.items():
            similarity = cosine_similarity([major_embedding], [embedding])[0][0]
            similarities[subject] = similarity
        
        # Get the most similar subject
        best_match = max(similarities.items(), key=lambda x: x[1])[0]
        
        # Get resources for the best matching subject
        resources = self.resources_data[self.resources_data['subject'] == best_match].iloc[0]
        
        # Create a study plan
        study_plan = {
            "major": major,
            "matched_subject": best_match,
            "resources": {
                "books": resources['books'].split(','),
                "courses": resources['courses'].split(','),
                "videos": resources['videos']
            },
            "study_timeline": {
                "year_1": {
                    "focus": "Fundamentals",
                    "courses": ["Introduction to " + best_match, "Basic Principles"],
                    "projects": ["Simple application of concepts"]
                },
                "year_2": {
                    "focus": "Core Concepts",
                    "courses": ["Intermediate " + best_match, "Specialized Topics"],
                    "projects": ["More complex application of concepts"]
                },
                "year_3": {
                    "focus": "Advanced Topics",
                    "courses": ["Advanced " + best_match, "Research Methods"],
                    "projects": ["Independent research project"]
                },
                "year_4": {
                    "focus": "Specialization",
                    "courses": ["Specialized Electives", "Capstone Project"],
                    "projects": ["Comprehensive capstone project"]
                }
            }
        }
        
        return study_plan
    
    def run_assessment(self) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
        """
        Run the full assessment process
        
        Returns:
            Tuple containing personality traits, career recommendations, and university recommendations
        """
        logger.info("Starting assessment process...")
        
        # In a real implementation, this would interact with the user
        # For this example, we'll simulate user responses
        
        # Simulate personality question answers (1-5 scale)
        personality_answers = {
            "analytical": 4,
            "creative": 3,
            "detail_oriented": 5,
            "patient": 2,
            "communicative": 3,
            "organized": 4,
            "persuasive": 2,
            "curious": 5,
            "technical": 5,
            "compassionate": 3
        }
        
        # Simulate subject interest answers (1-5 scale)
        interest_answers = {
            "programming": 5,
            "mathematics": 4,
            "biology": 2,
            "chemistry": 2,
            "education": 3,
            "business": 3,
            "writing": 2,
            "technology": 5,
            "helping_others": 3,
            "research": 4
        }
        
        # Assess personality and interests
        trait_scores = self.assess_personality(personality_answers)
        interest_scores = self.assess_interests(interest_answers)
        
        # Generate recommendations
        career_recommendations = self.recommend_careers(trait_scores, interest_scores)
        university_recommendations = self.recommend_universities(career_recommendations)
        
        # Generate study plan for the top career recommendation
        top_career = career_recommendations[0]['occupation']
        study_plan = self.generate_study_plan(top_career)
        
        return trait_scores, career_recommendations, university_recommendations, study_plan
    
    def chat_interface(self):
        """
        Simple command-line chat interface for the career advisor
        """
        print("Welcome to the Career Advisor AI!")
        print("I'll help you find the right university and career path.")
        print("Let's start with some questions to understand your personality and interests.")
        
        personality_answers = {}
        interest_answers = {}
        
        # Ask personality questions
        print("\n--- Personality Assessment ---")
        for question in self.personality_questions:
            while True:
                try:
                    answer = int(input(f"{question['question']} (1-5, where 1=Not at all, 5=Very much): "))
                    if 1 <= answer <= 5:
                        personality_answers[question['id']] = answer
                        break
                    else:
                        print("Please enter a number between 1 and 5.")
                except ValueError:
                    print("Please enter a valid number.")
        
        # Ask interest questions
        print("\n--- Interest Assessment ---")
        for question in self.subject_interest_questions:
            while True:
                try:
                    answer = int(input(f"{question['question']} (1-5, where 1=Not interested, 5=Very interested): "))
                    if 1 <= answer <= 5:
                        interest_answers[question['id']] = answer
                        break
                    else:
                        print("Please enter a number between 1 and 5.")
                except ValueError:
                    print("Please enter a valid number.")
        
        # Assess personality and interests
        trait_scores = self.assess_personality(personality_answers)
        interest_scores = self.assess_interests(interest_answers)
        
        # Generate recommendations
        career_recommendations = self.recommend_careers(trait_scores, interest_scores)
        university_recommendations = self.recommend_universities(career_recommendations)
        
        # Display results
        print("\n--- Your Personality Traits ---")
        for trait, score in trait_scores.items():
            print(f"{trait.capitalize()}: {score:.2f}/5.00")
        
        print("\n--- Recommended Careers ---")
        for i, career in enumerate(career_recommendations, 1):
            print(f"{i}. {career['occupation']} (Match: {career['score']:.2f})")
            print(f"   Description: {career['description']}")
            print(f"   Education Required: {career['education_required']}")
            print()
        
        print("\n--- Recommended Universities ---")
        for i, university in enumerate(university_recommendations, 1):
            print(f"{i}. {university['university']} (Match: {university['score']:.2f})")
            print(f"   Location: {university['location']}")
            print(f"   Programs: {university['programs']}")
            print(f"   Annual Cost: ${university['cost']}")
            print(f"   Acceptance Rate: {university['acceptance_rate']*100:.1f}%")
            print(f"   Graduation Rate: {university['graduation_rate']*100:.1f}%")
            print()
        
        # Ask if user wants a study plan
        while True:
            major = input("\nEnter a major to get a study plan (or 'quit' to exit): ")
            if major.lower() == 'quit':
                break
            
            study_plan = self.generate_study_plan(major)
            
            print(f"\n--- Study Plan for {major} ---")
            print(f"Matched Subject: {study_plan['matched_subject']}")
            
            print("\nRecommended Resources:")
            print("Books:")
            for book in study_plan['resources']['books']:
                print(f"- {book}")
            
            print("\nCourses:")
            for course in study_plan['resources']['courses']:
                print(f"- {course}")
            
            print("\nVideos:")
            print(f"- {study_plan['resources']['videos']}")
            
            print("\nStudy Timeline:")
            for year, details in study_plan['study_timeline'].items():
                print(f"\n{year.replace('_', ' ').title()}:")
                print(f"Focus: {details['focus']}")
                print("Courses:")
                for course in details['courses']:
                    print(f"- {course}")
                print("Projects:")
                for project in details['projects']:
                    print(f"- {project}")

# Main execution
if __name__ == "__main__":
    advisor = CareerAdvisorAI()
    
    # Run the chat interface
    advisor.chat_interface()
    
    # Alternatively, run the automated assessment
    # trait_scores, career_recommendations, university_recommendations, study_plan = advisor.run_assessment()
    # print("Assessment complete!")

