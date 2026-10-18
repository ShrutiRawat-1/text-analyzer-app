# Text Analyzer

This is a basic Flask web application for analysing text with the Gemini API.
Registered users can do analyses on the entered text and every result is saved to a personal history page.

## Features

- **User authentication:** signup and login with hashed passwords and session-based access
- **Named entity recognition:** entities grouped by type
- **Sentiment analysis:** classifies text as Positive, Negative or Neutral
- **Language detection:** identifies the language of the text
- **Analysis history:** each user sees only their own past results
- **Protected pages:** the analysis and history pages require a login
- **Error handling:** a user friendly message is shown if the Gemini API call fails
- **UI:** built with Bootstrap 5 templates

## Tech Stack

- Python 3
- Flask and Flask-WTF (routing, templates, form validation, CSRF protection)
- SQLite (users and history)
- Gemini API (text analysis)
- Bootstrap 5 (styling)


## Project Structure

```
.
├── app.py              # Flask routes
├── api.py              # Gemini API calls
├── db.py               # SQLite: users and history
├── forms.py            # Signup, login and text forms
├── config.py           # API key and secret key 
├── requirements.txt
└── templates/
    ├── layout.html
    ├── navbar.html
    ├── signup.html
    ├── login.html
    ├── profile.html
    ├── ner.html
    ├── sentiment.html
    ├── language.html
    └── history.html
```

## Working

1. The user signs up and the password is hashed with Werkzeug before it is stored.
2. During login the typed password is checked against the stored hash and the user's email is saved in the Flask session.
3. Each protected route checks the session and redirects to the login page if it is missing.
4. A analysis feature route sends the text to `api.py`, which  inturn prompts Gemini and returns the result.
5. The result is shown on the page and saved to the history table that is linked to the user's email.

