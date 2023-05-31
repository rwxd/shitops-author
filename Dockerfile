FROM docker.io/python:3.11

RUN apt-get update && apt-get install -y \
	python3 \
	libssl-dev \
	build-essential \
	libssl-dev \
	ca-certificates \
	libasound2 \
	wget \
	curl \
	ffmpeg \
	&& rm -rf /var/lib/apt/lists/*

# install poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -

# add poetry to path
ENV PATH="${PATH}:/etc/poetry/bin"

WORKDIR /app

# install dependencies
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
	&& poetry update

# copy project
COPY . .

ENTRYPOINT ["poetry", "run", "python3", "-m", "author"]
