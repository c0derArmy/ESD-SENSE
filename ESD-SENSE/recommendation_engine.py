from typing import Dict, List

class RecommendationEngine:
    """
    Generates personalized intervention recommendations based on detected gaps.
    Provides actionable, specific suggestions for teachers and students.
    """
    
    def __init__(self):
        self.intervention_library = self._build_intervention_library()
    
    def generate_recommendations(self, analysis_results: Dict) -> List[Dict]:
        """
        Generate personalized recommendations based on analysis.
        
        Args:
            analysis_results: Dictionary from LearningGapDetector.analyze_student()
            
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        gaps = analysis_results['gaps']
        accuracy = analysis_results['accuracy']
        
        # Sort gaps by severity
        sorted_gaps = sorted(
            gaps.items(),
            key=lambda x: {'high': 3, 'medium': 2, 'low': 1}.get(x[1]['severity'], 0),
            reverse=True
        )
        
        for gap_name, gap_details in sorted_gaps:
            rec = self._create_recommendation(gap_name, gap_details, accuracy)
            if rec:
                recommendations.append(rec)
        
        # Add general recommendations if no specific gaps
        if not recommendations:
            recommendations.append(self._get_maintenance_recommendation())
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def _create_recommendation(self, gap_name: str, gap_details: Dict, accuracy: float) -> Dict:
        """Create a specific recommendation for a detected gap."""
        
        gap_type = gap_name.split('_')[0]
        
        if gap_type == 'concept':
            return self._recommend_concept_review(gap_name, gap_details)
        elif gap_type == 'confidence':
            return self._recommend_confidence_building(gap_details)
        elif gap_type == 'speed':
            return self._recommend_deliberate_practice(gap_details)
        
        return None
    
    def _recommend_concept_review(self, gap_name: str, gap_details: Dict) -> Dict:
        """Recommend focused topic review."""
        topic = gap_name.replace('concept_gap_', '').replace('_', ' ').title()
        
        return {
            'title': f'Focused {topic} Review',
            'description': gap_details['description'],
            'priority': gap_details['severity'].upper(),
            'practice_type': 'Structured Review + Practice',
            'target_topics': [topic],
            'duration': '2-3 days, 30-45 min daily',
            'expected_impact': 0.25,
            'steps': [
                f'1. Review key concepts in {topic}',
                f'2. Work through 5-7 example problems',
                f'3. Practice 10 similar problems',
                f'4. Take a quick assessment',
            ]
        }
    
    def _recommend_confidence_building(self, gap_details: Dict) -> Dict:
        """Recommend confidence-building exercises."""
        return {
            'title': 'Confidence & Clarity Building',
            'description': gap_details['description'],
            'priority': gap_details['severity'].upper(),
            'practice_type': 'Guided Problem-Solving',
            'target_topics': ['All covered topics'],
            'duration': '1-2 weeks, 20 min daily',
            'expected_impact': 0.20,
            'steps': [
                '1. Start with easier problems to build momentum',
                '2. Work through step-by-step solutions',
                '3. Write down reasoning before answering',
                '4. Review mistakes carefully',
                '5. Gradually increase difficulty',
            ]
        }
    
    def _recommend_deliberate_practice(self, gap_details: Dict) -> Dict:
        """Recommend slower, more careful practice."""
        return {
            'title': 'Deliberate, Focused Practice',
            'description': gap_details['description'],
            'priority': 'MEDIUM',
            'practice_type': 'Slow & Thoughtful Practice',
            'target_topics': ['Problem-solving strategy'],
            'duration': '1 week, 25 min daily',
            'expected_impact': 0.15,
            'steps': [
                '1. Set a timer for 3-5 minutes per problem',
                '2. Read the question carefully twice',
                '3. Plan your approach before answering',
                '4. Work through each step deliberately',
                '5. Double-check your answer',
            ]
        }
    
    def _get_maintenance_recommendation(self) -> Dict:
        """Recommend continued practice for students on track."""
        return {
            'title': 'Continued Practice & Advancement',
            'description': 'Student is performing well; continue with current pace',
            'priority': 'LOW',
            'practice_type': 'Regular Practice + Challenge',
            'target_topics': ['All topics'],
            'duration': 'Ongoing',
            'expected_impact': 0.10,
            'steps': [
                '1. Continue regular daily practice',
                '2. Try progressively harder problems',
                '3. Explore different problem types',
                '4. Help other students',
            ]
        }
    
    def _build_intervention_library(self) -> Dict:
        """Build library of intervention strategies."""
        return {
            'fractions': {
                'practice_problems': 15,
                'estimated_time': '45 minutes',
                'key_concepts': ['Numerator', 'Denominator', 'Simplification', 'Comparison']
            },
            'algebra': {
                'practice_problems': 12,
                'estimated_time': '60 minutes',
                'key_concepts': ['Variables', 'Equations', 'Solving', 'Substitution']
            },
            'geometry': {
                'practice_problems': 10,
                'estimated_time': '50 minutes',
                'key_concepts': ['Shapes', 'Area', 'Perimeter', 'Angles']
            }
        }
    
    def estimate_improvement_time(self, severity: str) -> str:
        """Estimate time needed to address a gap."""
        time_map = {
            'high': '2-3 weeks',
            'medium': '1-2 weeks',
            'low': '3-5 days'
        }
        return time_map.get(severity, '1 week')
