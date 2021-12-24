import click


def confirm(question: str, tries: int = 2, fg: str = None) -> bool:
    question = f"{question} [y/N] "
    valid = {"yes": True, "ye": True, "y": True, "no": False, "n": False}

    while tries > 0:
        if fg:
            click.secho(question, nl=False, fg=fg)
            choice = input().lower()
        else:
            choice = input(question).lower()

        if choice in valid:
            return valid[choice]

        tries = tries - 1

        if tries > 0:
            click.secho("Please enter 'yes' or 'no'", fg='yellow')

    return False
