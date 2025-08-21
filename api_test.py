from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import random

app = Flask(__name__)
CORS(app)

# Simulated strategies (docs array)
# Enhanced strategies for world-class prompt optimization
enhanced_strategies = [
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

# World-Class Image and Video Generation Strategies
context_strategies = {
    "rephrase": "Text rephrasing and optimization: Focus on grammar correction, spelling fixes, clarity improvement, and professional language refinement.",
    "technical": "Technical prompting: Request detailed explanations, step-by-step processes, and include technical specifications.",
    "image_generation": "Create world-class image generation prompts using structured prompting: Subject + Details + Style + Technical Specifications + Negative Prompts. Focus on clarity, control, creativity, and quality. Generate prompts that produce stunning, professional-grade images with maximum detail, artistic direction, and technical precision.",
    "video_generation": "Create world-class video generation prompts using structured prompting: Subject + Motion + Style + Technical Specifications + Negative Prompts. Focus on cinematic quality, smooth transitions, dynamic camera movements, and engaging visual storytelling. Generate prompts that produce professional-grade videos with maximum visual impact and narrative flow.",
    "general": "General prompting: Use clear, direct language with specific instructions and expected outcomes, include step-by-step guidance and comprehensive information."
}

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

def apply_strategy_simulated(user_prompt: str, context: str = "general"):
    """Simulated strategy application with context awareness"""
    cleaned_prompt = clean_prompt(user_prompt)
    
    # Get context-specific strategy
    strategy = context_strategies.get(context, context_strategies["general"])
    
    # Enhanced optimization logic based on context with world-class image and video generation
    if context == "rephrase":
        # Simulate grammar correction and text optimization
        corrected_text = user_prompt
        # Fix common spelling mistakes
        corrections = {
            "recieve": "receive",
            "messege": "message",
            "definately": "definitely",
            "occured": "occurred",
            "begining": "beginning",
            "accomodate": "accommodate",
            "requirments": "requirements",
            "maintanence": "maintenance",
            "cruicial": "crucial",
            "sucess": "success",
            "importent": "important",
            "reqyouirements": "requirements",
            "ensyoyoure": "ensure",
            "cryoucial": "crucial",
            "syouccess": "success",
            "calender": "calendar",
            "cemetary": "cemetery",
            "collegue": "colleague",
            "concious": "conscious",
            "embarass": "embarrass",
            "enviroment": "environment",
            "existance": "existence",
            "foriegn": "foreign",
            "fourty": "forty",
            "freind": "friend",
            "garentee": "guarantee",
            "goverment": "government",
            "harrass": "harass",
            "idiosyncracy": "idiosyncrasy",
            "immediatly": "immediately",
            "independant": "independent",
            "knowlege": "knowledge",
            "liase": "liaise",
            "liason": "liaison",
            "neccessary": "necessary",
            "occassion": "occasion",
            "occassionally": "occasionally",
            "occurence": "occurrence",
            "pavillion": "pavilion",
            "persistant": "persistent",
            "posession": "possession",
            "prefered": "preferred",
            "priviledge": "privilege",
            "probaly": "probably",
            "proffesional": "professional",
            "promiss": "promise",
            "pronounciation": "pronunciation",
            "prufe": "proof",
            "pursuade": "persuade",
            "quater": "quarter",
            "questionaire": "questionnaire",
            "reccomend": "recommend",
            "rediculous": "ridiculous",
            "refered": "referred",
            "refering": "referring",
            "religous": "religious",
            "rember": "remember",
            "resistence": "resistance",
            "responce": "response",
            "responcibility": "responsibility",
            "rythm": "rhythm",
            "sence": "sense",
            "seperate": "separate",
            "sieze": "seize",
            "similiar": "similar",
            "sincerly": "sincerely",
            "speach": "speech",
            "sucessful": "successful",
            "suprise": "surprise",
            "tatoo": "tattoo",
            "tendancy": "tendency",
            "therefor": "therefore",
            "threshhold": "threshold",
            "tommorow": "tomorrow",
            "tounge": "tongue",
            "truely": "truly",
            "unfortunatly": "unfortunately",
            "untill": "until",
            "wierd": "weird",
            "whereever": "wherever",
            "wich": "which",
            "womens": "women's",
            "wonderfull": "wonderful",
            "writeing": "writing"
        }
        
        for wrong, right in corrections.items():
            corrected_text = corrected_text.replace(wrong, right)
            corrected_text = corrected_text.replace(wrong.capitalize(), right.capitalize())
        
        # Improve grammar and structure
        if "i " in corrected_text.lower():
            corrected_text = corrected_text.replace("i ", "I ")
        
        # Fix common abbreviations and informal language
        informal_corrections = {
            " ur ": " your ",
            " u ": " you ",
            " its ": " it's ",
            " cant ": " can't ",
            " dont ": " don't ",
            " wont ": " won't ",
            " wouldnt ": " wouldn't ",
            " couldnt ": " couldn't ",
            " shouldnt ": " shouldn't ",
            " havent ": " haven't ",
            " hasnt ": " hasn't ",
            " hadnt ": " hadn't ",
            " isnt ": " isn't ",
            " arent ": " aren't ",
            " wasnt ": " wasn't ",
            " werent ": " weren't "
        }
        
        for informal, formal in informal_corrections.items():
            corrected_text = corrected_text.replace(informal, formal)
            corrected_text = corrected_text.replace(informal.capitalize(), formal.capitalize())
        
        # Remove filler words
        filler_words = ["just", "basically", "actually", "like", "you know", "I mean"]
        for word in filler_words:
            corrected_text = corrected_text.replace(word, "").replace(word.capitalize(), "")
        
        # Clean up extra spaces and punctuation
        corrected_text = re.sub(r'\s+', ' ', corrected_text)
        corrected_text = corrected_text.strip()
        
        if "just" in user_prompt.lower() or "basically" in user_prompt.lower():
            final_prompt = f"{corrected_text}"
        else:
            final_prompt = f"{corrected_text}"
    
    elif context == "technical":
        if "just" in user_prompt.lower() or "basically" in user_prompt.lower():
            final_prompt = f"Please provide a detailed technical explanation of {cleaned_prompt.replace('just', '').replace('basically', '').strip()}, including step-by-step processes, technical specifications, implementation details, and technical terminology."
        else:
            final_prompt = f"Please provide a comprehensive technical analysis of {cleaned_prompt}, including detailed explanations, step-by-step processes, technical specifications, and implementation guidance."
    
    elif context == "image_generation":
        # World-class image generation prompt creation using structured prompting
        # Simple spelling corrections for common image generation terms
        corrected_prompt = user_prompt
        
        # Apply spelling corrections one by one to avoid corruption
        if "beutiful" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("beutiful", "beautiful")
        if "beutifull" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("beutifull", "beautiful")
        if "beautifull" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("beautifull", "beautiful")
        if "portret" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("portret", "portrait")
        if "mountin" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("mountin", "mountain")
        if "sunsett" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("sunsett", "sunset")
        if "landskape" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("landskape", "landscape")
        
        # Grammar improvements
        if "i want" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("i want", "I want")
        if "i need" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("i need", "I need")
        if "i like" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("i like", "I like")
        if "its" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("its", "it's")
        if "ur" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("ur", "your")
        if "u " in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("u ", "you ")
        if " r " in corrected_prompt:
            corrected_prompt = corrected_prompt.replace(" r ", " are ")
        if " 2 " in corrected_prompt:
            corrected_prompt = corrected_prompt.replace(" 2 ", " to ")
        if " 4 " in corrected_prompt:
            corrected_prompt = corrected_prompt.replace(" 4 ", " for ")
        
        # Clean up extra spaces
        corrected_prompt = re.sub(r'\s+', ' ', corrected_prompt).strip()
        
        # Apply the enhanced strategy from context_strategies
        enhanced_strategy = context_strategies["image_generation"]
        
        # Structured Prompting: Subject + Details + Style + Technical Specifications + Negative Prompts
        # Analyze user intent and create comprehensive, professional-grade prompt
        if "portrait" in corrected_prompt.lower() or "person" in corrected_prompt.lower() or "face" in corrected_prompt.lower() or "headshot" in corrected_prompt.lower():
            final_prompt = f"Professional portrait photography masterpiece: {corrected_prompt}, shot with a Canon EOS R5, 85mm f/1.4 GM lens, shallow depth of field (f/1.4), studio lighting with soft key light, rim lighting, and hair light, high-resolution 8K quality, cinematic composition with rule of thirds, professional color grading with skin tone optimization, sharp focus on eyes with natural catch lights, natural skin texture preservation, professional headshot style, neutral background with subtle depth, corporate photography aesthetic, 4:5 aspect ratio, professional retouching, commercial photography quality, professional photography standards -- Negative prompt: blurry, low quality, distorted, extra fingers, bad anatomy, watermark, text, logo, oversaturated, underexposed, noise, grain, artifacts, compression"
        elif "landscape" in corrected_prompt.lower() or "nature" in corrected_prompt.lower() or "outdoor" in corrected_prompt.lower() or "sunset" in corrected_prompt.lower() or "mountains" in corrected_prompt.lower():
            final_prompt = f"Stunning landscape photography masterpiece: {corrected_prompt}, captured with a Sony A7R IV, 16-35mm f/2.8 GM lens, golden hour lighting with dramatic sky, foreground interest with leading lines composition, HDR processing for maximum dynamic range, vibrant natural colors with professional color grading, ultra-wide perspective for environmental storytelling, weather atmosphere enhancement, seasonal color optimization, natural texture preservation, 16:9 cinematic aspect ratio, National Geographic quality, professional nature photography standards -- Negative prompt: blurry, low quality, distorted, oversaturated, underexposed, noise, grain, artifacts, compression, unrealistic colors, artificial lighting, poor composition"
        elif "abstract" in corrected_prompt.lower() or "art" in corrected_prompt.lower() or "creative" in corrected_prompt.lower() or "painting" in corrected_prompt.lower():
            final_prompt = f"Abstract artistic masterpiece: {corrected_prompt}, digital art with high-resolution 8K quality, vibrant color palette with professional color theory, dynamic composition with visual hierarchy, artistic lighting with creative effects, creative textures and materials, modern art style with contemporary aesthetics, gallery quality with professional finish, professional digital painting techniques, artistic expression with visual impact, professional art direction, museum-quality finish, creative lighting effects, artistic color harmony, professional digital art standards -- Negative prompt: blurry, low quality, distorted, oversaturated, underexposed, noise, grain, artifacts, compression, amateur, childish, unprofessional"
        elif "product" in corrected_prompt.lower() or "luxury" in corrected_prompt.lower() or "watch" in corrected_prompt.lower() or "jewelry" in corrected_prompt.lower():
            final_prompt = f"Professional product photography masterpiece: {corrected_prompt}, shot with professional camera equipment (Canon EOS R5), studio-quality lighting with three-point lighting system, cinematic composition with professional framing, high-resolution 8K quality, professional color grading with product optimization, sharp focus with depth of field control, artistic style with commercial appeal, professional photography standards, commercial quality with market appeal, visual storytelling with product narrative, professional image composition, artistic direction with brand alignment, technical excellence, professional finish, gallery-worthy quality, commercial photography standards -- Negative prompt: blurry, low quality, distorted, oversaturated, underexposed, noise, grain, artifacts, compression, amateur, unprofessional, poor lighting, bad composition"
        else:
            final_prompt = f"Professional high-quality image masterpiece: {corrected_prompt}, shot with professional camera equipment (Canon EOS R5), studio-quality lighting with professional three-point system, cinematic composition with professional framing, high-resolution 8K quality, professional color grading with visual optimization, sharp focus with depth of field control, artistic style with professional appeal, professional photography standards, commercial quality with market appeal, visual storytelling with narrative elements, professional image composition, artistic direction with creative vision, technical excellence with professional standards, professional finish with quality assurance, gallery-worthy quality with artistic merit, professional photography standards -- Negative prompt: blurry, low quality, distorted, oversaturated, underexposed, noise, grain, artifacts, compression, amateur, unprofessional, poor lighting, bad composition"
    
    elif context == "video_generation":
        # World-class video generation prompt creation using structured prompting
        # Simple spelling corrections for common video generation terms
        corrected_prompt = user_prompt
        
        # Apply spelling corrections one by one to avoid corruption
        if "vidio" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("vidio", "video")
        if "beutiful" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("beutiful", "beautiful")
        if "beutifull" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("beutifull", "beautiful")
        if "beautifull" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("beautifull", "beautiful")
        if "mountin" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("mountin", "mountain")
        if "sunsett" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("sunsett", "sunset")
        if "landskape" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("landskape", "landscape")
        
        # Grammar improvements
        if "i want" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("i want", "I want")
        if "i need" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("i need", "I need")
        if "i like" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("i like", "I like")
        if "its" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("its", "it's")
        if "ur" in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("ur", "your")
        if "u " in corrected_prompt:
            corrected_prompt = corrected_prompt.replace("u ", "you ")
        if " r " in corrected_prompt:
            corrected_prompt = corrected_prompt.replace(" r ", " are ")
        if " 2 " in corrected_prompt:
            corrected_prompt = corrected_prompt.replace(" 2 ", " to ")
        if " 4 " in corrected_prompt:
            corrected_prompt = corrected_prompt.replace(" 4 ", " for ")
        
        # Clean up extra spaces
        corrected_prompt = re.sub(r'\s+', ' ', corrected_prompt).strip()
        
        # Apply the enhanced strategy from context_strategies
        enhanced_strategy = context_strategies["video_generation"]
        
        # Structured Prompting: Subject + Motion + Style + Technical Specifications + Negative Prompts
        # Analyze user intent and create comprehensive, professional-grade video prompt
        if "action" in corrected_prompt.lower() or "movement" in corrected_prompt.lower() or "dynamic" in corrected_prompt.lower():
            final_prompt = f"Dynamic action video masterpiece: {corrected_prompt}, captured with professional cinema cameras (RED Komodo 6K), smooth motion tracking, dynamic camera movements with gimbal stabilization, cinematic composition with rule of thirds, professional lighting with dramatic shadows, high frame rate (60fps) for smooth motion, professional color grading with cinematic LUTs, dynamic scene transitions, engaging visual storytelling, professional cinematography standards, commercial quality with market appeal, visual effects integration, professional video composition, artistic direction with creative vision, technical excellence with professional standards, professional finish with quality assurance, cinema-worthy quality with artistic merit, professional video production standards -- Negative prompt: choppy motion, low quality, distorted, oversaturated, underexposed, noise, grain, artifacts, compression, amateur, unprofessional, poor lighting, bad composition, shaky camera, blurry frames"
        elif "nature" in corrected_prompt.lower() or "landscape" in corrected_prompt.lower() or "outdoor" in corrected_prompt.lower():
            final_prompt = f"Stunning nature video masterpiece: {corrected_prompt}, captured with professional cinema cameras (Sony FX6), smooth panning and tilting movements, cinematic composition with leading lines, natural lighting with golden hour enhancement, time-lapse techniques for environmental storytelling, high dynamic range processing, professional color grading with natural color palette, smooth scene transitions, engaging visual narrative, professional cinematography standards, documentary quality with educational appeal, visual effects enhancement, professional video composition, artistic direction with environmental focus, technical excellence with professional standards, professional finish with quality assurance, documentary-worthy quality with artistic merit, professional nature video production standards -- Negative prompt: choppy motion, low quality, distorted, oversaturated, underexposed, noise, grain, artifacts, compression, amateur, unprofessional, poor lighting, bad composition, shaky camera, blurry frames, artificial movement"
        elif "product" in corrected_prompt.lower() or "commercial" in corrected_prompt.lower() or "advertising" in corrected_prompt.lower():
            final_prompt = f"Professional commercial video masterpiece: {corrected_prompt}, shot with professional cinema cameras (Canon C300 Mark III), smooth product reveal movements, cinematic composition with professional framing, studio-quality lighting with three-point system, high frame rate (30fps) for smooth playback, professional color grading with brand color optimization, smooth scene transitions, engaging product narrative, professional cinematography standards, commercial quality with market appeal, visual effects integration, professional video composition, artistic direction with brand alignment, technical excellence with professional standards, professional finish with quality assurance, commercial-worthy quality with artistic merit, professional commercial video production standards -- Negative prompt: choppy motion, low quality, distorted, oversaturated, underexposed, noise, grain, artifacts, compression, amateur, unprofessional, poor lighting, bad composition, shaky camera, blurry frames, unprofessional movement"
        else:
            final_prompt = f"Professional high-quality video masterpiece: {corrected_prompt}, shot with professional cinema cameras (RED Komodo 6K), smooth motion with professional stabilization, cinematic composition with professional framing, studio-quality lighting with professional three-point system, high frame rate (30fps) for smooth playback, professional color grading with visual optimization, smooth scene transitions, engaging visual narrative, professional cinematography standards, commercial quality with market appeal, visual effects integration, professional video composition, artistic direction with creative vision, technical excellence with professional standards, professional finish with quality assurance, cinema-worthy quality with artistic merit, professional video production standards -- Negative prompt: choppy motion, low quality, distorted, oversaturated, underexposed, noise, grain, artifacts, compression, amateur, unprofessional, poor lighting, bad composition, shaky camera, blurry frames, unprofessional movement"
    
    else:  # general context
        if "just" in user_prompt.lower() or "basically" in user_prompt.lower():
            final_prompt = f"Please provide detailed, step-by-step information about {cleaned_prompt.replace('just', '').replace('basically', '').strip()}"
        else:
            final_prompt = f"Please provide detailed, step-by-step information about {cleaned_prompt}"

    return {
        "original": user_prompt,
        "strategy": strategy,
        "optimized": final_prompt
    }

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Prompt Optimizer Test API is running"})

@app.route('/optimize', methods=['POST'])
def optimize_prompt():
    try:
        data = request.get_json()
        user_prompt = data.get('prompt', '')
        context = data.get('context', 'general')
        
        if not user_prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        # Validate context
        if context not in context_strategies:
            context = "general"
        
        result = apply_strategy_simulated(user_prompt, context)
        return jsonify(result)
        
    except Exception as e:
        print(f"Error optimizing prompt: {e}")
        return jsonify({"error": "Failed to optimize prompt"}), 500

@app.route('/strategies', methods=['GET'])
def get_strategies():
    """Get available strategies and contexts"""
    return jsonify({
        "contexts": list(context_strategies.keys()),
        "strategies": enhanced_strategies
    })

if __name__ == '__main__':
    print("🚀 Starting Prompt Optimizer Test API...")
    print(f"📝 Available contexts: {len(context_strategies)}")
    print(f"🌐 API will be available at: http://localhost:5000")
    print("⚠️  This is a TEST version - no external API calls required")
    app.run(debug=True, host='0.0.0.0', port=5000)
