from flask import Flask, request, jsonify, make_response
import logging
from flask_cors import CORS
import os
import pinecone
import re
from dotenv import load_dotenv
from http.server import BaseHTTPRequestHandler
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Setup logger
logger = logging.getLogger("prompt_optimizer")
logger.setLevel(logging.INFO)
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
if not logger.hasHandlers():
    logger.addHandler(log_handler)

# Pinecone configuration
pc = None
index_name = "prompt-technique2"

# Fallback strategies if Pinecone is unavailable
docs = [
    "Few-shot prompting: Provide a few input-output examples before the actual query to guide the model.",
    "Chain-of-thought prompting: Ask the model to reason step by step before answering.",
    "Zero-shot prompting: Directly ask the model without giving examples.",
    "Role prompting: Assign a role to the model, e.g., 'You are an expert teacher...'.",
    "Self-consistency prompting: Sample multiple reasoning paths and pick the most consistent answer.",
    "Intent Understanding: Analyze user's core desire, emotional goal, and intended use case to create contextually perfect prompts.",
    "Subject Mastery: Begin with crystal-clear subject definition, then layer with specific attributes, characteristics, and unique features.",
    "Composition Excellence: Specify camera angles, framing, perspective, depth of field, and visual hierarchy for professional composition.",
    "Lighting Mastery: Define light source, intensity, color temperature, shadows, highlights, and atmospheric lighting effects.",
    "Style Definition: Establish artistic style, medium, technique, and aesthetic direction with specific reference points and visual language.",
    "Emotional Resonance: Capture mood, atmosphere, emotion, and psychological impact through descriptive language and visual metaphors.",
    "Technical Precision: Include resolution, quality, detail level, texture, material properties, and technical specifications.",
    "Environmental Context: Describe setting, background, atmosphere, weather, time of day, and spatial relationships.",
    "Color Harmony: Define color palette, contrast, saturation, color theory, and visual harmony principles.",
    "Negative Space Control: Specify what to avoid, exclude, or minimize for clean, focused image generation.",
    "Reference Integration: Incorporate specific artistic references, photography styles, cinematic techniques, and visual inspirations.",
    "Iterative Refinement: Structure prompts for easy modification, allowing users to adjust specific elements while maintaining core vision.",
      # 🚀 Vibe coding fallback strategies
    "General feature prompting: Start with vibe PMing by restating the feature as a product spec, keep the tech stack simple, offer multiple solution options with pros/cons, recommend the simplest, break down the implementation into small iterative steps, suggest a test plan, and provide commit/diff outputs only when requested.",
    "Refactor code prompting: Begin with a short spec of the intended improvement, preserve the existing API and tests, restrict scope to the specified files, propose 2–3 refactor strategies, outline an iterative plan, add or reuse tests, and deliver results as commit/diff format with a clear revert option.",
    "Debug/Fix prompting: Restate the problem and symptoms, analyze root cause, propose minimal fixes, suggest adding failing and regression tests, outline stepwise plan, limit changes to specific files, return results as commit/diff only if requested, and finish with a plain-language explanation."

]

