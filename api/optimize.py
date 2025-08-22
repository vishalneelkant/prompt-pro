from flask import Flask, request, jsonify
import logging
from flask_cors import CORS
import os
import pinecone
import re
from dotenv import load_dotenv
import sys
import traceback
import builtins

# Load environment variables
load_dotenv()


app = Flask(__name__)
CORS(app)

# Setup logger
logger = logging.getLogger("prompt_optimizer")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)

# Diagnostic: check key package versions to help debug issubclass() TypeError
try:
    import typing_extensions
    te_version = getattr(typing_extensions, '__version__', str(typing_extensions.__dict__.get('__version__', 'unknown')))
except Exception:
    te_version = 'not installed or import failed'

try:
    import pydantic
    pydantic_version = getattr(pydantic, '__version__', 'unknown')
except Exception:
    pydantic_version = 'not installed or import failed'

try:
    import openai
    openai_version = getattr(openai, '__version__', 'unknown')
except Exception:
    openai_version = 'not installed or import failed'

try:
    import langchain
    langchain_version = getattr(langchain, '__version__', 'unknown')
except Exception:
    langchain_version = 'not installed or import failed'

logger.info(f"Python version: {sys.version.split()[0]}")
logger.info(f"typing_extensions: {te_version}, pydantic: {pydantic_version}, openai: {openai_version}, langchain: {langchain_version}")

# Wrap risky third-party imports that previously caused crashes so we can log their tracebacks
try:
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
except Exception as e:
    logger.error("Failed to import langchain_openai module", exc_info=True)
    OpenAIEmbeddings = None
    ChatOpenAI = None

try:
    from langchain_pinecone import PineconeVectorStore
except Exception as e:
    logger.error("Failed to import langchain_pinecone module", exc_info=True)
    PineconeVectorStore = None

# Initialize Pinecone (commented out due to version compatibility)
pc = None

# Create index if not exists
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
    "Iterative Refinement: Structure prompts for easy modification, allowing users to adjust specific elements while maintaining core vision."
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
    "general": "General prompting: Use clear, direct language with specific instructions and expected outcomes."
}

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# Create vectorstore if Pinecone is available (commented out due to version compatibility)
vectorstore = None
retriever = None

def setup_pinecone_and_vectorstore():
    """Initialize Pinecone client, ensure index exists, and create vectorstore + retriever lazily.
    Safe to call multiple times; it will no-op if already initialized.
    """
    global pc, vectorstore, retriever
    # If retriever already initialized, nothing to do
    if retriever:
        logger.info("Pinecone vectorstore and retriever already initialized. Skipping setup.")
        return

    # Initialize Pinecone client if not present
    if not pc:
        try:
            logger.info("Initializing Pinecone client (lazy)...")
            pinecone_api_key = os.getenv('PINECONE_API_KEY')
            pc_local = pinecone.Pinecone(api_key=pinecone_api_key)
            pc = pc_local
            logger.info("Pinecone client initialized successfully (lazy).")
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone client (lazy): {e}")
            pc = None
            return

    # Ensure index exists
    try:
        if pc:
            logger.info(f"Checking if Pinecone index '{index_name}' exists (lazy)...")
            try:
                index_list = pc.list_indexes()
            except Exception as e:
                logger.error(f"Failed to list Pinecone indexes: {e}")
                index_list = []

            if index_name not in [i.get("name") if isinstance(i, dict) else i for i in index_list]:
                try:
                    logger.info(f"Index '{index_name}' not found. Creating index (lazy)...")
                    pc.create_index(
                        name=index_name,
                        dimension=1536,
                        metric="cosine",
                        spec=pinecone.ServerlessSpec(
                            cloud="aws",
                            region="us-east-1"
                        )
                    )
                    logger.info(f"Index '{index_name}' created successfully (lazy).")
                except Exception as e:
                    logger.error(f"Failed to create index '{index_name}': {e}")
            else:
                logger.info(f"Index '{index_name}' already exists (lazy).")
        else:
            logger.warning("Pinecone client is not initialized (lazy). Skipping index creation.")
    except Exception as e:
        logger.error(f"Pinecone index creation/listing failed (lazy): {e}")

    # Initialize vectorstore and retriever wrapper
    try:
        if pc:
            logger.info(f"Initializing Pinecone vectorstore wrapper (lazy) with index_name='{index_name}' and docs count={len(docs)}.")
            try:
                index = pc.Index(index_name)
                vectorstore = PineconeVectorStore(index=index, embedding=embeddings)
                retriever = vectorstore.as_retriever()
                logger.info(f"Vectorstore and retriever initialized successfully (lazy). retriever={retriever}")
            except Exception as e:
                logger.error(f"Error initializing PineconeVectorStore lazily: {e}")
        else:
            logger.warning("Pinecone client not available (lazy). Skipping vectorstore and retriever initialization.")
    except Exception as e:
        logger.error(f"Vectorstore or retriever initialization failed (lazy): {e}")

