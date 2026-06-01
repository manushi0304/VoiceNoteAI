import random
import pandas as pd

random.seed(42)

# --------------------
# TEMPLATES
# --------------------

TODO_TEMPLATES = [
    "I need to {task}",
    "Add {task} to my to-do list",
    "Remember to {task}",
    "Please {task}",
    "Make sure to {task}",
    "I should {task}",
]

NOTE_TEMPLATES = [
    "The meeting went well and we discussed {topic}",
    "Notes from today's meeting about {topic}",
    "This is an idea about {topic}",
    "Thoughts on {topic}",
    "Discussion summary regarding {topic}",
]

REMINDER_TEMPLATES = [
    "Remind me to {action} at {time}",
    "Set a reminder to {action} {time}",
    "Don't let me forget to {action} at {time}",
    "Schedule a reminder for {action}",
    "I need a reminder to {action} at {time}",
]

# --------------------
# SLOT VALUES
# --------------------

TASKS = [
    "finish the project report",
    "buy groceries",
    "call the client",
    "submit the assignment",
    "review the code",
]

TOPICS = [
    "project timelines",
    "system architecture",
    "future development",
    "API design",
    "deployment strategy",
]

ACTIONS = [
    "take medicine",
    "call John",
    "attend the meeting",
    "submit the report",
]

TIMES = [
    "8 PM",
    "tomorrow",
    "next Monday",
    "in the evening",
]

# --------------------
# GENERATION FUNCTION
# --------------------

def generate(templates, slots, label, n):
    rows = []
    for _ in range(n):
        text = random.choice(templates).format(**{
            k: random.choice(v) for k, v in slots.items()
        })
        rows.append((text, label))
    return rows

# --------------------
# GENERATE DATA
# --------------------

data = []
data += generate(TODO_TEMPLATES, {"task": TASKS}, "todo", 300)
data += generate(NOTE_TEMPLATES, {"topic": TOPICS}, "note", 300)
data += generate(REMINDER_TEMPLATES, {"action": ACTIONS, "time": TIMES}, "reminder", 300)

df = pd.DataFrame(data, columns=["text", "label"])
df = df.sample(frac=1).reset_index(drop=True)

df.to_csv("data/processed/train.csv", index=False)
print("✅ Generated", len(df), "training samples")
