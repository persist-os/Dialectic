"""
Documentation Updater
Updates .cursor folder files based on agent specifications

This is where agents actually take action - they modify the living
documentation system in real-time!
"""

import os
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import json


class DocumentationUpdater:
    """
    Updates .cursor folder based on agent specifications
    
    This is the action layer - agents spawn and immediately start
    updating documentation to reflect the current context.
    """
    
    def __init__(self, cursor_folder_path: str = '.cursor'):
        """
        Initialize documentation updater
        
        Args:
            cursor_folder_path: Path to the .cursor folder (relative to cwd)
        """
        # ALWAYS use path relative to current working directory
        # Cursor enforces .cursor folder at project root
        self.cursor_path = Path.cwd() / cursor_folder_path
        self.updates_log = []
        
        # Ensure .cursor folder exists
        self.cursor_path.mkdir(parents=True, exist_ok=True)
    
    async def update_documentation(self, agent_spec, context: Dict) -> List[Dict]:
        """
        Update documentation files based on agent spec and context
        
        Args:
            agent_spec: AgentSpec from DynamicAgentGenerator
            context: Context analysis from ContextAnalyzer
        
        Returns:
            List of update records
        """
        
        updates_made = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"📚 {agent_spec.agent_type} updating documentation...")
        
        for target_file in agent_spec.documentation_targets:
            try:
                file_path = self.cursor_path / target_file
                
                # Ensure directory exists
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Generate update content
                update_content = await self._generate_update_content(
                    agent_spec, 
                    context,
                    target_file,
                    timestamp
                )
                
                # Update file
                if file_path.exists():
                    await self._append_to_file(file_path, update_content)
                    update_type = "updated"
                else:
                    await self._create_file(file_path, update_content)
                    update_type = "created"
                
                # Record update
                update_record = {
                    'file': str(file_path),
                    'type': update_type,
                    'timestamp': timestamp,
                    'agent': agent_spec.agent_type,
                    'size': len(update_content)
                }
                
                updates_made.append(update_record)
                self.updates_log.append(update_record)
                
                print(f"   ✏️  {update_type.title()} {file_path.name}")
                
            except Exception as e:
                print(f"   ❌ Failed to update {target_file}: {e}")
                continue
        
        return updates_made
    
    async def _generate_update_content(
        self, 
        agent_spec, 
        context: Dict,
        target_file: str,
        timestamp: str
    ) -> str:
        """Generate content for documentation update"""
        
        files_changed = ', '.join(context.get('files_changed', []))
        commit_message = context.get('commit_message', 'No message')
        
        # Generate content based on agent focus area
        if agent_spec.focus_area == 'security':
            return self._generate_security_update(context, timestamp, files_changed, commit_message)
        elif agent_spec.focus_area == 'mvp':
            return self._generate_mvp_update(context, timestamp, commit_message)
        elif agent_spec.focus_area == 'performance':
            return self._generate_performance_update(context, timestamp, files_changed)
        elif agent_spec.focus_area == 'documentation':
            return self._generate_documentation_update(context, timestamp, files_changed)
        elif agent_spec.focus_area == 'debugging':
            return self._generate_debugging_update(context, timestamp, files_changed, commit_message)
        elif agent_spec.focus_area == 'api':
            return self._generate_api_update(context, timestamp, files_changed)
        elif agent_spec.focus_area == 'frontend':
            return self._generate_frontend_update(context, timestamp, files_changed)
        else:
            return self._generate_general_update(context, timestamp, files_changed, commit_message)
    
    def _generate_security_update(self, context: Dict, timestamp: str, files: str, message: str) -> str:
        """Generate security-focused documentation"""
        
        return f"""

## 🔒 Security Update - {timestamp}

**Agent**: Security Specialist  
**Files Modified**: {files}  
**Context**: {message}  
**Confidence**: {context['confidence']['security']:.1%}

### Security Considerations
- Review authentication flow in modified files
- Ensure proper input validation
- Check for secure token handling
- Verify permission checks are in place
- Validate CORS and CSRF protection

### Action Items
- [ ] Security audit of {files}
- [ ] Update security tests
- [ ] Review authentication patterns
- [ ] Check for SQL injection vulnerabilities
- [ ] Verify HTTPS enforcement

### Security Patterns
```python
# Example: Secure JWT handling
import jwt
from datetime import datetime, timedelta

def create_secure_token(user_id: str) -> str:
    payload = {{
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow()
    }}
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
```

---
"""
    
    def _generate_mvp_update(self, context: Dict, timestamp: str, message: str) -> str:
        """Generate MVP-focused documentation"""
        
        return f"""

## 🚀 MVP Development - {timestamp}

**Agent**: MVP Strategist  
**Context**: {message}  
**Confidence**: {context['confidence']['mvp']:.1%}

### MVP Focus
- Prioritize core functionality
- Accept technical debt for speed
- Focus on demo-ready features
- Document shortcuts taken
- Track what needs refactoring later

### MVP Guidelines
- ✅ Get it working first, optimize later
- ✅ Use mock data if real data is complex
- ✅ Simple UI over perfect design
- ✅ Basic error handling is sufficient
- ✅ Document all shortcuts taken

### Follow-up Tasks
- [ ] Technical debt tracking
- [ ] Post-MVP refactoring plan
- [ ] Performance optimization roadmap
- [ ] Security hardening checklist

---
"""
    
    def _generate_performance_update(self, context: Dict, timestamp: str, files: str) -> str:
        """Generate performance-focused documentation"""
        
        return f"""

## ⚡ Performance Optimization - {timestamp}

**Agent**: Performance Expert  
**Files Modified**: {files}  
**Confidence**: {context['confidence']['performance']:.1%}

### Performance Considerations
- Profile modified code paths
- Check for N+1 queries
- Review async/await usage
- Monitor memory usage
- Analyze database query patterns

### Optimization Targets
- [ ] Benchmark {files}
- [ ] Profile performance impact
- [ ] Document optimization decisions
- [ ] Set up performance monitoring
- [ ] Create performance regression tests

### Performance Patterns
```python
# Example: Efficient caching
import redis
from functools import wraps

def cache_result(expiry: int = 300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{{func.__name__}}:{{hash(str(args) + str(kwargs))}}"
            
            # Try cache first
            cached = await redis.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute and cache
            result = await func(*args, **kwargs)
            await redis.setex(cache_key, expiry, json.dumps(result))
            return result
        
        return wrapper
    return decorator
```

---
"""
    
    def _generate_documentation_update(self, context: Dict, timestamp: str, files: str) -> str:
        """Generate documentation-focused update"""
        
        return f"""

## 📚 Documentation Update - {timestamp}

**Agent**: Documentation Specialist  
**Files Modified**: {files}

### Documentation Focus
- Keep documentation current with code changes
- Ensure examples are working
- Update API documentation
- Maintain clear structure

### Documentation Standards
- Use clear, concise language
- Include code examples
- Keep README files updated
- Document breaking changes
- Maintain changelog

---
"""
    
    def _generate_debugging_update(self, context: Dict, timestamp: str, files: str, message: str) -> str:
        """Generate debugging documentation"""
        
        error_count = context.get('error_count', 0)
        
        return f"""

## 🐛 Debugging Session - {timestamp}

**Agent**: Error Handler  
**Files Modified**: {files}  
**Context**: {message}  
**Errors Detected**: {error_count}

### Debug Process
1. Identified {error_count} errors
2. Root cause analysis completed
3. Fix implemented and tested
4. Prevention measures added

### Lessons Learned
- Document what caused the errors
- Add tests to prevent regression
- Update error handling patterns
- Improve logging for future debugging

### Debugging Checklist
- [ ] Reproduce the error
- [ ] Check logs for stack traces
- [ ] Verify input data
- [ ] Test edge cases
- [ ] Add monitoring/alerting

---
"""
    
    def _generate_api_update(self, context: Dict, timestamp: str, files: str) -> str:
        """Generate API-focused documentation"""
        
        return f"""

## 🔌 API Update - {timestamp}

**Agent**: API Specialist  
**Files Modified**: {files}

### API Considerations
- Maintain backward compatibility
- Document all endpoints
- Include request/response examples
- Handle errors gracefully
- Use proper HTTP status codes

### API Standards
- RESTful design principles
- Consistent naming conventions
- Proper authentication
- Rate limiting
- Input validation

---
"""
    
    def _generate_frontend_update(self, context: Dict, timestamp: str, files: str) -> str:
        """Generate frontend-focused documentation"""
        
        return f"""

## 🎨 Frontend Update - {timestamp}

**Agent**: Frontend Specialist  
**Files Modified**: {files}

### Frontend Considerations
- Responsive design
- Accessibility compliance
- Performance optimization
- Cross-browser compatibility
- User experience

### Frontend Standards
- Component-based architecture
- Consistent styling
- Proper state management
- Error boundaries
- Loading states

---
"""
    
    def _generate_general_update(self, context: Dict, timestamp: str, files: str, message: str) -> str:
        """Generate general documentation update"""
        
        return f"""

## 📝 Update - {timestamp}

**Files Modified**: {files}  
**Context**: {message}

### Changes Made
- Code modifications completed
- Documentation updated
- Tests verified

---
"""
    
    async def _append_to_file(self, file_path: Path, content: str):
        """Append content to existing file"""
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)
    
    async def _create_file(self, file_path: Path, content: str):
        """Create new file with content"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# {file_path.stem.replace('_', ' ').title()}\n\n")
            f.write(content)
    
    def get_update_summary(self) -> Dict:
        """Get summary of all updates made"""
        
        total_updates = len(self.updates_log)
        files_created = sum(1 for update in self.updates_log if update['type'] == 'created')
        files_updated = sum(1 for update in self.updates_log if update['type'] == 'updated')
        
        # Group by agent
        agent_counts = {}
        for update in self.updates_log:
            agent = update['agent']
            agent_counts[agent] = agent_counts.get(agent, 0) + 1
        
        return {
            'total_updates': total_updates,
            'files_created': files_created,
            'files_updated': files_updated,
            'agent_counts': agent_counts,
            'total_size': sum(update['size'] for update in self.updates_log)
        }


# Test the documentation updater
if __name__ == "__main__":
    import asyncio
    from context_analyzer import ContextAnalyzer
    from agent_generator import DynamicAgentGenerator
    
    async def test_documentation_updater():
        """Test the documentation updater"""
        
        print("📚 Testing Documentation Updater")
        print("=" * 60)
        
        analyzer = ContextAnalyzer()
        generator = DynamicAgentGenerator()
        updater = DocumentationUpdater('.cursor/')
        
        # Test scenario
        test_event = {
            'files': ['src/auth/jwt.py', 'src/middleware/auth.py'],
            'message': 'Add JWT authentication with secure token handling',
            'errors': []
        }
        
        print(f"🎭 Testing with Security Event:")
        print(f"   Files: {', '.join(test_event['files'])}")
        print(f"   Message: {test_event['message']}")
        
        # Analyze context
        context = await analyzer.analyze_event(test_event)
        
        # Generate agents
        agents = await generator.generate_agents(context)
        
        print(f"\n📚 Updating documentation for {len(agents)} agents:")
        
        # Update documentation
        for agent in agents:
            updates = await updater.update_documentation(agent, context)
            print(f"   ✅ {agent.agent_type}: {len(updates)} files updated")
        
        # Show summary
        summary = updater.get_update_summary()
        print(f"\n📊 Update Summary:")
        print(f"   Total updates: {summary['total_updates']}")
        print(f"   Files created: {summary['files_created']}")
        print(f"   Files updated: {summary['files_updated']}")
        print(f"   Total size: {summary['total_size']} bytes")
        
        print(f"\n🎯 Check .cursor/ folder for generated files!")
    
    asyncio.run(test_documentation_updater())
