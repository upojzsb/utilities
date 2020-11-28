import glob
import os
import sys
import json


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    input_file_list = glob.glob(path + '*.bcc')

    if 0 == len(input_file_list):
        print('No file ending with ".bcc" in ', path)
        print('usage: python3', sys.argv[0], '[directory]')
        sys.exit(1)

    for input_file_name in input_file_list:
        print('Converting', input_file_name)

        with open(input_file_name, 'r', encoding='utf8') as fd_in:
            output_file_name = input_file_name[:input_file_name.rfind('.bcc')] + '.srt'

            if os.path.exists(output_file_name):
                print(output_file_name, 'exists, skip...')
                continue

            with open(output_file_name, 'w', encoding='utf8') as fd_out:
                ori_data = json.loads(fd_in.read())['body']
                srt_list = []
                for i, record in zip(range(len(ori_data)), ori_data):
                    time_from = record['from']
                    time_to = record['to']
                    content = record['content']

                    # hour:minute:second,millisecond --> hour:minute:second,millisecond
                    time_from = '%02d' % int(int(time_from) / 3600) + ':' + \
                                '%02d' % int((int(time_from) % 3600) / 60) + ':' + \
                                '%02d' % int((int(time_from) % 3600) % 60) + ',' + \
                                '%03.0f' % (1000 * (time_from - int(time_from)))
                    time_to = '%02d' % int(int(time_to) / 3600) + ':' + \
                              '%02d' % int((int(time_to) % 3600) / 60) + ':' + \
                              '%02d' % int((int(time_to) % 3600) % 60) + ',' + \
                              '%03.0f' % (1000 * (time_to - int(time_to)))

                    srt_content = str(i + 1) + '\n' + \
                                  str(time_from) + ' --> ' + str(time_to) + '\n' + \
                                  str(content).replace('\n', '\\n') + '\n\n'

                    srt_list.append(srt_content)

                fd_out.write(''.join(srt_list))
                print(output_file_name, 'converted.')
    print('Convert finished.')


if __name__ == '__main__':
    main()
