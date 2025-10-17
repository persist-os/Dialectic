"""
Dynamic Agent Generator (AI-Powered)
Uses LLM to generate agent specifications dynamically based on actual codebase analysis

This replaces template-based generation with true AI intelligence!
"""

import json
import uuid
from typing import Dict, List
from datetime import datetime
from pathlib import Path

from agents.models import AgentSpec, ContextAnalysis
from config.llm_config import get_llm


class AIAgentGenerator:
    """
    Generates agent specifications using LLM
    
    NO TEMPLATES - Pure AI-driven agent generation!
    """
    
    def __init__(self, use_ai: bool = True):
        """
        Initialize AI agent generator
        
        Args:
            use_ai: If False, falls back to keyword-based generation (for testing)
        """
        self.use_ai = use_ai
        self.llm = get_llm() if use_ai else None
    
    async def generate_agents(self, context_analysis: Dict) -> List[AgentSpec]:
        """
        Generate agents using LLM based on context analysis
        
        Args:
            context_analysis: Output from ContextAnalyzer
        
        Returns:
            List of AgentSpec objects
        """
        
        if self.use_ai and self.llm:
            return await self._generate_with_ai(context_analysis)
        else:
            return await self._generate_fallback(context_analysis)
    
    async def _generate_with_ai(self, context: Dict) -> List[AgentSpec]:
        """Generate agents using LLM"""
        
        # Build prompt for LLM
        prompt = self._build_agent_generation_prompt(context)
        
        system_prompt = """You are an AI that generates specialized software development agents based on code changes.

Your task: Analyze the code changes and determine what specialist agents are needed.

For each agent, provide:
- agent_type: A descriptive name (snake_case) like "security_specialist" or "api_documentation_expert"
- focus_area: Primary focus (e.g., "security", "performance", "documentation")
- priority: 1 (critical), 2 (important), or 3 (nice-to-have)
- confidence: Float 0.0-1.0 indicating how sure you are this agent is needed
- context_reason: WHY this agent is needed (human-readable)
- estimated_duration: Rough time estimate (e.g., "15-30 min")
- documentation_targets: List of 2-4 .cursor folder files this agent should update
- tags: 2-4 relevant tags

Be specific and context-aware. Only generate agents that are truly needed for these changes."""

        try:
            # Call LLM
            response = await self.llm.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=2000,
                response_format="json"
            )
            
            # Parse response
            data = json.loads(response)
            agents_data = data.get("agents", [])
            
            # Convert to AgentSpec objects
            agents = []
            timestamp = datetime.now().isoformat()
            
            for agent_data in agents_data:
                agent = AgentSpec(
                    agent_id=f"{agent_data['agent_type']}_{uuid.uuid4().hex[:8]}",
                    agent_type=agent_data['agent_type'],
                    focus_area=agent_data['focus_area'],
                    documentation_targets=agent_data['documentation_targets'],
                    priority=agent_data['priority'],
                    confidence=agent_data['confidence'],
                    created_at=timestamp,
                    context_reason=agent_data['context_reason'],
                    estimated_duration=agent_data['estimated_duration'],
                    tags=agent_data.get('tags', []),
                    dependencies=agent_data.get('dependencies', [])
                )
                agents.append(agent)
            
            return sorted(agents, key=lambda x: (x.priority, -x.confidence))
            
        except Exception as e:
            print(f"⚠️  AI agent generation failed: {e}")
            print(f"   Falling back to keyword-based generation")
            return await self._generate_fallback(context)
    
    def _build_agent_generation_prompt(self, context: Dict) -> str:
        """Build prompt for LLM"""
        
        files = context.get('files_changed', [])
        message = context.get('commit_message', '')
        error_count = context.get('error_count', 0)
        complexity = context.get('complexity_score', 0)
        file_types = context.get('file_types', {})
        
        prompt = f"""Analyze these code changes and determine what specialist agents are needed:

**Files Changed:**
{chr(10).join(f'- {f}' for f in files)}

**Commit Message:**
{message}

**Context:**
- Errors detected: {error_count}
- Complexity score: {complexity}
- File types: {json.dumps(file_types, indent=2)}
- Security focus: {context.get('security_focus', False)}
- MVP focus: {context.get('mvp_focus', False)}
- Performance focus: {context.get('performance_focus', False)}

Generate a JSON object with this structure:
{{
  "agents": [
    {{
      "agent_type": "security_specialist",
      "focus_area": "security",
      "priority": 1,
      "confidence": 0.95,
      "context_reason": "JWT authentication changes require security review",
      "estimated_duration": "20-30 min",
      "documentation_targets": [
        ".cursor/rules/security_rules.md",
        ".cursor/commands/security_commands.md",
        ".cursor/development/patterns/auth_patterns.md"
      ],
      "tags": ["security", "authentication", "jwt"],
      "dependencies": []
    }}
  ]
}}

Only generate agents that are actually needed for these specific changes."""
        
        return prompt
    
    async def _generate_fallback(self, context: Dict) -> List[AgentSpec]:
        """Fallback: keyword-based generation (like old version)"""
        
        agents = []
        timestamp = datetime.now().isoformat()
        
        # Security agent
        if context.get('security_focus'):
            agents.append(AgentSpec(
                agent_id=f"security_specialist_{uuid.uuid4().hex[:8]}",
                agent_type='security_specialist',
                focus_area='security',
                documentation_targets=[
                    '.cursor/rules/security_rules.md',
                    '.cursor/commands/security_commands.md',
                    '.cursor/development/patterns/auth_patterns.md'
                ],
                priority=1,
                confidence=context['confidence']['security'],
                created_at=timestamp,
                context_reason=f"Security focus detected (confidence: {context['confidence']['security']:.1%})",
                estimated_duration='15-30 min',
                tags=['security', 'auth'],
                dependencies=[]
            ))
        
        # MVP agent
        if context.get('mvp_focus'):
            agents.append(AgentSpec(
                agent_id=f"mvp_strategist_{uuid.uuid4().hex[:8]}",
                agent_type='mvp_strategist',
                focus_area='mvp',
                documentation_targets=[
                    '.cursor/rules/mvp_guidelines.md',
                    '.cursor/commands/rapid_prototyping.md'
                ],
                priority=2,
                confidence=context['confidence']['mvp'],
                created_at=timestamp,
                context_reason=f"MVP work detected (confidence: {context['confidence']['mvp']:.1%})",
                estimated_duration='10-20 min',
                tags=['mvp', 'prototype'],
                dependencies=[]
            ))
        
        # Performance agent
        if context.get('performance_focus'):
            agents.append(AgentSpec(
                agent_id=f"performance_expert_{uuid.uuid4().hex[:8]}",
                agent_type='performance_expert',
                focus_area='performance',
                documentation_targets=[
                    '.cursor/rules/performance_rules.md',
                    '.cursor/commands/optimization_commands.md'
                ],
                priority=2,
                confidence=context['confidence']['performance'],
                created_at=timestamp,
                context_reason=f"Performance optimization detected (confidence: {context['confidence']['performance']:.1%})",
                estimated_duration='20-40 min',
                tags=['performance', 'optimization'],
                dependencies=[]
            ))
        
        return sorted(agents, key=lambda x: (x.priority, -x.confidence))
    
    def get_agent_summary(self, agents: List[AgentSpec]) -> str:
        """Get human-readable summary of generated agents"""
        
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