# Context-specific strategy mappings
context_strategies = {
    "business": "Business-focused prompting: Use professional language, include business metrics, ROI considerations, and industry-specific terminology.",
    "rephrase": "Text rephrasing and optimization: Focus on grammar correction, spelling fixes, clarity improvement, and professional language refinement.",
    "technical": "Technical prompting: Request detailed explanations, step-by-step processes, and include technical specifications.",
    "academic": "Academic prompting: Ask for citations, research-based responses, and scholarly analysis.",
    "marketing": "Marketing prompting: Focus on audience engagement, persuasive language, and conversion optimization.",
    "image_generation": "Image generation prompting: Use vivid, descriptive language, specify visual elements, composition, style, mood, lighting, and artistic direction for AI image generation tools.",
    "video_generation": "Video generation prompting: Specify visual elements, motion, timing, scene transitions, camera movements, and narrative flow for AI video generation tools.",
    "general": "General prompting: Use clear, direct language with specific instructions and expected outcomes.",
    "cursor_code_optimizer": "Cursor Code Optimizer: Transform coding ideas into structured development prompts optimized for Cursor AI with clear product specs, simple tech stacks, multiple solution options with pros/cons, step-by-step implementation plans, and comprehensive testing strategies.",
      # 🚀 Vibe coding strategies
    "feature": "General feature prompting: Start with vibe PMing by restating the feature as a product spec, offer multiple solution options with pros/cons, recommend the simplest, break down the implementation into small iterative steps, suggest a test plan, and provide commit/diff outputs only when requested.",
    "refactor": "Refactor code prompting: Begin with a short spec of the intended improvement, preserve the existing API and tests, restrict scope to the specified files, propose 2–3 refactor strategies, outline an iterative plan, add or reuse tests, and deliver results as commit/diff format with a clear revert option.",
    "debug": "Debug/Fix prompting: Restate the problem and symptoms, analyze root cause, propose minimal fixes, suggest adding failing and regression tests, outline stepwise plan, limit changes to specific files, return results as commit/diff only if requested, and finish with a plain-language explanation."

}

# Context-specific instructions for different optimization types
context_instructions = {
    "rephrase": "Focus on grammar correction, spelling fixes, clarity improvement, professional language refinement, sentence structure optimization, and ensuring the text is clear, concise, and error-free.",
    "technical": "Provide detailed technical explanations, include step-by-step processes, use precise terminology, technical specifications, and implementation guidance.",
    "image_generation": "Create world-class image generation prompts using structured prompting: Subject + Details + Style + Technical Specifications + Negative Prompts. Focus on clarity, control, creativity, and quality. Generate prompts that produce stunning, professional-grade images with maximum detail, artistic direction, and technical precision.",
    "video_generation": "Create world-class video generation prompts using structured prompting: Subject + Motion + Style + Technical Specifications + Negative Prompts. Focus on cinematic quality, smooth transitions, dynamic camera movements, and engaging visual storytelling. Generate prompts that produce professional-grade videos with maximum visual impact and narrative flow.",
    "general": "Use clear, direct language with specific instructions and expected outcomes, include step-by-step guidance and comprehensive information.",
    "cursor_code_optimizer": "Enhanced Cursor Code Optimizer: Transform coding ideas into comprehensive, structured development prompts optimized for Cursor AI. Provides deep user intent analysis, detailed product specifications, intelligent technology recommendations, multiple solution approaches with pros/cons, granular step-by-step implementation roadmaps, comprehensive testing strategies, Cursor AI interaction optimization, development best practices, risk mitigation, and post-implementation considerations. Designed to create actionable prompts that enable successful AI-assisted development regardless of user experience level."

}

# Lazy initialize components
embeddings = None
vectorstore = None
retriever = None

def get_embeddings():
    """Initialize and return OpenAI embeddings instance"""
    global embeddings
    if embeddings is not None:
        return embeddings
    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        return embeddings
    except Exception as e:
        logger.error(f"Failed to initialize embeddings: {e}")
        return None

def get_llm():
    """Initialize and return ChatOpenAI instance"""
    try:
        return ChatOpenAI(model="gpt-4o", temperature=0)
    except Exception as e:
        logger.error(f"Failed to initialize ChatOpenAI: {e}")
        return None

def setup_pinecone_and_vectorstore():
    """Initialize Pinecone client, ensure index exists, and create vectorstore + retriever"""
    global pc, vectorstore, retriever
    
    if retriever:
        return

    # Initialize Pinecone client
    if not pc:
        try:
            pinecone_api_key = os.getenv('PINECONE_API_KEY')
            pc = pinecone.Pinecone(api_key=pinecone_api_key)
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone client: {e}")
            return

    # Ensure index exists
    try:
        index_list = pc.list_indexes()
        if index_name not in [i.get("name") if isinstance(i, dict) else i for i in index_list]:
            pc.create_index(
                name=index_name,
                dimension=1536,
                metric="cosine",
                spec=pinecone.ServerlessSpec(cloud="aws", region="us-east-1")
            )
    except Exception as e:
        logger.error(f"Pinecone index setup failed: {e}")
        return

    # Initialize vectorstore and retriever
    try:
        index = pc.Index(index_name)
        embeddings_instance = get_embeddings()
        if embeddings_instance:
            vectorstore = PineconeVectorStore(index=index, embedding=embeddings_instance)
            retriever = vectorstore.as_retriever()
    except Exception as e:
        logger.error(f"Vectorstore initialization failed: {e}")

