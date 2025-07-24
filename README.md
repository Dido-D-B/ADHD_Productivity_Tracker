


# ADHD Productivity Tracker

This is a privacy-respecting productivity tracking app built with Streamlit and Supabase. The goal is to help individuals with ADHD better understand their productivity patterns and improve focus over time.

## Features

- Secure login system using `streamlit-authenticator` with hashed passwords
- Personal dashboard for visualizing recent productivity logs
- Simple input form to log daily focus and productivity level
- Cloud-hosted PostgreSQL database via Supabase
- Secrets and credentials safely managed via `.streamlit/secrets.toml` (excluded from GitHub)

## Tech Stack

- Python 3.12
- Streamlit
- Supabase (PostgreSQL + REST API)
- `streamlit-authenticator`
- `sqlalchemy`, `pandas`, `matplotlib`

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/your-username/ADHD_tracker.git
cd ADHD_tracker
```

2. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a file at `.streamlit/secrets.toml` and add your Supabase keys and login credentials:

```toml
[supabase]
url = "https://your-supabase-url.supabase.co"
key = "your-supabase-api-key"

[credentials]
usernames = { yourusername = {email = "you@example.com", name = "Your Name", password = "hashed_password_here"} }
```

> Use `streamlit_authenticator.Hasher` to generate hashed passwords in a secure way.

5. Run the app:

```bash
streamlit run app.py
```

## Future Plans

- Add optional tags and notes to each log entry
- Train ML models after enough data is collected to find productivity trends
- Allow export of user data
- Add dark mode and improved UI/UX

## GitHub Safety

This repo excludes sensitive files like:

`.streamlit/secrets.toml`


## Contact

For questions, ideas, or feedback, feel free to open an issue or reach out: [Dido De Boodt](https://www.linkedin.com/in/dido-de-boodt/)