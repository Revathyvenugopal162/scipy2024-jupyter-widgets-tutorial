# AUTOGENERATED! DO NOT EDIT! File to edit: ../02a_nbdev.ipynb.

# %% auto 0
__all__ = ['exception', 'answer', 'export']

# %% ../02a_nbdev.ipynb 8
from IPython import get_ipython
from IPython.core.magic import register_line_magic, register_cell_magic
import re
import sys
import os

# %% ../02a_nbdev.ipynb 10
@register_cell_magic('exception')
def exception(line, cell):
    ip = get_ipython()
    try:
        exec(cell, None, ip.user_ns)
    except Exception as e:
        etype, value, tb = sys.exc_info()
        value.__cause__ = None  # suppress chained exceptions
        ip._showtraceback(etype, value, ip.InteractiveTB.get_exception_only(etype, value))

# %% ../02a_nbdev.ipynb 17
@register_line_magic('answer')
def answer(inputs):
    '''
    This is a cell magic called answer that allows tutorial goers to import the correct answer from the key. 
    '''
    words = []
    for word in inputs.split(' '):
        if not word.startswith('#') and len(word) != 0:
            words.append(word)
        else:
            break

    flag = False
    if len(words) == 2:
        if words[1] == '-e':
            flag = True
        else:
            filepath = words[0]
            cell_number = int(words[1])

            with open(filepath, 'r') as file:
                lines = file.readlines()

            pattern = r'# %%\s+(.+)\s+(\d+)'
            start_line = None
            end_line = None

            for i, line in enumerate(lines):
                if re.match(pattern, line):
                    match = re.search(pattern, line)
                    if match and int(match.group(2)) == cell_number:
                        start_line = i + 1
                        break
            if start_line is not None:
                for i in range(start_line, len(lines)):
                    if re.match(pattern, lines[i]):
                        end_line = i
                        break
                else:
                    end_line = len(lines)

            if start_line is not None and end_line is not None:
                code_chunk = f"#| export\n# %answer {inputs}\n\n" + ''.join(lines[start_line:end_line])
                code_chunk = code_chunk.rstrip("\n")
                get_ipython().set_next_input(code_chunk, replace=True)
            else:
                raise Exception(f"Cell number {cell_number} not found in the Python file.")

    if len(words) == 1 or words[1] == '-e':
        filepath = words[0]
        with open(filepath, 'r') as file:
            lines = file.readlines()
        code_chunk = ''.join(lines[:])
        if flag:
            code_chunk = f"# %%export {filepath}\n\n" + code_chunk
        else: 
            code_chunk = f"# %answer {filepath}\n\n" + code_chunk
        get_ipython().set_next_input(code_chunk, replace=True)

    with open(filepath, 'r') as file:
        lines = file.readlines()

# %% ../02a_nbdev.ipynb 29
@register_cell_magic('export')
def export(line, cell=None):
    line_args = line.split()
    export_filepath = None

    if len(line_args):
        export_filepath = line_args[0]
        directory = os.path.dirname(export_filepath)
        os.makedirs(directory, exist_ok=True)
        with open(export_filepath, 'w') as file:
            file.write(cell)
        print(f"exported to {export_filepath}")
            
    processed_lines = []
    for line in cell.split('\n'):
        comment_match = re.search(r'#', line)
        if comment_match:
            line = line[comment_match.start():]
            processed_lines.append(line)

    processed_cell = '\n'.join(processed_lines)
    if len(line_args):
        processed_cell = '# %answer ' + line_args[0] + '\n\n' + processed_cell
    get_ipython().set_next_input(processed_cell, replace=True)
