"""
Redpanda Client for Dialectic A2A Communication
Handles streaming communication between agents using Redpanda Connect
"""
import asyncio
import json
import time
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import subprocess
import os

logger = logging.getLogger(__name__)

@dataclass
class AgentMessage:
    """Message structure for agent communication"""
    agent_id: str
    message: str
    timestamp: float
    message_type: str = "communication"
    metadata: Optional[Dict[str, Any]] = None

class RedpandaClient:
    """Client for managing Redpanda Connect streams for agent communication"""
    
    def __init__(self, config_path: str = "redpanda_config.yaml"):
        self.config_path = config_path
        self.topics = {
            'agent_communication': 'dialectic_agents',
            'documentation_updates': 'dialectic_docs', 
            'learning_events': 'dialectic_learning'
        }
        self.process: Optional[subprocess.Popen] = None
        self.is_running = False
        
    async def setup_streams(self) -> bool:
        """Setup Redpanda Connect streams for A2A communication"""
        try:
            # Create Redpanda Connect configuration
            await self._create_config()
            
            # Start Redpanda Connect process
            await self._start_redpanda_connect()
            
            logger.info("Redpanda Connect streams setup successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup Redpanda streams: {e}")
            return False
    
    async def _create_config(self):
        """Create Redpanda Connect configuration file"""
        # Use the connect.yaml file that was created with rpk connect create
        if os.path.exists("connect.yaml"):
            logger.info("Using existing connect.yaml configuration")
            self.config_path = "connect.yaml"
            return
        
        # Fallback configuration
        config = {
            "input": {
                "stdin": {}
            },
            "pipeline": {
                "processors": [
                    {
                        "mapping": "root.topic = this.topic"
                    }
                ]
            },
            "output": {
                "redpanda": {
                    "addresses": ["localhost:9092"],
                    "topic": "dialectic_agents"
                }
            }
        }
        
        with open(self.config_path, 'w') as f:
            import yaml
            yaml.dump(config, f)
            
        logger.info(f"Created Redpanda config at {self.config_path}")
    
    async def _start_redpanda_connect(self):
        """Start Redpanda Connect process"""
        try:
            # Check if rpk is available
            result = subprocess.run(['rpk', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                logger.warning("rpk not found, using mock mode")
                self.is_running = True
                return
                
            # Start Redpanda Connect
            self.process = subprocess.Popen(
                ['rpk', 'connect', 'run', self.config_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True
            )
            
            self.is_running = True
            logger.info("Redpanda Connect started successfully")
            
        except Exception as e:
            logger.warning(f"Could not start Redpanda Connect: {e}")
            # Fallback to mock mode
            self.is_running = True
    
    async def stream_agent_message(self, agent_id: str, message: str, 
                                 message_type: str = "communication",
                                 metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Stream message between agents"""
        try:
            agent_message = AgentMessage(
                agent_id=agent_id,
                message=message,
                timestamp=time.time(),
                message_type=message_type,
                metadata=metadata
            )
            
            if self.is_running and self.process:
                # Send to Redpanda Connect
                message_json = json.dumps({
                    "agent_id": agent_message.agent_id,
                    "message": agent_message.message,
                    "timestamp": agent_message.timestamp,
                    "message_type": agent_message.message_type,
                    "metadata": agent_message.metadata or {}
                })
                
                self.process.stdin.write(message_json + "\n")
                self.process.stdin.flush()
                
            else:
                # Mock mode - log the message
                logger.info(f"[MOCK] Agent {agent_id}: {message}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to stream agent message: {e}")
            return False
    
    async def stream_documentation_update(self, update_data: Dict[str, Any]) -> bool:
        """Stream documentation update events"""
        return await self.stream_agent_message(
            agent_id="documentation_agent",
            message=f"Updated {update_data.get('file', 'unknown file')}",
            message_type="documentation_update",
            metadata=update_data
        )
    
    async def stream_learning_event(self, event_data: Dict[str, Any]) -> bool:
        """Stream learning events for pattern recognition"""
        return await self.stream_agent_message(
            agent_id="learning_engine",
            message=f"Learning event: {event_data.get('event_type', 'unknown')}",
            message_type="learning_event",
            metadata=event_data
        )
    
    async def consume_messages(self, topic: str, callback) -> None:
        """Consume messages from a topic"""
        try:
            if not self.is_running:
                logger.warning("Redpanda Connect not running, cannot consume messages")
                return
                
            # In a real implementation, this would set up a consumer
            # For now, we'll use a mock approach
            logger.info(f"Mock consuming messages from topic: {topic}")
            
        except Exception as e:
            logger.error(f"Failed to consume messages: {e}")
    
    async def stop(self):
        """Stop Redpanda Connect process"""
        try:
            if self.process:
                self.process.terminate()
                self.process.wait()
                self.process = None
            
            self.is_running = False
            logger.info("Redpanda Connect stopped")
            
        except Exception as e:
            logger.error(f"Error stopping Redpanda Connect: {e}")
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of Redpanda streams"""
        return {
            "is_running": self.is_running,
            "process_active": self.process is not None,
            "topics": list(self.topics.keys()),
            "config_path": self.config_path
        }

# Test function for development
async def test_redpanda_client():
    """Test the Redpanda client functionality"""
    client = RedpandaClient()
    
    # Setup streams
    success = await client.setup_streams()
    print(f"Setup success: {success}")
    
    # Test message streaming
    await client.stream_agent_message(
        agent_id="test_agent",
        message="Hello from test agent",
        message_type="test"
    )
    
    # Test documentation update
    await client.stream_documentation_update({
        "file": "test.md",
        "action": "created",
        "content": "Test documentation"
    })
    
    # Test learning event
    await client.stream_learning_event({
        "event_type": "pattern_recognized",
        "pattern": "security_focus",
        "confidence": 0.85
    })
    
    # Health check
    health = await client.health_check()
    print(f"Health check: {health}")
    
    # Cleanup
    await client.stop()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_redpanda_client())
