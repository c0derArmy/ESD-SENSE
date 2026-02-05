import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

class LearningGapDetector:
    """
    Detects learning gaps in students based on question attempt patterns.
    Analyzes mistakes, timing, and conceptual weaknesses.
    """
    
    def __init__(self):
        self.gaps_detected = {}
        self.min_attempts_threshold = 3
        
    def analyze_student(self, student_df: pd.DataFrame) -> Dict:
        """
        Comprehensive analysis of a student's learning patterns.
        
        Args:
            student_df: DataFrame with student's question attempts
            
        Returns:
            Dictionary with detected gaps and metrics
        """
        
        if len(student_df) == 0:
            return self._empty_analysis()
        
        # Basic metrics
        total_attempts = len(student_df)
        correct_answers = (student_df['Correct'] == 1).sum()
        accuracy = correct_answers / total_attempts if total_attempts > 0 else 0
        avg_time = student_df['Time_Taken'].mean()
        
        # Detect different types of gaps
        concept_gaps = self._detect_concept_gaps(student_df)
        confidence_gaps = self._detect_confidence_gaps(student_df)
        speed_gaps = self._detect_speed_gaps(student_df)
        
        # Combine all gaps
        all_gaps = {**concept_gaps, **confidence_gaps, **speed_gaps}
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(
            accuracy, 
            len(all_gaps),
            student_df
        )
        
        return {
            'total_attempts': total_attempts,
            'correct_answers': correct_answers,
            'accuracy': accuracy,
            'avg_time': avg_time,
            'gaps': all_gaps,
            'overall_score': overall_score,
            'student_id': student_df['Student_ID'].iloc[0] if 'Student_ID' in student_df.columns else 'Unknown'
        }
    
    def _detect_concept_gaps(self, student_df: pd.DataFrame) -> Dict:
        """Detect conceptual misunderstandings through repeated mistakes."""
        gaps = {}
        
        # Group by topic
        if 'Topic' not in student_df.columns:
            return gaps
        
        for topic in student_df['Topic'].unique():
            topic_data = student_df[student_df['Topic'] == topic]
            topic_attempts = len(topic_data)
            
            if topic_attempts < self.min_attempts_threshold:
                continue
            
            topic_accuracy = (topic_data['Correct'] == 1).sum() / topic_attempts
            
            # Flag as concept gap if accuracy is low
            if topic_accuracy < 0.6:
                gaps[f'concept_gap_{topic.lower().replace(" ", "_")}'] = {
                    'severity': self._severity_from_accuracy(topic_accuracy),
                    'confidence': 1 - topic_accuracy,
                    'affected_questions': topic_attempts,
                    'description': f"Struggling with {topic}: {topic_accuracy:.1%} accuracy"
                }
        
        return gaps
    
    def _detect_confidence_gaps(self, student_df: pd.DataFrame) -> Dict:
        """Detect confidence issues through hesitation patterns."""
        gaps = {}
        
        # Analyze time patterns - too much time might indicate confusion
        avg_time = student_df['Time_Taken'].mean()
        high_time_attempts = student_df[student_df['Time_Taken'] > avg_time * 1.5]
        
        if len(high_time_attempts) > 0:
            high_time_wrong = (high_time_attempts['Correct'] == 0).sum()
            high_time_ratio = high_time_wrong / len(high_time_attempts)
            
            if high_time_ratio > 0.5:
                gaps['confidence_gap'] = {
                    'severity': 'medium' if high_time_ratio < 0.7 else 'high',
                    'confidence': high_time_ratio,
                    'affected_questions': len(high_time_attempts),
                    'description': f"Takes excessive time ({avg_time*1.5:.1f}s+) but still gets answers wrong"
                }
        
        return gaps
    
    def _detect_speed_gaps(self, student_df: pd.DataFrame) -> Dict:
        """Detect speed-related gaps."""
        gaps = {}
        
        # Fast but wrong answers indicate rushing or lack of understanding
        avg_time = student_df['Time_Taken'].mean()
        fast_attempts = student_df[student_df['Time_Taken'] < avg_time * 0.5]
        
        if len(fast_attempts) > 2:
            fast_wrong = (fast_attempts['Correct'] == 0).sum()
            fast_ratio = fast_wrong / len(fast_attempts)
            
            if fast_ratio > 0.4:
                gaps['speed_gap'] = {
                    'severity': 'medium',
                    'confidence': fast_ratio,
                    'affected_questions': len(fast_attempts),
                    'description': "Answers too quickly without careful consideration"
                }
        
        return gaps
    
    def _severity_from_accuracy(self, accuracy: float) -> str:
        """Convert accuracy to severity level."""
        if accuracy < 0.4:
            return 'high'
        elif accuracy < 0.7:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_overall_score(self, accuracy: float, num_gaps: int, df: pd.DataFrame) -> float:
        """Calculate overall performance score (0-1)."""
        # Base score from accuracy
        base_score = accuracy
        
        # Penalty for gaps
        gap_penalty = num_gaps * 0.1
        
        # Bonus for consistency
        if 'Time_Taken' in df.columns:
            time_std = df['Time_Taken'].std()
            time_mean = df['Time_Taken'].mean()
            consistency_bonus = 0.05 if time_std < time_mean * 0.5 else 0
        else:
            consistency_bonus = 0
        
        overall = max(0, min(1, base_score - gap_penalty + consistency_bonus))
        return overall
    
    def _empty_analysis(self) -> Dict:
        """Return empty analysis structure."""
        return {
            'total_attempts': 0,
            'correct_answers': 0,
            'accuracy': 0,
            'avg_time': 0,
            'gaps': {},
            'overall_score': 0,
            'student_id': 'Unknown'
        }
