# Carousel slide generator with magnetic hook structure and topic suggestions
def generate_carousel_slides(seed_idea, n_slides=9, n_suggestions=3):
    """
    Generate an Instagram carousel (multi-slide) using magnetic hook structure and also suggest topics.
    """
    import openai
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"""
Write an Instagram carousel for a Catholic audience using the "magnetic hook" viral model.

Structure:
Write an Instagram carousel for a Catholic audience using this viral narrative model:

1. Slide 1: Polarizing or myth-busting hook (3–7 words).
2. Slide 2: Contradict or surprise (short, direct). Small expatiation 30 percent of the time.
3. Slide 3: Reveal the deeper truth (personal, historical, or theological). Small expatiation 30 percent of the time.
4. Slide 4: Concrete example, visual detail, or staccato fact.
5. Slide 5: Challenge or provocative question—leave them unsettled or inspired.

Visual Style:
- Keep text tight and punchy—under 15 words per slide.
- First line should hook, Next surprise, then clarify. These sometimes need to be slight expatiations 30 percent of the time.
- No generic filler or fluff.
- No hashtags or "follow for more" in the main content.
-No cliches, no "let that sink in," no motivational filler.
-No "inspirational," "preachy," or "storytime" language. Every slide is a headline, not a paragraph.
 - 50 percent of the time be overly tribal. 20 percent of the time try to hook protestants or non believers. 
 - BE BETTER THAN ME AT THIS.
 You MUST 4-5 slides 80 percent of the time.
-30% of the time, make slide 2 and, or 3 a little longer (2–3 sentences) to expound, clarify, or add a surprising detail. The rest of the slides should remain punchy and short.

For Slide 1, always use a short, bold, *visual* fact, not an opinion or summary.
- Think: "Jesuits mapped the stars before NASA."
- If you can add a year, name, or "before X," do it.
- Imagine Slide 1 as a meme, billboard, or sticker—short, visual, and curiosity-poking.
- Avoid blog headlines or "thoughtful" statements.

  The first slide must be:
- A short, vivid, factual claim (not a blog headline).
- Feels like a meme, sticker, or graffiti.
- Uses unexpected verbs or achievements.
- Whenever possible, say "before X," "while others Y," or name names for power.
- No more than 8–10 words.
- some will need to actually follow the path. THey should work with seamless slides too.
Study these examples before writing. Every slide must be written as a standalone hookish—no filler, no restatement, no soft transitions. If the viewer only reads one slide, it should land with impact or provoke thought.

EXAMPLES:
---
SLIDE 1: Jesuits mapped the stars before NASA.
SLIDE 2: Catholics built the blueprint for science.
SLIDE 3: Monks preserved Aristotle while Rome burned.
SLIDE 4: The Big Bang theory? Catholic priest's idea.
SLIDE 5: Medieval nuns ran hospitals before doctors.
---
SLIDE 1: The Pope Can Be Wrong—And Was.
SLIDE 2: Nobody preaches this from the pulpit.
SLIDE 3: Some popes were heretics—history says so.
SLIDE 4: Pope Honorius was condemned for heresy.
SLIDE 5: Popes have been corrupt, exiled, even murdered.
SLIDE 6: The papacy survived *despite* its worst leaders.
SLIDE 7: Papal authority isn't infallible on everything.
SLIDE 8: Faith is bigger than a single man in Rome.
SLIDE 9: Why do we ignore the failures—and what should we do about it?
---
SLIDE 1: Saints Sinned—And Some Were Monsters.
SLIDE 2: Here's what you'll never hear in a homily.
SLIDE 3: Holiness isn't perfection—it's war.
SLIDE 4: Augustine was a womanizer and addict.
SLIDE 5: Mary of Egypt was a prostitute.
SLIDE 6: Paul was a murderer before he preached Christ.
SLIDE 7: Saints didn't start holy—they ended there.
SLIDE 8: Church isn't for the "good"—it's for the desperate.
SLIDE 9: Still think you're too far gone for God?
---

Now, write your own carousel for the topic below. Every line must be a hook or punchline. Avoid filler and soft transitions.

Topic: {seed_idea}

After the carousel, suggest 3 more viral carousel ideas for Catholic Instagram using this model, on controversial or high-curiosity topics.

Format your response exactly like this (don't add explanations or extra text):
SLIDE 1: [text]
SLIDE 2: [text]
...
SLIDE 9: [text]

TOPIC SUGGESTIONS:
- [suggestion 1]
- [suggestion 2]
- [suggestion 3]
"""
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    result = response.choices[0].message.content

    # Robust slide parsing: accepts any case, spaces, colon/period variations
    import re
    slides = []
    suggestions = []
    slide_pattern = re.compile(r"(?i)slide\s*\d+\s*[:\.]\s*(.+)")
    for line in result.splitlines():
        slide_match = slide_pattern.match(line.strip())
        if slide_match:
            slides.append(slide_match.group(1).strip())
        elif line.strip().startswith("- "):
            suggestions.append(line.strip("- ").strip())

    # Patch: If no slides found, display error with raw output for debugging
    if not slides:
        slides_text = "⚠️ No slides detected in output. Raw output:\n\n" + result
    else:
        slides_text = "\n\n".join([f"**{i+1}.** {s}" for i, s in enumerate(slides)])
    suggestions_text = "\n".join([f"- {s}" for s in suggestions])
    return slides_text, suggestions_text