def clean_prompt(prompt: str) -> str:
    """Remove filler words and clean the prompt while preserving important context"""
    useless_words = ["actually", "basically", "just", "like", "I mean", "you know", "um", "uh", "well"]
    
    cleaned = prompt
    for word in useless_words:
        pattern = r'\b' + re.escape(word) + r'\b'
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # Clean up whitespace and punctuation
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = re.sub(r'\s*,\s*', ', ', cleaned)
    cleaned = re.sub(r'\s*\.\s*', '. ', cleaned)
    cleaned = re.sub(r'^\s*[,.\s]+', '', cleaned)
    cleaned = re.sub(r'[,.\s]+\s*$', '', cleaned)
    
    return cleaned.strip()

def analyze_user_intent(cleaned_prompt: str) -> dict:
    """Analyze user intent for better understanding of coding requirements"""
    prompt_lower = cleaned_prompt.lower()
    
    # Intent categories
    intent_analysis = {
        "primary_goal": "unknown",
        "complexity_level": "medium",
        "domain": "general",
        "urgency": "normal",
        "user_experience_level": "intermediate",
        "specific_technologies": [],
        "constraints": []
    }
    
    # Analyze primary goal
    if any(word in prompt_lower for word in ["bug", "error", "fix", "broken", "not working", "debug", "issue", "problem"]):
        intent_analysis["primary_goal"] = "debug_fix"
    elif any(word in prompt_lower for word in ["refactor", "improve", "optimize", "clean up", "restructure", "reorganize", "performance"]):
        intent_analysis["primary_goal"] = "refactor_optimize"
    elif any(word in prompt_lower for word in ["new", "create", "build", "develop", "implement", "add", "feature"]):
        intent_analysis["primary_goal"] = "new_feature"
    elif any(word in prompt_lower for word in ["test", "testing", "unit test", "integration test", "automation"]):
        intent_analysis["primary_goal"] = "testing"
    elif any(word in prompt_lower for word in ["deploy", "deployment", "ci/cd", "pipeline", "production"]):
        intent_analysis["primary_goal"] = "deployment"
    elif any(word in prompt_lower for word in ["api", "endpoint", "rest", "graphql", "backend"]):
        intent_analysis["primary_goal"] = "api_development"
    elif any(word in prompt_lower for word in ["ui", "frontend", "react", "vue", "angular", "interface"]):
        intent_analysis["primary_goal"] = "frontend_development"
    elif any(word in prompt_lower for word in ["database", "db", "sql", "nosql", "migration", "schema"]):
        intent_analysis["primary_goal"] = "database_work"
    
    # Analyze complexity level
    if any(word in prompt_lower for word in ["simple", "basic", "quick", "easy", "minimal"]):
        intent_analysis["complexity_level"] = "low"
    elif any(word in prompt_lower for word in ["complex", "advanced", "comprehensive", "enterprise", "scalable", "production-ready"]):
        intent_analysis["complexity_level"] = "high"
    
    # Analyze domain
    if any(word in prompt_lower for word in ["ecommerce", "shop", "cart", "payment", "order"]):
        intent_analysis["domain"] = "ecommerce"
    elif any(word in prompt_lower for word in ["auth", "login", "user", "account", "profile"]):
        intent_analysis["domain"] = "authentication"
    elif any(word in prompt_lower for word in ["data", "analytics", "dashboard", "chart", "report"]):
        intent_analysis["domain"] = "data_analytics"
    elif any(word in prompt_lower for word in ["chat", "message", "real-time", "websocket", "notification"]):
        intent_analysis["domain"] = "communication"
    elif any(word in prompt_lower for word in ["ml", "ai", "machine learning", "model", "prediction"]):
        intent_analysis["domain"] = "ai_ml"
    
    # Analyze urgency
    if any(word in prompt_lower for word in ["urgent", "asap", "quickly", "fast", "immediately"]):
        intent_analysis["urgency"] = "high"
    elif any(word in prompt_lower for word in ["when possible", "eventually", "future", "later"]):
        intent_analysis["urgency"] = "low"
    
    # Analyze user experience level
    if any(word in prompt_lower for word in ["beginner", "new to", "learning", "tutorial", "help me understand"]):
        intent_analysis["user_experience_level"] = "beginner"
    elif any(word in prompt_lower for word in ["expert", "advanced", "professional", "enterprise", "production"]):
        intent_analysis["user_experience_level"] = "expert"
    
    # Extract specific technologies
    tech_keywords = ["react", "vue", "angular", "node", "python", "java", "typescript", "javascript", 
                    "django", "flask", "express", "mongodb", "postgresql", "mysql", "redis", 
                    "docker", "kubernetes", "aws", "azure", "gcp", "firebase"]
    for tech in tech_keywords:
        if tech in prompt_lower:
            intent_analysis["specific_technologies"].append(tech)
    
    # Extract constraints
    if "budget" in prompt_lower or "cost" in prompt_lower:
        intent_analysis["constraints"].append("budget_conscious")
    if "time" in prompt_lower and ("limit" in prompt_lower or "deadline" in prompt_lower):
        intent_analysis["constraints"].append("time_constrained")
    if "existing" in prompt_lower and ("code" in prompt_lower or "system" in prompt_lower):
        intent_analysis["constraints"].append("legacy_integration")
    
    return intent_analysis

