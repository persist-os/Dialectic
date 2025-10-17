"""
Context Analyzer
Analyzes events from Sentry to determine which agents are needed

This is the core intelligence layer that decides what agents to spawn
based on the context of code changes and events.
"""

from typing import Dict, List, Set
import re


class ContextAnalyzer:
    """
    Analyzes events to determine context and focus areas
    
    This is the brain that decides which specialized agents to spawn
    based on file paths, commit messages, and error patterns.
    """
    
    def __init__(self):
        """Initialize the context analyzer with keyword patterns"""
        
        # Security-related keywords
        self.security_keywords = {
            'auth', 'password', 'token', 'security', 'encrypt', 'decrypt',
            'permission', 'login', 'session', 'jwt', 'oauth', 'ssl', 'tls',
            'cors', 'csrf', 'xss', 'sql', 'injection', 'hash', 'salt',
            'private', 'secret', 'key', 'certificate', 'signature'
        }
        
        # MVP/Prototype keywords
        self.mvp_keywords = {
            'mvp', 'prototype', 'quick', 'rapid', 'hackathon', 'demo',
            'poc', 'proof of concept', 'minimal', 'basic', 'simple',
            'temporary', 'placeholder', 'mock', 'stub'
        }
        
        # Performance keywords
        self.performance_keywords = {
            'optimize', 'performance', 'speed', 'cache', 'async', 'await',
            'slow', 'latency', 'bottleneck', 'efficiency', 'memory',
            'cpu', 'load', 'scale', 'concurrent', 'parallel', 'thread',
            'queue', 'buffer', 'pool', 'connection'
        }
        
        # Documentation keywords
        self.documentation_keywords = {
            'readme', 'docs', 'documentation', 'guide', 'tutorial',
            'api', 'spec', 'schema', 'comment', 'explain', 'describe'
        }
        
        # Error-related patterns
        self.error_patterns = {
            'error', 'exception', 'fail', 'crash', 'bug', 'fix',
            'debug', 'trace', 'stack', 'log', 'warning', 'alert'
        }
        
        # File path patterns for context
        self.file_patterns = {
            'security': [
                r'.*auth.*', r'.*security.*', r'.*login.*', r'.*jwt.*',
                r'.*middleware.*', r'.*guard.*', r'.*permission.*'
            ],
            'performance': [
                r'.*optimize.*', r'.*cache.*', r'.*async.*', r'.*queue.*',
                r'.*pool.*', r'.*connection.*', r'.*database.*'
            ],
            'api': [
                r'.*api.*', r'.*endpoint.*', r'.*route.*', r'.*controller.*',
                r'.*handler.*', r'.*service.*'
            ],
            'frontend': [
                r'.*component.*', r'.*ui.*', r'.*view.*', r'.*template.*',
                r'.*css.*', r'.*scss.*', r'.*js.*', r'.*ts.*'
            ]
        }
    
    async def analyze_event(self, event_data: Dict) -> Dict:
        """
        Analyze an event and determine what context it represents
        
        Args:
            event_data: Event data from Sentry or simulator
                - files: List of file paths
                - message: Commit/event message
                - errors: List of errors (if any)
        
        Returns:
            Context analysis with focus areas and metadata
        """
        
        # Extract key information
        files_changed = event_data.get('files', [])
        commit_message = event_data.get('message', '')
        errors = event_data.get('errors', [])
        
        # Analyze different aspects
        analysis = {
            # Core focus areas
            'security_focus': self._check_security_context(files_changed, commit_message),
            'mvp_focus': self._check_mvp_context(commit_message),
            'performance_focus': self._check_performance_context(files_changed, commit_message),
            'documentation_focus': self._check_documentation_context(files_changed, commit_message),
            'error_focus': len(errors) > 0,
            
            # Metadata
            'files_changed': files_changed,
            'commit_message': commit_message,
            'error_count': len(errors),
            'file_types': self._analyze_file_types(files_changed),
            'complexity_score': self._calculate_complexity(files_changed, commit_message),
            
            # Confidence scores
            'confidence': {
                'security': self._calculate_security_confidence(files_changed, commit_message),
                'mvp': self._calculate_mvp_confidence(commit_message),
                'performance': self._calculate_performance_confidence(files_changed, commit_message)
            }
        }
        
        return analysis
    
    def _check_security_context(self, files: List[str], message: str) -> bool:
        """Check if this event has security implications"""
        
        # Check file paths
        files_text = ' '.join(files).lower()
        for pattern in self.file_patterns['security']:
            if re.search(pattern, files_text):
                return True
        
        # Check keywords in files and message
        text_to_check = files_text + ' ' + message.lower()
        return any(keyword in text_to_check for keyword in self.security_keywords)
    
    def _check_mvp_context(self, message: str) -> bool:
        """Check if this is MVP/prototype work"""
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in self.mvp_keywords)
    
    def _check_performance_context(self, files: List[str], message: str) -> bool:
        """Check if this event is performance-related"""
        
        # Check file paths
        files_text = ' '.join(files).lower()
        for pattern in self.file_patterns['performance']:
            if re.search(pattern, files_text):
                return True
        
        # Check keywords
        text_to_check = files_text + ' ' + message.lower()
        return any(keyword in text_to_check for keyword in self.performance_keywords)
    
    def _check_documentation_context(self, files: List[str], message: str) -> bool:
        """Check if this is documentation work"""
        
        files_text = ' '.join(files).lower()
        
        # Check for documentation files
        doc_extensions = ['.md', '.rst', '.txt', '.doc', '.docx']
        if any(file.endswith(tuple(doc_extensions)) for file in files):
            return True
        
        # Check keywords
        text_to_check = files_text + ' ' + message.lower()
        return any(keyword in text_to_check for keyword in self.documentation_keywords)
    
    def _analyze_file_types(self, files: List[str]) -> Dict[str, int]:
        """Analyze what types of files are being changed"""
        
        file_types = {
            'python': 0,
            'javascript': 0,
            'typescript': 0,
            'html': 0,
            'css': 0,
            'markdown': 0,
            'config': 0,
            'other': 0
        }
        
        for file_path in files:
            file_lower = file_path.lower()
            
            if file_lower.endswith(('.py', '.pyi')):
                file_types['python'] += 1
            elif file_lower.endswith(('.js', '.jsx')):
                file_types['javascript'] += 1
            elif file_lower.endswith(('.ts', '.tsx')):
                file_types['typescript'] += 1
            elif file_lower.endswith(('.html', '.htm')):
                file_types['html'] += 1
            elif file_lower.endswith(('.css', '.scss', '.sass')):
                file_types['css'] += 1
            elif file_lower.endswith(('.md', '.rst', '.txt')):
                file_types['markdown'] += 1
            elif file_lower.endswith(('.json', '.yaml', '.yml', '.toml', '.ini', '.cfg')):
                file_types['config'] += 1
            else:
                file_types['other'] += 1
        
        return file_types
    
    def _calculate_complexity(self, files: List[str], message: str) -> int:
        """Calculate a complexity score for the event"""
        
        score = 0
        
        # More files = more complex
        score += len(files) * 2
        
        # Longer message = more complex
        score += len(message.split()) * 0.5
        
        # Different file types = more complex
        file_types = self._analyze_file_types(files)
        unique_types = sum(1 for count in file_types.values() if count > 0)
        score += unique_types * 3
        
        # Security-related changes = more complex
        if self._check_security_context(files, message):
            score += 5
        
        # Performance changes = more complex
        if self._check_performance_context(files, message):
            score += 3
        
        return int(score)
    
    def _calculate_security_confidence(self, files: List[str], message: str) -> float:
        """Calculate confidence that this is security-related (0.0 to 1.0)"""
        
        confidence = 0.0
        
        # File path patterns
        files_text = ' '.join(files).lower()
        for pattern in self.file_patterns['security']:
            if re.search(pattern, files_text):
                confidence += 0.4
        
        # Keyword matches
        text_to_check = files_text + ' ' + message.lower()
        keyword_matches = sum(1 for keyword in self.security_keywords 
                             if keyword in text_to_check)
        confidence += min(keyword_matches * 0.1, 0.6)
        
        return min(confidence, 1.0)
    
    def _calculate_mvp_confidence(self, message: str) -> float:
        """Calculate confidence that this is MVP-related (0.0 to 1.0)"""
        
        message_lower = message.lower()
        keyword_matches = sum(1 for keyword in self.mvp_keywords 
                             if keyword in message_lower)
        
        return min(keyword_matches * 0.3, 1.0)
    
    def _calculate_performance_confidence(self, files: List[str], message: str) -> float:
        """Calculate confidence that this is performance-related (0.0 to 1.0)"""
        
        confidence = 0.0
        
        # File path patterns
        files_text = ' '.join(files).lower()
        for pattern in self.file_patterns['performance']:
            if re.search(pattern, files_text):
                confidence += 0.4
        
        # Keyword matches
        text_to_check = files_text + ' ' + message.lower()
        keyword_matches = sum(1 for keyword in self.performance_keywords 
                             if keyword in text_to_check)
        confidence += min(keyword_matches * 0.1, 0.6)
        
        return min(confidence, 1.0)
    
    def get_context_summary(self, analysis: Dict) -> str:
        """Get a human-readable summary of the context analysis"""
        
        focuses = []
        
        if analysis['security_focus']:
            confidence = analysis['confidence']['security']
            focuses.append(f"🔒 Security ({confidence:.1%})")
        
        if analysis['mvp_focus']:
            confidence = analysis['confidence']['mvp']
            focuses.append(f"🚀 MVP ({confidence:.1%})")
        
        if analysis['performance_focus']:
            confidence = analysis['confidence']['performance']
            focuses.append(f"⚡ Performance ({confidence:.1%})")
        
        if analysis['documentation_focus']:
            focuses.append("📚 Documentation")
        
        if analysis['error_focus']:
            focuses.append(f"🐛 Errors ({analysis['error_count']})")
        
        if not focuses:
            focuses.append("📝 General")
        
        complexity = analysis['complexity_score']
        complexity_desc = "Low" if complexity < 5 else "Medium" if complexity < 15 else "High"
        
        return f"{', '.join(focuses)} | Complexity: {complexity_desc} ({complexity})"


