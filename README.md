# Gemini API Integration Documentation

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Setting Up Your Gemini API Key](#setting-up-your-gemini-api-key)
- [Usage](#usage)
    - [Extract YouTube Transcripts.](#extract)
    - [Generate AI Assignment](#generate)
    - [Summarize and listen to Note](#summarize)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Buy me coffee](#coffee)

---

## Introduction
This documentation provides a step-by-step guide to integrating and using the 3mtt assignment maker with darey.io to do your assignments and summarize and listen the to the notes. 

By following these instructions, you will be able to set up the API, install the necessary dependencies, and start using.

---

## Installation
Ensure you have Python installed (preferably version 3.8 or higher). Then, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/ndemafiawilsmith/3mtt-assignment-maker.git
   cd 3mtt-assignment-maker
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Setting Up Your Gemini API Key
To use the Script, you need to set up your API key. Follow these steps:

1. Obtain your Gemini API key from [Google AI Studio](https://ai.google.com/studio/gemini).
2. copy the `.env.example` file in the root directory of your project to a `.env` File:
   ```bash
   cp .env.example .env
   ```
3. Open the `.env` file and add your API key:
   ```plaintext
   GEMINI_API_KEY=your_api_key_here
   ```
4. Save the file.

---

## Usage
Once everything is set up, you can start Using the Script.

### Generating Responses
Use the following code snippet to generate responses:

```bash
py .\Assignment.py
```

---

## Performing Operations
That will give you an option to choose what operation you want to perform:
1. [Extract YouTube Transcripts.](#extract)
2. [Generate AI Assignment](#generate)
3. [Summarize and listen to Note](#summarize)

---
## Extract
Extracting YouTube Transcripts
    1. Include all the links to the youtube videos in the `links.json` File in this format below
```bash
        {
            "links": [
                "https://youtu.be/VIDEO_ID_1",
                "https://youtube.com/watch?v=VIDEO_ID_2"
            ]
        }
```
Note: You can put up to 10 links

---

## Generate
Generating AI Assignments
1. Create an assignment.txt file with your assignment prompt.
2. Ensure note.txt exists (from the transcript extraction step).
3. Run the script and choose option 2.
4. Provide the following details when prompted:
- Student Name
- Fellow ID
- Course Name
- Assignment Title

📄 Output: A PDF file named [Assignment_Title].pdf is generated.

---

## summarize
1. Ensure note.txt exists (from the transcript extraction step).

2. Run the script and choose option 3.

3. Type y and press enter if you want the summary to be read aloud.

📝 Output: A summary is saved in summary.txt, and audio playback is available if selected.


---

## Troubleshooting
If you encounter issues, check the following:
- Ensure your `.env` file contains the correct API key.
- Verify you have installed all dependencies (`pip install -r requirements.txt`).
- Check your internet connection and API usage limits.

---

## Contributing
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Added new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.


---

## Coffee
To Buy me Coffe my details a below
- Account Number: 0150299261
- Bank: Union Bank
- Name: Abwa Ndemafia Wilsmith
