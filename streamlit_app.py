import streamlit as st
import base64
import os
import random
from openai import OpenAI
from caption_generator import process_video, refine_caption_with_claude

# --- FULL OPENAI API KEY (replace with your actual key if needed) ---
OPENAI_API_KEY = "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"

def set_background_from_bytes(image_bytes, image_type="jpg"):
    encoded = base64.b64encode(image_bytes).decode()
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/{image_type};base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Move background uploader to sidebar (settings area)
with st.sidebar:
    st.markdown("### Settings")
    uploaded_bg = st.file_uploader("Background image (jpg/png)", type=["jpg", "jpeg", "png"])
    # (Optional) Uncomment for URL-based backgrounds
    # bg_url = st.text_input("Or paste background image URL")

    with st.sidebar.expander("ℹ️ About this app", expanded=False):
        st.markdown("""
**✍️ nio.scribe – Catholic Caption + Editorial Generator**

This Streamlit app is an advanced tool for Catholic media, content creation, and social marketing. It streamlines the production of Instagram Reels, Carousels, YouTube Shorts, and bold editorial posts.

**Key Features:**
- **Background Customization:** Instantly change the app's background by uploading a local image or pasting an image URL.
- **Content Generation Modes:** Reels, Carousels, Editorials, and more.
- **Viral Hashtag Block Selector:** Curated, SEO-optimized blocks for each content type.
- **Media Upload:** Drop in a video file to auto-transcribe and caption.
- **UI/UX:** Clean sidebar settings and live preview.
- **Non-Technical User Ready:** No coding required.

**How to use:**
1. Launch the app: `$ streamlit run streamlit_app.py`
2. Use the sidebar to select background, output mode, account, and upload files.
3. Generate captions, carousels, or editorials as needed.

For issues or enhancements, contact the developer or open a GitHub issue.

---
with 🖤 nio haus
""")

if uploaded_bg is not None:
    file_type = uploaded_bg.type.split("/")[-1]
    set_background_from_bytes(uploaded_bg.read(), image_type=file_type)
else:
    if os.path.exists("parlorcore.jpg"):
        with open("parlorcore.jpg", "rb") as f:
            set_background_from_bytes(f.read(), image_type="jpg")
    # (Optional) Uncomment if using bg_url:
    # elif bg_url:
    #     st.markdown(f"""
    #         <style>
    #         [data-testid="stAppViewContainer"] {{
    #             background-image: url("{bg_url}");
    #             background-size: cover;
    #             background-repeat: no-repeat;
    #             background-attachment: fixed;
    #             background-position: center;
    #         }}
    #         </style>
    #     """, unsafe_allow_html=True)

HASHTAG_BLOCKS = {
    "Main Catholic": [
        "#catholic", "#CatholicChurch", "#Catholicism", "#Catholicfaith", "#catholiclife",
        "#Holy", "#JesusChrist", "#Prayer", "#Bible", "#Catholics"
    ],
    "SEO": [
        "#mercy", "#sacrifice", "#confession", "#repentance", "#Saint", "#Eucharist"
    ],
    "Protestant Outreach": [
        "#protestant", "#reformationday", "#Christian"
    ],
    "Trad Mass": [
        "#TraditionalCatholic", "#FSSP", "#ICKSP", "#romancatholic", "#latinmass"
    ],
    "All Approved": [
        "#catholic", "#CatholicChurch", "#Catolico", "#catolica", "#Holy", "#Pray", "#Prayer", "#God", "#JesusChrist",
        "#TraditionalCatholic", "#Catholicism", "#Catholicmen", "#Bible", "#Christian", "#Catholicwomen", "#Catholics",
        "#faith", "#hope", "#charity", "#FSSP", "#ICKSP", "#love", "#catholicyouth", "#catholiclife", "#romancatholic",
        "#VirginMary", "#gladtrad", "#catholicreels", "#orthodoxchurch", "#mercy", "#sacrifice", "#Christ", "#Saint",
        "#Eucharist", "#confession", "#penance", "#repentance", "#protestant", "#reformationday", "#Catholicfaith"
    ]
}

HOOK_ARCHETYPES = [
    ("Fortune Teller", "Frame the hook as a prophecy or revival of forgotten Catholic teaching."),
    ("Experimenter", "Frame the hook as a personal experiment or lived experience."),
    ("Teacher", "Frame the hook as practical, ancient Catholic wisdom for serious spiritual growth."),
    ("Magician", "Frame the hook with mystery, visual awe, and wonder."),
    ("Investigator", "Frame the hook as a secret, hidden pattern, or treasure hunt."),
    ("Contrarian", "Frame the hook as a hot take, flipping common assumptions or debates.")
]

def generate_hook(topic, archetype="Random"):
    client = OpenAI(api_key=OPENAI_API_KEY)
    if archetype == "Random":
        _, archetype_prompt = random.choice(HOOK_ARCHETYPES)
    else:
        archetype_prompt = dict(HOOK_ARCHETYPES)[archetype]
    prompt = f'''Write a single, magnetic, punchy Instagram hook for this topic: "{topic}".
{archetype_prompt}
Style: Short, surprising, not generic or preachy. No hashtags. Never bland.
Return just the hook. Never use 'you', 'your', or 'we'.
'''
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    return response.choices[0].message.content.strip().strip('"').strip("'")

