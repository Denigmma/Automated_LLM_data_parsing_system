from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Локальный путь к модели
# local_dir = "./qwen_model(2.5-7B)"
# local_dir ="./qwen_model(2.5-3B)"
local_dir = "qwen_model(1.5-1.8B)"
# local_dir ="./qwen_model(1.5-0.5B)"
# local_dir ="./gemma_model_2b"

# Загружаем из локального кэша (без интернета)
tokenizer = AutoTokenizer.from_pretrained(local_dir, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(local_dir, trust_remote_code=True).to("cpu")

def qwen_reply(prompt: str, max_tokens: int = 50) -> str:
    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")
    model.eval()
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            min_new_tokens=5,  # Минимальная длина ответа
            repetition_penalty=1.1, # Штраф за повторение
            do_sample=True,  # Включает стохастическую выборку
            temperature=0.5,  # Контролирует креативность
            top_p=0.8,  # Фильтрует маловероятные варианты
            eos_token_id=tokenizer.eos_token_id, # Прерывает генерацию на конце ответа
            use_cache=False
        )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    if response.startswith(prompt):
        response = response[len(prompt):].strip()
    return response


# Пример использования
if __name__ == "__main__":
    while True:

        user_input = input("Ты: ")
        # prompt = "You are a friendly and smart assistant. Answer clearly and clearly.\n\n" + user_input
        prompt = "Ты — помощьник. Отвечай четко и понятно.\n\n" + user_input

        # prompt = input("Ты: ")
        if prompt.lower() in ("выход", "exit", "quit"):
            break
        response = qwen_reply(prompt)
        print("llm:", response)


# # Пример использования
# if __name__ == "__main__":
#     html_code = """
# Ты — парсер страниц html. Отвечай четко и понятно.
# Перепиши только содержание этой статьи в барузере:
# <html>
# <body>
#     <h1>Статья про лягушек</h1>
#     <h2>Особенности лягушек</h2>
#     <p>У лягушек гладкая и влажная кожа, которая помогает им дышать не только через лёгкие, но и через кожный покров.</p>
#     </body>
# </html>
# """
#
#     print("Отправляем HTML-код модели. Ждём ответ...\n")
#     response = qwen_reply(html_code)
#     print(" ответила:\n")
#     print(response)
