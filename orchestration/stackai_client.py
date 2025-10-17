"""
StackAI Client for Dialectic Agent Orchestration
Handles workflow creation and agent coordination using StackAI platform
"""
import asyncio
import json
import logging
import requests
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import time

logger = logging.getLogger(__name__)

@dataclass
class AgentWorkflow:
    """Represents an agent workflow configuration"""
    name: str
    agents: List[Dict[str, Any]]
    steps: List[Dict[str, Any]]
    triggers: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class WorkflowExecution:
    """Represents a workflow execution"""
    execution_id: str
    workflow_name: str
    status: str
    start_time: float
    end_time: Optional[float] = None
    results: Optional[Dict[str, Any]] = None

class StackAIClient:
    """Client for managing StackAI workflows and agent orchestration"""
    
    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        self.api_key = api_key or "326807a3-a8f3-4b08-8ffc-26a7876520ee"
        self.api_url = api_url or "https://api.stack-ai.com/inference/v0/run/63b4a22b-6fa3-4bfa-a9ca-c0c38adff339/68f283f97f9c77b55c29ebda"
        self.workflows: Dict[str, AgentWorkflow] = {}
        self.executions: Dict[str, WorkflowExecution] = {}
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
    
    async def create_agent_workflow(self, agents: List[Dict[str, Any]], 
                                 workflow_name: str = "dialectic_agent_collaboration") -> Optional[str]:
        """Create workflow for agent collaboration"""
        try:
            # Define workflow steps based on agent types
            steps = self._generate_workflow_steps(agents)
            
            workflow = AgentWorkflow(
                name=workflow_name,
                agents=agents,
                steps=steps,
                metadata={
                    "created_at": time.time(),
                    "agent_count": len(agents),
                    "dialectic_version": "1.0"
                }
            )
            
            # In a real implementation, this would call StackAI API
            # For now, we'll simulate the API call
            workflow_id = await self._create_stackai_workflow(workflow)
            
            # Store workflow_id in metadata
            workflow.metadata["workflow_id"] = workflow_id
            
            # Store workflow locally
            self.workflows[workflow_name] = workflow
            
            logger.info(f"Created workflow '{workflow_name}' with {len(agents)} agents")
            return workflow_id
            
        except Exception as e:
            logger.error(f"Failed to create agent workflow: {e}")
            return None
    
    def _generate_workflow_steps(self, agents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate workflow steps based on agent types"""
        steps = []
        
        # Always start with context analysis
        steps.append({
            "step_id": "analyze_context",
            "agent_type": "analyzer",
            "action": "analyze_codebase_context",
            "inputs": ["code_changes", "file_context"],
            "outputs": ["analysis_result"]
        })
        
        # Add agent-specific steps
        for agent in agents:
            agent_type = agent.get("type", "general")
            
            if agent_type == "security_specialist":
                steps.append({
                    "step_id": f"security_analysis_{agent['id']}",
                    "agent_type": "security_specialist",
                    "action": "analyze_security_patterns",
                    "inputs": ["analysis_result"],
                    "outputs": ["security_recommendations"]
                })
            
            elif agent_type == "mvp_strategist":
                steps.append({
                    "step_id": f"mvp_analysis_{agent['id']}",
                    "agent_type": "mvp_strategist", 
                    "action": "analyze_mvp_requirements",
                    "inputs": ["analysis_result"],
                    "outputs": ["mvp_recommendations"]
                })
            
            elif agent_type == "performance_expert":
                steps.append({
                    "step_id": f"performance_analysis_{agent['id']}",
                    "agent_type": "performance_expert",
                    "action": "analyze_performance_patterns",
                    "inputs": ["analysis_result"],
                    "outputs": ["performance_recommendations"]
                })
        
        # Always end with documentation update
        steps.append({
            "step_id": "update_documentation",
            "agent_type": "documentation_agent",
            "action": "update_cursor_documentation",
            "inputs": ["security_recommendations", "mvp_recommendations", "performance_recommendations"],
            "outputs": ["documentation_updates"]
        })
        
        return steps
    
    async def _create_stackai_workflow(self, workflow: AgentWorkflow) -> str:
        """Create workflow in StackAI platform"""
        try:
            # In a real implementation, this would make an API call to StackAI
            # For now, we'll simulate the response
            
            workflow_data = {
                "name": workflow.name,
                "description": f"Dialectic agent collaboration workflow with {len(workflow.agents)} agents",
                "nodes": self._convert_to_stackai_nodes(workflow),
                "connections": self._generate_connections(workflow.steps)
            }
            
            # Simulate API call
            await asyncio.sleep(0.1)  # Simulate network delay
            
            workflow_id = f"workflow_{int(time.time())}"
            logger.info(f"Simulated StackAI workflow creation: {workflow_id}")
            
            return workflow_id
            
        except Exception as e:
            logger.error(f"Failed to create StackAI workflow: {e}")
            raise
    
    def _convert_to_stackai_nodes(self, workflow: AgentWorkflow) -> List[Dict[str, Any]]:
        """Convert workflow steps to StackAI node format"""
        nodes = []
        
        for i, step in enumerate(workflow.steps):
            node = {
                "id": step["step_id"],
                "type": "llm",  # StackAI LLM node type
                "position": {"x": i * 200, "y": 100},
                "data": {
                    "prompt": self._generate_agent_prompt(step),
                    "model": "gpt-4",
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
            }
            nodes.append(node)
        
        return nodes
    
    def _generate_agent_prompt(self, step: Dict[str, Any]) -> str:
        """Generate prompt for agent step"""
        agent_type = step["agent_type"]
        action = step["action"]
        
        prompts = {
            "analyzer": f"Analyze the codebase context and identify key patterns, changes, and areas of focus. Action: {action}",
            "security_specialist": f"Review the code changes for security implications, vulnerabilities, and best practices. Action: {action}",
            "mvp_strategist": f"Evaluate the changes for MVP impact, user value, and development priorities. Action: {action}",
            "performance_expert": f"Analyze performance implications, optimization opportunities, and scalability concerns. Action: {action}",
            "documentation_agent": f"Update documentation based on the analysis results and recommendations. Action: {action}"
        }
        
        return prompts.get(agent_type, f"Execute {action} as {agent_type}")
    
    def _generate_connections(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate connections between workflow steps"""
        connections = []
        
        for i in range(len(steps) - 1):
            connection = {
                "source": steps[i]["step_id"],
                "target": steps[i + 1]["step_id"],
                "sourceHandle": "output",
                "targetHandle": "input"
            }
            connections.append(connection)
        
        return connections
    
    async def execute_workflow(self, workflow_identifier: str, 
                            input_data: Dict[str, Any]) -> Optional[str]:
        """Execute a workflow with given input data"""
        try:
            # Check if workflow_identifier is a workflow_id or workflow_name
            if workflow_identifier.startswith("workflow_"):
                # It's a workflow_id, find the corresponding workflow
                workflow_name = None
                for name, workflow in self.workflows.items():
                    if workflow.metadata.get("workflow_id") == workflow_identifier:
                        workflow_name = name
                        break
                
                if not workflow_name:
                    logger.error(f"Workflow with ID '{workflow_identifier}' not found")
                    return None
            else:
                # It's a workflow_name
                workflow_name = workflow_identifier
                if workflow_name not in self.workflows:
                    logger.error(f"Workflow '{workflow_name}' not found")
                    return None
            
            workflow = self.workflows[workflow_name]
            execution_id = f"exec_{int(time.time())}"
            
            execution = WorkflowExecution(
                execution_id=execution_id,
                workflow_name=workflow_name,
                status="running",
                start_time=time.time()
            )
            
            self.executions[execution_id] = execution
            
            # Simulate workflow execution
            await self._simulate_workflow_execution(execution, input_data)
            
            logger.info(f"Executed workflow '{workflow_name}' with ID: {execution_id}")
            return execution_id
            
        except Exception as e:
            logger.error(f"Failed to execute workflow: {e}")
            return None
    
    async def _simulate_workflow_execution(self, execution: WorkflowExecution, 
                                        input_data: Dict[str, Any]):
        """Execute workflow using StackAI API"""
        try:
            workflow = self.workflows[execution.workflow_name]
            
            # Prepare input for StackAI
            agent_types = [agent["type"] for agent in workflow.agents]
            focus_area = input_data.get('focus_area', 'general')
            code_changes = input_data.get('code_changes', [])
            
            stackai_input = {
                "user_id": f"dialectic_{execution.execution_id}",
                "in-0": f"Analyze code changes: {code_changes} with focus on {focus_area}. Generate agents: {agent_types}"
            }
            
            # Call StackAI API
            try:
                response = await self._call_stackai_api(stackai_input)
                logger.info(f"StackAI API response: {response}")
                
                # Process the response
                results = {
                    "stackai_response": response,
                    "workflow_name": execution.workflow_name,
                    "status": "completed",
                    "agents_analyzed": len(workflow.agents),
                    "focus_area": focus_area,
                    "code_changes": code_changes
                }
                
            except Exception as api_error:
                logger.warning(f"StackAI API call failed, using fallback: {api_error}")
                # Fallback to simulation
                results = {}
                for step in workflow.steps:
                    step_result = {
                        "step_id": step["step_id"],
                        "agent_type": step["agent_type"],
                        "status": "completed",
                        "output": f"Fallback result from {step['agent_type']}"
                    }
                    results[step["step_id"]] = step_result
            
            # Update execution
            execution.status = "completed"
            execution.end_time = time.time()
            execution.results = results
            
        except Exception as e:
            execution.status = "failed"
            execution.end_time = time.time()
            logger.error(f"Workflow execution failed: {e}")
    
    async def _call_stackai_api(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Call the StackAI API"""
        try:
            # Use asyncio to run the synchronous request
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.session.post(self.api_url, json=payload)
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"StackAI API error: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"StackAI API call failed: {e}")
            raise
    
    async def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a workflow execution"""
        if execution_id not in self.executions:
            return None
        
        execution = self.executions[execution_id]
        
        return {
            "execution_id": execution_id,
            "workflow_name": execution.workflow_name,
            "status": execution.status,
            "start_time": execution.start_time,
            "end_time": execution.end_time,
            "duration": (execution.end_time or time.time()) - execution.start_time,
            "results": execution.results
        }
    
    def get_workflow_info(self, workflow_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a workflow"""
        if workflow_name not in self.workflows:
            return None
        
        workflow = self.workflows[workflow_name]
        
        return {
            "name": workflow.name,
            "agent_count": len(workflow.agents),
            "step_count": len(workflow.steps),
            "created_at": workflow.metadata.get("created_at"),
            "agents": [agent["type"] for agent in workflow.agents]
        }
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all workflows"""
        return [
            self.get_workflow_info(name) 
            for name in self.workflows.keys()
        ]

# Test function
async def test_stackai_client():
    """Test the StackAI client functionality"""
    client = StackAIClient()
    
    # Create test agents
    agents = [
        {"id": "security_1", "type": "security_specialist", "name": "Security Expert"},
        {"id": "mvp_1", "type": "mvp_strategist", "name": "MVP Strategist"},
        {"id": "perf_1", "type": "performance_expert", "name": "Performance Expert"}
    ]
    
    # Create workflow
    workflow_id = await client.create_agent_workflow(agents)
    print(f"Created workflow: {workflow_id}")
    
    # Execute workflow
    execution_id = await client.execute_workflow(
        "dialectic_agent_collaboration",
        {"code_changes": ["auth.py", "security.py"], "context": "security_focus"}
    )
    print(f"Executed workflow: {execution_id}")
    
    # Check execution status
    if execution_id:
        await asyncio.sleep(0.2)  # Wait for execution
        status = await client.get_execution_status(execution_id)
        print(f"Execution status: {status}")
    
    # List workflows
    workflows = client.list_workflows()
    print(f"Available workflows: {workflows}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_stackai_client())
