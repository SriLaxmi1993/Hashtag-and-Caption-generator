import streamlit as st
import cohere

# Initialize Cohere client with a placeholder key
co = cohere.Client('placeholder-key')

def generate_social_media_content(keyword, description, creativity):
    """
    Generate hashtags and a caption for a social media post given a keyword and description.
    Arguments:
    keyword(str): the main word related to the post
    description(str): a brief description of the post
    creativity(float): the Generate model `temperature` value
    Returns:
    hashtags(str), caption(str): the generated hashtags and caption for the post
    """
    prompt = f"""Given a keyword and a brief description, generate hashtags and a short caption for a social media post.

Keyword: {keyword}
Description: {description}
Hashtags:"""

    # Generate hashtags
    hashtags_response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=30,
        temperature=creativity,
        stop_sequences=["\n"],
    )
    hashtags = hashtags_response.generations[0].text.strip()

    caption_prompt = f"""Given the following keyword and description, create a compelling caption for a social media post.

Keyword: {keyword}
Description: {description}
Caption:"""

    # Generate caption
    caption_response = co.generate(
        model="command",
        prompt=caption_prompt,
        max_tokens=100,
        temperature=creativity,
        stop_sequences=["\n"],
    )
    caption = caption_response.generations[0].text.strip()

    return hashtags, caption

# Frontend: Title and API Key Input
st.title("🌟 Social Media Content Generator")
api_key = st.text_input("Enter your Cohere API key", type="password")

if api_key:
    # Update the Cohere client with the actual API key
    co = cohere.Client(api_key)
    st.success("API Key accepted!")

# Input form for generating content
form = st.form(key="social_media_content_form")
with form:
    keyword_input = st.text_input("Keyword")
    description_input = st.text_area("Post Description")

    creativity_input = st.slider(
        "Creativity",
        value=0.5,
        min_value=0.1,
        max_value=1.0,
        help="Adjust the creativity level. Higher values may produce more unique content."
    )

    generate_button = form.form_submit_button("Generate Content")

if generate_button:
    if not keyword_input or not description_input:
        st.error("Please fill in both the keyword and description fields.")
    else:
        hashtags, caption = generate_social_media_content(keyword_input, description_input, creativity_input)
        st.subheader("Generated Hashtags")
        st.write(hashtags)
        st.subheader("Generated Caption")
        st.write(caption)
