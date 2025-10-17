"""
WebSocket Bridge for Dialectic
Connects backend (live_demo.py) to frontend (dashboard.html)

This is the integration layer between Aria's backend and Shrey's frontend.
"""

import asyncio
import websockets
import json
import logging
from typing import Set, Dict, Any, Optional, Callable
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class WebSocketClient:
    """Represents a connected WebSocket client"""
    websocket: websockets.WebSocketServerProtocol
    client_id: str
    connected_at: float


class WebSocketBridge:
    """
    WebSocket bridge between backend and frontend
    
    Handles:
    - Broadcasting backend events to frontend dashboard
    - Receiving demo triggers from frontend
    - Managing WebSocket connections
    """
    
    def __init__(self, host: str = "localhost", port: int = 8000):
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.server = None
        self.is_running = False
        
        # Callback handlers for frontend triggers
        self.demo_triggers: Dict[str, Callable] = {}
        
        logger.info(f"WebSocket bridge initialized on {host}:{port}")
    
    async def start(self):
        """Start the WebSocket server"""
        try:
            self.server = await websockets.serve(
                self.handler,
                self.host,
                self.port
            )
            self.is_running = True
            logger.info(f"🌐 WebSocket server started on ws://{self.host}:{self.port}/ws")
            print(f"🌐 WebSocket server ready at ws://{self.host}:{self.port}/ws")
            
        except Exception as e:
            logger.error(f"Failed to start WebSocket server: {e}")
            raise
    
    async def stop(self):
        """Stop the WebSocket server"""
        self.is_running = False
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        logger.info("WebSocket server stopped")
    
    async def handler(self, websocket, path):
        """Handle WebSocket connection"""
        client_id = f"client_{id(websocket)}"
        
        # Register client
        await self.register(websocket)
        logger.info(f"✅ Client connected: {client_id}")
        
        try:
            # Send welcome message
            await websocket.send(json.dumps({
                'type': 'connection_established',
                'client_id': client_id,
                'message': 'Connected to Dialectic backend'
            }))
            
            # Listen for messages from frontend
            async for message in websocket:
                await self.handle_frontend_message(websocket, message)
                
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client disconnected: {client_id}")
        except Exception as e:
            logger.error(f"Error handling client {client_id}: {e}")
        finally:
            await self.unregister(websocket)
    
    async def register(self, websocket):
        """Register a new WebSocket client"""
        self.clients.add(websocket)
        logger.debug(f"Total clients: {len(self.clients)}")
    
    async def unregister(self, websocket):
        """Unregister a WebSocket client"""
        self.clients.discard(websocket)
        logger.debug(f"Total clients: {len(self.clients)}")
    
    async def handle_frontend_message(self, websocket, message: str):
        """Handle incoming messages from frontend"""
        try:
            data = json.loads(message)
            action = data.get('action')
            
            if action == 'trigger_demo':
                # Handle demo trigger from frontend button
                scenario = data.get('scenario')
                await self.trigger_demo(scenario)
                
            elif action == 'ping':
                # Respond to ping
                await websocket.send(json.dumps({
                    'type': 'pong',
                    'timestamp': data.get('timestamp')
                }))
            
            else:
                logger.warning(f"Unknown action from frontend: {action}")
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON from frontend: {e}")
        except Exception as e:
            logger.error(f"Error handling frontend message: {e}")
    
    async def trigger_demo(self, scenario: str):
        """Trigger a demo scenario from frontend"""
        if scenario in self.demo_triggers:
            callback = self.demo_triggers[scenario]
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(scenario)
                else:
                    callback(scenario)
                logger.info(f"Triggered demo scenario: {scenario}")
            except Exception as e:
                logger.error(f"Error triggering demo {scenario}: {e}")
        else:
            logger.warning(f"No handler for demo scenario: {scenario}")
    
    def register_demo_trigger(self, scenario: str, callback: Callable):
        """Register a callback for demo scenario triggers"""
        self.demo_triggers[scenario] = callback
        logger.info(f"Registered demo trigger: {scenario}")
    
    async def broadcast(self, message: Dict[str, Any]):
        """
        Broadcast message to all connected clients
        
        Args:
            message: Dictionary to send (will be JSON serialized)
        """
        if not self.clients:
            logger.debug("No clients connected, skipping broadcast")
            return
        
        try:
            message_json = json.dumps(message)
            
            # Send to all connected clients
            await asyncio.gather(
                *[client.send(message_json) for client in self.clients],
                return_exceptions=True
            )
            
            logger.debug(f"Broadcasted {message.get('type')} to {len(self.clients)} clients")
            
        except Exception as e:
            logger.error(f"Error broadcasting message: {e}")
    
    async def broadcast_agent_generated(self, agent: Dict[str, Any]):
        """Broadcast agent generation event"""
        await self.broadcast({
            'type': 'agent_generated',
            'agent': agent
        })
    
    async def broadcast_documentation_updated(self, update: Dict[str, Any]):
        """Broadcast documentation update event"""
        await self.broadcast({
            'type': 'documentation_updated',
            'update': update
        })
    
    async def broadcast_learning_event(self, event: Dict[str, Any]):
        """Broadcast learning event"""
        await self.broadcast({
            'type': 'learning_event',
            'event': event
        })
    
    async def broadcast_workflow_executed(self, workflow: Dict[str, Any]):
        """Broadcast workflow execution event"""
        await self.broadcast({
            'type': 'workflow_executed',
            'workflow': workflow
        })
    
    def get_stats(self) -> Dict[str, Any]:
        """Get WebSocket bridge statistics"""
        return {
            'is_running': self.is_running,
            'connected_clients': len(self.clients),
            'registered_triggers': list(self.demo_triggers.keys()),
            'server_address': f"ws://{self.host}:{self.port}/ws"
        }


# Example usage / test
async def test_websocket_bridge():
    """Test the WebSocket bridge"""
    bridge = WebSocketBridge()
    
    # Register demo trigger handlers
    async def handle_security_demo(scenario):
        print(f"🔒 Security demo triggered: {scenario}")
        await bridge.broadcast_agent_generated({
            'id': 'test_security_1',
            'type': 'security_specialist',
            'name': 'Security Specialist',
            'description': 'Test agent from demo trigger',
            'capabilities': ['vulnerability_detection'],
            'generated_at': asyncio.get_event_loop().time()
        })
    
    bridge.register_demo_trigger('security', handle_security_demo)
    
    # Start server
    await bridge.start()
    
    print("\n🎯 WebSocket bridge running")
    print(f"   Connect from: ws://{bridge.host}:{bridge.port}/ws")
    print("   Open dashboard.html to test")
    print("   Press Ctrl+C to stop\n")
    
    try:
        # Keep server running
        await asyncio.Future()  # Run forever
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    finally:
        await bridge.stop()


if __name__ == "__main__":
    # Test the bridge
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    asyncio.run(test_websocket_bridge())

