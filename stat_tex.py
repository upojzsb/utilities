import os
import subprocess

def list_tex_files(directory):
    tex_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".tex"):
                tex_files.append(os.path.join(root, file))
    return tex_files

if __name__ == "__main__":
    verbose = False

    tex_file_base_path = '/thesis'
    texcount_bin_path = '/texcount.exe'

    tex_files = list_tex_files(tex_file_base_path)

    statistics = []
    statistics_dict_template = {
        'file_name': '',
        'words_text': 0,
        'words_headers': 0,
        'words_outside': 0,
        'num_headers': 0,
        'num_floats_tables_figures': 0,
        'num_math_inline': 0,
        'num_math_display': 0
    }
    for tex_file in tex_files:
        cmdline = '"' + texcount_bin_path + '" "' + tex_file + '"'
        results = subprocess.run(cmdline, capture_output=True, text=True)
        results = results.stdout.split('\n')

        statistics_dict = statistics_dict_template.copy()
        statistics_dict['file_name'] = tex_file
        for result in results:
            if 'Words in text:' in result:
                statistics_dict['words_text'] = int(result.split(':')[1].strip())
            elif 'Words in headers:' in result:
                statistics_dict['words_headers'] = int(result.split(':')[1].strip())
            elif 'Words outside text:' in result:
                statistics_dict['words_outside'] = int(result.split(':')[1].strip())
            elif 'Headers:' in result:
                statistics_dict['num_headers'] = int(result.split(':')[1].strip())
            elif 'floats/tables/figures:' in result:
                statistics_dict['num_floats_tables_figures'] = int(result.split(':')[1].strip())
            elif 'math inlines' in result:
                statistics_dict['num_math_inline'] = int(result.split(':')[1].strip())
            elif 'math displayed:' in result:
                statistics_dict['num_math_display'] = int(result.split(':')[1].strip())
        statistics.append(statistics_dict)
        if verbose:
            print(statistics_dict)

    statistics_dict_all = statistics_dict_template.copy()

    for stat in statistics:
        if verbose:
            print(stat)
        
        for k, v in stat.items():
            print(k, v)
            statistics_dict_all[k] += v if k != 'file_name' else ''
    print(statistics_dict_all)