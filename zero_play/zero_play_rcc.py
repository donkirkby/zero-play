from argparse import ArgumentParser
from pathlib import Path
from subprocess import run

from zero_play.rules_formatter import convert_markdown

HTML_PREFIX = """\
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body>
"""
HTML_SUFFIX = """\
</body>
</html>
"""


def parse_args():
    parser = ArgumentParser(description='Compile resources for a Zero Play project.')
    # noinspection PyTypeChecker
    parser.add_argument('folder',
                        type=Path,
                        help='Folder with resource files to pack.')
    parser.add_argument('--name',
                        help='Part of root path for resources, defaults to '
                             'folder name.')
    # noinspection PyTypeChecker
    parser.add_argument('--output', '-o',
                        type=Path,
                        help='Output Python file, defaults to {NAME}_rc.py.')
    parser.add_argument('--markdown', '-m',
                        action='store_true',
                        help='Convert .md files to .html files before packing.')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    folder: Path = args.folder
    output_name = args.name or folder.name
    resources = sorted(folder.glob('**/*'))
    if not resources:
        exit(f'No resources found in {folder}.')
    files_to_tidy = []
    print('Resources can be loaded from these paths:')
    for resource in resources:
        if args.markdown and resource.suffix == '.md':
            html_resource = resource.with_suffix('.html')
            if html_resource.exists():
                raise FileExistsError(f'HTML already exists in {html_resource}.')
            html_fragment = convert_markdown(resource.read_text())
            html_resource.write_text(HTML_PREFIX + html_fragment + HTML_SUFFIX)
            files_to_tidy.append(html_resource)
            resource = html_resource
        rel_path = resource.relative_to(folder)
        print(f':/{output_name}/{rel_path}')

    output = args.output or Path(output_name + '_rc.py')
    project_result = run(['pyside2-rcc', '--project'],
                         check=True,
                         capture_output=True,
                         encoding='utf8',
                         cwd=folder)
    project_lines = project_result.stdout.splitlines()
    project_text = '\n'.join(line
                             for line in project_lines
                             if not line.endswith('.md</file>'))
    project_path = folder / (output_name + '.qrc')
    project_path.write_text(project_text)
    files_to_tidy.append(project_path)
    run(['pyside2-rcc',
         '-o', output,
         '--root', '/'+output_name,
         project_path],
        check=True)
    for path in files_to_tidy:
        path.unlink()
    print()
    print(f"Generated {output} (don't forget to import it).")


if __name__ == '__main__':
    main()