def get_strategy_for_context(context: str, cleaned_prompt: str):
    """Get the best strategy based on context and prompt content"""
    if context == "cursor_code_optimizer":
        # Enhanced intelligent strategy selection with intent analysis
        intent = analyze_user_intent(cleaned_prompt)
        
        if intent["primary_goal"] == "debug_fix":
            return context_strategies["debug"]
        elif intent["primary_goal"] == "refactor_optimize":
            return context_strategies["refactor"]
        else:
            return context_strategies["feature"]
    
    context_strategy = context_strategies.get(context, context_strategies["general"])
    
    if retriever:
        try:
            results = retriever.get_relevant_documents(cleaned_prompt)
            if results:
                return results[0].page_content
        except Exception as e:
            logger.error(f"Strategy retrieval failed: {e}")
    
    return context_strategy

def create_template(context: str, strategy: str, cleaned_prompt: str) -> str:
    """Create the appropriate template based on context"""
    context_instruction = context_instructions.get(context, context_instructions["general"])
    
    if context in ["image_generation", "video_generation"]:
        return f"""You are a World-Class {'Image' if context == 'image_generation' else 'Video'} Generation Prompt Engineer.

Your mission is to transform the user's basic idea into a masterpiece-level prompt.

OPTIMIZATION STRATEGY: {strategy}
CONTEXT INSTRUCTIONS: {context_instruction}

PROMPT STRUCTURE REQUIREMENTS:
- Start with a clear, powerful subject description
- Add specific visual attributes and characteristics
- Include professional composition details
- Specify lighting with professional terminology
- Define artistic style and medium with specific references
- Add emotional and atmospheric elements
- Include technical quality specifications
- Add environmental context and background details
- Specify color palette and visual harmony
- Include negative prompts to avoid common issues

USER'S ORIGINAL REQUEST: {cleaned_prompt}

Return ONLY the optimized, professional-grade {'image' if context == 'image_generation' else 'video'} generation prompt."""

    elif context == "rephrase":
        return f"""You are a Text Optimization AI specializing in grammar correction and text refinement.

Your task:
1. Apply the given prompting strategy: {strategy}
2. {context_instruction}
3. Correct all spelling mistakes and grammatical errors
4. Improve sentence structure and flow
5. Make the text more professional and clear

Original User Text: {cleaned_prompt}

Return ONLY the corrected and optimized text with proper grammar, spelling, and clarity."""

    elif context == "cursor_code_optimizer":
        # Analyze user intent for enhanced optimization
        intent = analyze_user_intent(cleaned_prompt)
        
        return f"""You are a Senior Software Developer and Prompt Engineering Expert specializing in Cursor AI optimization.

Your mission is to transform the user's coding idea into a comprehensive, structured development prompt optimized specifically for Cursor AI that follows best practices for AI-assisted development.

STRATEGY APPLIED: {strategy}

USER INTENT ANALYSIS:
- Primary Goal: {intent['primary_goal']}
- Complexity Level: {intent['complexity_level']}
- Domain: {intent['domain']}
- User Experience Level: {intent['user_experience_level']}
- Technologies Mentioned: {', '.join(intent['specific_technologies']) if intent['specific_technologies'] else 'None specified'}
- Constraints: {', '.join(intent['constraints']) if intent['constraints'] else 'None identified'}

ENHANCED CURSOR CODE OPTIMIZATION FRAMEWORK:

## 1. INTENT UNDERSTANDING & REQUIREMENTS ANALYSIS
- Analyze the user's core desire and emotional goal behind the request
- Identify explicit and implicit requirements
- Clarify the intended use case and target audience
- Define success criteria and acceptance criteria

## 2. DETAILED PRODUCT SPECIFICATION
- Restate the feature as a clear, comprehensive product spec
- Create user stories with acceptance criteria
- Define functional and non-functional requirements
- Specify user experience expectations
- Identify integration points and dependencies

## 3. INTELLIGENT TECHNOLOGY STACK RECOMMENDATION
- Recommend technologies based on: complexity level, user experience, project constraints
- Justify each technology choice with specific benefits for Cursor AI development
- Consider learning curve, community support, and AI assistance quality
- Provide alternative options for different scenarios

## 4. COMPREHENSIVE SOLUTION ANALYSIS
- Present 3 distinct implementation approaches:
  a) **Quick & Simple**: Minimal viable solution for rapid prototyping
  b) **Balanced & Scalable**: Production-ready with good maintainability
  c) **Enterprise & Advanced**: Full-featured with maximum flexibility
- Include detailed pros/cons analysis for each approach
- Consider development time, maintenance cost, scalability, and Cursor AI compatibility

## 5. RECOMMENDED APPROACH WITH JUSTIFICATION
- Select the optimal approach based on intent analysis
- Provide detailed justification considering user experience level and constraints
- Explain why this approach works best with Cursor AI assistance
- Include fallback options if the primary approach faces issues

## 6. DETAILED IMPLEMENTATION ROADMAP
- Break down into 8-12 granular, iterative steps
- Each step should be completable in 1-2 hours with Cursor AI
- Include specific Cursor AI prompts for each step
- Define clear completion criteria and validation points
- Specify file structure and code organization
- Include error handling and edge case considerations

## 7. COMPREHENSIVE TESTING STRATEGY
- Unit testing approach with specific test cases
- Integration testing scenarios
- User acceptance testing criteria
- Performance testing considerations (if applicable)
- Security testing requirements (if applicable)
- Cursor AI-assisted test generation strategies

## 8. CURSOR AI INTERACTION OPTIMIZATION
- Specific prompting strategies for each development phase
- Code generation best practices for Cursor AI
- Debugging and troubleshooting approaches with AI assistance
- Code review and optimization techniques using Cursor AI
- Documentation generation strategies

## 9. DEVELOPMENT BEST PRACTICES & GUIDELINES
- Code quality standards and conventions
- Version control workflow optimized for AI-assisted development
- Error handling patterns and logging strategies
- Performance optimization guidelines
- Security best practices
- Accessibility considerations (if applicable)

## 10. RISK MITIGATION & CONTINGENCY PLANNING
- Identify potential technical risks and blockers
- Provide specific mitigation strategies for each risk
- Include troubleshooting guides for common issues
- Define rollback procedures if needed
- Suggest monitoring and alerting strategies

## 11. POST-IMPLEMENTATION CONSIDERATIONS
- Deployment strategy and environment setup
- Monitoring and maintenance procedures
- Future enhancement opportunities
- Documentation and knowledge transfer
- Performance metrics and success measurement

ORIGINAL CODE REQUEST: {cleaned_prompt}

Create a comprehensive, actionable development prompt optimized for Cursor AI that transforms this request into a structured, step-by-step implementation guide. The output should be so detailed and well-structured that any developer can follow it successfully with Cursor AI assistance, regardless of their experience level. Focus on clarity, practicality, maintainability, and optimal Cursor AI interaction patterns."""

    else:
        return f"""You are a Prompt Optimizer AI specializing in {context} content.

Your task:
1. Apply the given prompting strategy: {strategy}
2. {context_instruction}
3. Remove filler words and unnecessary phrases
4. Ensure the final prompt maximizes reasoning and output quality
5. Correct any spelling and grammatical mistakes

Original User Prompt: {cleaned_prompt}

Return ONLY the optimized and reformulated prompt."""

