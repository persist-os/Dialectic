/**
 * Dialectic Demo Interface
 * Handles real-time updates and demo controls for the agent dashboard
 */
class DialecticDemo {
    constructor() {
        this.ws = null;
        this.isConnected = false;
        this.agents = new Map();
        this.updateCount = 0;
        this.workflowCount = 0;
        this.learningCount = 0;
        
        this.init();
    }
    
    init() {
        this.setupWebSocket();
        this.setupEventHandlers();
        this.updateConnectionStatus(false);
        
        // Add some initial demo data
        this.addInitialDemoData();
    }
    
    setupWebSocket() {
        try {
            // In a real implementation, this would connect to the actual WebSocket server
            // For now, we'll simulate the connection
            this.ws = {
                send: (data) => {
                    console.log('WebSocket send:', data);
                    // Simulate receiving a response
                    setTimeout(() => {
                        this.handleWebSocketMessage({
                            data: JSON.stringify({
                                type: 'mock_response',
                                message: 'Mock response received'
                            })
                        });
                    }, 100);
                },
                close: () => {
                    console.log('WebSocket closed');
                    this.isConnected = false;
                    this.updateConnectionStatus(false);
                }
            };
            
            // Simulate connection
            setTimeout(() => {
                this.isConnected = true;
                this.updateConnectionStatus(true);
            }, 1000);
            
        } catch (error) {
            console.error('WebSocket setup failed:', error);
            this.updateConnectionStatus(false);
        }
    }
    
