"""
Workflow Manager for Dialectic Agent Coordination
Manages agent workflows and coordinates between different components
"""
import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
import time

from orchestration.stackai_client import StackAIClient, AgentWorkflow
from streams.message_handler import MessageHandler, MessageType, Message

logger = logging.getLogger(__name__)

@dataclass
class AgentContext:
    """Context information for agent generation"""
    code_changes: List[str]
    file_context: Dict[str, Any]
    focus_area: str  # "security", "mvp", "performance", "general"
    urgency: str  # "low", "medium", "high"
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class AgentCoordinationResult:
    """Result of agent coordination"""
    workflow_id: str
    execution_id: str
    agents_generated: List[Dict[str, Any]]
    documentation_updates: List[Dict[str, Any]]
    learning_events: List[Dict[str, Any]]
    success: bool
    error_message: Optional[str] = None

class WorkflowManager:
    """Manages agent workflows and coordinates between components"""
    
    def __init__(self, stackai_client: StackAIClient, message_handler: MessageHandler):
        self.stackai_client = stackai_client
        self.message_handler = message_handler
        self.active_workflows: Dict[str, str] = {}  # context_id -> workflow_id
        self.agent_templates: Dict[str, Dict[str, Any]] = {}
        self._setup_agent_templates()
        self._register_message_handlers()
    
    def _setup_agent_templates(self):
        """Setup predefined agent templates"""
        self.agent_templates = {
            "security_specialist": {
                "type": "security_specialist",
                "name": "Security Specialist",
                "description": "Analyzes code for security vulnerabilities and best practices",
                "capabilities": ["vulnerability_detection", "security_patterns", "auth_analysis"],
                "prompt_template": "As a security specialist, analyze the following code changes for security implications: {context}"
            },
            "mvp_strategist": {
                "type": "mvp_strategist", 
                "name": "MVP Strategist",
                "description": "Focuses on MVP requirements and user value",
                "capabilities": ["mvp_analysis", "user_value_assessment", "feature_prioritization"],
                "prompt_template": "As an MVP strategist, evaluate these changes for MVP impact and user value: {context}"
            },
            "performance_expert": {
                "type": "performance_expert",
                "name": "Performance Expert", 
                "description": "Analyzes performance implications and optimization opportunities",
                "capabilities": ["performance_analysis", "optimization_recommendations", "scalability_assessment"],
                "prompt_template": "As a performance expert, analyze these changes for performance implications: {context}"
            },
            "documentation_agent": {
                "type": "documentation_agent",
                "name": "Documentation Agent",
                "description": "Updates documentation based on code changes and analysis",
                "capabilities": ["doc_generation", "pattern_documentation", "update_cursor_folder"],
                "prompt_template": "As a documentation agent, update documentation based on: {context}"
            }
        }
    
    def _register_message_handlers(self):
        """Register message handlers for different message types"""
        self.message_handler.register_handler(
            MessageType.AGENT_GENERATION, 
            self._handle_agent_generation_request
        )
        
        self.message_handler.register_handler(
            MessageType.WORKFLOW_TRIGGER,
            self._handle_workflow_trigger
        )
    
    async def _handle_agent_generation_request(self, message: Message):
        """Handle agent generation requests"""
        try:
            # Prevent recursive calls
            if message.sender_id == "workflow_manager":
                return
                
            context = AgentContext(
                code_changes=message.content.get("code_changes", []),
                file_context=message.content.get("file_context", {}),
                focus_area=message.content.get("focus_area", "general"),
                urgency=message.content.get("urgency", "medium"),
                metadata=message.content.get("metadata", {})
            )
            
            result = await self.coordinate_agents(context)
            
            # Send result back (but not to ourselves)
            if message.sender_id != "workflow_manager":
                await self.message_handler.broadcast_message(
                    sender_id="workflow_manager",
                    message_type=MessageType.AGENT_GENERATION,
                    content={
                        "result": result.__dict__,
                        "status": "completed"
                    }
                )
            
        except Exception as e:
            logger.error(f"Failed to handle agent generation request: {e}")
    
    async def _handle_workflow_trigger(self, message: Message):
        """Handle workflow trigger requests"""
        try:
            workflow_name = message.content.get("workflow_name")
            input_data = message.content.get("input_data", {})
            
            if workflow_name:
                execution_id = await self.stackai_client.execute_workflow(
                    workflow_name, input_data
                )
                
                logger.info(f"Triggered workflow '{workflow_name}' with execution ID: {execution_id}")
            
        except Exception as e:
            logger.error(f"Failed to handle workflow trigger: {e}")
    
    async def coordinate_agents(self, context: AgentContext) -> AgentCoordinationResult:
        """Coordinate agents based on context"""
        try:
            # Determine which agents to generate based on context
            agents_to_generate = self._determine_agents_needed(context)
            
            # Generate agents
            agents = []
            for agent_type in agents_to_generate:
                agent = await self._generate_agent(agent_type, context)
                agents.append(agent)
            
            # Create workflow
            workflow_id = await self.stackai_client.create_agent_workflow(
                agents, f"dialectic_context_{int(time.time())}"
            )
            
            if not workflow_id:
                return AgentCoordinationResult(
                    workflow_id="",
                    execution_id="",
                    agents_generated=[],
                    documentation_updates=[],
                    learning_events=[],
                    success=False,
                    error_message="Failed to create workflow"
                )
            
            # Execute workflow using the returned workflow_id
            execution_id = await self.stackai_client.execute_workflow(
                workflow_id, {
                    "code_changes": context.code_changes,
                    "file_context": context.file_context,
                    "focus_area": context.focus_area
                }
            )
            
            # Generate documentation updates
            documentation_updates = await self._generate_documentation_updates(
                context, agents
            )
            
            # Generate learning events
            learning_events = await self._generate_learning_events(context, agents)
            
            # Store active workflow
            context_id = f"{context.focus_area}_{int(time.time())}"
            self.active_workflows[context_id] = workflow_id
            
            return AgentCoordinationResult(
                workflow_id=workflow_id,
                execution_id=execution_id or "",
                agents_generated=agents,
                documentation_updates=documentation_updates,
                learning_events=learning_events,
                success=True
            )
            
        except Exception as e:
            logger.error(f"Failed to coordinate agents: {e}")
            return AgentCoordinationResult(
                workflow_id="",
                execution_id="",
                agents_generated=[],
                documentation_updates=[],
                learning_events=[],
                success=False,
                error_message=str(e)
            )
    
    def _determine_agents_needed(self, context: AgentContext) -> List[str]:
        """Determine which agents are needed based on context"""
        agents_needed = []
        
        # Always include documentation agent
        agents_needed.append("documentation_agent")
        
        # Determine focus-specific agents
        focus_area = context.focus_area.lower()
        
        if focus_area == "security" or any("auth" in change.lower() or "security" in change.lower() 
                                         for change in context.code_changes):
            agents_needed.append("security_specialist")
        
        if focus_area == "mvp" or any("prototype" in change.lower() or "feature" in change.lower()
                                   for change in context.code_changes):
            agents_needed.append("mvp_strategist")
        
        if focus_area == "performance" or any("optimize" in change.lower() or "performance" in change.lower()
                                             for change in context.code_changes):
            agents_needed.append("performance_expert")
        
        # If no specific focus, include all for general analysis
        if focus_area == "general" or len(agents_needed) == 1:
            agents_needed.extend(["security_specialist", "mvp_strategist", "performance_expert"])
        
        return list(set(agents_needed))  # Remove duplicates
    
    async def _generate_agent(self, agent_type: str, context: AgentContext) -> Dict[str, Any]:
        """Generate an agent based on type and context"""
        template = self.agent_templates.get(agent_type, {})
        
        agent = {
            "id": f"{agent_type}_{int(time.time())}",
            "type": agent_type,
            "name": template.get("name", agent_type.title()),
            "description": template.get("description", ""),
            "capabilities": template.get("capabilities", []),
            "context": {
                "focus_area": context.focus_area,
                "urgency": context.urgency,
                "code_changes": context.code_changes,
                "file_context": context.file_context
            },
            "generated_at": time.time()
        }
        
        return agent
    
    async def _generate_documentation_updates(self, context: AgentContext, 
                                           agents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate documentation updates based on context and agents"""
        updates = []
        
        # Generate updates for each agent's analysis
        for agent in agents:
            agent_type = agent["type"]
            
            if agent_type == "security_specialist":
                updates.append({
                    "file": "security_patterns.md",
                    "action": "update",
                    "content": f"Security analysis for: {', '.join(context.code_changes)}",
                    "agent_id": agent["id"]
                })
            
            elif agent_type == "mvp_strategist":
                updates.append({
                    "file": "mvp_guidelines.md", 
                    "action": "update",
                    "content": f"MVP analysis for: {', '.join(context.code_changes)}",
                    "agent_id": agent["id"]
                })
            
            elif agent_type == "performance_expert":
                updates.append({
                    "file": "performance_patterns.md",
                    "action": "update", 
                    "content": f"Performance analysis for: {', '.join(context.code_changes)}",
                    "agent_id": agent["id"]
                })
        
        # Always update main documentation
        updates.append({
            "file": "dialectic_analysis.md",
            "action": "create",
            "content": f"Analysis of {context.focus_area} focus for changes: {', '.join(context.code_changes)}",
            "agent_id": "workflow_manager"
        })
        
        return updates
    
    async def _generate_learning_events(self, context: AgentContext, 
                                     agents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate learning events for pattern recognition"""
        events = []
        
        # Pattern recognition event
        events.append({
            "event_type": "pattern_recognized",
            "pattern": context.focus_area,
            "confidence": 0.85,
            "context": {
                "code_changes": context.code_changes,
                "agent_count": len(agents),
                "urgency": context.urgency
            },
            "timestamp": time.time()
        })
        
        # Agent generation event
        events.append({
            "event_type": "agents_generated",
            "agent_types": [agent["type"] for agent in agents],
            "context": context.focus_area,
            "timestamp": time.time()
        })
        
        return events
    
    async def get_workflow_status(self, context_id: str) -> Optional[Dict[str, Any]]:
        """Get status of an active workflow"""
        if context_id not in self.active_workflows:
            return None
        
        workflow_id = self.active_workflows[context_id]
        return self.stackai_client.get_workflow_info(workflow_id)
    
    def get_active_workflows(self) -> Dict[str, str]:
        """Get all active workflows"""
        return self.active_workflows.copy()
    
    async def cleanup_completed_workflows(self):
        """Clean up completed workflows"""
        completed_contexts = []
        
        for context_id, workflow_id in self.active_workflows.items():
            workflow_info = self.stackai_client.get_workflow_info(workflow_id)
            if workflow_info and workflow_info.get("status") == "completed":
                completed_contexts.append(context_id)
        
        for context_id in completed_contexts:
            del self.active_workflows[context_id]
        
        logger.info(f"Cleaned up {len(completed_contexts)} completed workflows")

# Test function
async def test_workflow_manager():
    """Test the workflow manager functionality"""
    from streams.message_handler import MessageHandler
    
    # Initialize components
    stackai_client = StackAIClient()
    message_handler = MessageHandler()
    workflow_manager = WorkflowManager(stackai_client, message_handler)
    
    # Test context
    context = AgentContext(
        code_changes=["auth.py", "security.py", "middleware.py"],
        file_context={"auth.py": "authentication logic", "security.py": "security utilities"},
        focus_area="security",
        urgency="high"
    )
    
    # Test agent coordination
    result = await workflow_manager.coordinate_agents(context)
    print(f"Coordination result: {result}")
    
    # Test active workflows
    active = workflow_manager.get_active_workflows()
    print(f"Active workflows: {active}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_workflow_manager())
