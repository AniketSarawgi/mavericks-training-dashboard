#!/usr/bin/env python3
"""
Assessment Agent CLI - Mavericks Training Dashboard
Phase 1 Prototype

This CLI demonstrates the core Assessment Agent functionality:
- Automated quiz evaluation with AI feedback
- Code challenge assessment and review
- Assignment grading with detailed feedback
- Performance analytics and recommendations
"""

import json
import os
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Any
import sqlite3
from dataclasses import dataclass, asdict
from enum import Enum


# Simulating AI integration (replace with actual OpenAI/LangChain in
# production)
class MockAI:
    """Mock AI service for demonstration purposes"""

    @staticmethod
    def evaluate_quiz(question: str, correct_answer: str,
                      user_answer: str) -> Dict:
        """Simulate AI-powered quiz evaluation"""
        is_correct = (correct_answer.lower().strip() == user_answer.lower().
                      strip())

        if is_correct:
            feedback = (f"Excellent! Your answer '{user_answer}' is correct. "
                        f"This demonstrates good understanding of the "
                        f"concept.")
        else:
            feedback = (f"Not quite right. You answered '{user_answer}' but "
                        f"the correct answer is '{correct_answer}'. Here's "
                        f"why: This concept is fundamental to understanding "
                        f"the underlying principles.")

        return {
            "is_correct": is_correct,
            "score": 100 if is_correct else 0,
            "feedback": feedback,
            "improvement_tip": "Review the related documentation and "
                               "practice similar problems."
        }

    @staticmethod
    def review_code(code: str, problem_description: str) -> Dict:
        """Simulate AI-powered code review"""
        # Simple heuristic-based evaluation for demo
        score = 70  # Base score
        feedback_points = []

        if "def " in code or "function" in code:
            score += 10
            feedback_points.append("✓ Good use of functions")

        if "class " in code:
            score += 10
            feedback_points.append("✓ Object-oriented approach detected")

        if "#" in code or '"""' in code:
            score += 5
            feedback_points.append("✓ Code includes comments/documentation")

        if len(code.split('\n')) > 20:
            score += 5
            feedback_points.append("✓ Comprehensive solution")

        if "import" in code:
            score += 5
            feedback_points.append("✓ Proper use of libraries")

        feedback = "AI Code Review Analysis:\n" + "\n".join(feedback_points)
        feedback += (f"\n\nOverall Assessment: The code demonstrates "
                     f"{'excellent' if score >= 85 else 'good' if score >= 70 else 'basic'} programming skills.")
        return {
            "score": min(score, 100),
            "feedback": feedback,
            "suggestions": [
                "Consider adding error handling",
                "Add more descriptive variable names",
                "Include unit tests for better reliability"
            ]
        }

    @staticmethod
    def analyze_performance(assessment_history: List[Dict]) -> Dict:
        """Generate performance analytics and recommendations"""
        if not assessment_history:
            return {"error": "No assessment data available"}

        scores = [a['score'] for a in assessment_history]
        avg_score = sum(scores) / len(scores)
        trend = "improving" if len(scores) > 1 and scores[-1] > scores[
            0] else "stable"

        strengths = []
        weaknesses = []

        # Analyze by assessment type
        quiz_scores = [a['score'] for a in assessment_history if
                       a['type'] == 'quiz']
        code_scores = [a['score'] for a in assessment_history if
                       a['type'] == 'code']

        if quiz_scores and sum(quiz_scores) / len(quiz_scores) > 80:
            strengths.append("Strong theoretical knowledge")
        elif quiz_scores:
            weaknesses.append("Needs improvement in theoretical concepts")

        if code_scores and sum(code_scores) / len(code_scores) > 80:
            strengths.append("Excellent coding skills")
        elif code_scores:
            weaknesses.append("Needs more coding practice")

        recommendations = []
        if avg_score < 70:
            recommendations.append("Focus on fundamental concepts")
            recommendations.append("Allocate more time for practice")
        elif avg_score < 85:
            recommendations.append("Work on advanced topics")
            recommendations.append("Practice more complex problems")
        else:
            recommendations.append(
                "Excellent progress! Focus on specialization")
            recommendations.append("Consider mentoring other learners")

        return {
            "average_score": round(avg_score, 2),
            "trend": trend,
            "total_assessments": len(assessment_history),
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations
        }


class AssessmentType(Enum):
    QUIZ = "quiz"
    CODE = "code"
    ASSIGNMENT = "assignment"


@dataclass
class Assessment:
    id: str
    fresher_id: str
    type: AssessmentType
    content: Dict
    score: float
    feedback: str
    timestamp: str


