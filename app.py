import streamlit as st
from image_generator import ImageGenerator
from image_processor import ImageProcessor
from error_handler import RetryError
import time
from datetime import datetime
import os

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="🎨 Multimodal Image Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CUSTOM CSS (Deploy Button Hide) =====
st.markdown("""
    <style>
    /* 🔥 Hide Deploy Button */
    .stDeployButton {
        display: none !important;
    }
    
    /* Hide Streamlit Footer */
    footer {
        display: none !important;
    }
    
    /* Hide Streamlit Menu */
    #MainMenu {
        display: none !important;
    }
    
    /* Main Container */
    .main {
        padding: 1rem;
    }
    
    /* Header */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* Divider */
    .divider {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
        margin: 1.5rem 0;
        border-radius: 10px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 2rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
    
    /* Success Box */
    .success-box {
        padding: 1.2rem;
        background: #d4edda;
        color: #155724;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        border: 2px solid #b7eb8f;
        margin: 1rem 0;
    }
    
    /* Error Box */
    .error-box {
        padding: 1.2rem;
        background: #f8d7da;
        color: #721c24;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        border: 2px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    /* Info Box */
    .info-box {
        padding: 1.2rem;
        background: #d1ecf1;
        color: #0c5460;
        border-radius: 12px;
        text-align: center;
        border: 2px solid #bee5eb;
        margin: 1rem 0;
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        text-align: center;
        border: 1px solid #e8e8e8;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
        transform: translateY(-3px);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a1a2e;
    }
    
    .feature-desc {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.3rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1.5rem 0;
        color: #888;
        font-size: 0.9rem;
        border-top: 2px solid #eee;
        margin-top: 2rem;
    }
    
    .footer-name {
        color: #667eea;
        font-weight: 600;
    }
    
    .footer-heart {
        color: #e74c3c;
    }
    </style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.markdown('<h1 class="main-header">🎨 Multimodal Image Studio</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">🚀 Where Imagination Meets Artificial Intelligence</p>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.header("⚙️ Generation Settings")
    st.markdown("---")
    
    st.subheader("📝 Text Prompt")
    prompt = st.text_area(
        "Describe your vision:",
        placeholder="A cyberpunk city at night, neon lights reflecting on wet streets, raining, cinematic...",
        height=120
    )
    
    st.markdown("---")
    
    st.subheader("📐 Image Settings")
    
    aspect_preset = st.selectbox(
        "🎯 Aspect Ratio",
        [
            "1:1 (Square) - 1024x1024",
            "16:9 (Landscape) - 1344x768",
            "9:16 (Portrait) - 768x1344",
            "Custom"
        ],
        index=0
    )
    
    if aspect_preset == "1:1 (Square) - 1024x1024":
        width, height = 1024, 1024
    elif aspect_preset == "16:9 (Landscape) - 1344x768":
        width, height = 1344, 768
    elif aspect_preset == "9:16 (Portrait) - 768x1344":
        width, height = 768, 1344
    else:
        col1, col2 = st.columns(2)
        with col1:
            width = st.selectbox("Width", [512, 768, 1024, 1344], index=2)
        with col2:
            height = st.selectbox("Height", [512, 768, 1024, 1344], index=2)
    
    st.caption(f"📐 Resolution: {width} x {height}")
    
    samples = st.slider("📸 Number of Images", 1, 4, 2)
    
    st.markdown("---")
    
    st.subheader("🎨 Style")
    style_preset = st.selectbox(
        "Choose a style:",
        ["photographic", "cinematic", "anime", "digital-art", "fantasy-art", "3d-model", "none"],
        index=0
    )
    
    st.markdown("---")
    
    generate_button = st.button("🚀 Generate Image", type="primary", use_container_width=True)
    
    st.markdown("---")
    
    with st.expander("ℹ️ About"):
        st.markdown("""
        **Project 3: Multimodal Image Generation Studio**
        
        - 🎯 Text-to-Image Generation
        - 🎨 Multiple Art Styles
        - 📐 Aspect Ratios
        - ✅ Auto Quality Check
        - 🔄 Smart Retry System
        
        **Tech:** Python • Streamlit • Stability AI
        """)

# ===== MAIN AREA =====
if generate_button:
    if not prompt or len(prompt.strip()) == 0:
        st.markdown('<div class="error-box">⚠️ Please enter a prompt before generating!</div>', unsafe_allow_html=True)
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        generated_images = []
        
        try:
            status_text.markdown('<div class="info-box">🔄 Initializing AI Engine...</div>', unsafe_allow_html=True)
            progress_bar.progress(10)
            
            generator = ImageGenerator()
            processor = ImageProcessor()
            
            for i in range(samples):
                status_text.markdown(f'<div class="info-box">🎨 Generating image {i+1}/{samples}: "{prompt[:30]}..."</div>', unsafe_allow_html=True)
                progress_bar.progress(30 + (i * 60 // samples))
                
                image = generator.generate_image(
                    prompt=prompt,
                    width=width,
                    height=height,
                    samples=1
                )
                
                status_text.markdown(f'<div class="info-box">🔍 Validating image {i+1}...</div>', unsafe_allow_html=True)
                if not processor.validate_image(image):
                    st.markdown(f'<div class="error-box">❌ Image {i+1} corrupted! Skipping...</div>', unsafe_allow_html=True)
                    continue
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filepath = processor.save_image(image, filename=f"generated_{timestamp}_{i+1}.png")
                generated_images.append((image, filepath))
                
                progress_bar.progress(70 + (i * 30 // samples))
            
            progress_bar.progress(95)
            status_text.empty()
            progress_bar.progress(100)
            
            if not generated_images:
                st.markdown('<div class="error-box">❌ No valid images generated!</div>', unsafe_allow_html=True)
                st.stop()
            
            st.markdown(f'<div class="success-box">✅ {len(generated_images)} Image(s) Generated Successfully! 🎉</div>', unsafe_allow_html=True)
            
            if len(generated_images) == 1:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(generated_images[0][0], caption=f"✨ {prompt[:100]}...", width=700)
                    with open(generated_images[0][1], "rb") as f:
                        image_data = f.read()
                    st.download_button(
                        label="📥 Download Image",
                        data=image_data,
                        file_name=f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                        mime="image/png",
                        use_container_width=True
                    )
            else:
                cols_per_row = min(len(generated_images), 3)
                cols = st.columns(cols_per_row)
                
                for idx, (img, path) in enumerate(generated_images):
                    col_idx = idx % cols_per_row
                    with cols[col_idx]:
                        st.image(img, caption=f"🖼️ Image {idx+1}", width=300)
                        with open(path, "rb") as f:
                            img_data = f.read()
                        st.download_button(
                            label=f"📥 Download {idx+1}",
                            data=img_data,
                            file_name=f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{idx+1}.png",
                            mime="image/png",
                            use_container_width=True
                        )
            
            st.info(f"💾 All images saved in: `outputs/` folder")
            
            with st.expander("📊 Image Details"):
                info = processor.get_image_info(generated_images[0][0])
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Width", f"{info['width']}px")
                    st.metric("Height", f"{info['height']}px")
                with col2:
                    st.metric("Total Pixels", f"{info['pixels']:,}")
                    st.metric("Format", info['format'])
                with col3:
                    st.metric("Mode", info['mode'])
                    st.metric("Total Generated", len(generated_images))
            
            with st.expander("📝 Prompt & Settings"):
                st.code(prompt, language="text")
                st.markdown(f"**Style:** {style_preset}")
                st.markdown(f"**Resolution:** {width}x{height}")
                st.markdown(f"**Samples:** {len(generated_images)}")
            
            status_text.empty()
            
        except RetryError as e:
            st.markdown(f'<div class="error-box">❌ Failed: {str(e)}</div>', unsafe_allow_html=True)
            st.info("💡 Check internet & API key")
            
        except Exception as e:
            st.markdown(f'<div class="error-box">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
            st.info("💡 Check API key in .env file")

else:
    st.markdown('<div class="info-box">👈 Enter a prompt and click Generate Image</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Text-to-Image</div>
            <div class="feature-desc">Describe anything, AI creates it</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎨</div>
            <div class="feature-title">Multiple Styles</div>
            <div class="feature-desc">Photographic, Anime, Cinematic & more</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📐</div>
            <div class="feature-title">Aspect Ratios</div>
            <div class="feature-desc">Square, Landscape, Portrait</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    with st.expander("💡 Example Prompts"):
        st.markdown("""
        ### 🏔️ Switzerland / Nature
        1. `A breathtaking view of the Swiss Alps, snow-capped mountains, green meadows with wildflowers, crystal clear blue lake, traditional Swiss chalet, golden hour, photorealistic, 8k`
        
        ### 🌃 Cyberpunk
        2. `A futuristic cyberpunk city at night, neon lights reflecting on wet streets, flying cars, holographic billboards, intense blue and purple colors, cinematic, highly detailed`
        
        ### 🎀 Anime
        3. `A cute anime girl with cat ears, wearing a hoodie, drinking bubble tea, cherry blossom trees in background, studio ghibli style, pastel colors`
        
        ### 🏰 Fantasy
        4. `A majestic fantasy castle floating in the clouds, waterfalls cascading from it, magical glowing crystals, rainbow in background, epic fantasy art, highly detailed`
        
        ### 🌺 Japanese Garden
        5. `A beautiful Japanese garden in spring, cherry blossom trees, koi pond, red wooden bridge, soft pink petals falling, calm peaceful atmosphere, photorealistic`
        """)

# ===== FOOTER =====
st.markdown("---")
st.markdown("""
    <div class="footer">
        🚀 Built with <span class="footer-heart">❤️</span> by <span class="footer-name">Malaika Tariq</span> | DecodeLabs Batch 2026
    </div>
""", unsafe_allow_html=True)