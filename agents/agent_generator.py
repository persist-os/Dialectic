"""
Dynamic Agent Generator
Generates agent specifications based on context analysis

This is where the magic happens - agents are created dynamically
based on the context, not hardcoded!
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class AgentSpec:
    """Specification for a dynamically generated agent"""
    
    # Core identification
    agent_id: str
    agent_type: str
    focus_area: str
    
    # Capabilities
    documentation_targets: List[str]
    priority: int
    confidence: float
    
    # Context
    created_at: str
    context_reason: str
    estimated_duration: str
    
    # Metadata
    tags: List[str]
    dependencies: List[str]


class DynamicAgentGenerator:
    """
    Generates agent specifications dynamically based on context
    
    This is the core innovation - no hardcoded agents!
    Agents emerge from the context analysis.
    """
    
    def __init__(self):
        """Initialize the agent generator with templates"""
        
        # Agent templates - these define what agents CAN be, not what they ARE
        self.agent_templates = {
            'security_specialist': {
                'base_priority': 1,
                'focus_area': 'security',
                'documentation_targets': [
                    '.cursor/rules/security_rules.md',
                    '.cursor/commands/security_commands.md',
                    '.cursor/development/patterns/auth_patterns.md',
                    '.cursor/development/debugging/security_debugging.md'
                ],
                'tags': ['security', 'auth', 'permissions'],
                'estimated_duration': '15-30 min'
            },
            'mvp_strategist': {
                'base_priority': 2,
                'focus_area': 'mvp',
                'documentation_targets': [
                    '.cursor/rules/mvp_guidelines.md',
                    '.cursor/commands/rapid_prototyping.md',
                    '.cursor/development/patterns/mvp_patterns.md',
                    '.cursor/plans/mvp_tracking.md'
                ],
                'tags': ['mvp', 'prototype', 'rapid'],
                'estimated_duration': '10-20 min'
            },
            'performance_expert': {
                'base_priority': 2,
                'focus_area': 'performance',
                'documentation_targets': [
                    '.cursor/rules/performance_rules.md',
                    '.cursor/commands/optimization_commands.md',
                    '.cursor/development/patterns/performance_patterns.md',
                    '.cursor/development/debugging/performance_debugging.md'
                ],
                'tags': ['performance', 'optimization', 'caching'],
                'estimated_duration': '20-40 min'
            },
            'documentation_specialist': {
                'base_priority': 3,
                'focus_area': 'documentation',
                'documentation_targets': [
                    '.cursor/README.md',
                    '.cursor/development/debugging/',
                    '.cursor/plans/',
                    '.cursor/commands/'
                ],
                'tags': ['documentation', 'docs', 'guides'],
                'estimated_duration': '5-15 min'
            },
            'error_handler': {
                'base_priority': 1,
                'focus_area': 'debugging',
                'documentation_targets': [
                    '.cursor/development/debugging/',
                    '.cursor/commands/debugging_commands.md',
                    '.cursor/rules/error_handling_rules.md'
                ],
                'tags': ['debugging', 'errors', 'fixes'],
                'estimated_duration': '10-25 min'
            },
            'api_specialist': {
                'base_priority': 2,
                'focus_area': 'api',
                'documentation_targets': [
                    '.cursor/rules/api_rules.md',
                    '.cursor/commands/api_commands.md',
                    '.cursor/development/patterns/api_patterns.md'
                ],
                'tags': ['api', 'endpoints', 'rest'],
                'estimated_duration': '15-30 min'
            },
            'frontend_specialist': {
                'base_priority': 2,
                'focus_area': 'frontend',
                'documentation_targets': [
                    '.cursor/rules/frontend_rules.md',
                    '.cursor/commands/frontend_commands.md',
                    '.cursor/development/patterns/ui_patterns.md'
                ],
                'tags': ['frontend', 'ui', 'components'],
                'estimated_duration': '15-25 min'
            }
        }
    
    async def generate_agents(self, context_analysis: Dict) -> List[AgentSpec]:
        """
        Generate agents based on context analysis
        
        Args:
            context_analysis: Output from ContextAnalyzer
        
        Returns:
            List of AgentSpec objects for agents to spawn
        """
        
        agents = []
        timestamp = datetime.now().isoformat()
        
        # Security agent - high priority
        if context_analysis['security_focus']:
            security_confidence = context_analysis['confidence']['security']
            if security_confidence > 0.3:  # Threshold for spawning
                agents.append(self._create_agent(
                    'security_specialist',
                    context_analysis,
                    timestamp,
                    f"Security focus detected (confidence: {security_confidence:.1%})"
                ))
        
        # MVP agent
        if context_analysis['mvp_focus']:
            mvp_confidence = context_analysis['confidence']['mvp']
            if mvp_confidence > 0.2:
                agents.append(self._create_agent(
                    'mvp_strategist',
                    context_analysis,
                    timestamp,
                    f"MVP/prototype work detected (confidence: {mvp_confidence:.1%})"
                ))
        
        # Performance agent
        if context_analysis['performance_focus']:
            perf_confidence = context_analysis['confidence']['performance']
            if perf_confidence > 0.3:
                agents.append(self._create_agent(
                    'performance_expert',
                    context_analysis,
                    timestamp,
                    f"Performance optimization detected (confidence: {perf_confidence:.1%})"
                ))
        
        # Documentation agent - always include if docs changed
        if context_analysis['documentation_focus']:
            agents.append(self._create_agent(
                'documentation_specialist',
                context_analysis,
                timestamp,
                "Documentation files modified"
            ))
        
        # Error handler agent - high priority for errors
        if context_analysis['error_focus']:
            agents.append(self._create_agent(
                'error_handler',
                context_analysis,
                timestamp,
                f"Errors detected ({context_analysis['error_count']} errors)"
            ))
        
        # API specialist - based on file types
        file_types = context_analysis['file_types']
        if file_types.get('python', 0) > 0 and 'api' in ' '.join(context_analysis['files_changed']).lower():
            agents.append(self._create_agent(
                'api_specialist',
                context_analysis,
                timestamp,
                "API-related Python files detected"
            ))
        
        # Frontend specialist - based on file types
        frontend_files = file_types.get('javascript', 0) + file_types.get('typescript', 0) + file_types.get('html', 0) + file_types.get('css', 0)
        if frontend_files > 0:
            agents.append(self._create_agent(
                'frontend_specialist',
                context_analysis,
                timestamp,
                f"Frontend files detected ({frontend_files} files)"
            ))
        
        # Sort by priority and confidence
        agents.sort(key=lambda x: (x.priority, -x.confidence))
        
        return agents
    
    def _create_agent(self, agent_type: str, context: Dict, timestamp: str, reason: str) -> AgentSpec:
        """Create an agent specification from template and context"""
        
        template = self.agent_templates[agent_type]
        
        # Calculate confidence based on context
        confidence = self._calculate_agent_confidence(agent_type, context)
        
        # Generate unique ID
        agent_id = f"{agent_type}_{uuid.uuid4().hex[:8]}"
        
        # Determine dependencies
        dependencies = self._determine_dependencies(agent_type, context)
        
        return AgentSpec(
            agent_id=agent_id,
            agent_type=agent_type,
            focus_area=template['focus_area'],
            documentation_targets=template['documentation_targets'].copy(),
            priority=template['base_priority'],
            confidence=confidence,
            created_at=timestamp,
            context_reason=reason,
            estimated_duration=template['estimated_duration'],
            tags=template['tags'].copy(),
            dependencies=dependencies
        )
    
    def _calculate_agent_confidence(self, agent_type: str, context: Dict) -> float:
        """Calculate confidence that this agent is needed"""
        
        if agent_type == 'security_specialist':
            return context['confidence']['security']
        elif agent_type == 'mvp_strategist':
            return context['confidence']['mvp']
        elif agent_type == 'performance_expert':
            return context['confidence']['performance']
        elif agent_type == 'documentation_specialist':
            return 1.0 if context['documentation_focus'] else 0.0
        elif agent_type == 'error_handler':
            return min(context['error_count'] * 0.2, 1.0)
        else:
            # For other agents, use file type analysis
            file_types = context['file_types']
            if agent_type == 'api_specialist':
                return min(file_types.get('python', 0) * 0.1, 1.0)
            elif agent_type == 'frontend_specialist':
                frontend_files = file_types.get('javascript', 0) + file_types.get('typescript', 0)
                return min(frontend_files * 0.2, 1.0)
        
        return 0.5  # Default confidence
    
    def _determine_dependencies(self, agent_type: str, context: Dict) -> List[str]:
        """Determine what other agents this agent might depend on"""
        
        dependencies = []
        
        # Security agents might need documentation
        if agent_type == 'security_specialist':
            dependencies.append('documentation_specialist')
        
        # Performance agents might need error handling
        if agent_type == 'performance_expert':
            dependencies.append('error_handler')
        
        # API agents might need both security and performance
        if agent_type == 'api_specialist':
            if context['security_focus']:
                dependencies.append('security_specialist')
            if context['performance_focus']:
                dependencies.append('performance_expert')
        
        return dependencies
    
    def get_agent_summary(self, agents: List[AgentSpec]) -> str:
        """Get a human-readable summary of generated agents"""
        
        if not agents:
            return "No agents generated"
        
        summary_parts = []
        
        for agent in agents:
            priority_emoji = "🔴" if agent.priority == 1 else "🟡" if agent.priority == 2 else "🟢"
            confidence_pct = f"{agent.confidence:.0%}"
            
            summary_parts.append(
                f"{priority_emoji} {agent.agent_type} ({confidence_pct})"
            )
        
        return " | ".join(summary_parts)


# Test the agent generator
if __name__ == "__main__":
    import asyncio
    from context_analyzer import ContextAnalyzer
    
    async def test_agent_generator():
        """Test the agent generator with different contexts"""
        
        print("🤖 Testing Dynamic Agent Generator")
        print("=" * 60)
        
        analyzer = ContextAnalyzer()
        generator = DynamicAgentGenerator()
        
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
                'name': 'Frontend Event',
                'event': {
                    'files': ['src/components/Button.tsx', 'src/styles/button.css'],
                    'message': 'Add new button component',
                    'errors': []
                }
            }
        ]
        
        for scenario in test_scenarios:
            print(f"\n🎭 {scenario['name']}:")
            print(f"   Files: {', '.join(scenario['event']['files'])}")
            print(f"   Message: {scenario['event']['message']}")
            
            # Analyze context
            context = await analyzer.analyze_event(scenario['event'])
            
            # Generate agents
            agents = await generator.generate_agents(context)
            
            # Show results
            summary = generator.get_agent_summary(agents)
            print(f"   Agents: {summary}")
            
            for agent in agents:
                print(f"      • {agent.agent_type}: {agent.context_reason}")
                print(f"        Targets: {len(agent.documentation_targets)} files")
                print(f"        Duration: {agent.estimated_duration}")
    
    asyncio.run(test_agent_generator())
