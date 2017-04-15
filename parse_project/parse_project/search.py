import re


def get_unnecessary_elements(tag, clear_elem):
    """
    Find unnecessary element of tags. There are the same.
    """
    tag_list = list(filter(lambda e: 'none' not in e, tag))

    garbage_full = list()

    for each_tag in tag_list:
        split_tag = each_tag.split('"')
        try:
            clear_tag = split_tag[1]
            if clear_tag in clear_elem or 'inline' in clear_tag or re.search(r'^\d+$', clear_tag):
                pass
            else:
                garbage_full.append(each_tag)
        except IndexError:
            garbage_full.append(each_tag)
    return garbage_full


def clear_tags(tag, clear_elem):
    """
    Clearing the tag list from replays.
    """
    if tag:
        c_tag = list(set(get_unnecessary_elements(tag, clear_elem)))
    else:
        c_tag = get_unnecessary_elements(tag, clear_elem)
    return c_tag


def get_amount_tags(un_span, un_div, clear_elem):
    """
    Merge two tag lists of tags without replace.
    """
    span = get_unnecessary_elements(un_span, clear_elem)
    div = get_unnecessary_elements(un_div, clear_elem)
    if span and div:
        amount = clear_tags(span, clear_elem).extend(clear_tags(div, clear_elem))
    elif span and (not div):
        amount = clear_tags(span, clear_elem)
    elif (not span) and div:
        amount = clear_tags(div, clear_elem)
    else:
        amount = list()
    return amount


def without_style_garb(garb):
    """
    Getting garbage without style
    """
    try:
        new_garbage = garb[0].split('</style>')[1]
    except IndexError:
        new_garbage = garb
    return new_garbage


def split_garbage(garb, span, div, clear_elem):
    """
    Garbage collection by regular expression
    For example: "n>.</s" or "v>34</d" or "v></s"
    """
    unnecessary_tags = get_amount_tags(span, div, clear_elem)

    split_garb = re.split(r'(\w>[0-9.]*<\w)', without_style_garb(garb))

    if unnecessary_tags:
        for each in unnecessary_tags:
            try:
                split_garb.remove(each)
            except ValueError:
                pass
    return split_garb


def split_ip_data(garbage, span, div, clear_elem):
    """
    Get ip with html tags
    """
    getting_content = list()

    for each_garb in split_garbage(garbage, span, div, clear_elem):
        for each_attr in clear_elem:
            try:
                if (re.search(r'^[0-9]+$', each_garb.split('"')[1])) and (not re.search(r'\.', each_garb)) and (each_garb not in getting_content):
                    getting_content.append(each_garb)
            except IndexError:
                pass
            finally:
                if (each_attr in each_garb or 'inline' in each_garb or re.search(r'\w>\.*[0-9]+\.*<\w', each_garb)) and (each_garb not in getting_content) and (not re.search(r'\.', each_garb)):
                    getting_content.append(each_garb)
                elif (re.search(r'\w>\.*[0-9]+\.*', each_garb)) and (each_garb not in getting_content):
                    getting_content.append(each_garb)
                elif (re.search(r'^\s*\.*[0-9]+\.*<\w', each_garb)) and (each_garb not in getting_content):
                    getting_content.append(each_garb)
                elif (re.search(r'\s*\.*[0-9]+\.*\s*$', each_garb)) and (each_garb not in getting_content):
                    getting_content.append(each_garb)
                elif (re.search(r'^\s*\.*[0-9]+\.*\s*$', each_garb)) and (each_garb not in getting_content):
                    getting_content.append(each_garb)
                elif (re.search(r'^\s\.*[0-9]+\.*\s*', each_garb)) and (each_garb not in getting_content):
                    getting_content.append(each_garb)
                elif (re.search(r'\s*\.*[0-9]+\.*\s', each_garb)) and (each_garb not in getting_content):
                    getting_content.append(each_garb)
                elif (re.search(r'\s\.*[0-9]+\.*\s*$', each_garb)) and (each_garb not in getting_content):
                    getting_content.append(each_garb)
                elif (re.search(r'\s*\.*[0-9]+\.*\s$', each_garb)) and (each_garb not in getting_content):
                    getting_content.append(each_garb)
                else:
                    pass
    return getting_content


def get_ip(garbage, span, div, clear_elem):
    """
    Finally part.Get IP.
    """
    cont_ip = list(map(lambda e: re.split(r'(>[0-9.]*<)', e), split_ip_data(garbage, span, div, clear_elem)))

    all_part_ip = list()

    for i in cont_ip:
        ip_part = i[1].replace('>', '').replace('<', '').replace('.', '')
        all_part_ip.append(ip_part)

    ip = '.'.join(all_part_ip)
    return ip
