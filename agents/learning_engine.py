"""
Learning Engine
Learns from events to improve agent generation over time

This is the intelligence layer that makes the system truly "living" -
it learns patterns and gets better at generating the right agents!
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict
from datetime import datetime
import asyncio


class LearningEngine:
    """
    Learns from events to improve agent generation over time
    
    This is what makes Dialectic truly "living" - it learns patterns
    and gets smarter about which agents to spawn for different contexts.
    """
    
    def __init__(self, storage_path: str = '.cursor/learning'):
        """
        Initialize learning engine
        
        Args:
            storage_path: Path to store learning data (relative to cwd)
        """
        # ALWAYS use path relative to current working directory
        self.storage_path = Path.cwd() / storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Learning data files
        self.patterns_file = self.storage_path / 'patterns.json'
        self.success_metrics_file = self.storage_path / 'success_metrics.json'
        self.agent_effectiveness_file = self.storage_path / 'agent_effectiveness.json'
        self.learning_log_file = self.storage_path / 'learning_log.json'
        
        # Load existing data
        self.patterns = self._load_patterns()
        self.success_metrics = self._load_success_metrics()
        self.agent_effectiveness = self._load_agent_effectiveness()
        self.learning_log = self._load_learning_log()
    
    def _load_patterns(self) -> Dict:
        """Load learned patterns from storage"""
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return defaultdict(int)
    
    def _load_success_metrics(self) -> Dict:
        """Load success metrics from storage"""
        if self.success_metrics_file.exists():
            try:
                with open(self.success_metrics_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return {
            'total_events': 0,
            'successful_updates': 0,
            'failed_updates': 0,
            'total_patterns': 0
        }
    
    def _load_agent_effectiveness(self) -> Dict:
        """Load agent effectiveness data"""
        if self.agent_effectiveness_file.exists():
            try:
                with open(self.agent_effectiveness_file, 'r') as f:
                    data = json.load(f)
                    # Convert to defaultdict to handle new agent types
                    result = defaultdict(lambda: {
                        'total_spawned': 0,
                        'successful_updates': 0,
                        'average_confidence': 0.0,
                        'last_used': None
                    })
                    result.update(data)
                    return result
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return defaultdict(lambda: {
            'total_spawned': 0,
            'successful_updates': 0,
            'average_confidence': 0.0,
            'last_used': None
        })
    
    def _load_learning_log(self) -> List[Dict]:
        """Load learning log"""
        if self.learning_log_file.exists():
            try:
                with open(self.learning_log_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return []
    
    async def learn_from_event(
        self, 
        event_data: Dict, 
        agents_generated: List, 
        outcome: str,
        updates_made: List[Dict] = None
    ):
        """
        Learn from an event and update patterns
        
        Args:
            event_data: Original event data
            agents_generated: List of AgentSpec objects
            outcome: 'success', 'partial', or 'failure'
            updates_made: List of update records
        """
        
        timestamp = datetime.now().isoformat()
        
        # Extract pattern key
        pattern_key = self._extract_pattern_key(event_data)
        
        # Update pattern count
        self.patterns[pattern_key] = self.patterns.get(pattern_key, 0) + 1
        
        # Update success metrics
        self.success_metrics['total_events'] += 1
        
        if outcome == 'success':
            self.success_metrics['successful_updates'] += 1
        elif outcome == 'failure':
            self.success_metrics['failed_updates'] += 1
        
        # Update agent effectiveness
        for agent in agents_generated:
            agent_key = agent.agent_type
            
            self.agent_effectiveness[agent_key]['total_spawned'] += 1
            self.agent_effectiveness[agent_key]['last_used'] = timestamp
            
            # Update confidence average
            current_avg = self.agent_effectiveness[agent_key]['average_confidence']
            total_spawned = self.agent_effectiveness[agent_key]['total_spawned']
            
            new_avg = ((current_avg * (total_spawned - 1)) + agent.confidence) / total_spawned
            self.agent_effectiveness[agent_key]['average_confidence'] = new_avg
            
            # Count successful updates for this agent
            if updates_made:
                agent_updates = [u for u in updates_made if u.get('agent') == agent.agent_type]
                if agent_updates:
                    self.agent_effectiveness[agent_key]['successful_updates'] += len(agent_updates)
        
        # Record learning event
        learning_event = {
            'timestamp': timestamp,
            'pattern_key': pattern_key,
            'agents_spawned': [agent.agent_type for agent in agents_generated],
            'outcome': outcome,
            'updates_count': len(updates_made) if updates_made else 0,
            'event_summary': {
                'files': event_data.get('files', []),
                'message': event_data.get('message', ''),
                'error_count': len(event_data.get('errors', []))
            }
        }
        
        self.learning_log.append(learning_event)
        
        # Keep only last 100 learning events
        if len(self.learning_log) > 100:
            self.learning_log = self.learning_log[-100:]
        
        # Save all data
        await self._save_all_data()
    
    def _extract_pattern_key(self, event_data: Dict) -> str:
        """Extract a pattern key from event data"""
        
        files = event_data.get('files', [])
        message = event_data.get('message', '')
        errors = len(event_data.get('errors', []))
        
        # Create pattern signature
        has_security = any(kw in str(files).lower() + message.lower() 
                          for kw in ['auth', 'security', 'token', 'jwt'])
        has_mvp = any(kw in message.lower() 
                     for kw in ['mvp', 'prototype', 'hackathon', 'quick'])
        has_performance = any(kw in str(files).lower() + message.lower() 
                            for kw in ['optimize', 'performance', 'cache', 'async'])
        has_errors = errors > 0
        has_docs = any(file.endswith(('.md', '.rst', '.txt')) for file in files)
        
        # File type patterns
        file_types = []
        for file_path in files:
            if file_path.endswith('.py'):
                file_types.append('py')
            elif file_path.endswith(('.js', '.ts', '.jsx', '.tsx')):
                file_types.append('js')
            elif file_path.endswith(('.html', '.css')):
                file_types.append('web')
        
        file_type_key = '_'.join(sorted(set(file_types))) if file_types else 'other'
        
        pattern_key = f"sec:{has_security}|mvp:{has_mvp}|perf:{has_performance}|err:{has_errors}|doc:{has_docs}|type:{file_type_key}"
        
        return pattern_key
    
    async def get_recommended_agents(self, event_data: Dict) -> List[str]:
        """
        Get recommended agents based on learned patterns
        
        Args:
            event_data: Event data to analyze
        
        Returns:
            List of recommended agent types
        """
        
        pattern_key = self._extract_pattern_key(event_data)
        
        # Find similar patterns
        similar_patterns = {}
        for stored_pattern, count in self.patterns.items():
            similarity = self._calculate_pattern_similarity(pattern_key, stored_pattern)
            if similarity > 0.5:  # Threshold for similarity
                similar_patterns[stored_pattern] = count * similarity
        
        # Find most effective agents for similar patterns
        agent_scores = defaultdict(float)
        
        for learning_event in self.learning_log:
            if learning_event['pattern_key'] in similar_patterns:
                weight = similar_patterns[learning_event['pattern_key']]
                
                for agent_type in learning_event['agents_spawned']:
                    # Score based on outcome and effectiveness
                    outcome_score = {
                        'success': 1.0,
                        'partial': 0.5,
                        'failure': 0.0
                    }.get(learning_event['outcome'], 0.0)
                    
                    agent_scores[agent_type] += weight * outcome_score
        
        # Sort by score and return top recommendations
        sorted_agents = sorted(
            agent_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [agent_type for agent_type, score in sorted_agents[:3]]
    
    def _calculate_pattern_similarity(self, pattern1: str, pattern2: str) -> float:
        """Calculate similarity between two pattern keys"""
        
        # Simple similarity based on matching components
        components1 = set(pattern1.split('|'))
        components2 = set(pattern2.split('|'))
        
        if not components1 or not components2:
            return 0.0
        
        intersection = len(components1.intersection(components2))
        union = len(components1.union(components2))
        
        return intersection / union if union > 0 else 0.0
    
    async def _save_all_data(self):
        """Save all learning data to files"""
        
        # Save patterns
        with open(self.patterns_file, 'w') as f:
            json.dump(dict(self.patterns), f, indent=2)
        
        # Save success metrics
        with open(self.success_metrics_file, 'w') as f:
            json.dump(self.success_metrics, f, indent=2)
        
        # Save agent effectiveness
        with open(self.agent_effectiveness_file, 'w') as f:
            json.dump(dict(self.agent_effectiveness), f, indent=2)
        
        # Save learning log
        with open(self.learning_log_file, 'w') as f:
            json.dump(self.learning_log, f, indent=2)
    
    def get_learning_summary(self) -> Dict:
        """Get summary of what the system has learned"""
        
        total_events = self.success_metrics.get('total_events', 0)
        successful_updates = self.success_metrics.get('successful_updates', 0)
        failed_updates = self.success_metrics.get('failed_updates', 0)
        
        success_rate = (successful_updates / total_events * 100) if total_events > 0 else 0
        
        # Get most effective agents
        most_effective = sorted(
            self.agent_effectiveness.items(),
            key=lambda x: x[1]['successful_updates'],
            reverse=True
        )[:3]
        
        # Get most common patterns
        most_common_patterns = sorted(
            self.patterns.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            'total_events_processed': total_events,
            'successful_updates': successful_updates,
            'failed_updates': failed_updates,
            'success_rate': f"{success_rate:.1f}%",
            'patterns_learned': len(self.patterns),
            'most_effective_agents': [
                {
                    'agent_type': agent_type,
                    'successful_updates': data['successful_updates'],
                    'average_confidence': f"{data['average_confidence']:.1%}",
                    'total_spawned': data['total_spawned']
                }
                for agent_type, data in most_effective
            ],
            'most_common_patterns': [
                {'pattern': pattern, 'count': count}
                for pattern, count in most_common_patterns
            ],
            'learning_events_logged': len(self.learning_log)
        }
    
    def get_agent_insights(self, agent_type: str) -> Dict:
        """Get insights about a specific agent type"""
        
        if agent_type not in self.agent_effectiveness:
            return {'error': f'No data for agent type: {agent_type}'}
        
        data = self.agent_effectiveness[agent_type]
        
        # Find recent events involving this agent
        recent_events = [
            event for event in self.learning_log[-20:]  # Last 20 events
            if agent_type in event['agents_spawned']
        ]
        
        return {
            'agent_type': agent_type,
            'total_spawned': data['total_spawned'],
            'successful_updates': data['successful_updates'],
            'average_confidence': f"{data['average_confidence']:.1%}",
            'last_used': data['last_used'],
            'recent_performance': [
                {
                    'timestamp': event['timestamp'],
                    'outcome': event['outcome'],
                    'updates_count': event['updates_count']
                }
                for event in recent_events
            ]
        }


# Test the learning engine
if __name__ == "__main__":
    import asyncio
    from context_analyzer import ContextAnalyzer
    from agent_generator import DynamicAgentGenerator
    from documentation_updater import DocumentationUpdater
    
    async def test_learning_engine():
        """Test the learning engine with multiple scenarios"""
        
        print("🧠 Testing Learning Engine")
        print("=" * 60)
        
        analyzer = ContextAnalyzer()
        generator = DynamicAgentGenerator()
        updater = DocumentationUpdater('.cursor/')
        learner = LearningEngine()
        
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
            }
        ]
        
        print("🎭 Processing test scenarios...")
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n{i}. {scenario['name']}:")
            
            # Analyze context
            context = await analyzer.analyze_event(scenario['event'])
            
            # Generate agents
            agents = await generator.generate_agents(context)
            
            # Update documentation
            updates_made = []
            for agent in agents:
                updates = await updater.update_documentation(agent, context)
                updates_made.extend(updates)
            
            # Learn from event
            outcome = 'success' if updates_made else 'failure'
            await learner.learn_from_event(scenario['event'], agents, outcome, updates_made)
            
            print(f"   ✅ Learned from {len(agents)} agents, {len(updates_made)} updates")
        
        # Show learning summary
        print("\n" + "=" * 60)
        print("📊 LEARNING SUMMARY")
        print("=" * 60)
        
        summary = learner.get_learning_summary()
        
        print(f"Total events processed: {summary['total_events_processed']}")
        print(f"Success rate: {summary['success_rate']}")
        print(f"Patterns learned: {summary['patterns_learned']}")
        
        print(f"\n🏆 Most Effective Agents:")
        for agent in summary['most_effective_agents']:
            print(f"   • {agent['agent_type']}: {agent['successful_updates']} updates, {agent['average_confidence']} confidence")
        
        print(f"\n🔍 Most Common Patterns:")
        for pattern in summary['most_common_patterns']:
            print(f"   • {pattern['pattern']}: {pattern['count']} occurrences")
        
        # Test recommendations
        print(f"\n🎯 Testing Recommendations:")
        test_event = {
            'files': ['src/auth/login.py'],
            'message': 'Add user login functionality',
            'errors': []
        }
        
        recommendations = await learner.get_recommended_agents(test_event)
        print(f"   For login event: {', '.join(recommendations)}")
        
        print(f"\n💡 Learning data saved to: {learner.storage_path}")
    
    asyncio.run(test_learning_engine())
