import argparse
import logging
from career_advisor import CareerAdvisorAI
from data_processor import DataProcessor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main entry point for the Career Advisor AI application"""
    parser = argparse.ArgumentParser(description='Career Advisor AI')
    parser.add_argument('--prepare-data', action='store_true', help='Prepare datasets before running the advisor')
    parser.add_argument('--assessment-only', action='store_true', help='Run automated assessment without chat interface')
    args = parser.parse_args()
    
    logger.info("Starting Career Advisor AI application...")
    
    if args.prepare_data:
        logger.info("Preparing datasets...")
        processor = DataProcessor()
        datasets = processor.prepare_all_datasets()
        logger.info("Datasets prepared successfully")
    
    advisor = CareerAdvisorAI()
    
    if args.assessment_only:
        logger.info("Running automated assessment...")
        trait_scores, career_recommendations, university_recommendations, study_plan = advisor.run_assessment()
        
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
        
        print("\n--- Study Plan for Top Career ---")
        print(f"Major: {study_plan['major']}")
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
    else:
        # Run the interactive chat interface
        logger.info("Starting interactive chat interface...")
        advisor.chat_interface()
    
    logger.info("Career Advisor AI application completed")

if __name__ == "__main__":
    main()

