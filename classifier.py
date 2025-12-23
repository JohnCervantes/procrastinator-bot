import re
from typing import Tuple

class ProgressClassifier:
    def __init__(self):
        # Strong action verbs that indicate completion/progress
        self.action_verbs = [
            'completed', 'finished', 'done', 'solved', 'built', 'made', 'created',
            'implemented', 'coded', 'developed', 'shipped', 'deployed', 'learned',
            'mastered', 'understood', 'studied', 'practiced', 'watched', 'read',
            'submitted', 'pushed', 'committed', 'merged', 'reviewed', 'debugged',
            'fixed', 'refactored', 'optimized', 'achieved', 'accomplished'
        ]
        
        # Progress indicators
        self.progress_patterns = [
            r'day \d+',
            r'week \d+',
            r'chapter \d+',
            r'assignment \d+',
            r'exercise \d+',
            r'problem \d+',
            r'lecture \d+',
            r'lesson \d+',
            r'part \d+',
            r'section \d+',
            r'\d+%',
            r'\d+/\d+',
        ]
        
        # Technology/learning context keywords
        self.context_keywords = [
            'javascript', 'python', 'java', 'c++', 'cpp', 'rust', 'go', 'typescript',
            'react', 'vue', 'angular', 'node', 'django', 'flask', 'spring',
            'algorithm', 'data structure', 'leetcode', 'hackerrank', 'codewars',
            'tutorial', 'course', 'video', 'documentation', 'docs', 'book',
            'assignment', 'homework', 'project', 'research', 'paper', 'article',
            'app', 'website', 'api', 'database', 'sql', 'mongodb',
            'machine learning', 'ml', 'ai', 'deep learning', 'neural network',
            'advent of code', 'aoc', 'fso', 'cs50', 'mooc'
        ]
        
        # Phrases that indicate NOT progress (future/planning/questions)
        self.disqualifiers = [
            r'\?',  # Questions
            r'will\s', r"i'll\s", r'gonna\s', r'going to\s',  # Future tense
            r"didn't\s", r"haven't\s", r"hasn't\s", r"couldn't\s", r"can't\s",  # Negations
            r'need to\s', r'want to\s', r'planning to\s', r'should\s', r'trying to\s',
            r'how do i\s', r'how to\s', r'help with\s', r'stuck on\s',
            r'tomorrow', r'next week', r'later', r'soon'
        ]
    
    def classify(self, message: str) -> Tuple[bool, float, str]:
        """
        Classify if a message is about progress.
        
        Returns:
            Tuple[bool, float, str]: (is_progress, confidence_score, reason)
        """
        original_message = message
        message = message.lower().strip()
        
        if not message:
            return False, 0.0, "Empty message"
        
        score = 0.0
        reasons = []
        
        # Check for disqualifiers first
        for pattern in self.disqualifiers:
            if re.search(pattern, message):
                return False, 0.0, f"Contains disqualifier: {pattern}"
        
        # Check for action verbs (strong signal)
        action_found = False
        for verb in self.action_verbs:
            if re.search(r'\b' + verb + r'\b', message):
                score += 0.4
                action_found = True
                reasons.append(f"action verb: '{verb}'")
                break
        
        # Check for progress patterns (strong signal)
        progress_pattern_found = False
        for pattern in self.progress_patterns:
            if re.search(pattern, message):
                score += 0.3
                progress_pattern_found = True
                reasons.append(f"progress pattern: {pattern}")
                break
        
        # Check for context keywords (moderate signal)
        context_count = 0
        for keyword in self.context_keywords:
            if keyword in message:
                context_count += 1
        
        if context_count > 0:
            score += min(0.3, context_count * 0.15)
            reasons.append(f"context keywords: {context_count}")
        
        # Bonus: phrases that strongly indicate progress
        strong_phrases = [
            'made progress', 'got done', 'worked on', 'spent time',
            'finally', 'successfully', 'managed to'
        ]
        
        for phrase in strong_phrases:
            if phrase in message:
                score += 0.2
                reasons.append(f"strong phrase: '{phrase}'")
                break
        
        # Decision threshold
        is_progress = score >= 0.5
        
        reason_str = ", ".join(reasons) if reasons else "No clear indicators"
        
        return is_progress, score, reason_str
    
    def classify_simple(self, message: str) -> bool:
        """Simple boolean classification without details."""
        is_progress, _, _ = self.classify(message)
        return is_progress


# Test function
def test_classifier():
    classifier = ProgressClassifier()
    
    test_messages = [
        # Expected: True (progress messages)
        "watched a video on javascript",
        "completed fso assignment 3",
        "day 5 of advent of code completed",
        "made an app using c++",
        "did some research on multithreading",
        "finished reading chapter 5",
        "solved 3 leetcode problems today",
        "pushed my project to github",
        "finally understood recursion!",
        "worked on my react app for 2 hours",
        
        # Expected: False (not progress)
        "what video should i watch?",
        "planning to complete assignment 3 tomorrow",
        "i will study javascript tonight",
        "need help with c++ pointers",
        "couldn't finish the assignment",
        "anyone know how to do problem 5?",
        "just chatting here",
        "hello everyone",
    ]
    
    print("Testing Progress Classifier\n" + "="*60)
    
    for msg in test_messages:
        is_progress, score, reason = classifier.classify(msg)
        status = "✓ PROGRESS" if is_progress else "✗ NOT PROGRESS"
        print(f"\n{status} (score: {score:.2f})")
        print(f"Message: {msg}")
        print(f"Reason: {reason}")


if __name__ == "__main__":
    test_classifier()