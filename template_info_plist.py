#!/usr/bin/env python


import sys
import os
import re

template_str_regex = re.compile("TEMPLATE_THIS_[0-9]+")
template_file_number = re.compile(r"\d+")


def get_info_plist_content(info_plist):
    file = open(info_plist, 'r')
    info_plist_lines = []
    for line in file.readlines():
        info_plist_lines.append(line)
    file.close()
    return info_plist_lines


def get_template_matches(info_plist_lines_list, template_files_list):
    matches = {}
    info_plist_lines = []
    for line in info_plist_lines_list:
        info_plist_lines.append(line)
        match = template_str_regex.findall(line)
        if match:
            for m in match:
                file_number = int(template_file_number.findall(m)[0]) - 1
                if matches.get(m):
                    matches[m][template_files_list[file_number]] += 1
                else:
                    matches[m] = {template_files_list[file_number]: 1}
    return matches


def replace_templates_with_files_content(info_plist_lines_list, template_files_list):
    temp_info_plist = []
    for line in info_plist_lines_list:
        match = template_str_regex.findall(line)
        new_line = line
        for m in match:
            file_numbers = template_file_number.findall(m) if m else None
            if match and file_numbers:
                for file_number in file_numbers:
                    file_number = int(file_number) - 1
                    tf = open(template_files_list[file_number], 'r')
                    new_line = new_line.replace(m, ''.join(tf.readlines()))
        temp_info_plist.append(new_line)
    return temp_info_plist


def write_updated_info_plist(info_plist, info_plist_lines_list):
    info_plist_file = open(info_plist, 'w')
    for line in info_plist_lines_list:
        info_plist_file.write(line)
    info_plist_file.close()


def print_what_will_be_replaced(info_plist_matches):
    for k, v in info_plist_matches.items():
        print("'%s' will be replaced with '%s' file '%s' times" % (k, v.items(), v.values()))


def main():
    if len(sys.argv) < 2:
        print('Please provide a info.plist')
        sys.exit(1)

    info_plist = sys.argv[1]

    if not os.path.exists(info_plist):
        print('info.plist not found')
        sys.exit(2)

    template_files = os.environ.get("TEMPLATE_FILES")
    if template_files:
        temp_files_list = template_files.split(',')

        info_plist_lines = get_info_plist_content(info_plist)
        info_plist_matches = get_template_matches(info_plist_lines, temp_files_list)

        if len(temp_files_list) != len(info_plist_matches.keys()):
            print(
                """template files and template strings in info.plist are not matching 
                (probably you are trying to template more files than info.plist contains templating strings or vise versa)"""
            )
            sys.exit(2)
        print_what_will_be_replaced(info_plist_matches)
        updated_info_plist = replace_templates_with_files_content(info_plist_lines, temp_files_list)
        write_updated_info_plist(info_plist, updated_info_plist)


if __name__ == '__main__':
    main()
