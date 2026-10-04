# ProjectPulse AI

A simple tool that checks if your software idea is worth building.

Type in your app idea, and it:
- Finds the top 10 most popular similar projects on GitHub
- Uses Google Gemini AI to write a short report on your competition, tech stack, and how to stand out

🔗 **Try it live:** https://project-validator-sqkxpke4sfy57aqeyyzmsf.streamlit.app/

(If the app is asleep, give it a few seconds to wake up.)

## Built with
Python, Streamlit, GitHub API, Google Gemini

## Run it yourself

1. Install the requirements:
```
   pip install -r requirements.txt
```
2. Create a `.env` file with your keys:
```
   GEMINI_API_KEY=your_key_here
   GITHUB_TOKEN=your_token_here
```
3. Start the app:
```
   streamlit run webapp.py
```

## Note
The results are a quick snapshot based on GitHub keyword matches and AI analysis. Use them as a starting point, not a final answer.
