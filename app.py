from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import torch
import os
import json
import logging
from career_advisor import CareerAdvisorAI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Check for GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {device}")

# Initialize Career Advisor AI
advisor = CareerAdvisorAI()

@app.route('/')
def index():
    """Landing page"""
    # Reset session data when starting fresh
    session.clear()
    return render_template('index.html')

@app.route('/assessment/personality', methods=['GET', 'POST'])
def personality_assessment():
    """Personality assessment page"""
    if request.method == 'POST':
        # Process form data
        personality_answers = {}
        for question in advisor.personality_questions:
            qid = question['id']
            if qid in request.form:
                try:
                    personality_answers[qid] = int(request.form[qid])
                except ValueError:
                    pass
        
        # Store in session
        session['personality_answers'] = personality_answers
        
        # Redirect to interest assessment
        return redirect(url_for('interest_assessment'))
    
    # GET request - show the form
    return render_template('personality_assessment.html', questions=advisor.personality_questions)

@app.route('/assessment/interests', methods=['GET', 'POST'])
def interest_assessment():
    """Interest assessment page"""
    # Check if personality assessment is completed
    if 'personality_answers' not in session:
        return redirect(url_for('personality_assessment'))
    
    if request.method == 'POST':
        # Process form data
        interest_answers = {}
        for question in advisor.subject_interest_questions:
            qid = question['id']
            if qid in request.form:
                try:
                    interest_answers[qid] = int(request.form[qid])
                except ValueError:
                    pass
        
        # Store in session
        session['interest_answers'] = interest_answers
        
        # Process assessments and generate recommendations
        personality_answers = session['personality_answers']
        
        # Assess personality and interests
        trait_scores = advisor.assess_personality(personality_answers)
        interest_scores = advisor.assess_interests(interest_answers)
        
        # Generate recommendations
        career_recommendations = advisor.recommend_careers(trait_scores, interest_scores)
        university_recommendations = advisor.recommend_universities(career_recommendations)
        
        # Store results in session
        session['trait_scores'] = trait_scores
        session['career_recommendations'] = career_recommendations
        session['university_recommendations'] = university_recommendations
        
        # Redirect to results page
        return redirect(url_for('results'))
    
    # GET request - show the form
    return render_template('interest_assessment.html', questions=advisor.subject_interest_questions)

@app.route('/results')
def results():
    """Results page showing recommendations"""
    # Check if assessments are completed
    if 'personality_answers' not in session or 'interest_answers' not in session:
        return redirect(url_for('personality_assessment'))
    
    # Get results from session
    trait_scores = session.get('trait_scores', {})
    career_recommendations = session.get('career_recommendations', [])
    university_recommendations = session.get('university_recommendations', [])
    
    return render_template('results.html', 
                          trait_scores=trait_scores,
                          career_recommendations=career_recommendations,
                          university_recommendations=university_recommendations)

@app.route('/study-plan', methods=['GET', 'POST'])
def study_plan():
    """Study plan generator page"""
    if request.method == 'POST':
        major = request.form.get('major', '')
        if major:
            study_plan = advisor.generate_study_plan(major)
            return render_template('study_plan.html', study_plan=study_plan, major=major)
    
    # Default - show form
    # If we have career recommendations, pre-populate with top recommendation
    career_recommendations = session.get('career_recommendations', [])
    suggested_major = career_recommendations[0]['occupation'] if career_recommendations else ''
    
    return render_template('study_plan_form.html', suggested_major=suggested_major)

@app.route('/api/generate-study-plan', methods=['POST'])
def api_generate_study_plan():
    """API endpoint for generating study plans"""
    data = request.json
    major = data.get('major', '')
    
    if not major:
        return jsonify({'error': 'Major is required'}), 400
    
    study_plan = advisor.generate_study_plan(major)
    return jsonify(study_plan)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)