# Test the context analyzer
if __name__ == "__main__":
    import asyncio
    
    async def test_context_analyzer():
        """Test the context analyzer with different scenarios"""
        
        print("🧠 Testing Context Analyzer")
        print("=" * 50)
        
        analyzer = ContextAnalyzer()
        
        # Test scenarios
        test_scenarios = [
            {
                'name': 'Security Event',
                'event': {
                    'files': ['src/auth/jwt.py', 'src/middleware/auth.py'],
                    'message': 'Add JWT authentication with secure token handling',
                    'errors': []
                }
            },
            {
                'name': 'MVP Event',
                'event': {
                    'files': ['src/prototype/feature.py'],
                    'message': 'Quick MVP prototype for hackathon demo',
                    'errors': []
                }
            },
            {
                'name': 'Performance Event',
                'event': {
                    'files': ['src/api/optimize.py', 'src/cache/redis.py'],
                    'message': 'Optimize API response time with caching',
                    'errors': []
                }
            },
            {
                'name': 'Error Event',
                'event': {
                    'files': ['src/api/handler.py'],
                    'message': 'Fix TypeError in user handler',
                    'errors': [{'type': 'TypeError', 'count': 5}]
                }
            },
            {
                'name': 'Documentation Event',
                'event': {
                    'files': ['README.md', 'docs/api.md'],
                    'message': 'Update API documentation',
                    'errors': []
                }
            }
        ]
        
        for scenario in test_scenarios:
            print(f"\n🎭 {scenario['name']}:")
            print(f"   Files: {', '.join(scenario['event']['files'])}")
            print(f"   Message: {scenario['event']['message']}")
            
            analysis = await analyzer.analyze_event(scenario['event'])
            summary = analyzer.get_context_summary(analysis)
            
            print(f"   Analysis: {summary}")
            print(f"   Focus areas: {analysis['file_types']}")
    
    asyncio.run(test_context_analyzer())