def clean_prompt(prompt: str) -> str:
    """Remove filler words and clean the prompt while preserving important context"""
    # Only remove truly unnecessary filler words, preserve context-relevant words
    useless_words = ["actually", "basically", "just", "like", "I mean", "you know", "um", "uh", "well"]
    
    # Create a more targeted regex that doesn't remove words that might be part of the actual request
    cleaned = prompt
    for word in useless_words:
        # Use word boundaries and be more careful about removal
        pattern = r'\b' + re.escape(word) + r'\b'
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # Clean up extra whitespace and punctuation
    cleaned = re.sub(r'\s+', ' ', cleaned)  # Multiple spaces to single space
    cleaned = re.sub(r'\s*,\s*', ', ', cleaned)  # Clean up comma spacing
    cleaned = re.sub(r'\s*\.\s*', '. ', cleaned)  # Clean up period spacing
    cleaned = re.sub(r'^\s*[,.\s]+', '', cleaned)  # Remove leading separators
    cleaned = re.sub(r'[,.\s]+\s*$', '', cleaned)  # Remove trailing separators
    
    return cleaned.strip()

def get_strategy_for_context(context: str, cleaned_prompt: str):
    """Get the best strategy based on context and prompt content"""
    # First, try to get context-specific strategy
    context_strategy = context_strategies.get(context, context_strategies["general"])
    
    # If Pinecone is available, try to get a more specific strategy
    if retriever:
        try:
            logger.info(f"Attempting to retrieve strategy for context '{context}' and prompt '{cleaned_prompt}'...")
            results = retriever.get_relevant_documents(cleaned_prompt)
            logger.info(f"Retriever results: {results}")
            if results:
                logger.info("Strategy retrieved from retriever.")
                return results[0].page_content
            else:
                logger.warning("No relevant documents found by retriever. Using context strategy fallback.")
        except Exception as e:
            logger.error(f"Strategy retrieval via retriever failed: {e}")
    else:
        logger.warning("Retriever is not initialized. Using context strategy fallback.")
    # Fallback to context-specific strategy
    return context_strategy

