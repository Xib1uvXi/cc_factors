# CC_FACTOR

## ENV INSTALL

### install poetry

```shell
curl -sSL https://install.python-poetry.org | python3 -
```

### config poetry > zsh

```shell
mkdir $ZSH_CUSTOM/plugins/poetry
poetry completions zsh > $ZSH_CUSTOM/plugins/poetry/_poetry
```

### update apt 

```shell
sudo apt-get install python3.10-dev default-libmysqlclient-dev build-essential
```

### install dependencies

```shell
poetry install -vvv
```