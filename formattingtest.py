import streamlit as st

# Apply dark mode styling
st.markdown(
    """
    <style>
    .reportview-container {
        background: #2E2E2E;
        color: white;
    }
    .sidebar .sidebar-content {
        background: #2E2E2E;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Initialize the session state
if 'page' not in st.session_state:
    st.session_state.page = 1

# Define the content for each page
def page1():
    st.write("This is Page 1")
    st.write("hello")
    if st.button("Next Page"):
        st.session_state.page += 1

def page2():
    st.write("This is Page 2")
    st.write("meow")
    if st.button("Next Page"):
        st.session_state.page += 1

def page3():
    st.write("This is Page 3")
    st.write("meep")
    if st.button("Previous Page"):
        st.session_state.page -= 1

# Display the appropriate page based on the session state
if st.session_state.page == 1:
    page1()
elif st.session_state.page == 2:
    page2()
elif st.session_state.page == 3:
    page3()

# Add navigation links to jump directly to pages
st.markdown("---")
if st.button("Go to Page 1"):
    st.session_state.page = 1
if st.button("Go to Page 2"):
    st.session_state.page = 2
if st.button("Go to Page 3"):
    st.session_state.page = 3


st.markdown("*Streamlit* is **really** ***cool***.")
st.markdown('''
    :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
    :gray[pretty] :rainbow[colors] and :blue-background[highlight] text.''')
st.markdown("Here's a bouquet &mdash;\
            :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")

multi = '''If you end a line with two spaces,
a soft return is used for the next line.

Two (or more) newline characters in a row will result in a hard return.
'''
st.markdown(multi)


import streamlit.components.v1 as components

# Function to create a tooltip
def tooltip(text, tooltip_text):
    return f'<span style="position: relative; cursor: pointer;">{text}<span style="visibility: hidden; background-color: black; color: #fff; text-align: center; border-radius: 6px; padding: 5px; position: absolute; z-index: 1; bottom: 125%; left: 50%; margin-left: -60px; width: 120px;">{tooltip_text}</span></span>'

# JavaScript to show/hide the tooltip
tooltip_js = """
<script>
    const tooltips = document.querySelectorAll('span[style*="position: relative"]');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseover', () => {
            const tooltipText = tooltip.querySelector('span[style*="visibility: hidden"]');
            tooltipText.style.visibility = 'visible';
        });
        tooltip.addEventListener('mouseout', () => {
            const tooltipText = tooltip.querySelector('span[style*="visibility: hidden"]');
            tooltipText.style.visibility = 'hidden';
        });
    });
</script>
"""

# Example usage of the tooltip function
tooltip_html = tooltip("Streamlit", "An awesome app framework")
components.html(tooltip_html + tooltip_js, height=30)
