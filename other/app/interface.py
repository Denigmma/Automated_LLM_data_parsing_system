def process_user_message(message: str) -> str:
    """
    Обрабатывает сообщение пользователя.
    На данном этапе просто возвращает сообщение с префиксом 'Echo:'.
    """
    return f"Echo: {message}"
