from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random

router = APIRouter(prefix="/quiz", tags=["quiz-api"])

# Quiz Question Model
class QuizQuestion(BaseModel):
    id: int
    question: str
    options: List[str]
    correct: int
    explanation: str
    difficulty: str
    category: str

class QuizAnswer(BaseModel):
    question_id: int
    selected_option: int

class QuizResult(BaseModel):
    total_questions: int
    correct_answers: int
    score_percentage: float
    grade: str
    answers: List[dict]

# Analytics Quiz Questions Database
ANALYTICS_QUESTIONS = [
    {
        "id": 1,
        "question": "What does EDA stand for in data analytics?",
        "options": ["Exploratory Data Analysis", "Enhanced Data Algorithm", "Extended Data Application", "Evaluated Data Approach"],
        "correct": 0,
        "explanation": "EDA stands for Exploratory Data Analysis - the process of analyzing data to understand patterns and insights.",
        "difficulty": "Easy",
        "category": "Fundamentals"
    },
    {
        "id": 2,
        "question": "Which metric is best for measuring user engagement?",
        "options": ["Page views only", "Session duration + interaction frequency", "Number of clicks", "Time on site only"],
        "correct": 1,
        "explanation": "Session duration combined with interaction frequency gives a comprehensive view of user engagement.",
        "difficulty": "Medium",
        "category": "Engagement"
    },
    {
        "id": 3,
        "question": "What is a good conversion rate for most websites?",
        "options": ["1-3%", "5-10%", "15-20%", "25-30%"],
        "correct": 0,
        "explanation": "Most websites see conversion rates between 1-3%, though this varies by industry.",
        "difficulty": "Medium",
        "category": "Metrics"
    },
    {
        "id": 4,
        "question": "Which visualization is best for showing trends over time?",
        "options": ["Pie chart", "Bar chart", "Line chart", "Scatter plot"],
        "correct": 2,
        "explanation": "Line charts are ideal for showing how values change over time periods.",
        "difficulty": "Easy",
        "category": "Visualization"
    },
    {
        "id": 5,
        "question": "What does CTR stand for?",
        "options": ["Click Through Rate", "Customer Total Revenue", "Content Transfer Rate", "Customer Tracking Report"],
        "correct": 0,
        "explanation": "CTR stands for Click Through Rate - the percentage of people who click on a specific link.",
        "difficulty": "Easy",
        "category": "Metrics"
    },
    {
        "id": 6,
        "question": "Which is NOT a common KPI for user engagement?",
        "options": ["Bounce rate", "Session duration", "CPU usage", "Pages per session"],
        "correct": 2,
        "explanation": "CPU usage is a technical metric, not a user engagement KPI.",
        "difficulty": "Easy",
        "category": "KPIs"
    },
    {
        "id": 7,
        "question": "What is A/B testing used for?",
        "options": ["Debugging code", "Comparing two versions", "Database optimization", "Server monitoring"],
        "correct": 1,
        "explanation": "A/B testing compares two versions to see which performs better.",
        "difficulty": "Medium",
        "category": "Testing"
    },
    {
        "id": 8,
        "question": "Which metric indicates user retention?",
        "options": ["New user count", "Returning visitor ratio", "Total page views", "Server response time"],
        "correct": 1,
        "explanation": "Returning visitor ratio shows how well you retain users over time.",
        "difficulty": "Medium",
        "category": "Retention"
    },
    {
        "id": 9,
        "question": "What is cohort analysis used for?",
        "options": ["Server performance", "User behavior over time", "Code quality", "Database speed"],
        "correct": 1,
        "explanation": "Cohort analysis tracks user behavior patterns over time for specific user groups.",
        "difficulty": "Hard",
        "category": "Analysis"
    },
    {
        "id": 10,
        "question": "Which tool is commonly used for web analytics?",
        "options": ["Microsoft Word", "Google Analytics", "Notepad", "Calculator"],
        "correct": 1,
        "explanation": "Google Analytics is the most widely used web analytics platform.",
        "difficulty": "Easy",
        "category": "Tools"
    },
    {
        "id": 11,
        "question": "What does DAU stand for in analytics?",
        "options": ["Daily Active Users", "Data Analysis Unit", "Digital Analytics Update", "Database Activity Usage"],
        "correct": 0,
        "explanation": "DAU stands for Daily Active Users - a key metric for measuring daily engagement.",
        "difficulty": "Medium",
        "category": "Metrics"
    },
    {
        "id": 12,
        "question": "Which statistical measure is best for understanding data distribution?",
        "options": ["Mean only", "Median and quartiles", "Mode only", "Range only"],
        "correct": 1,
        "explanation": "Median and quartiles provide the best understanding of data distribution, especially with outliers.",
        "difficulty": "Hard",
        "category": "Statistics"
    },
    {
        "id": 13,
        "question": "What is the primary purpose of data normalization?",
        "options": ["Increase data size", "Make data comparable", "Delete data", "Encrypt data"],
        "correct": 1,
        "explanation": "Data normalization makes different datasets comparable by scaling them to similar ranges.",
        "difficulty": "Medium",
        "category": "Data Processing"
    },
    {
        "id": 14,
        "question": "Which Python library is best for data visualization?",
        "options": ["requests", "matplotlib/seaborn", "json", "os"],
        "correct": 1,
        "explanation": "Matplotlib and Seaborn are the most popular Python libraries for data visualization.",
        "difficulty": "Easy",
        "category": "Tools"
    },
    {
        "id": 15,
        "question": "What does p-value indicate in statistical testing?",
        "options": ["Data size", "Significance level", "Average value", "Maximum value"],
        "correct": 1,
        "explanation": "P-value indicates the significance level and probability of obtaining results by chance.",
        "difficulty": "Hard",
        "category": "Statistics"
    }
]