def apply_strategy(user_prompt: str, context: str = "general"):
    """Apply optimization strategy based on context and prompt"""
    # print("str ", str)
    # Step 1: Clean the prompt
    cleaned_prompt = clean_prompt(user_prompt)
    
    # Step 2: Get strategy based on context
    strategy = get_strategy_for_context(context, cleaned_prompt)
    
    # Step 3: Create context-aware optimization template
    context_instructions = {

        "rephrase": "Focus on grammar correction, spelling fixes, clarity improvement, professional language refinement, sentence structure optimization, and ensuring the text is clear, concise, and error-free.",
        "technical": "Provide detailed technical explanations, include step-by-step processes, use precise terminology, technical specifications, and implementation guidance.",
        "image_generation": "Create world-class image generation prompts using structured prompting: Subject + Details + Style + Technical Specifications + Negative Prompts. Focus on clarity, control, creativity, and quality. Generate prompts that produce stunning, professional-grade images with maximum detail, artistic direction, and technical precision.",
        "video_generation": "Create world-class video generation prompts using structured prompting: Subject + Motion + Style + Technical Specifications + Negative Prompts. Focus on cinematic quality, smooth transitions, dynamic camera movements, and engaging visual storytelling. Generate prompts that produce professional-grade videos with maximum visual impact and narrative flow.",
        "image_generation": "Create world-class image generation prompts that understand user intent, analyze visual requirements, and generate comprehensive prompts with professional composition, lighting, style, mood, technical specifications, color harmony, and artistic direction. Focus on creating prompts that generate stunning, professional-quality images with maximum detail and visual impact.",
        "video_generation": "Specify visual elements, motion dynamics, timing, scene transitions, camera movements, narrative flow, and visual storytelling elements for AI video generation. Include details about pacing, visual effects, cinematic techniques, and narrative structure.",
        "general": "Use clear, direct language with specific instructions and expected outcomes, include step-by-step guidance and comprehensive information."
    }
    
    context_instruction = context_instructions.get(context, context_instructions["general"])
    
    # Enhanced template for image and video generation
    if context in ["image_generation", "video_generation"]:
        template = f"""
        You are a World-Class Image Generation Prompt Engineer, an expert at creating prompts that generate stunning, professional-quality images.

        Your mission is to transform the user's basic idea into a masterpiece-level prompt that will create exceptional AI-generated images.

        ANALYSIS PHASE:
        1. Understand the user's core intent and emotional goal
        2. Identify what type of image they want to create
        3. Determine the level of detail and sophistication needed
        4. Assess the intended use case and audience
        5. Improve sentence structure and flow

        OPTIMIZATION STRATEGY:
        Apply this strategy: {strategy}
        
        CONTEXT INSTRUCTIONS:
        {context_instruction}

        PROMPT STRUCTURE REQUIREMENTS:
        - Start with a clear, powerful subject description
        - Add specific visual attributes and characteristics
        - Include professional composition details (camera angle, framing, perspective)
        - Specify lighting with professional terminology
        - Define artistic style and medium with specific references
        - Add emotional and atmospheric elements
        - Include technical quality specifications
        - Add environmental context and background details
        - Specify color palette and visual harmony
        - Include negative prompts to avoid common issues
        - Use cinematic and artistic language that AI models understand

        USER'S ORIGINAL REQUEST:
        {cleaned_prompt}

        YOUR TASK:
        Create a world-class image generation prompt that:
        1. Captures the user's exact vision and intent
        2. Uses professional visual language and terminology
        3. Includes all necessary technical specifications
        4. Creates an emotionally compelling and visually stunning image
        5. Is optimized for maximum AI model performance
        6. Follows industry best practices for prompt engineering

        Return ONLY the optimized, professional-grade image generation prompt.
        """
    elif context == "rephrase":
        template = f"""
        You are a Text Optimization AI specializing in grammar correction and text refinement.

        Your task:
        1. Apply the given prompting strategy: {strategy}
        2. Focus on grammar correction, spelling fixes, and clarity improvement
        3. {context_instruction}
        4. Correct all spelling mistakes and grammatical errors
        5. Improve sentence structure and flow
        6. Make the text more professional and clear
        7. Ensure proper punctuation and capitalization
        8. Remove redundant words while preserving meaning
        9. Return a polished, error-free version of the original text

        Original User Text:
        {cleaned_prompt}

        Return ONLY the corrected and optimized text with proper grammar, spelling, and clarity.
        """
    else:
        template = f"""
        You are a Prompt Optimizer AI specializing in {context} content.

        Your task:
        1. Apply the given prompting strategy: {strategy}
        2. Optimize the user's prompt for {context} context
        3. {context_instruction}
        4. Remove filler words and unnecessary phrases
        5. Ensure the final prompt maximizes reasoning and output quality
        6. Correct any spelling and grammatical mistakes from the prompt

        Original User Prompt:
        {cleaned_prompt}

        Return ONLY the optimized and reformulated prompt.
        """
    
    try:
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        response = llm.predict(template)
        # print("response ", response)
        # Clean up response for rephrase context
        if context == "rephrase":
            # Remove common prefixes that might be added by the LLM
            cleaned_response = response
            prefixes_to_remove = [
                "Corrected and optimized text:",
                "Corrected text:",
                "Optimized text:",
                "Here's the corrected text:",
                "The corrected version is:"
            ]
            
            for prefix in prefixes_to_remove:
                if cleaned_response.startswith(prefix):
                    cleaned_response = cleaned_response[len(prefix):].strip()
                    break
            
            # Clean up any extra whitespace or punctuation
            cleaned_response = cleaned_response.strip()
            if cleaned_response.startswith("."):
                cleaned_response = cleaned_response[1:].strip()
            
            return {
                "original": user_prompt,
                "strategy": strategy,
                "optimized": cleaned_response
            }
        else:
            return {
                "original": user_prompt,
                "strategy": strategy,
                "optimized": response
            }
            
    except Exception as e:
            print(f"⚠️  LLM call failed: {e}")
            # Fallback optimization with context-specific logic
            if context == "image_generation":
                fallback_prompt = f"Create a detailed image of {cleaned_prompt} with vivid colors, clear composition, artistic style, and professional lighting. Include specific visual elements and mood."
            elif context == "video_generation":
                fallback_prompt = f"Generate a video of {cleaned_prompt} with smooth motion, clear scene transitions, dynamic camera movements, and engaging visual storytelling elements."
            # elif context == "rephrase":
            #     # Clean fallback response for rephrase context
            #     fallback_prompt = f"I receive your message and will definitely respond."
            else:
                fallback_prompt = f"Please provide a detailed, {context}-focused response about: {cleaned_prompt}"
            
            return {
                "original": user_prompt,
                "strategy": strategy,
                "optimized": fallback_prompt
            }

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Prompt Optimizer API is running"})

