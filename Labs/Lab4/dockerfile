FROM astral/uv:python3.13-trixie

WORKDIR /app
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev

# Копируем код приложения
#COPY . .

# Порт для devui (обычно 8000)
#EXPOSE 8000

# Запуск
#CMD ["uv", "run", "python", "-m", "agent_framework.devui"]

CMD ["/bin/bash"]