@router.get("/questions", response_model=List[QuizQuestion])
async def get_quiz_questions(
    difficulty: Optional[str] = None,
    category: Optional[str] = None,
    limit: Optional[int] = 10
):
    """Get quiz questions with optional filtering"""
    try:
        questions = ANALYTICS_QUESTIONS.copy()
        
        # Filter by difficulty
        if difficulty:
            questions = [q for q in questions if q["difficulty"].lower() == difficulty.lower()]
        
        # Filter by category
        if category:
            questions = [q for q in questions if q["category"].lower() == category.lower()]
        
        # Randomize and limit
        random.shuffle(questions)
        questions = questions[:limit]
        
        return [QuizQuestion(**q) for q in questions]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching questions: {str(e)}")

@router.get("/categories")
async def get_quiz_categories():
    """Get all available quiz categories"""
    categories = list(set([q["category"] for q in ANALYTICS_QUESTIONS]))
    return {"categories": sorted(categories)}

@router.get("/difficulties")
async def get_quiz_difficulties():
    """Get all available difficulty levels"""
    difficulties = list(set([q["difficulty"] for q in ANALYTICS_QUESTIONS]))
    return {"difficulties": sorted(difficulties)}

@router.post("/submit", response_model=QuizResult)
async def submit_quiz(answers: List[QuizAnswer]):
    """Submit quiz answers and get results"""
    try:
        total_questions = len(answers)
        correct_answers = 0
        detailed_answers = []
        
        for answer in answers:
            # Find the question
            question = next((q for q in ANALYTICS_QUESTIONS if q["id"] == answer.question_id), None)
            
            if question:
                is_correct = answer.selected_option == question["correct"]
                if is_correct:
                    correct_answers += 1
                
                detailed_answers.append({
                    "question_id": answer.question_id,
                    "question": question["question"],
                    "selected_option": answer.selected_option,
                    "correct_option": question["correct"],
                    "is_correct": is_correct,
                    "explanation": question["explanation"],
                    "difficulty": question["difficulty"],
                    "category": question["category"]
                })
        
        score_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        # Determine grade
        if score_percentage >= 90:
            grade = "A+ (Excellent! 🏆)"
        elif score_percentage >= 80:
            grade = "A (Great Job! 🥇)"
        elif score_percentage >= 70:
            grade = "B+ (Good Work! 🥈)"
        elif score_percentage >= 60:
            grade = "B (Not Bad! 🥉)"
        elif score_percentage >= 50:
            grade = "C (Keep Learning! 📚)"
        else:
            grade = "F (Practice More! 💪)"
        
        return QuizResult(
            total_questions=total_questions,
            correct_answers=correct_answers,
            score_percentage=round(score_percentage, 1),
            grade=grade,
            answers=detailed_answers
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing quiz results: {str(e)}")

@router.get("/random")
async def get_random_question():
    """Get a single random question for quick testing"""
    try:
        question = random.choice(ANALYTICS_QUESTIONS)
        return QuizQuestion(**question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching random question: {str(e)}")

@router.get("/stats")
async def get_quiz_stats():
    """Get quiz statistics"""
    try:
        categories = {}
        difficulties = {}
        
        for q in ANALYTICS_QUESTIONS:
            cat = q["category"]
            diff = q["difficulty"]
            
            categories[cat] = categories.get(cat, 0) + 1
            difficulties[diff] = difficulties.get(diff, 0) + 1
        
        return {
            "total_questions": len(ANALYTICS_QUESTIONS),
            "categories": categories,
            "difficulties": difficulties,
            "average_options": sum(len(q["options"]) for q in ANALYTICS_QUESTIONS) / len(ANALYTICS_QUESTIONS)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching quiz stats: {str(e)}")
