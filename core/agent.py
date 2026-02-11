from .memory import ShortTermMemory
from .llm_engine import generate_response
from config.config import OWNER_PHONE_NUMBER

memory = ShortTermMemory(max_len=10)
# Global flag for the Kill Switch
is_active = True

def process_incoming_message(sender_id, message_text):
    global is_active

    # --- Kill Switch Logic ---
    # Only the owner can toggle the bot
    if sender_id == OWNER_PHONE_NUMBER:
        if message_text.strip() == "!stop" or message_text.strip() == "!قفل":
            is_active = False
            return "تم إيقاف البوت. المايك معاك يا هندسة."
        elif message_text.strip() == "!start" or message_text.strip() == "!شغل":
            is_active = True
            return "البوت رجع يشتغل تاني."

    # If bot is inactive, ignore everything
    if not is_active:
        return None 

    # --- Normal Processing ---
    history = memory.get_history(sender_id)
    response = generate_response(history, message_text)

    # Update Memory
    memory.add_message(sender_id, "user", message_text)
    memory.add_message(sender_id, "assistant", response)

    return response