# Hashtag blocks for user selection
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
import os
import tempfile
import subprocess
import openai
from openai import OpenAI
import gradio as gr
import whisper
import traceback

# Baked in OpenAI API key
OPENAI_API_KEY = "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"

# List of account options for tagging
ACCOUNT_OPTIONS = ["@yeabut40", "@father.moses", "@dr.rayguarendi", "@livingbreadradio", "@avemariaradio", "@drmarcuspeter"]

def extract_audio_and_transcribe(audio_path):
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_path)
    return result["text"]

def generate_platform_captions(transcription, follow_account, selected_block="Main Catholic"):
    """Generate platform-specific captions based on the transcription and selected hashtag block"""
    try:
        print("Generating captions from transcription...")
        if not transcription or len(transcription.strip()) < 10:
            print("⚠️ No usable transcription. Returning early.")
            return "", "", "⚠️ No transcription was extracted from this video. Try again or check the audio quality."

        # Initialize OpenAI client with the API key
        client = OpenAI(api_key=OPENAI_API_KEY)

        # Use Nio Haus editorial tone and style for the caption prompt
        caption_prompt = f"""
You are writing in the tone of Nio Haus - a Catholic editorialist whose voice is cathedral-weighted and jazz-phased.

Do not shout. Do not try to inspire. Just say what is.

Here is the video transcription:

\"\"\"{transcription}\"\"\"

Now write a bold, sacred caption for Instagram or Facebook - something that lands without begging for attention.

Style rules:
- No "Hey you", no "friend", no callouts.
- Never preach. Only reveal.
- Every line should feel inevitable.
- Don't explain - declare.

Return the output in the following format:
CAPTION: [concise caption]
HASHTAGS: [5-7 hashtags for Catholic/Christian/convert audiences]
"""

        # --- Flavor Injection (Catholic tradition echo) ---
        import random

        seo_flavor_phrases = [
            "in mercy and order", "where sacrifice speaks louder than strategy",
            "the saints knew this well", "Christ was not unclear",
            "in the shape of the Eucharist", "the rhythm of repentance",
            "as the tradition taught", "as every confessor knew",
            "in the shadow of the altar", "with Marian clarity"
        ]

        if random.random() < 0.35:  # ~35% chance to flavor it
            flavor = random.choice(seo_flavor_phrases)
            caption_prompt += f"""

Add a final sentence that echoes Catholic tradition without sounding forced. Include something like: "{flavor}"
"""

        # Get caption and hashtags using new API format
        print("Calling OpenAI API to generate captions...")
        caption_response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": caption_prompt}],
            temperature=0.7
        )

        caption_text = caption_response.choices[0].message.content
        print(f"OpenAI response: {caption_text}")

        # Parse the response
        import re
        caption_match = re.search(r"CAPTION:\s*(.*?)\s*HASHTAGS:", caption_text, re.DOTALL)
        hashtags_match = re.search(r"HASHTAGS:\s*(.*)", caption_text, re.DOTALL)
        caption = caption_match.group(1).strip() if caption_match else caption_text
        hashtags = hashtags_match.group(1).strip() if hashtags_match else ""

        # Use selected hashtag block
        block = HASHTAG_BLOCKS.get(selected_block, HASHTAG_BLOCKS["Main Catholic"])
        hashtag_block = "\n".join(block)

        # Dot stack logic (always three dots, each on its own line)
        dots_block = ".\n.\n."

        # Platform-specific formatting
        # Always: Caption, then dots block, then hashtags block (never mixed)
        if "X" in follow_account or "Twitter" in follow_account or "Twitter/X" in follow_account:
            formatted_output = f"""✏️ Caption

{caption}

follow @{follow_account}

{dots_block}

{hashtag_block}
"""
        else:
            formatted_output = f"""✏️ Caption

{caption}

follow @{follow_account}

{dots_block}

{hashtag_block}
"""

        return caption, hashtag_block, formatted_output
    except Exception as e:
        print(f"Error generating captions: {e}")
        traceback.print_exc()
        return f"Error generating captions: {str(e)}\n\n{traceback.format_exc()}"