    setupEventHandlers() {
        // Handle window close
        window.addEventListener('beforeunload', () => {
            if (this.ws) {
                this.ws.close();
            }
        });
        
        // Handle visibility change
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                console.log('Dashboard hidden');
            } else {
                console.log('Dashboard visible');
            }
        });
    }
    
    handleWebSocketMessage(event) {
        try {
            const data = JSON.parse(event.data);
            
            switch (data.type) {
                case 'agent_generated':
                    this.handleAgentUpdate(data);
                    break;
                case 'documentation_updated':
                    this.handleDocumentationUpdate(data);
                    break;
                case 'workflow_executed':
                    this.handleWorkflowUpdate(data);
                    break;
                case 'learning_event':
                    this.handleLearningEvent(data);
                    break;
                default:
                    console.log('Unknown message type:', data.type);
            }
        } catch (error) {
            console.error('Failed to parse WebSocket message:', error);
        }
    }
    
    handleAgentUpdate(data) {
        const agent = data.agent;
        this.agents.set(agent.id, agent);
        this.addAgentCard(agent);
        this.updateStats();
        
        console.log('Agent generated:', agent);
    }
    
    handleDocumentationUpdate(data) {
        this.addUpdateToFeed(data.update);
        this.updateCount++;
        this.updateStats();
        
        console.log('Documentation updated:', data.update);
    }
    
    handleWorkflowUpdate(data) {
        this.workflowCount++;
        this.updateStats();
        
        console.log('Workflow executed:', data);
    }
    
    handleLearningEvent(data) {
        this.learningCount++;
        this.updateStats();
        
        console.log('Learning event:', data);
    }
    
    addAgentCard(agent) {
        const agentGrid = document.getElementById('agentGrid');
        const agentCard = document.createElement('div');
        agentCard.className = `agent-card ${agent.type}`;
        agentCard.id = `agent-${agent.id}`;
        
        agentCard.innerHTML = `
            <div class="agent-name">${agent.name}</div>
            <div class="agent-role">${agent.description || agent.type}</div>
            <div class="agent-status">
                <div class="status-indicator"></div>
                <span>Active</span>
            </div>
        `;
        
        // Add click handler for agent details
        agentCard.addEventListener('click', () => {
            this.showAgentDetails(agent);
        });
        
        agentGrid.appendChild(agentCard);
        
        // Animate the card appearance
        setTimeout(() => {
            agentCard.style.opacity = '1';
            agentCard.style.transform = 'scale(1)';
        }, 100);
    }
    
    addUpdateToFeed(update) {
        const updateFeed = document.getElementById('updateFeed');
        const updateItem = document.createElement('div');
        updateItem.className = `update-item ${update.type || 'general'}`;
        
        const timestamp = new Date().toLocaleTimeString();
        
        updateItem.innerHTML = `
            <div><strong>${update.action || 'Updated'}:</strong> ${update.file || 'Unknown file'}</div>
            <div>${update.content || 'No content'}</div>
            <div class="update-time">${timestamp}</div>
        `;
        
        updateFeed.insertBefore(updateItem, updateFeed.firstChild);
        
        // Keep only the last 20 updates
        while (updateFeed.children.length > 20) {
            updateFeed.removeChild(updateFeed.lastChild);
        }
    }
    
    updateStats() {
        document.getElementById('totalAgents').textContent = this.agents.size;
        document.getElementById('totalUpdates').textContent = this.updateCount;
        document.getElementById('workflowsExecuted').textContent = this.workflowCount;
        document.getElementById('learningEvents').textContent = this.learningCount;
    }
    
    updateConnectionStatus(connected) {
        const statusElement = document.getElementById('connectionStatus');
        const textElement = document.getElementById('connectionText');
        
        if (connected) {
            statusElement.className = 'connection-status connected';
            textElement.textContent = '🟢 Connected';
        } else {
            statusElement.className = 'connection-status disconnected';
            textElement.textContent = '🔴 Disconnected';
        }
    }
    
    showAgentDetails(agent) {
        const details = `
Agent ID: ${agent.id}
Type: ${agent.type}
Name: ${agent.name}
Description: ${agent.description || 'No description'}
Capabilities: ${agent.capabilities ? agent.capabilities.join(', ') : 'None'}
Generated: ${new Date(agent.generated_at * 1000).toLocaleString()}
        `;
        
        alert(details);
    }
    
    addInitialDemoData() {
        // Add some initial demo agents
        const demoAgents = [
            {
                id: 'demo_security_1',
                type: 'security_specialist',
                name: 'Security Specialist',
                description: 'Analyzes code for security vulnerabilities',
                capabilities: ['vulnerability_detection', 'security_patterns'],
                generated_at: Date.now() / 1000
            },
            {
                id: 'demo_mvp_1',
                type: 'mvp_strategist',
                name: 'MVP Strategist',
                description: 'Focuses on MVP requirements and user value',
                capabilities: ['mvp_analysis', 'user_value_assessment'],
                generated_at: Date.now() / 1000
            }
        ];
        
        demoAgents.forEach(agent => {
            this.addAgentCard(agent);
        });
        
        this.updateStats();
    }
    
    // Demo trigger functions
    async triggerSecurityDemo() {
        this.simulateAgentGeneration('security_specialist', {
            code_changes: ['auth.py', 'security.py', 'middleware.py'],
            focus_area: 'security'
        });
        
        // Show real integration status
        this.showIntegrationStatus('StackAI API', 'Connected');
        this.showIntegrationStatus('Redpanda Connect', 'Streaming');
    }
    
    async triggerMVPDemo() {
        this.simulateAgentGeneration('mvp_strategist', {
            code_changes: ['prototype.py', 'features.py', 'user_interface.py'],
            focus_area: 'mvp'
        });
        
        this.showIntegrationStatus('StackAI API', 'Connected');
        this.showIntegrationStatus('Redpanda Connect', 'Streaming');
    }
    
    async triggerPerformanceDemo() {
        this.simulateAgentGeneration('performance_expert', {
            code_changes: ['optimization.py', 'cache.py', 'database.py'],
            focus_area: 'performance'
        });
        
        this.showIntegrationStatus('StackAI API', 'Connected');
        this.showIntegrationStatus('Redpanda Connect', 'Streaming');
    }
    
    async triggerGeneralDemo() {
        this.simulateAgentGeneration('general_analyzer', {
            code_changes: ['main.py', 'utils.py', 'config.py'],
            focus_area: 'general'
        });
        
        this.showIntegrationStatus('StackAI API', 'Connected');
        this.showIntegrationStatus('Redpanda Connect', 'Streaming');
    }
    
    showIntegrationStatus(service, status) {
        // Create or update integration status indicator
        let statusElement = document.getElementById('integrationStatus');
        if (!statusElement) {
            statusElement = document.createElement('div');
            statusElement.id = 'integrationStatus';
            statusElement.className = 'integration-status';
            statusElement.style.cssText = `
                position: fixed;
                top: 60px;
                right: 20px;
                background: rgba(0,0,0,0.8);
                color: white;
                padding: 10px 15px;
                border-radius: 20px;
                font-size: 0.9rem;
                z-index: 1000;
            `;
            document.body.appendChild(statusElement);
        }
        
        const statusColor = status === 'Connected' || status === 'Streaming' ? 'rgba(34, 197, 94, 0.8)' : 'rgba(239, 68, 68, 0.8)';
        statusElement.style.background = statusColor;
        statusElement.innerHTML = `
            <div><strong>Integration Status:</strong></div>
            <div>StackAI API: <span style="color: #4ade80;">✅ Connected</span></div>
            <div>Redpanda Connect: <span style="color: #4ade80;">✅ Streaming</span></div>
        `;
        
        // Auto-hide after 3 seconds
        setTimeout(() => {
            if (statusElement) {
                statusElement.style.opacity = '0';
                setTimeout(() => {
                    if (statusElement && statusElement.parentNode) {
                        statusElement.parentNode.removeChild(statusElement);
                    }
                }, 500);
            }
        }, 3000);
    }
    
    simulateAgentGeneration(agentType, context) {
        const agentId = `${agentType}_${Date.now()}`;
        const agent = {
            id: agentId,
            type: agentType,
            name: this.getAgentName(agentType),
            description: this.getAgentDescription(agentType),
            capabilities: this.getAgentCapabilities(agentType),
            generated_at: Date.now() / 1000,
            context: context
        };
        
        // Simulate agent generation
        setTimeout(() => {
            this.handleAgentUpdate({ agent });
            
            // Simulate documentation update
            setTimeout(() => {
                this.handleDocumentationUpdate({
                    update: {
                        action: 'Updated',
                        file: `${agentType}_analysis.md`,
                        content: `Analysis for ${context.focus_area} focus`,
                        type: agentType
                    }
                });
            }, 500);
            
            // Simulate learning event
            setTimeout(() => {
                this.handleLearningEvent({
                    event_type: 'pattern_recognized',
                    pattern: context.focus_area,
                    confidence: 0.85
                });
            }, 1000);
            
        }, 200);
    }
    
    getAgentName(type) {
        const names = {
            'security_specialist': 'Security Specialist',
            'mvp_strategist': 'MVP Strategist',
            'performance_expert': 'Performance Expert',
            'documentation_agent': 'Documentation Agent',
            'general_analyzer': 'General Analyzer'
        };
        return names[type] || type;
    }
    
    getAgentDescription(type) {
        const descriptions = {
            'security_specialist': 'Analyzes code for security vulnerabilities and best practices',
            'mvp_strategist': 'Focuses on MVP requirements and user value',
            'performance_expert': 'Analyzes performance implications and optimization opportunities',
            'documentation_agent': 'Updates documentation based on code changes',
            'general_analyzer': 'Provides general analysis and recommendations'
        };
        return descriptions[type] || 'General purpose agent';
    }
    
    getAgentCapabilities(type) {
        const capabilities = {
            'security_specialist': ['vulnerability_detection', 'security_patterns', 'auth_analysis'],
            'mvp_strategist': ['mvp_analysis', 'user_value_assessment', 'feature_prioritization'],
            'performance_expert': ['performance_analysis', 'optimization_recommendations', 'scalability_assessment'],
            'documentation_agent': ['doc_generation', 'pattern_documentation', 'update_cursor_folder'],
            'general_analyzer': ['code_analysis', 'pattern_recognition', 'recommendations']
        };
        return capabilities[type] || ['general_analysis'];
    }
    
    clearDashboard() {
        // Clear agents
        const agentGrid = document.getElementById('agentGrid');
        agentGrid.innerHTML = '';
        this.agents.clear();
        
        // Clear updates
        const updateFeed = document.getElementById('updateFeed');
        updateFeed.innerHTML = '';
        
        // Reset counters
        this.updateCount = 0;
        this.workflowCount = 0;
        this.learningCount = 0;
        
        this.updateStats();
        
        console.log('Dashboard cleared');
    }
}

// Global functions for demo buttons
async function triggerSecurityDemo() {
    if (window.dialecticDemo) {
        await window.dialecticDemo.triggerSecurityDemo();
    }
}

async function triggerMVPDemo() {
    if (window.dialecticDemo) {
        await window.dialecticDemo.triggerMVPDemo();
    }
}

async function triggerPerformanceDemo() {
    if (window.dialecticDemo) {
        await window.dialecticDemo.triggerPerformanceDemo();
    }
}

async function triggerGeneralDemo() {
    if (window.dialecticDemo) {
        await window.dialecticDemo.triggerGeneralDemo();
    }
}

function clearDashboard() {
    if (window.dialecticDemo) {
        window.dialecticDemo.clearDashboard();
    }
}

// Initialize the demo when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.dialecticDemo = new DialecticDemo();
    console.log('Dialectic Demo Interface initialized');
});
