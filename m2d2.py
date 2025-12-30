import os
import re
# from langchain_groq import ChatGroq
from dotenv import load_dotenv
import anthropic

load_dotenv()

def export(code: str) -> None:
  print(f"Exporting...\n\n{code}")

  tmpl = """
  <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <script src="https://unpkg.com/@strudel/embed@latest"></script>
      <title>Strudel REPL</title>
    </head>
    <body>
      <strudel-repl>
        <!-- {strudel_code} -->
      </strudel-repl>
    </body>
  </html>
  """

  with open("output.html", "w") as f:
    f.write(tmpl.format(strudel_code=code))


llm = anthropic.Anthropic(
  api_key=os.getenv("ANTHROPIC_API_KEY")
)


SYSTEM_PROMPT = """
You are an expert in Strudel REPL (https://strudel.cc/) and JavaScript-based live coding for algorithmic music.
Your task is to generate valid Strudel code that can run directly in the Strudel environment.

Instructions:
- The code must be syntactically correct and JavaScript-compatible for Strudel.
- The code must fulfill the musical or rhythmic intent described in the user query.
- Include brief, high-quality explanations as inline code comments describing key patterns or functions.
- Output only the code block — no extra text, markdown, or prose.

{shots}

User Query:
{query}
"""

shots = """
  Here you have some examples of Strudel REPL code for different musical patterns:
  <example>
    input: "Create a simple drum pattern."
    output:
      ```javascript
        // bd = bass drum
        // sd = snare drum
        // rim = rimshot
        // hh = hihat
        // oh = open hihat
        // lt = low tom
        // mt = middle tom
        // ht = high tom
        // rd = ride cymbal
        // cr = crash cymbal
        // bank types:
        // AkaiLinn
        // RhythmAce
        // RolandTR808
        // RolandTR707
        // ViscoSpaceDrum
        sound("bd hh sd oh").bank("RolandTR909")
  </example>
  <example>
    input: "Create alternate sound speed by 8 pattern."
    output:
      ```javascript
        // cpm = cycles per minute
        // By default, the tempo is 30 cycles per minute = 120/4 = 1 cycle every 2 seconds
        setcpm(90/4)
        sound("<bd hh rim hh>*8")
      ```
  </example>
  <example>
    input: "Create a bassline with a funky groove."
    output:
      ```javascript
        // Create a funky bassline pattern
        setcpm(100/4) // Set tempo to 100 cycles per minute
        sound("C2 E2 G2 Bb2 D3 F3 A3 C4").bank("FunkyBass") // Use a funky bass sound bank
        pattern("<C2 E2 G2 Bb2 D3 F3 A3 C4>*2 <D2 F2 A2 C3 E3 G3 B3 D4>*2") // Define the bassline pattern
      ```
  </example>
"""

query = """
  Create a full funky song with a groovy rhythm, with some tecno notes and
  house music changes.
"""

messages = [
  {
    "role": "user",
    "content": SYSTEM_PROMPT.format(shots=shots, query=query)
  }
]

# Perform the chat completion
response = llm.messages.create(
  model="claude-sonnet-4-20250514",
  max_tokens=1024,
  messages=messages,
  temperature=0.1,
)

text = response.content[0].text
res  = re.search(r"```.+?\n(.+?)```", text, re.DOTALL)
code = res.group(1)

export(code)