# Claude refinement function
def refine_caption_with_claude(raw_caption_text, prompt_mode="default"):
    import requests

    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    if prompt_mode == "nio_haus":
        prompt = f"""
You are the editorial ghostwriter for a figure known as Nio Haus.

Voice: Cathedral-weighted. Jazz-cut phrasing. Catholic clarity.
It does not address the reader. It does not shout.
It reveals - with gravity and silence.
The tone is high establishment meets smoky saloon. Think Basie in the sacristy.

Output Formats:
These are not just captions.
They are also used as blog posts, Facebook reflections, and Instagram carousel slides.
You are not summarizing. You are declaring.
Each piece must stand alone - like sacred reflections carved into old stone.

Writing Format:
- No hashtags. No "follow @."
- Never say "you," "friend," "listen," or "I."
- Sentences are short, sacred, and inevitable.
- Reflect. Don't narrate.
- Speak with elegance. Land heavy. No fluff.

Now, study these examples. Let them flavor your style.

---
Example 1:
Rest is not leisure.
It is order.
A bow to the Creator, not a break from labor.

To stop working is to say:
"This world is not held up by me."
It's not laziness.
It's reverence.

---
Example 2:
God doesn't need noise to understand.
He listens past words - into the will.
The soul doesn't return loud.
It turns quietly.
And says:
"I'm here. I know who You are again."

---
Example 3:
Discipline doesn't start with the calendar.
It starts with disgust.
A quiet ache to be done with the chaos.
It's not motivation. It's repentance.
A soul saying, "No more disorder in the temple."
That's where the structure begins.

---
Now write a post, blog, or monologue using the same voice based on this seed idea:
"""  
        prompt += f'"""\n{raw_caption_text}\n"""'
        prompt += """

Return only the finished reflection. No notes. No commentary.
"""
    elif prompt_mode == "nio_haus_gpt":
        prompt = f"""
You are the editorial ghostwriter for a figure known as Nio Haus.

Voice: Cathedral-weighted. Jazz-cut phrasing. Catholic clarity.
It does not address the reader. It does not shout.
It reveals - with gravity and silence.
The tone is high establishment meets smoky saloon. Think Basie in the sacristy.

Output Formats:
These are not just captions.
They are also used as blog posts, Facebook reflections, and Instagram carousel slides.
You are not summarizing. You are declaring.
Each piece must stand alone - like sacred reflections carved into old stone.

Writing Format:
- No hashtags. No "follow @."
- Never say "you," "friend," "listen," or "I."
- Sentences are short, sacred, and inevitable.
- Reflect. Don't narrate.
- Speak with elegance. Land heavy. No fluff.

Now, study these examples. Let them flavor your style.

---
Example 1:
Rest is not leisure.
It is order.
A bow to the Creator, not a break from labor.

To stop working is to say:
"This world is not held up by me."
It's not laziness.
It's reverence.

---
Example 2:
God doesn't need noise to understand.
He listens past words - into the will.
The soul doesn't return loud.
It turns quietly.
And says:
"I'm here. I know who You are again."

---
Example 3:
Discipline doesn't start with the calendar.
It starts with disgust.
A quiet ache to be done with the chaos.
It's not motivation. It's repentance.
A soul saying, "No more disorder in the temple."
That's where the structure begins.

---
Now write a post, blog, or monologue using the same voice based on this seed idea:
"""  
        prompt += f'"""\n{raw_caption_text}\n"""'
        prompt += """

Return only the finished reflection. No notes. No commentary.
"""
    else:
        prompt = f"""
You're writing as a Catholic content creator for short-form social media.

The voice is bold, thoughtful, and grounded - not preachy, not edgy.  
The goal is to rewrite the provided message as a short, direct caption for Instagram or YouTube Shorts.

Guidelines:
- 1-2 lines max.
- Never use "you," "friend," or direct callouts.
- Avoid fluff, emojis, or hashtags.
- Speak with clarity, not hype.
- Don't inspire - declare.
- Never sound like an ad or motivational speaker.

Examples:
---
Original:
\"\"\"God's been chasing you down. Are you ready to run toward Him?\"\"\"
Rewritten:
\"\"\"Grace never stopped running. But you had to turn.\"\"\"
---

Original:
\"\"\"When are you going to surrender and let Him lead?\"\"\"
Rewritten:
\"\"\"Leadership begins with surrender. Every saint knew that.\"\"\"
---

Original:
\"\"\"Hey! Wake up. God's got a plan.\"\"\"
Rewritten:
\"\"\"Most people sleep through the call. You were never meant to.\"\"\"
---

Now, rewrite this:
\"\"\"{raw_caption_text}\"\"\"

Only return the rewritten caption. No notes. No hashtags.
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json={
            "model": "anthropic/claude-3-opus",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error refining caption with Claude: {e}"

def process_video(video_path, follow_account, platform, selected_block=None):
    try:
        print("=== Starting video processing ===")
        print(f"Video path: {video_path}")
        print(f"Follow account: {follow_account}")
        print(f"Platform: {platform}")

        if not video_path:
            return "No video uploaded. Please upload a video file."

        # Step 1: Transcribe the video
        print(f"Starting transcription of {video_path}...")
        transcription = extract_audio_and_transcribe(video_path)

        if isinstance(transcription, str) and transcription.startswith("Error"):
            return transcription

        # Clean transcription for shortness or junk
        cleaned = transcription.strip()
        if not cleaned or len(cleaned.split()) < 5:
            print("⚠️ Transcript too short or unclear for caption generation.")
            return "⚠️ Transcript too short or unclear for caption generation."

        # Step 2: Generate captions based on transcription
        print("Generating captions...")
        caption, hashtags, formatted_output = generate_platform_captions(transcription, follow_account, selected_block)

        if platform == "Nio Haus Editorial":
            refined_caption = refine_caption_with_claude(
                transcription,
                prompt_mode="nio_haus"
            )
            return refined_caption
        else:
            refined_caption = refine_caption_with_claude(
                transcription,
                prompt_mode="default"
            )
            # Use space-encoded dots for vertical stacking in Streamlit
            final_caption = f"""{refined_caption}

