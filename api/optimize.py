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
    "feature": "General feature prompting: Start with vibe PMing by restating the feature as a product spec, keep the tech stack simple, offer multiple solution options with pros/cons, recommend the simplest, break down the implementation into small iterative steps, suggest a test plan, and provide commit/diff outputs only when requested.",
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
    "cursor_code_optimizer" : "Cursor Code Optimizer: Transform coding ideas into structured development prompts optimized for Cursor AI with clear product specs, simple tech stacks, multiple solution options with pros/cons, step-by-step implementation plans, and comprehensive testing strategies."

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

def get_strategy_for_context(context: str, cleaned_prompt: str):
    """Get the best strategy based on context and prompt content"""
    if context == "cursor_code_optimizer":
        # Intelligent strategy selection for cursor code optimization based on prompt content
        prompt_lower = cleaned_prompt.lower()
        
        if any(word in prompt_lower for word in ["bug", "error", "fix", "broken", "not working", "debug", "issue"]):
            return context_strategies["debug"]
        elif any(word in prompt_lower for word in ["refactor", "improve", "optimize", "clean up", "restructure", "reorganize"]):
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
        return f"""You are a Senior Software Developer and Prompt Engineering Expert specializing in Cursor AI optimization.

Your task is to transform the user's coding idea into a comprehensive, structured development prompt optimized specifically for Cursor AI that follows best practices for AI-assisted development.

STRATEGY APPLIED: {strategy}

CURSOR CODE OPTIMIZATION FRAMEWORK:
1. **Product Specification**: Restate the feature as a clear product spec with user stories and acceptance criteria
2. **Technology Stack**: Recommend simple, proven technologies and explain the rationale
3. **Solution Options**: Provide 2-3 implementation approaches with pros/cons analysis
4. **Recommended Approach**: Select and justify the simplest, most maintainable solution
5. **Implementation Plan**: Break down into small, iterative steps with clear milestones
6. **Testing Strategy**: Outline comprehensive test plan including unit, integration, and user acceptance tests
7. **Development Guidelines**: Include code quality standards and best practices
8. **Risk Mitigation**: Identify potential issues and provide mitigation strategies

ORIGINAL CODE REQUEST: {cleaned_prompt}

Create a comprehensive, actionable development prompt optimized for Cursor AI that a developer can use to implement this feature successfully with AI assistance. Focus on clarity, practicality, maintainability, and optimal Cursor AI interaction patterns."""

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
                
                return {"original": user_prompt, "strategy": strategy, "optimized": response}
        except Exception as e:
            logger.error(f"LLM call failed: {e}")

    # Fallback optimization if LLM not available or failed
    if context == "image_generation":
        fallback_prompt = f"Create a detailed image of {cleaned_prompt} with vivid colors, clear composition, artistic style, and professional lighting. Include specific visual elements and mood."
    elif context == "video_generation":
        fallback_prompt = f"Generate a video of {cleaned_prompt} with smooth motion, clear scene transitions, dynamic camera movements, and engaging visual storytelling elements."
    elif context == "cursor_code_optimizer":
        fallback_prompt = f"""**Cursor-Optimized Code Request**: {cleaned_prompt}

**Implementation Plan for Cursor AI**:
1. Set up development environment with Cursor AI integration
2. Create basic project structure with clear file organization
3. Implement core functionality using AI-assisted development
4. Add error handling and validation with AI suggestions
5. Write comprehensive tests with AI-generated test cases
6. Document the implementation with AI-enhanced documentation

**Technology Stack**: Use modern, well-supported technologies optimized for AI assistance
**Cursor AI Strategy**: Leverage AI for code generation, debugging, and optimization
**Testing Strategy**: Include unit tests, integration tests, and user acceptance testing with AI assistance
**Best Practices**: Follow coding standards, use version control, and implement proper error handling with Cursor AI guidance"""
    else:
        fallback_prompt = f"Please provide a detailed, {context}-focused response about: {cleaned_prompt}"

    return {"original": user_prompt, "strategy": strategy, "optimized": fallback_prompt}

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
