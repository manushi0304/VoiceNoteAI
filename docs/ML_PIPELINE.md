# VoiceNote AI: ML & NLP Pipeline

This document details the machine learning models, text processing libraries, and utility scripts used in the VoiceNote AI ecosystem.

---

## 🎙️ Speech-to-Text Transcription Engine
- **Framework**: `openai-whisper`
- **Model Size**: `"base"`
- **Workflow**:
  1. The audio file uploaded by the user is stored in a temporary path.
  2. The `TranscriptionService` calls the Whisper model's `transcribe` function.
  3. The service parses the returned segments, text transcript, and predicted audio language, which are then passed forward to the classification and entity pipelines.

---

## 🧠 Intent Classification Pipeline

### 1. Model Overview
- **Base Architecture**: `distilbert-base-uncased` (DistilBERT Sequence Classification model from Hugging Face).
- **Target Intents**:
  - `note` (index 0)
  - `todo` (index 1)
  - `reminder` (index 2)

### 2. Fine-Tuning Setup
The model config is defined in `ml-training/configs/classification.yaml` and is trained using:
- **Optimizer**: AdamW with learning rate `2e-5`.
- **Loss Function**: Cross-Entropy Loss.
- **Batch Size**: 16.
- **Epochs**: 4.

### 3. Classification Process
For incoming text:
1. The text is tokenized into standard indices utilizing `DistilBertTokenizerFast`.
2. Tensor arrays are passed to the PyTorch model running in inference (`eval()`) mode.
3. The raw model logit outputs are converted to probabilities using Softmax.
4. The label matching the maximum probability score is mapped and returned alongside its confidence value.

### 4. Rule-Based Overrides
To ensure 100% accuracy on highly direct triggers, a heuristic override layer runs on top of the model in `voice_create.py`:
- Contains `"remind me"` → intent forced to `reminder` (confidence = 1.0)
- Contains `"note"`, `"notes"`, `"write down"`, or `"journal"` → intent forced to `note` (confidence = 1.0)
- Contains `"buy"`, `"complete"`, `"finish"`, or `"task"` → intent forced to `todo` (confidence = 1.0)

---

## 🏷️ Entity Extraction Engine
- **Framework**: `spaCy`
- **Model**: `en_core_web_sm` (English small pipeline).
- **Extracted Labels**:
  - **`PERSON`**: Extracted names (e.g. "Sarah", "John") are stored in the database note or task parameters.
  - **`DATE` / `TIME`**: Extracted expressions are parsed by the date parser to schedule future alerts.
- **Task Priority Heuristic**: Priority is classified as `HIGH` if the transcript contains urgency indicators (e.g. `"urgent"`, `"asap"`, `"important"`, `"emergency"`), otherwise defaulting to `MEDIUM`.

---

## 🔄 Translation & Command Engines
- **Translation (`Argos Translate`)**: Evaluates foreign-language voice notes and translates the transcripts dynamically using local language packs before creating database entries.
- **Command Parser**: Analyzes transcripts to parse structured system commands like `"add ..."` or `"delete ..."` directly via voice.