@app.route('/api/optimize', methods=['POST'])
def optimize_prompt():
    try:
        # Ensure Pinecone and retriever are initialized on-demand when this API is called
        try:
            setup_pinecone_and_vectorstore()
        except Exception as e:
            logger.error(f"Lazy setup of Pinecone/vectorstore failed at request time: {e}")

        data = request.get_json()
        user_prompt = data.get('prompt', '')
        context = data.get('context', 'general')
        logger.info(f"Received optimize request: prompt='{user_prompt}', context='{context}'")
        
        if not user_prompt:
            logger.warning("Prompt is required but missing in request.")
            return jsonify({"error": "Prompt is required"}), 400
        
        # Validate context
        if context not in context_strategies:
            logger.info(f"Context '{context}' not recognized. Defaulting to 'general'.")
            context = "general"
        
        result = apply_strategy(user_prompt, context)
        logger.info(f"Optimization result: {result}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error optimizing prompt: {e}", exc_info=True)
        return jsonify({"error": "Failed to optimize prompt"}), 500

@app.route('/api/strategies', methods=['GET'])
def get_strategies():
    """Get available strategies and contexts"""
    return jsonify({
        "contexts": list(context_strategies.keys()),
        "strategies": docs
    })


# Diagnostic wrapper: intercept issubclass calls to log offending non-class first args
if not getattr(builtins, '_issubclass_wrapped_for_diagnostics', False):
    _orig_issubclass = builtins.issubclass
    def _diagnostic_issubclass(cls, classinfo):
        try:
            return _orig_issubclass(cls, classinfo)
        except TypeError as te:
            try:
                logger.error("issubclass() raised TypeError — logging diagnostic info", exc_info=True)
                # Log the exact type and a safe repr of the first argument
                try:
                    arg_type = type(cls)
                    arg_repr = repr(cls)
                except Exception:
                    arg_type = 'unrepresentable'
                    arg_repr = '<unrepresentable>'
                logger.error(f"Offending issubclass first-arg type: {arg_type}; value repr (truncated): {arg_repr[:1000]}")
            except Exception:
                pass
            # Re-raise the original error to keep behavior unchanged
            raise
    builtins.issubclass = _diagnostic_issubclass
    builtins._issubclass_wrapped_for_diagnostics = True


# # Vercel Python Function handler
# def handler(environ, start_response):
#     from werkzeug.middleware.dispatcher import DispatcherMiddleware
#     application = DispatcherMiddleware(app)
#     return application(environ, start_response)


# Local development entry point
if __name__ == "__main__":
    app.run()
