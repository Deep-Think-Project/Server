# Deep Think Project

This project provides an API that classifies sentences into *clear* or *ambiguous* based on linguistic and contextual analysis. It also enriches ambiguous sentences with external supporting sources using two LLMs: **OpenAI GPT** and **Perplexity Sonar**.

---

## 🚀 Features

- Accepts either raw text or a URL as input.
- Automatically extracts and preprocesses web content.
- Classifies each sentence using GPT into:
  - `clear_sentence`: Fact-based and contextually grounded.
  - `ambiguous_sentence`: Contains bias, implication, vagueness, or emotional tone.
- Extracts ambiguous sentences and passes them to **Sonar AI** to search for real-world supporting sources.
- Merges and returns enriched sentence-level analysis and metadata.

---

## 📦 Input Format

POST JSON to the API endpoint `https://localhost:8000/main_app/`:

```json
{
  "input": "https://example.com/article" // or plain text
}
```

---

## 📤 Output Format

Returns a JSON object with:
- `sentences`: A list of objects containing:
  - `index`: Sentence index.
  - `sentence`: The sentence itself.
  - `type`: One of `clear_sentence`, `ambiguous_sentence`.
  - `reason`: Explanation of classification.
  - `other_interpretations`: (if ambiguous) Alternative ways the sentence might be interpreted.
  - `references`: Real-world sources supporting the interpretations.
- `results`: Aggregated analysis including:
  - Counts of each sentence type.
  - A bullet-style `summary` of the full text.
  - The `author_intent`, listing main arguments or goals.

---

## 🧪 Example Output

```json
{
  "sentences": [
    {
      "index": 0,
      "sentence": "...",
      "type": "ambiguous_sentence",
      "reason": "...",
      "other_interpretations": [
        "...",
        "..."
      ],
      "references": [
        {
          "source_title": "...",
          "url": "https://www.example.com/..."
        }
      ]
    },
    {
      "index": 1,
      "sentence": "...",
      "type": "clear_sentence",
      "reason": "..."
    }
  ],
  "results": {
    "clear_sentence": 1,
    "ambiguous_sentence": 1,
    "summary": [
      ...
    ],
    "author_intent": [
      ...
    ]
  }
}
```

---

## ⚙️ Requirements

- Python 3.9+
- Django
- `requests`, `beautifulsoup4`, `spacy`, `openai`, `dotenv`

> ⚠ **Note:** The `spaCy` library and its dependencies (e.g., `blis`) may not be fully compatible with **Python 3.13**.  
> It is recommended to use **Python 3.12.10 or earlier** for full compatibility.

```bash
pip install -r requirements.txt
python -m spacy download ko_core_news_sm
```

---

## 🔐 API Keys

Place your API keys in a `.env` file:

```
OPEN_API_KEY=your_openai_key
SONAR_API_KEY=your_perplexity_key
```

---

## 📂 Output Debug Files

Intermediate outputs are saved for debugging:
- Raw text extraction
- Indexed sentences
- GPT-4o output
- Sonar references
- Final merged output

---

## 🧑‍💻 Author

This project was developed as part of a social problem-solving initiative.
It leverages AI to analyze sentence clarity and credibility in media and public discourse,
helping users evaluate information with greater transparency, accountability, and visual insight through contextual references and sourced evidence.

---

## 📜 License

MIT License