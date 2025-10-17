"""
Workflow Manager for Dialectic Agent Coordination
Manages agent workflows and coordinates between different components
Uses ACTUAL AI-powered agent generation - NO HARDCODING!
"""
import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
import time
import sys
from pathlib import Path

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestration.stackai_client import StackAIClient, AgentWorkflow
from streams.message_handler import MessageHandler, MessageType, Message
from agents.dynamic_agent_generator import AIAgentGenerator
from agents.context_analyzer import ContextAnalyzer
from agents.documentation_updater import DocumentationUpdater
from agents.learning_engine import LearningEngine

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
    """Manages agent workflows and coordinates between components - AI-POWERED!"""
    
    def __init__(self, stackai_client: StackAIClient, message_handler: MessageHandler, use_ai: bool = True):
        self.stackai_client = stackai_client
        self.message_handler = message_handler
        self.active_workflows: Dict[str, str] = {}  # context_id -> workflow_id
        
        # AI-POWERED COMPONENTS - NO TEMPLATES!
        self.ai_generator = AIAgentGenerator(use_ai=use_ai)
        self.context_analyzer = ContextAnalyzer()
        self.documentation_updater = DocumentationUpdater('.cursor/')
        self.learning_engine = LearningEngine()
        
        self._register_message_handlers()
        
        logger.info("WorkflowManager initialized with AI-powered agent generation")
    
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
        """Coordinate agents using ACTUAL AI - NO HARDCODING!"""
        try:
            # Step 1: AI-POWERED CONTEXT ANALYSIS
            logger.info(f"🧠 AI analyzing context: {context.focus_area}")
            
            # Build event data for context analyzer
            event_data = {
                'files': context.code_changes,
                'message': f"{context.focus_area} focus: {', '.join(context.code_changes)}",
                'errors': context.metadata.get('errors', []) if context.metadata else []
            }
            
            # AI analyzes the context
            context_analysis = await self.context_analyzer.analyze_event(event_data)
            logger.info(f"   📊 Context analysis complete: {self.context_analyzer.get_context_summary(context_analysis)}")
            
            # Step 2: AI-POWERED AGENT GENERATION
            logger.info(f"🤖 AI generating specialized agents...")
            agents_specs, llm_data = await self.ai_generator.generate_agents(context_analysis)
            
            logger.info(f"   ✨ AI generated {len(agents_specs)} agents")
            logger.info(f"   🧠 LLM reasoning: {llm_data.get('llm_response', 'N/A')[:100]}...")
            
            # Convert AgentSpec objects to dict format for workflow
            agents = []
            for agent_spec in agents_specs:
                agent_dict = {
                    "id": agent_spec.agent_id,
                    "type": agent_spec.agent_type,
                    "name": agent_spec.agent_type.replace('_', ' ').title(),
                    "description": agent_spec.context_reason,
                    "capabilities": agent_spec.tags,
                    "context": {
                        "focus_area": agent_spec.focus_area,
                        "urgency": context.urgency,
                        "code_changes": context.code_changes,
                        "confidence": agent_spec.confidence,
                        "documentation_targets": agent_spec.documentation_targets
                    },
                    "generated_at": time.time(),
                    "llm_generated": True
                }
                agents.append(agent_dict)
            
            # Step 3: Create workflow with AI-generated agents
            workflow_id = await self.stackai_client.create_agent_workflow(
                agents, f"dialectic_ai_context_{int(time.time())}"
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
            
            # Step 4: Execute workflow
            execution_id = await self.stackai_client.execute_workflow(
                workflow_id, {
                    "code_changes": context.code_changes,
                    "file_context": context.file_context,
                    "focus_area": context.focus_area,
                    "ai_analysis": context_analysis,
                    "llm_reasoning": llm_data
                }
            )
            
            # Step 5: AI-POWERED DOCUMENTATION UPDATES (ACTUAL GENERATION!)
            logger.info(f"📚 AI generating documentation...")
            documentation_updates = []
            
            for agent_spec in agents_specs:
                updates, content_data = await self.documentation_updater.update_documentation(
                    agent_spec, context_analysis
                )
                documentation_updates.extend(updates)
                logger.info(f"   ✏️  {agent_spec.agent_type}: {len(updates)} files with AI-generated content")
            
            # Step 6: AI LEARNING
            logger.info(f"🧠 AI learning from interaction...")
            await self.learning_engine.learn_from_event(
                event_data, agents_specs, 'success', documentation_updates
            )
            
            learning_summary = self.learning_engine.get_learning_summary()
            learning_events = [{
                "event_type": "ai_learning",
                "success_rate": learning_summary['success_rate'],
                "patterns_learned": learning_summary['patterns_learned'],
                "timestamp": time.time()
            }]
            
            # Store active workflow
            context_id = f"{context.focus_area}_{int(time.time())}"
            self.active_workflows[context_id] = workflow_id
            
            logger.info(f"✅ AI coordination complete: {len(agents)} agents, {len(documentation_updates)} updates")
            
            return AgentCoordinationResult(
                workflow_id=workflow_id,
                execution_id=execution_id or "",
                agents_generated=agents,
                documentation_updates=documentation_updates,
                learning_events=learning_events,
                success=True
            )
            
        except Exception as e:
            logger.error(f"❌ AI coordination failed: {e}", exc_info=True)
            return AgentCoordinationResult(
                workflow_id="",
                execution_id="",
                agents_generated=[],
                documentation_updates=[],
                learning_events=[],
                success=False,
                error_message=str(e)
            )
    
    # OLD HARDCODED METHODS REMOVED - NOW USING AI!
    
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

# Test function - AI-POWERED!
async def test_workflow_manager():
    """Test the AI-powered workflow manager functionality"""
    from streams.message_handler import MessageHandler
    
    print("🌌 TESTING AI-POWERED WORKFLOW MANAGER")
    print("=" * 70)
    
    # Initialize components with AI enabled
    stackai_client = StackAIClient()
    message_handler = MessageHandler()
    workflow_manager = WorkflowManager(stackai_client, message_handler, use_ai=True)
    
    print("\n✅ Initialized with AI-powered agent generation")
    
    # Test context - security focus
    context = AgentContext(
        code_changes=[
            "src/auth/jwt_handler.py", 
            "src/middleware/auth_middleware.py",
            "src/models/user.py"
        ],
        file_context={
            "src/auth/jwt_handler.py": "JWT token generation and validation",
            "src/middleware/auth_middleware.py": "Authentication middleware for API routes",
            "src/models/user.py": "User model with password hashing"
        },
        focus_area="security",
        urgency="high",
        metadata={
            "errors": [
                {"type": "AuthenticationError", "count": 2},
                {"type": "ValidationError", "count": 1}
            ]
        }
    )
    
    print(f"\n🎭 Test Context:")
    print(f"   Focus: {context.focus_area}")
    print(f"   Urgency: {context.urgency}")
    print(f"   Files: {', '.join(context.code_changes)}")
    
    # Test AI agent coordination
    print(f"\n🤖 Running AI-powered agent coordination...")
    result = await workflow_manager.coordinate_agents(context)
    
    print(f"\n📊 Coordination Results:")
    print(f"   Success: {result.success}")
    print(f"   Workflow ID: {result.workflow_id}")
    print(f"   Agents Generated: {len(result.agents_generated)}")
    print(f"   Documentation Updates: {len(result.documentation_updates)}")
    print(f"   Learning Events: {len(result.learning_events)}")
    
    if result.agents_generated:
        print(f"\n🤖 AI-Generated Agents:")
        for agent in result.agents_generated:
            print(f"   • {agent['type']}: {agent['description']}")
            print(f"     Confidence: {agent['context'].get('confidence', 'N/A')}")
            print(f"     LLM Generated: {agent.get('llm_generated', False)}")
    
    if result.documentation_updates:
        print(f"\n📚 AI-Generated Documentation Updates:")
        for update in result.documentation_updates[:3]:  # Show first 3
            print(f"   • {update.get('file', 'Unknown')}: {update.get('size', 0)} bytes")
    
    # Test active workflows
    active = workflow_manager.get_active_workflows()
    print(f"\n📁 Active Workflows: {len(active)}")
    
    print(f"\n🎉 AI-Powered Workflow Manager Test Complete!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_workflow_manager())
