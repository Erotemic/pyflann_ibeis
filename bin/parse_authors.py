def parse_authors():
    """
    Parse the git authors of a repo

    Returns:
        List[str]: list of authors

    CommandLine:
        python bin/parse_authors.py
    """
    import subprocess
    try:
        output = subprocess.check_output(['git', 'shortlog', '-s'],
                                         universal_newlines=True)
    except Exception as ex:
        print('ex = {!r}'.format(ex))
        return []
    else:
        striped_lines = (l.strip() for l in output.split('\n'))
        freq_authors = [line.split(None, 1) for line in striped_lines if line]
        freq_authors = sorted((int(f), a) for f, a in freq_authors)[::-1]
        # keep authors with uppercase letters
        authors = [a for f, a in freq_authors if a.lower() != a]
        return authors


if __name__ == '__main__':
    print(parse_authors())
