from argparse import ArgumentParser
from pathlib import Path
from subprocess import run


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
    return parser.parse_args()


def main():
    args = parse_args()
    folder: Path = args.folder
    output_name = args.name or folder.name
    resources = sorted(folder.glob('**/*'))
    if not resources:
        exit(f'No resources found in {folder}.')
    print('Resources can be loaded from these paths:')
    for resource in resources:
        rel_path = resource.relative_to(folder)
        print(f':/{output_name}/{rel_path}')

    output = args.output or Path(output_name + '_rc.py')
    project_path = folder / (output_name + '.qrc')
    with project_path.open('w') as project_file:
        run(['pyside2-rcc', '--project'],
            stdout=project_file,
            check=True,
            cwd=folder)
    run(['pyside2-rcc',
         '-o', output,
         '--root', '/'+output_name,
         project_path],
        check=True)
    project_path.unlink()
    print()
    print(f"Generated {output} (don't forget to import it).")


if __name__ == '__main__':
    main()