# Test the AI agent generator
if __name__ == "__main__":
    import asyncio
    import sys
    from pathlib import Path
    
    # Add parent to path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    from context_analyzer import ContextAnalyzer
    
    async def test_ai_agent_generator():
        """Test AI agent generator"""
        
        print("🤖 Testing AI Agent Generator")
        print("=" * 60)
        
        # Test with AI
        print("\n1️⃣ Testing WITH AI:")
        analyzer = ContextAnalyzer()
        ai_generator = AIAgentGenerator(use_ai=True)
        
        test_event = {
            'files': ['src/auth/jwt.py', 'src/middleware/auth.py'],
            'message': 'Add JWT authentication with secure token handling',
            'errors': []
        }
        
        context = await analyzer.analyze_event(test_event)
        agents = await ai_generator.generate_agents(context)
        
        print(f"   Generated {len(agents)} agents:")
        for agent in agents:
            print(f"      • {agent.agent_type}: {agent.context_reason}")
        
        # Test fallback
        print("\n2️⃣ Testing FALLBACK (no AI):")
        fallback_generator = AIAgentGenerator(use_ai=False)
        agents = await fallback_generator.generate_agents(context)
        
        print(f"   Generated {len(agents)} agents:")
        for agent in agents:
            print(f"      • {agent.agent_type}: {agent.context_reason}")
    
    asyncio.run(test_ai_agent_generator())