def apply_strategy(user_prompt: str, context: str = "general"):
    """Apply optimization strategy based on context and prompt"""
    cleaned_prompt = clean_prompt(user_prompt)
    strategy = get_strategy_for_context(context, cleaned_prompt)
    
    # For cursor_code_optimizer, include intent analysis in response
    intent_analysis = None
    if context == "cursor_code_optimizer":
        intent_analysis = analyze_user_intent(cleaned_prompt)
    
    template = create_template(context, strategy, cleaned_prompt)
    
    # Try to call LLM if available
    llm = get_llm()
    if llm is not None:
        try:
            response = llm.predict(template)
            if response:
                if context == "rephrase":
                    # Clean response for rephrase context
                    prefixes_to_remove = [
                        "Corrected and optimized text:", "Corrected text:", "Optimized text:",
                        "Here's the corrected text:", "The corrected version is:"
                    ]
                    cleaned_response = response
                    for prefix in prefixes_to_remove:
                        if cleaned_response.startswith(prefix):
                            cleaned_response = cleaned_response[len(prefix):].strip()
                            break
                    cleaned_response = cleaned_response.strip()
                    if cleaned_response.startswith("."):
                        cleaned_response = cleaned_response[1:].strip()
                    return {"original": user_prompt, "strategy": strategy, "optimized": cleaned_response}
                
                # Include intent analysis for cursor_code_optimizer
                result = {"original": user_prompt, "strategy": strategy, "optimized": response}
                if intent_analysis:
                    result["intent_analysis"] = intent_analysis
                return result
        except Exception as e:
            logger.error(f"LLM call failed: {e}")

    # Fallback optimization if LLM not available or failed
    if context == "image_generation":
        fallback_prompt = f"Create a detailed image of {cleaned_prompt} with vivid colors, clear composition, artistic style, and professional lighting. Include specific visual elements and mood."
    elif context == "video_generation":
        fallback_prompt = f"Generate a video of {cleaned_prompt} with smooth motion, clear scene transitions, dynamic camera movements, and engaging visual storytelling elements."
    elif context == "cursor_code_optimizer":
        # Analyze intent for enhanced fallback
        intent = analyze_user_intent(cleaned_prompt)
        
        fallback_prompt = f"""# Cursor AI-Optimized Development Request

## Original Request
{cleaned_prompt}

## Intent Analysis
- **Primary Goal**: {intent['primary_goal']}
- **Complexity**: {intent['complexity_level']}
- **Domain**: {intent['domain']}
- **Technologies**: {', '.join(intent['specific_technologies']) if intent['specific_technologies'] else 'To be determined'}

## Structured Implementation Plan for Cursor AI

### Phase 1: Planning & Setup (30 minutes)
1. **Environment Setup**: Configure development environment with Cursor AI integration
2. **Project Structure**: Create organized file/folder structure optimized for AI assistance
3. **Requirements Analysis**: Define clear functional and technical requirements
4. **Technology Selection**: Choose appropriate tech stack based on complexity and domain

### Phase 2: Core Development (2-4 hours)
5. **Architecture Design**: Plan system architecture with clear separation of concerns
6. **Core Implementation**: Build main functionality using Cursor AI code generation
7. **Error Handling**: Implement robust error handling and validation
8. **Integration**: Connect components and ensure smooth data flow

### Phase 3: Quality Assurance (1-2 hours)
9. **Testing Strategy**: Create comprehensive test suite with Cursor AI assistance
10. **Code Review**: Use AI for code optimization and best practice compliance
11. **Documentation**: Generate clear documentation with AI enhancement
12. **Performance Check**: Validate performance and optimize if needed

### Phase 4: Deployment Preparation (30 minutes)
13. **Deployment Setup**: Configure deployment pipeline and environment
14. **Monitoring**: Set up basic monitoring and logging
15. **Final Validation**: Perform end-to-end testing and validation

## Cursor AI Optimization Guidelines
- **Use Specific Prompts**: Be explicit about requirements and expected outputs
- **Iterative Development**: Build in small, testable increments
- **Context Awareness**: Provide sufficient context for AI to understand the broader system
- **Code Quality**: Leverage AI for code review and optimization suggestions
- **Documentation**: Use AI to generate comprehensive documentation

## Success Criteria
- Code is clean, maintainable, and follows best practices
- All functionality works as expected with proper error handling
- Comprehensive tests cover main use cases
- Documentation is clear and complete
- System is ready for deployment with proper monitoring

**Next Steps**: Start with Phase 1 and use Cursor AI to assist with each step, providing clear context and specific requirements for optimal AI assistance."""
    else:
        fallback_prompt = f"Please provide a detailed, {context}-focused response about: {cleaned_prompt}"

    result = {"original": user_prompt, "strategy": strategy, "optimized": fallback_prompt}
    if context == "cursor_code_optimizer" and intent_analysis:
        result["intent_analysis"] = intent_analysis
    return result

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Prompt Optimizer API is running"})

