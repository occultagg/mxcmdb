# conding=utf-8
#
import re, sys

d = {"#": 1, "##": 2, "###": 3, "####": 4, "#####": 5, "######": 6}

code_pattern = re.compile(r'```(?:.|\s)*?```')
pattern = '#+\s'


def ganMenu(post_content):
    menu = []
    headId = 0
    new_content = ''.join(re.split(code_pattern, post_content))
    s_list = new_content.split('\n')
    for i in s_list:
        if not re.match(pattern, i.strip(' \t\n\r')):
            continue
        i = i.strip(' \t\n')
        head = i.split(' ')[0]
        menu.append('<li><a href="#' * (len(head) - 1) + '@[' + i[len(head):].strip(' \t\n') + '](#id' + str(
            headId) + ')  ')
        headId += 1
    return menu

