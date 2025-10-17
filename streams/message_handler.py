"""
Message Handler for Dialectic A2A Communication
Handles message routing and processing between agents
"""
import asyncio
import json
import logging
from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import time

logger = logging.getLogger(__name__)

class MessageType(Enum):
    """Types of messages in the system"""
    COMMUNICATION = "communication"
    DOCUMENTATION_UPDATE = "documentation_update"
    LEARNING_EVENT = "learning_event"
    AGENT_GENERATION = "agent_generation"
    WORKFLOW_TRIGGER = "workflow_trigger"

@dataclass
class Message:
    """Standard message format for agent communication"""
    id: str
    sender_id: str
    recipient_id: Optional[str]
    message_type: MessageType
    content: Dict[str, Any]
    timestamp: float
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary"""
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "message_type": self.message_type.value,
            "content": self.content,
            "timestamp": self.timestamp,
            "metadata": self.metadata or {}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create message from dictionary"""
        return cls(
            id=data["id"],
            sender_id=data["sender_id"],
            recipient_id=data.get("recipient_id"),
            message_type=MessageType(data["message_type"]),
            content=data["content"],
            timestamp=data["timestamp"],
            metadata=data.get("metadata")
        )

class MessageHandler:
    """Handles message routing and processing for agent communication"""
    
    def __init__(self):
        self.handlers: Dict[MessageType, List[Callable]] = {}
        self.message_queue: List[Message] = []
        self.is_processing = False
        
    def register_handler(self, message_type: MessageType, handler: Callable):
        """Register a handler for a specific message type"""
        if message_type not in self.handlers:
            self.handlers[message_type] = []
        
        self.handlers[message_type].append(handler)
        logger.info(f"Registered handler for {message_type.value}")
    
    async def send_message(self, message: Message) -> bool:
        """Send a message to the appropriate handlers"""
        try:
            # Add to queue
            self.message_queue.append(message)
            
            # Process immediately if not already processing
            if not self.is_processing:
                await self._process_queue()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    async def _process_queue(self):
        """Process all messages in the queue"""
        if self.is_processing:
            return
            
        self.is_processing = True
        
        try:
            while self.message_queue:
                message = self.message_queue.pop(0)
                await self._process_message(message)
                
        finally:
            self.is_processing = False
    
    async def _process_message(self, message: Message):
        """Process a single message"""
        try:
            message_type = message.message_type
            
            if message_type in self.handlers:
                handlers = self.handlers[message_type]
                
                # Execute all handlers for this message type
                for handler in handlers:
                    try:
                        await self._execute_handler(handler, message)
                    except Exception as e:
                        logger.error(f"Handler execution failed: {e}")
            else:
                logger.warning(f"No handlers registered for {message_type.value}")
                
        except Exception as e:
            logger.error(f"Failed to process message: {e}")
    
    async def _execute_handler(self, handler: Callable, message: Message):
        """Execute a message handler"""
        if asyncio.iscoroutinefunction(handler):
            await handler(message)
        else:
            handler(message)
    
    def create_message(self, sender_id: str, message_type: MessageType, 
                      content: Dict[str, Any], recipient_id: Optional[str] = None,
                      metadata: Optional[Dict[str, Any]] = None) -> Message:
        """Create a new message"""
        message_id = f"{sender_id}_{int(time.time() * 1000)}"
        
        return Message(
            id=message_id,
            sender_id=sender_id,
            recipient_id=recipient_id,
            message_type=message_type,
            content=content,
            timestamp=time.time(),
            metadata=metadata
        )
    
    async def broadcast_message(self, sender_id: str, message_type: MessageType,
                              content: Dict[str, Any], 
                              metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Broadcast a message to all agents"""
        message = self.create_message(
            sender_id=sender_id,
            message_type=message_type,
            content=content,
            metadata=metadata
        )
        
        return await self.send_message(message)
    
    async def send_direct_message(self, sender_id: str, recipient_id: str,
                                message_type: MessageType, content: Dict[str, Any],
                                metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Send a direct message to a specific agent"""
        message = self.create_message(
            sender_id=sender_id,
            message_type=message_type,
            content=content,
            recipient_id=recipient_id,
            metadata=metadata
        )
        
        return await self.send_message(message)
    
    def get_message_stats(self) -> Dict[str, Any]:
        """Get statistics about message processing"""
        return {
            "queue_size": len(self.message_queue),
            "is_processing": self.is_processing,
            "registered_handlers": {
                msg_type.value: len(handlers) 
                for msg_type, handlers in self.handlers.items()
            }
        }

# Example handlers for different message types
async def documentation_update_handler(message: Message):
    """Handle documentation update messages"""
    logger.info(f"Documentation update from {message.sender_id}: {message.content}")
    
    # In a real implementation, this would trigger documentation updates
    # For now, just log the event
    if message.content.get("action") == "create":
        logger.info(f"Creating documentation: {message.content.get('file')}")
    elif message.content.get("action") == "update":
        logger.info(f"Updating documentation: {message.content.get('file')}")

async def learning_event_handler(message: Message):
    """Handle learning event messages"""
    logger.info(f"Learning event from {message.sender_id}: {message.content}")
    
    # Process learning events for pattern recognition
    event_type = message.content.get("event_type")
    if event_type == "pattern_recognized":
        pattern = message.content.get("pattern")
        confidence = message.content.get("confidence", 0.0)
        logger.info(f"Pattern recognized: {pattern} (confidence: {confidence})")

async def agent_generation_handler(message: Message):
    """Handle agent generation messages"""
    logger.info(f"Agent generation from {message.sender_id}: {message.content}")
    
    # Process agent generation requests
    agent_type = message.content.get("agent_type")
    context = message.content.get("context", {})
    logger.info(f"Generating {agent_type} agent with context: {context}")

# Test function
async def test_message_handler():
    """Test the message handler functionality"""
    handler = MessageHandler()
    
    # Register handlers
    handler.register_handler(MessageType.DOCUMENTATION_UPDATE, documentation_update_handler)
    handler.register_handler(MessageType.LEARNING_EVENT, learning_event_handler)
    handler.register_handler(MessageType.AGENT_GENERATION, agent_generation_handler)
    
    # Test documentation update
    await handler.broadcast_message(
        sender_id="mcp_server",
        message_type=MessageType.DOCUMENTATION_UPDATE,
        content={
            "action": "create",
            "file": "security_patterns.md",
            "content": "Security patterns documentation"
        }
    )
    
    # Test learning event
    await handler.broadcast_message(
        sender_id="learning_engine",
        message_type=MessageType.LEARNING_EVENT,
        content={
            "event_type": "pattern_recognized",
            "pattern": "security_focus",
            "confidence": 0.85
        }
    )
    
    # Test agent generation
    await handler.broadcast_message(
        sender_id="agent_generator",
        message_type=MessageType.AGENT_GENERATION,
        content={
            "agent_type": "security_specialist",
            "context": {"files_changed": ["auth.py", "security.py"]}
        }
    )
    
    # Wait for processing
    await asyncio.sleep(0.1)
    
    # Get stats
    stats = handler.get_message_stats()
    print(f"Message handler stats: {stats}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_message_handler())
