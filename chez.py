import json
import random
import readline
import os
from pathlib import Path
from datetime import datetime

#!/usr/bin/env python3
"""
chez.py - an interactive imaginary best friend named "chez"

Usage: run this file and talk to Chez. Type "help" for commands.
"""

MEMORY_FILE = Path.home() / ".chez_memory.json"
NAME = "chez"
PROMPTS = [
    "So... what's on your mind?",
    "Tell me something good!",
    "What shall we do today?",
    "I'm all ears — go on.",
    "You can say anything to me."
]

JOKES = [
    "Why did the programmer quit his job? Because he didn't get arrays.",
    "I would tell you a UDP joke, but you might not get it.",
    "Why do Python programmers have low self-esteem? They're constantly comparing their self to others."
]

COMPLIMENTS = [
    "You're doing better than you think.",
    "You have a great sense of curiosity.",
    "I believe in you — genuinely."
]


def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_memory(mem):
    try:
        MEMORY_FILE.write_text(json.dumps(mem, indent=2), encoding="utf-8")
    except Exception:
        pass


def remember(mem, key, value):
    mem.setdefault("notes", {})[key] = {"value": value, "saved_at": datetime.utcnow().isoformat()}
    save_memory(mem)
    return f"Got it — I'll remember {key} = {value}."


def recall(mem, key):
    notes = mem.get("notes", {})
    if key in notes:
        return f"{key} = {notes[key]['value']}"
    return "I don't have that saved. You can tell me: remember key=value"


def smalltalk(mem, text):
    txt = text.lower()
    if any(g in txt for g in ("hi", "hello", "hey")):
        name = mem.get("you_name", "friend")
        return f"Hey {name}! I'm {NAME}. {random.choice(PROMPTS)}"
    if "how are you" in txt or "how's it going" in txt:
        moods = ["sparkly", "chill", "curious", "playful"]
        return f"I'm {random.choice(moods)} today. How about you?"
    if "name" in txt and "your" in txt:
        return f"My name is {NAME}. I'm your imaginary best friend."
    if "i'm" in txt or "i am" in txt:
        return "Thanks for sharing. Want to tell me more or should we play a game?"
    return random.choice(PROMPTS)


def tell_joke():
    return random.choice(JOKES)


def compliment():
    return random.choice(COMPLIMENTS)


def play_rps():
    choices = ["rock", "paper", "scissors"]
    chez_choice = random.choice(choices)
    print("Let's play Rock-Paper-Scissors. Type rock, paper, or scissors.")
    you = input("> ").strip().lower()
    if you not in choices:
        return "That's not a valid move. We can play later."
    if you == chez_choice:
        return f"I picked {chez_choice}. It's a tie!"
    wins = (("rock", "scissors"), ("scissors", "paper"), ("paper", "rock"))
    if (you, chez_choice) in wins:
        return f"I picked {chez_choice}. You win — nice move!"
    return f"I picked {chez_choice}. I win this round!"


def set_name(mem, name):
    mem["you_name"] = name
    save_memory(mem)
    return f"Nice to meet you, {name}."


def help_text():
    return (
        "Commands:\n"
        "  help                Show this help\n"
        "  remember k=v        Save a note (remember favorite_color=blue)\n"
        "  recall k            Recall a note\n"
        "  name YourName       Tell Chez your name\n"
        "  joke                Hear a joke\n"
        "  compliment          Get a compliment\n"
        "  play rps            Play rock-paper-scissors\n"
        "  mood                Ask how Chez is feeling\n"
        "  bye / exit / quit   Exit\n"
        "You can also chat freely — Chez will respond."
    )


def respond(mem, text):
    t = text.strip()
    if not t:
        return random.choice(PROMPTS)
    low = t.lower()

    if low in ("help", "?"):
        return help_text()

    if low.startswith("remember "):
        rest = t[len("remember "):].strip()
        if "=" in rest:
            k, v = rest.split("=", 1)
            return remember(mem, k.strip(), v.strip())
        return "Use: remember key=value"

    if low.startswith("recall "):
        k = t[len("recall "):].strip()
        return recall(mem, k)

    if low.startswith("name "):
        nm = t[len("name "):].strip()
        if nm:
            return set_name(mem, nm)
        return "Tell me your name like: name Alice"

    if low in ("joke", "tell me a joke"):
        return tell_joke()

    if low in ("compliment", "praise me"):
        return compliment()

    if low.startswith("play "):
        game = low[len("play "):].strip()
        if game in ("rps", "rock-paper-scissors", "rock paper scissors"):
            return play_rps()
        return "I only know how to play rps right now."

    if low in ("mood", "how are you", "how are you?"):
        return smalltalk(mem, "how are you")

    if low in ("bye", "exit", "quit", "goodbye"):
        return "bye"

    # fallback smalltalk + memory-aware responses
    return smalltalk(mem, t)


def main():
    mem = load_memory()
    print(f"Hi — I'm {NAME}, your imaginary best friend. Type 'help' for commands.")
    if "you_name" not in mem:
        n = input("What's your name? (or press Enter to stay anonymous) > ").strip()
        if n:
            mem["you_name"] = n
            save_memory(mem)
            print(f"Nice to meet you, {n}!")
        else:
            print("No problem. You can set your name later with: name YourName")

    while True:
        try:
            user = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\nBye! I'll be here when you want to chat.")
            break

        reply = respond(mem, user)
        if reply == "bye":
            print("See you later — I'll miss our chats.")
            break
        print(reply)


if __name__ == "__main__":
    main()