@app.route('/api/optimize', methods=['POST'])
def optimize_prompt():
    """Main endpoint for prompt optimization"""
    try:
        setup_pinecone_and_vectorstore()
        
        data = request.get_json()
        user_prompt = data.get('prompt', '')
        context = data.get('context', 'general')
        
        if not user_prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        if context not in context_strategies:
            context = "general"
        
        result = apply_strategy(user_prompt, context)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error optimizing prompt: {e}")
        return jsonify({"error": "Failed to optimize prompt"}), 500

@app.route('/api/strategies', methods=['GET'])
def get_strategies():
    """Get available strategies and contexts"""
    return jsonify({
        "contexts": list(context_strategies.keys()),
        "strategies": docs
    })

class handler(BaseHTTPRequestHandler):
    """Vercel serverless function handler"""
    
    def do_GET(self):
        """Handle GET requests"""
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')

    def do_POST(self):
        """Handle POST requests by delegating to Flask app"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length else b''
        headers = {k: v for k, v in self.headers.items()}

        try:
            with app.test_request_context(path=self.path, method='POST', headers=headers, data=body):
                result = optimize_prompt()
                flask_resp = make_response(result)

            self.send_response(flask_resp.status_code)
            for k, v in flask_resp.headers.items():
                if k.lower() not in ("transfer-encoding", "connection", "keep-alive", "proxy-authenticate", "proxy-authorization", "te", "trailers", "upgrade"):
                    self.send_header(k, v)
            self.end_headers()

            data = flask_resp.get_data()
            if data:
                self.wfile.write(data)
        except Exception as e:
            try:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
            except Exception:
                pass

if __name__ == "__main__":
    app.run()