class AssessmentDatabase:
    """Simple SQLite database for storing assessment data"""

    def __init__(self, db_path: str = "assessments.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assessments (
                id TEXT PRIMARY KEY,
                fresher_id TEXT NOT NULL,
                type TEXT NOT NULL,
                content TEXT NOT NULL,
                score REAL NOT NULL,
                feedback TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS freshers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                department TEXT,
                created_at TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def save_assessment(self, assessment: Assessment):
        """Save assessment to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO assessments 
            (id, fresher_id, type, content, score, feedback, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            assessment.id,
            assessment.fresher_id,
            assessment.type.value,
            json.dumps(assessment.content),
            assessment.score,
            assessment.feedback,
            assessment.timestamp
        ))

        conn.commit()
        conn.close()

    def get_assessments(self, fresher_id: str = None) -> List[Dict]:
        """Retrieve assessments from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if fresher_id:
            cursor.execute('''
                SELECT * FROM assessments WHERE fresher_id = ?
                ORDER BY timestamp DESC
            ''', (fresher_id,))
        else:
            cursor.execute('SELECT * FROM assessments ORDER BY timestamp DESC')

        rows = cursor.fetchall()
        conn.close()

        assessments = []
        for row in rows:
            assessments.append({
                'id': row[0],
                'fresher_id': row[1],
                'type': row[2],
                'content': json.loads(row[3]),
                'score': row[4],
                'feedback': row[5],
                'timestamp': row[6]
            })

        return assessments

    def add_fresher(self, fresher_id: str, name: str, email: str,
                    department: str = "General"):
        """Add a new fresher to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO freshers (id, name, email, department, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (fresher_id, name, email, department, datetime.now().isoformat()))

        conn.commit()
        conn.close()


class AssessmentAgent:
    """Main Assessment Agent class"""

    def __init__(self):
        self.db = AssessmentDatabase()
        self.ai = MockAI()

    def conduct_quiz(self, fresher_id: str, questions: List[Dict]) -> Dict:
        """Conduct a quiz assessment"""
        print(f"\n🎯 Starting Quiz Assessment for Fresher: {fresher_id}")
        print("=" * 50)

        total_score = 0
        detailed_feedback = []

        for i, question in enumerate(questions, 1):
            print(f"\nQuestion {i}: {question['question']}")
            if question.get('options'):
                for j, option in enumerate(question['options'], 1):
                    print(f"  {j}. {option}")

            user_answer = input("Your answer: ").strip()

            # Get AI evaluation
            evaluation = self.ai.evaluate_quiz(
                question['question'],
                question['correct_answer'],
                user_answer
            )

            total_score += evaluation['score']
            detailed_feedback.append({
                'question': question['question'],
                'your_answer': user_answer,
                'correct_answer': question['correct_answer'],
                'feedback': evaluation['feedback']
            })

            print(f"✓ Score: {evaluation['score']}/100")
            print(f"💡 {evaluation['feedback']}")

        avg_score = total_score / len(questions)

        # Save assessment
        assessment = Assessment(
            id=f"quiz_{fresher_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            fresher_id=fresher_id,
            type=AssessmentType.QUIZ,
            content={'questions': questions, 'answers': detailed_feedback},
            score=avg_score,
            feedback=f"Quiz completed with {avg_score:.1f}% score",
            timestamp=datetime.now().isoformat()
        )

        self.db.save_assessment(assessment)

        return {
            'assessment_id': assessment.id,
            'score': avg_score,
            'detailed_feedback': detailed_feedback
        }

    def review_code_challenge(self, fresher_id: str, problem: str,
                              code: str) -> Dict:
        """Review a coding challenge submission"""
        print(f"\n💻 Code Challenge Review for Fresher: {fresher_id}")
        print("=" * 50)
        print(f"Problem: {problem}")
        print(f"\nSubmitted Code:\n{'-' * 30}")
        print(code)
        print("-" * 30)

        # Get AI code review
        review = self.ai.review_code(code, problem)

        print(f"\n📊 Score: {review['score']}/100")
        print(f"\n📝 Feedback:\n{review['feedback']}")
        print(f"\n💡 Suggestions:")
        for suggestion in review['suggestions']:
            print(f"  • {suggestion}")

        # Save assessment
        assessment = Assessment(
            id=f"code_{fresher_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            fresher_id=fresher_id,
            type=AssessmentType.CODE,
            content={'problem': problem, 'code': code, 'review': review},
            score=review['score'],
            feedback=review['feedback'],
            timestamp=datetime.now().isoformat()
        )

        self.db.save_assessment(assessment)

        return {
            'assessment_id': assessment.id,
            'score': review['score'],
            'feedback': review['feedback'],
            'suggestions': review['suggestions']
        }

    def generate_performance_report(self, fresher_id: str) -> Dict:
        """Generate comprehensive performance report"""
        print(f"\n📈 Performance Report for Fresher: {fresher_id}")
        print("=" * 50)

        assessments = self.db.get_assessments(fresher_id)

        if not assessments:
            print("❌ No assessment data found for this fresher.")
            return {'error': 'No data available'}

        # Get AI analysis
        analysis = self.ai.analyze_performance(assessments)

        print(f"\n📊 Overall Statistics:")
        print(f"  • Total Assessments: {analysis['total_assessments']}")
        print(f"  • Average Score: {analysis['average_score']}%")
        print(f"  • Performance Trend: {analysis['trend']}")

        print(f"\n💪 Strengths:")
        for strength in analysis['strengths']:
            print(f"  • {strength}")

        if analysis['weaknesses']:
            print(f"\n⚠️  Areas for Improvement:")
            for weakness in analysis['weaknesses']:
                print(f"  • {weakness}")

        print(f"\n🎯 Recommendations:")
        for rec in analysis['recommendations']:
            print(f"  • {rec}")

        return analysis

    def list_assessments(self, fresher_id: str = None):
        """List all assessments"""
        assessments = self.db.get_assessments(fresher_id)

        if not assessments:
            print("❌ No assessments found.")
            return

        print(f"\n📋 Assessment History" + (
            f" for {fresher_id}" if fresher_id else ""))
        print("=" * 50)

        for assessment in assessments:
            print(f"\n🔸 ID: {assessment['id']}")
            print(f"   Type: {assessment['type'].upper()}")
            print(f"   Score: {assessment['score']:.1f}%")
            print(f"   Date: {assessment['timestamp'][:19]}")
            print(f"   Fresher: {assessment['fresher_id']}")


def load_sample_data():
    """Load sample quiz questions for demonstration"""
    return [
        {
            "question": "What is the primary purpose of version control "
                        "systems like Git?",
            "options": [
                "To compile code",
                "To track changes in source code",
                "To run tests",
                "To deploy applications"
            ],
            "correct_answer": "To track changes in source code"
        },
        {
            "question": "In object-oriented programming, what does "
                        "'inheritance' mean?",
            "correct_answer": "A class can inherit properties and methods "
                              "from another class"
        },
        {
            "question": "What does API stand for?",
            "correct_answer": "Application Programming Interface"
        }
    ]


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Assessment Agent CLI - Mavericks Training Dashboard")
    parser.add_argument('--fresher', '-f', help='Fresher ID',
                        required=False)

    subparsers = parser.add_subparsers(dest='command',
                                       help='Available commands')

    # Quiz command
    quiz_parser = subparsers.add_parser('quiz', help='Conduct quiz assessment')
    quiz_parser.add_argument('--fresher', '-f', help='Fresher ID',
                             required=True)

    # Code review command
    code_parser = subparsers.add_parser('code', help='Review code challenge')
    code_parser.add_argument('--fresher', '-f', help='Fresher ID',
                             required=True)
    code_parser.add_argument('--problem', '-p', help='Problem description',
                             required=True)
    code_parser.add_argument('--file', help='Code file path',
                             required=True)

    # Report command
    report_parser = subparsers.add_parser('report',
                                          help='Generate performance report')
    report_parser.add_argument('--fresher', '-f', help='Fresher ID',
                               required=True)

    # List command
    list_parser = subparsers.add_parser('list', help='List assessments')
    list_parser.add_argument('--fresher', '-f', help='Fresher ID (optional)')

    # Add fresher command
    add_parser = subparsers.add_parser('add-fresher', help='Add new fresher')
    add_parser.add_argument('--id', help='Fresher ID', required=True)
    add_parser.add_argument('--name', help='Fresher name', required=True)
    add_parser.add_argument('--email', help='Fresher email', required=True)
    add_parser.add_argument('--dept', help='Department', default='General')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    agent = AssessmentAgent()

    try:
        if args.command == 'quiz':
            questions = load_sample_data()
            result = agent.conduct_quiz(args.fresher, questions)
            print(
                f"\n✅ Quiz completed! Assessment ID: {result['assessment_id']}")

        elif args.command == 'code':
            if not os.path.exists(args.file):
                print(f"❌ Error: File '{args.file}' not found.")
                return

            with open(args.file, 'r') as f:
                code = f.read()

            result = agent.review_code_challenge(args.fresher, args.problem,
                                                 code)
            print(
                f"\n✅ Code review completed! Assessment ID: "
                f"{result['assessment_id']}")

        elif args.command == 'report':
            agent.generate_performance_report(args.fresher)

        elif args.command == 'list':
            agent.list_assessments(args.fresher)

        elif args.command == 'add-fresher':
            agent.db.add_fresher(args.id, args.name, args.email, args.dept)
            print(f"✅ Fresher {args.name} added successfully!")

    except KeyboardInterrupt:
        print("\n\n👋 Assessment Agent CLI terminated.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    print("🚀 Assessment Agent CLI - Mavericks Training Dashboard")
    print(
        "Phase 1 Prototype - Demonstrating AI-Powered Assessment Capabilities")
    print()

    main()