tab1, tab2 = st.tabs(["Main App", "Hook Generator"])

with tab1:
    st.title("✍️ nio.scribe ")

    mode = st.selectbox("Select Output Mode", [
        "Reels/TikTok/Instagram",
        "YouTube Shorts",
        "Twitter/X",
        "Instagram Carousel/Long-Form Caption",
        "Nio Haus Editorial – GPT",
        "Nio Haus Editorial – Claude"
    ])

    account = st.selectbox("Follow Account to Tag", [
        "@dr.rayguarendi", "@yeabut40", "@nio.haus", "@livingbreadradio", "@avemariaradio", "@drmarcuspeter"
    ])

    if mode.startswith("Nio Haus Editorial"):
        seed_idea = st.text_area("🧠 What do you want to write about?")
        if st.button("Generate"):
            if mode == "Nio Haus Editorial – GPT":
                result = refine_caption_with_claude(seed_idea, prompt_mode="nio_haus_gpt")
            else:
                result = refine_caption_with_claude(seed_idea, prompt_mode="nio_haus")
            st.markdown("### 📝 Generated Editorial")
            st.write(result)
    elif mode.startswith("Instagram Carousel"):
        seed_idea = st.text_area("🧠 What do you want to turn into a carousel?")
        if 'carousel_carousels' not in st.session_state:
            st.session_state.carousel_carousels = []
        if st.button("Generate New Carousel"):
            if seed_idea.strip():
                from caption_generator import generate_carousel_slides
                slides_text, suggestions_text = generate_carousel_slides(seed_idea)
                st.session_state.carousel_carousels.append((slides_text, suggestions_text))
            else:
                st.warning("Please enter a seed idea.")
        if st.session_state.carousel_carousels:
            latest_slides, latest_suggestions = st.session_state.carousel_carousels[-1]
            st.markdown("### 🪶 Instagram Carousel Slides")
            st.markdown(latest_slides)
            st.markdown("### 🔮 Viral Topic Suggestions")
            st.markdown(latest_suggestions)
            if len(st.session_state.carousel_carousels) > 1:
                st.markdown("### ⏪ Previous Carousels")
                for slides, suggestions in reversed(st.session_state.carousel_carousels[:-1]):
                    st.markdown("---")
                    st.markdown(slides)
                    st.markdown(suggestions)
        if st.button("Clear Carousels"):
            st.session_state.carousel_carousels = []
    else:
        hashtag_block = st.selectbox(
            "Choose hashtag block",
            list(HASHTAG_BLOCKS.keys()),
            index=0
        )
        video_file = st.file_uploader("Upload a Video", type=["mp4", "mov", "webm"])
        if st.button("Generate"):
            if video_file:
                with open("temp_video.mp4", "wb") as f:
                    f.write(video_file.read())
                result = process_video("temp_video.mp4", account, mode, hashtag_block)
                if isinstance(result, tuple) and len(result) == 3:
                    caption, hashtags, formatted_output = result
                    formatted_hashtags = "\n".join(hashtags.split())
                    formatted_output += f"\n\n{formatted_hashtags}"
                else:
                    formatted_output = result
                st.markdown("### 📝 Caption")
                st.markdown(formatted_output)
            else:
                st.warning("Please upload a video.")

    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; font-size: 1.3em; margin-top: 2em;'>with 🖤 nio haus</div>",
        unsafe_allow_html=True
    )

with tab2:
    st.header("🪝 Hook Generator")
    with st.expander("🕊️ Catholic Hook Archetypes: Viral Content Prompts", expanded=False):
        st.markdown("""
1. **The Fortune Teller**  
   *"This forgotten Catholic teaching is about to reshape the future of the Church."*  
   — *Context: Present vs. Future; tease revival, prophecy, or rediscovery of lost wisdom.*

2. **The Experimenter**  
   *"I tried praying the Liturgy of the Hours every day for 30 days… here's what changed."*  
   — *Peer-to-peer lens; simple, authentic, converts curiosity into lived witness.*

3. **The Teacher**  
   *"If you're serious about growing spiritually, here's the ancient rhythm the saints swore by."*  
   — *Frames spiritual discipline as timeless Catholic wisdom—practical, actionable.*

4. **The Magician**  
   *[Clips of Gregorian chant, incense, kneeling in adoration]*  
   *Voiceover: "What's really happening here? Most Catholics have no idea."*  
   — *Scroll-stopper + mystery; taps into visual awe, sacred unfamiliarity, and wonder.*

5. **The Investigator**  
   *"There's a hidden pattern in Catholic art no one talks about—and it reveals something stunning."*  
   — *Secret exposure vibe; turns tradition and history into a treasure hunt.*

6. **The Contrarian**  
   *"Modern Catholicism isn't too rigid—it's not rigid enough."*  
   — *Opinionated, sparks debate, flips common critiques on their head.*
        """)
    hook_topic = st.text_input("Enter a topic for your hook:", key="hook_topic")
    archetype_options = ["Random"] + [a[0] for a in HOOK_ARCHETYPES]
    selected_archetype = st.selectbox("Choose a hook archetype", archetype_options)
    if st.button("Generate Hook"):
        if hook_topic.strip():
            hook = generate_hook(hook_topic, archetype=selected_archetype)
            st.markdown(f"### Your Hook:\n\n> {hook}")
        else:
            st.warning("Please enter a topic.")
