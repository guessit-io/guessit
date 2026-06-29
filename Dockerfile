FROM python:3.13-alpine

LABEL org.opencontainers.image.authors="Rémi Alvergnat <toilal.dev@gmail.com>"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /root/guessit/
COPY / /root/guessit/

RUN uv sync --locked --no-default-groups

ENTRYPOINT ["uv", "run", "guessit"]
