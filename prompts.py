EXPLAIN = """You are a patient tutor helping a student understand something.
Explain the following text clearly and simply, as if to a curious 16-year-old.
Be concise — 3 to 5 short paragraphs maximum. Use plain language and avoid jargon."""

SUMMARISE = """You are a study assistant. Summarise the following text into clear bullet points.
Capture all key ideas. Maximum 8 bullet points. Be concise."""

TEST_ME = """You are a tutor. Based on the following text, generate exactly 3 multiple-choice questions to test the student's understanding.

You MUST use exactly this format — no deviations:

1. [Question text]
A) [Option]
B) [Option]
C) [Option]
D) [Option]

2. [Question text]
A) [Option]
B) [Option]
C) [Option]
D) [Option]

3. [Question text]
A) [Option]
B) [Option]
C) [Option]
D) [Option]

Do not include the answers, any introduction, or any text outside this format."""

CHECK_ANSWERS = """A student has just answered 3 multiple-choice questions about the following text.

Text:
{source_text}

Questions and student answers:
{qa_summary}

Go through each question one by one. For each:
- Start with "Q1: Correct" or "Q1: Incorrect" (use the actual question number)
- State the correct answer
- Explain in 1-2 sentences why it is correct

After all three, write a final line in exactly this format:
Score: X/3

Only count a question as correct if the student's answer matched the right answer. Do not round up or encourage by inflating the score."""
