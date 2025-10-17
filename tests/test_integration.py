"""
Integration Tests for Dialectic Streaming and Orchestration
Tests Redpanda streams and StackAI orchestration integration
"""
import asyncio
import json
import logging
import sys
import os
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streams.redpanda_client import RedpandaClient
from streams.message_handler import MessageHandler, MessageType, Message
from orchestration.stackai_client import StackAIClient
from orchestration.workflow_manager import WorkflowManager, AgentContext

logger = logging.getLogger(__name__)

class IntegrationTester:
    """Test integration between Redpanda streams and StackAI orchestration"""
    
    def __init__(self):
        self.redpanda_client = RedpandaClient()
        self.message_handler = MessageHandler()
        self.stackai_client = StackAIClient()
        self.workflow_manager = WorkflowManager(self.stackai_client, self.message_handler)
        self.test_results = {}
    
    async def run_full_integration_test(self) -> Dict[str, Any]:
        """Run complete integration test"""
        logger.info("Starting full integration test...")
        
        try:
            # Test 1: Redpanda streams setup
            await self.test_redpanda_streams()
            
            # Test 2: StackAI workflow creation
            await self.test_stackai_workflows()
            
            # Test 3: Message handling
            await self.test_message_handling()
            
            # Test 4: Agent coordination
            await self.test_agent_coordination()
            
            # Test 5: End-to-end workflow
            await self.test_end_to_end_workflow()
            
            logger.info("Integration test completed successfully")
            return {
                "success": True,
                "results": self.test_results,
                "summary": self._generate_summary()
            }
            
        except Exception as e:
            logger.error(f"Integration test failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": self.test_results
            }
    
    async def test_redpanda_streams(self):
        """Test Redpanda streaming functionality"""
        logger.info("Testing Redpanda streams...")
        
        try:
            # Setup streams
            success = await self.redpanda_client.setup_streams()
            assert success, "Failed to setup Redpanda streams"
            
            # Test agent message streaming
            agent_success = await self.redpanda_client.stream_agent_message(
                agent_id="test_agent",
                message="Test message from integration test",
                message_type="test"
            )
            assert agent_success, "Failed to stream agent message"
            
            # Test documentation update streaming
            doc_success = await self.redpanda_client.stream_documentation_update({
                "file": "integration_test.md",
                "action": "created",
                "content": "Integration test documentation"
            })
            assert doc_success, "Failed to stream documentation update"
            
            # Test learning event streaming
            learning_success = await self.redpanda_client.stream_learning_event({
                "event_type": "integration_test",
                "pattern": "test_pattern",
                "confidence": 0.95
            })
            assert learning_success, "Failed to stream learning event"
            
            # Health check
            health = await self.redpanda_client.health_check()
            assert health["is_running"], "Redpanda client not running"
            
            self.test_results["redpanda_streams"] = {
                "status": "PASSED",
                "details": {
                    "setup_success": success,
                    "agent_streaming": agent_success,
                    "doc_streaming": doc_success,
                    "learning_streaming": learning_success,
                    "health_check": health
                }
            }
            
            logger.info("Redpanda streams test PASSED")
            
        except Exception as e:
            logger.error(f"Redpanda streams test FAILED: {e}")
            self.test_results["redpanda_streams"] = {
                "status": "FAILED",
                "error": str(e)
            }
            raise
    
    async def test_stackai_workflows(self):
        """Test StackAI workflow creation and execution"""
        logger.info("Testing StackAI workflows...")
        
        try:
            # Create test agents
            test_agents = [
                {"id": "test_security", "type": "security_specialist", "name": "Test Security Agent"},
                {"id": "test_mvp", "type": "mvp_strategist", "name": "Test MVP Agent"},
                {"id": "test_doc", "type": "documentation_agent", "name": "Test Documentation Agent"}
            ]
            
            # Create workflow
            workflow_id = await self.stackai_client.create_agent_workflow(
                test_agents, "integration_test_workflow"
            )
            assert workflow_id, "Failed to create StackAI workflow"
            
            # Execute workflow
            execution_id = await self.stackai_client.execute_workflow(
                workflow_id, {
                    "code_changes": ["test.py", "integration.py"],
                    "context": "integration_test"
                }
            )
            assert execution_id, "Failed to execute StackAI workflow"
            
            # Check execution status
            await asyncio.sleep(0.2)  # Wait for execution
            status = await self.stackai_client.get_execution_status(execution_id)
            assert status, "Failed to get execution status"
            
            # Get workflow info
            workflow_info = self.stackai_client.get_workflow_info(workflow_id)
            assert workflow_info, "Failed to get workflow info"
            
            self.test_results["stackai_workflows"] = {
                "status": "PASSED",
                "details": {
                    "workflow_id": workflow_id,
                    "execution_id": execution_id,
                    "execution_status": status,
                    "workflow_info": workflow_info
                }
            }
            
            logger.info("StackAI workflows test PASSED")
            
        except Exception as e:
            logger.error(f"StackAI workflows test FAILED: {e}")
            self.test_results["stackai_workflows"] = {
                "status": "FAILED",
                "error": str(e)
            }
            raise
    
    async def test_message_handling(self):
        """Test message handling and routing"""
        logger.info("Testing message handling...")
        
        try:
            # Test message creation
            message = self.message_handler.create_message(
                sender_id="test_sender",
                message_type=MessageType.AGENT_GENERATION,
                content={"test": "data"},
                recipient_id="test_recipient"
            )
            assert message.id, "Failed to create message"
            
            # Test message broadcasting
            broadcast_success = await self.message_handler.broadcast_message(
                sender_id="test_sender",
                message_type=MessageType.DOCUMENTATION_UPDATE,
                content={"action": "test", "file": "test.md"}
            )
            assert broadcast_success, "Failed to broadcast message"
            
            # Test direct messaging
            direct_success = await self.message_handler.send_direct_message(
                sender_id="test_sender",
                recipient_id="test_recipient",
                message_type=MessageType.LEARNING_EVENT,
                content={"event_type": "test"}
            )
            assert direct_success, "Failed to send direct message"
            
            # Test message stats
            stats = self.message_handler.get_message_stats()
            assert "queue_size" in stats, "Failed to get message stats"
            
            self.test_results["message_handling"] = {
                "status": "PASSED",
                "details": {
                    "message_creation": True,
                    "broadcast_success": broadcast_success,
                    "direct_message_success": direct_success,
                    "stats": stats
                }
            }
            
            logger.info("Message handling test PASSED")
            
        except Exception as e:
            logger.error(f"Message handling test FAILED: {e}")
            self.test_results["message_handling"] = {
                "status": "FAILED",
                "error": str(e)
            }
            raise
    
    async def test_agent_coordination(self):
        """Test agent coordination through workflow manager"""
        logger.info("Testing agent coordination...")
        
        try:
            # Create test context
            context = AgentContext(
                code_changes=["auth.py", "security.py"],
                file_context={"auth.py": "authentication logic"},
                focus_area="security",
                urgency="high"
            )
            
            # Test agent coordination
            result = await self.workflow_manager.coordinate_agents(context)
            assert result.success, f"Agent coordination failed: {result.error_message}"
            assert result.workflow_id, "No workflow ID returned"
            assert len(result.agents_generated) > 0, "No agents generated"
            assert len(result.documentation_updates) > 0, "No documentation updates"
            assert len(result.learning_events) > 0, "No learning events"
            
            # Test active workflows
            active_workflows = self.workflow_manager.get_active_workflows()
            assert len(active_workflows) > 0, "No active workflows found"
            
            self.test_results["agent_coordination"] = {
                "status": "PASSED",
                "details": {
                    "coordination_success": result.success,
                    "workflow_id": result.workflow_id,
                    "execution_id": result.execution_id,
                    "agents_generated": len(result.agents_generated),
                    "documentation_updates": len(result.documentation_updates),
                    "learning_events": len(result.learning_events),
                    "active_workflows": len(active_workflows)
                }
            }
            
            logger.info("Agent coordination test PASSED")
            
        except Exception as e:
            logger.error(f"Agent coordination test FAILED: {e}")
            self.test_results["agent_coordination"] = {
                "status": "FAILED",
                "error": str(e)
            }
            raise
    
    async def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        logger.info("Testing end-to-end workflow...")
        
        try:
            # Simulate code change detection
            code_changes = ["auth.py", "middleware.py", "security.py"]
            file_context = {
                "auth.py": "authentication and authorization logic",
                "middleware.py": "request processing middleware",
                "security.py": "security utilities and helpers"
            }
            
            # Create context for security focus
            context = AgentContext(
                code_changes=code_changes,
                file_context=file_context,
                focus_area="security",
                urgency="high",
                metadata={"test_run": True}
            )
            
            # Coordinate agents
            result = await self.workflow_manager.coordinate_agents(context)
            assert result.success, f"End-to-end workflow failed: {result.error_message}"
            
            # Verify agents were generated
            security_agents = [a for a in result.agents_generated if a["type"] == "security_specialist"]
            assert len(security_agents) > 0, "No security agents generated"
            
            # Verify documentation updates
            security_docs = [d for d in result.documentation_updates if "security" in d["file"]]
            assert len(security_docs) > 0, "No security documentation updates"
            
            # Verify learning events
            pattern_events = [e for e in result.learning_events if e["event_type"] == "pattern_recognized"]
            assert len(pattern_events) > 0, "No pattern recognition events"
            
            self.test_results["end_to_end_workflow"] = {
                "status": "PASSED",
                "details": {
                    "workflow_success": result.success,
                    "security_agents": len(security_agents),
                    "security_docs": len(security_docs),
                    "pattern_events": len(pattern_events),
                    "total_agents": len(result.agents_generated),
                    "total_updates": len(result.documentation_updates),
                    "total_events": len(result.learning_events)
                }
            }
            
            logger.info("End-to-end workflow test PASSED")
            
        except Exception as e:
            logger.error(f"End-to-end workflow test FAILED: {e}")
            self.test_results["end_to_end_workflow"] = {
                "status": "FAILED",
                "error": str(e)
            }
            raise
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate test summary"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() 
                          if result["status"] == "PASSED")
        failed_tests = total_tests - passed_tests
        
        return {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "success_rate": f"{(passed_tests / total_tests * 100):.1f}%" if total_tests > 0 else "0%"
        }
    
    async def cleanup(self):
        """Cleanup test resources"""
        try:
            await self.redpanda_client.stop()
            logger.info("Test cleanup completed")
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")

async def run_integration_test():
    """Run the integration test"""
    tester = IntegrationTester()
    
    try:
        result = await tester.run_full_integration_test()
        
        print("\n" + "="*50)
        print("DIALECTIC INTEGRATION TEST RESULTS")
        print("="*50)
        
        if result["success"]:
            print("✅ ALL TESTS PASSED!")
            print(f"Success Rate: {result['summary']['success_rate']}")
        else:
            print("❌ TESTS FAILED!")
            print(f"Error: {result['error']}")
        
        print("\nDetailed Results:")
        for test_name, test_result in result["results"].items():
            status = "✅ PASSED" if test_result["status"] == "PASSED" else "❌ FAILED"
            print(f"  {test_name}: {status}")
            
            if test_result["status"] == "FAILED":
                print(f"    Error: {test_result['error']}")
        
        return result["success"]
        
    finally:
        await tester.cleanup()

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the test
    success = asyncio.run(run_integration_test())
    sys.exit(0 if success else 1)