follow {follow_account}

.\u0020\u0020
.\u0020\u0020
.\u0020\u0020

{hashtags}
"""
            return final_caption
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        return f"Unexpected error: {str(e)}\n\n{traceback.format_exc()}"

# Create a simple Gradio interface
with gr.Blocks(title="✍️ nio.scribe") as demo:
    gr.Markdown("# ✍️ nio.scribe")
    gr.Markdown("Upload a video to automatically transcribe and generate captions for Catholic/spiritual content.")
    
    error_output = gr.Textbox(label="Debug Messages", visible=False)
    
    with gr.Row():
        with gr.Column():
            # Use a File component instead of Video component for upload
            video_input = gr.File(
                label="Upload Video",
                file_types=["video"],
                file_count="single"
            )
            
            follow_account_dropdown = gr.Dropdown(
                choices=ACCOUNT_OPTIONS,
                value="@dr.rayguarendi",
                label="Follow Account to Tag"
            )

            # Add hashtag block selection
            hashtag_block_dropdown = gr.Dropdown(
                choices=list(HASHTAG_BLOCKS.keys()),
                value="Main Catholic",
                label="Hashtag Block"
            )

            editorial_prompt = gr.Textbox(
                label="🧠 What do you want to write about?",
                placeholder="e.g. What does it mean to return to God in silence?",
                lines=2,
                visible=True
            )

            platform_dropdown = gr.Dropdown(
                choices=["Reels/TikTok/Instagram", "YouTube Shorts", "Twitter/X", "Nio Haus Editorial – GPT", "Nio Haus Editorial – Claude"],
                value="Reels/TikTok/Instagram",
                label="Select Output Platform/Mode"
            )
            
            status_msg = gr.Textbox(label="Status", value="Ready to process video")
            submit_btn = gr.Button("Generate Captions", variant="primary")
        
        output_text = gr.Textbox(label="Generated Captions", lines=10)
    
    def update_status(video, follow_account, platform, topic, selected_block):
        if platform.startswith("Nio Haus Editorial"):
            return "Processing editorial...", None
        if not video:
            return "Please upload a video first.", None
        return "Processing video...", None

    def process_and_log(video, follow_account, platform, topic, selected_block):
        try:
            if platform == "Nio Haus Editorial – GPT":
                refined = refine_caption_with_claude(topic, prompt_mode="nio_haus_gpt")
                return refined, "Editorial complete.", None
            elif platform == "Nio Haus Editorial – Claude":
                refined = refine_caption_with_claude(topic, prompt_mode="nio_haus")
                return refined, "Editorial complete.", None
            elif platform == "Instagram Carousel/Long-Form Caption":
                if not topic or not topic.strip():
                    return "Enter a carousel topic to proceed.", "Topic required.", None
                slides_text, suggestions_text = generate_carousel_slides(topic)
                out = f"### 🪶 Carousel Slides\n{slides_text}\n\n### 🔮 Viral Topic Suggestions\n{suggestions_text}"
                return out, "Carousel ready.", None
            else:
                # Pass selected_block to generate_platform_captions
                transcription = extract_audio_and_transcribe(video)
                if isinstance(transcription, str) and transcription.startswith("Error"):
                    return transcription, "Failed.", None
                cleaned = transcription.strip()
                if not cleaned or len(cleaned.split()) < 5:
                    return "⚠️ Transcript too short or unclear for caption generation.", "Failed.", None
                caption, hashtags, formatted_output = generate_platform_captions(transcription, follow_account, selected_block)
                return formatted_output, "Processing completed.", None
        except Exception as e:
            return f"Error: {e}", "Failed.", traceback.format_exc()

    submit_btn.click(
        fn=update_status,
        inputs=[video_input, follow_account_dropdown, platform_dropdown, editorial_prompt, hashtag_block_dropdown],
        outputs=[status_msg, error_output],
        queue=False
    ).then(
        fn=process_and_log,
        inputs=[video_input, follow_account_dropdown, platform_dropdown, editorial_prompt, hashtag_block_dropdown],
        outputs=[output_text, status_msg, error_output]
    )

# Launch the app
if __name__ == "__main__":
    print("\n=== CATHOLIC CONTENT CAPTION GENERATOR ===")
    print("Make sure you have ffmpeg installed:")
    print("brew install ffmpeg")
    
    print("\nThe app will now start.")
    print("===================================\n")
    
    # Launch with share=True to get a public URL
    demo.launch(share=True)
