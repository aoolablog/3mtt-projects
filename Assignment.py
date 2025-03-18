import os
import sys
import json
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from google import genai
from google.genai import types
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from fpdf import FPDF
from dotenv import load_dotenv
import pyttsx3  # Text-to-Speech

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


# If API_KEY is missing, prompt the user
if not API_KEY:
    API_KEY = input("Enter your Google Gemini API Key: ").strip()
    os.environ["GEMINI_API_KEY"] = API_KEY  # Temporarily set for this session

# Initialize Gemini AI client
client = genai.Client(api_key=API_KEY)

# --- Function to Extract Lyrics from YouTube ---
def extract_lyrics(video_url):
    """Extracts lyrics/transcript from a YouTube video."""
    try:
        video_id_match = re.search(r"(?:v=|youtu.be/)([a-zA-Z0-9_-]+)", video_url)
        if not video_id_match:
            return None, "Invalid YouTube URL. Ensure it contains a valid video ID."

        video_id = video_id_match.group(1)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        lyrics = "\n".join([entry["text"] for entry in transcript])
        return lyrics, None
    except TranscriptsDisabled:
        return None, "Transcripts are disabled for this video."
    except NoTranscriptFound:
        return None, "No transcript found for this video."
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

# --- Function to Process YouTube Links from JSON ---
def process_links(json_file, output_file):
    """Reads YouTube links from a JSON file, extracts lyrics, and saves them to a text file."""
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            video_links = data.get("links", [])

            if not video_links:
                print("No links found in JSON file.")
                return

        with open(output_file, "w", encoding="utf-8") as output:
            for index, link in enumerate(video_links, start=1):
                lyrics, error = extract_lyrics(link)
                output.write(f"Video {index}: {link}\n")
                output.write("=" * 80 + "\n")

                if lyrics:
                    output.write(lyrics + "\n\n")
                else:
                    output.write(f"Error: {error}\n\n")

                output.write("-" * 80 + "\n\n")
                print(f"Processed {index}/{len(video_links)}: {link}")

        print(f"All lyrics have been saved to {output_file}")
    except FileNotFoundError:
        print(f"Error: The file '{json_file}' was not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in the file.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

# --- Function to Generate Assignment using AI ---
def generate_assignment():
    """Generates an assignment based on user input and saves it as a PDF."""
    name = input("Enter your Name: ")
    fellow_id = input("Enter your Fellow ID: ")
    course = input("Enter your Course Name: ")
    assignment_title = input("Enter the Assignment Title: ")

    # Check if required files exist
    assignment_file = "assignment.txt"
    notes_file = "note.txt"

    if not os.path.exists(assignment_file):
        print(f"❌ Error: '{assignment_file}' not found.\nMake sure you have an assignment.txt file in this directory with your assignment prompt.")
        sys.exit(1)  # Stop execution

    if not os.path.exists(notes_file):
        print(f"❌ Error: '{notes_file}' not found.\nMake sure you have generated transcripts first using the script's option 1.")
        sys.exit(1)  # Stop execution

    # Read the files
    with open(assignment_file, "r", encoding="utf-8") as file:
        assignment_prompt = file.read()

    with open(notes_file, "r", encoding="utf-8") as file:
        notes = file.read()

    # AI Prompt
    prompt = f"""
    You are an academic writer. Generate a **detailed, well-researched, and human-like written assignment** based on the following information.

    ### Assignment Details:
    - **Student Name:** {name}
    - **Fellow ID:** {fellow_id}
    - **Course Name:** {course}
    - **Assignment Title:** {assignment_title}

    ### Assignment Instructions:
    1. Do NOT return instructions. Write the assignment as if a human student completed it.
    2. The writing should be **coherent, natural, and well-structured**.
    3. The content should be **original, professional, and free of plagiarism**.
    4. Format it in a **formal academic style** with clear sections (Introduction, Body, Conclusion).
    5. **Use information from the provided notes.**
    6. Do NOT add Markdown formatting like `##`, `**`, etc. The text should be clear for PDF conversion.

    ### Assignment Prompt:
    {assignment_prompt}

    ### Notes:
    {notes}

    Now, **write the full assignment** as if it was completed by a student.
    """

    # Generate AI response
    response = client.models.generate_content(model="gemini-2.0-flash-exp", contents=[prompt])
    assignment_text = response.text  # Extract AI-generated text

    # PDF Class
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 14)
            self.set_text_color(0, 0, 139)
            self.cell(200, 10, "Assignment Document", ln=True, align="C")
            self.ln(10)

        def chapter_body(self, body):
            self.set_font("Arial", "", 11)
            self.set_text_color(0, 0, 0)
            self.multi_cell(0, 8, body)
            self.ln(5)

    # Create PDF
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Add Assignment Content
    pdf.chapter_body(assignment_text)

    # Save PDF
    pdf_file = f"{assignment_title.replace(' ', '_')}.pdf"
    pdf.output(pdf_file)

    print(f"✅ PDF Assignment saved as: {pdf_file}")

def summarize():
    """Summarizes the content of note.txt, saves it, and offers to read it aloud."""

    # Read notes
    try:
        with open("note.txt", "r", encoding="utf-8") as file:
            notes = file.read()

        if not notes.strip():
            print("Error: The note.txt file is empty.")
            return

    except FileNotFoundError:
        print("Error: The file 'note.txt' was not found.")
        return
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return

    # AI Prompt
    prompt = f"""
    You are an expert summarizer. Your task is to read the given notes and create a **concise, well-structured summary** that retains the key points and important details.

    ### **Instructions for the Summary**:
    - Keep it **concise and to the point**, while ensuring completeness.
    - Highlight the **main ideas, key facts, and relevant information**.
    - Maintain **clarity and coherence** so that the summary is easily understandable.
    - Avoid unnecessary details, filler words, or redundant explanations.
    - If the notes contain **technical or academic content**, ensure that the summary preserves the essential concepts.

    ### **Notes to Summarize**:
    {notes}

    Now, summarize the notes professionally.
    """

    # Generate AI response
    response = client.models.generate_content(model="gemini-2.0-flash-exp", contents=[prompt])
    summary_text = response.text.strip()  # Extract AI-generated summary

    # Print the summary
    print("\n🔹 **Summary of Notes:**")
    print(summary_text)

    # Save summary to file
    summary_file_path = "summary.txt"
    with open(summary_file_path, "w", encoding="utf-8") as summary_file:
        summary_file.write(summary_text)
    
    print(f"\n✅ Summary has been saved to {summary_file_path}")

    # Ask user if they want to hear the summary
    read_aloud = input("\n🔊 Do you want the summary to be read aloud? (yes/no): ").strip().lower()
    
    if read_aloud in ["yes", "y"]:
        try:
            engine = pyttsx3.init()
            engine.say(summary_text)
            engine.runAndWait()
            print("📢 Reading the summary aloud...")
        except Exception as e:
            print(f"Error with text-to-speech: {str(e)}")



# --- Main Program ---
if __name__ == "__main__":
    print("1. Extract YouTube Transcripts")
    print("2. Generate AI Assignment")
    print("3. Summarize and listen to Note")
    choice = input("Select an option (1,2 or 3): ")

    if choice == "1":
        json_filename = "links.json"
        output_filename = "note.txt"
        process_links(json_filename, output_filename)
    elif choice == "2":
        generate_assignment()
    elif choice == "3":
        print("Summarize")
        summarize()
    else:
        print("Invalid option. Please restart and choose 1 or 2.")
