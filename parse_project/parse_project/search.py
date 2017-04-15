import re

spans_garbage = ["<span>\n          <style>\n.WVU5{display:none}\n.vhVk{display:inline}\n.qpSZ{display:none}\n.Zrac{display:inline}\n.eGdP{display:none}\n.Ief-{display:inline}\n</style><span class=\"qpSZ\">159</span><span style=\"display: inline\">200</span><span style=\"display: inline\">.</span><span class=\"Zrac\">29</span><span style=\"display:none\">122</span><span class=\"qpSZ\">128</span><span></span><span style=\"display: inline\">.</span><span style=\"display:none\">70</span><div style=\"display:none\">70</div><span style=\"display:none\">102</span><div style=\"display:none\">102</div><span style=\"display:none\">105</span><span style=\"display:none\">154</span><span class=\"qpSZ\">154</span><span></span><span class=\"WVU5\">180</span>191<span style=\"display:none\">192</span><div style=\"display:none\">201</div><span class=\"eGdP\">239</span><span></span><span class=\"qpSZ\">253</span><span></span><span class=\"Zrac\">.</span><span style=\"display:none\">20</span><div style=\"display:none\">20</div><span style=\"display:none\">42</span><span class=\"eGdP\">42</span><div style=\"display:none\">42</div><span style=\"display:none\">46</span><div style=\"display:none\">46</div><span style=\"display:none\">84</span><span class=\"qpSZ\">84</span><div style=\"display:none\">84</div><span class=\"vhVk\">149</span><span style=\"display:none\">200</span><div style=\"display:none\">200</div><span class=\"qpSZ\">236</span><div style=\"display:none\">236</div>        </span>", "<span class=\"qpSZ\">159</span>", "<span style=\"display: inline\">200</span>", "<span style=\"display: inline\">.</span>", "<span class=\"Zrac\">29</span>", "<span style=\"display:none\">122</span>", "<span class=\"qpSZ\">128</span>", "<span></span>", "<span style=\"display: inline\">.</span>", "<span style=\"display:none\">70</span>", "<span style=\"display:none\">102</span>", "<span style=\"display:none\">105</span>", "<span style=\"display:none\">154</span>", "<span class=\"qpSZ\">154</span>", "<span></span>", "<span class=\"WVU5\">180</span>", "<span style=\"display:none\">192</span>", "<span class=\"eGdP\">239</span>", "<span></span>", "<span class=\"qpSZ\">253</span>", "<span></span>", "<span class=\"Zrac\">.</span>", "<span style=\"display:none\">20</span>", "<span style=\"display:none\">42</span>", "<span class=\"eGdP\">42</span>", "<span style=\"display:none\">46</span>", "<span style=\"display:none\">84</span>", "<span class=\"qpSZ\">84</span>", "<span class=\"vhVk\">149</span>", "<span style=\"display:none\">200</span>", "<span class=\"qpSZ\">236</span>"]
divs = ["<div style=\"display:none\">70</div>", "<div style=\"display:none\">102</div>", "<div style=\"display:none\">201</div>", "<div style=\"display:none\">20</div>", "<div style=\"display:none\">42</div>", "<div style=\"display:none\">46</div>", "<div style=\"display:none\">84</div>", "<div style=\"display:none\">200</div>", "<div style=\"display:none\">236</div>"]
clear_elements = ["vhVk", "Zrac", "Ief-"]

div = divs
span = spans_garbage[1:]
garbage = spans_garbage[:1]


def get_unnecessary_elements(tag):
    """
    Find unnecessary element of tags. There are the same.
    """
    tag_list = list(filter(lambda e: 'none' not in e, tag))

    garbage_full = list()

    for each_tag in tag_list:
        split_tag = each_tag.split('"')
        try:
            clear_tag = split_tag[1]
            if clear_tag in clear_elements or 'inline' in clear_tag or re.search(r'^\d+$', clear_tag):
                pass
            else:
                garbage_full.append(each_tag)
        except IndexError:
            garbage_full.append(each_tag)
    return garbage_full


def clear_tags(tag):
    """
    Clearing the tag list from replays.
    """
    if tag:
        c_tag = list(set(get_unnecessary_elements(tag)))
    else:
        c_tag = get_unnecessary_elements(tag)
    return c_tag


def get_amount_tags(un_span, un_div):
    """
    Merge two tag lists of tags without replace.
    """
    span = get_unnecessary_elements(un_span)
    div = get_unnecessary_elements(un_div)
    if span and div:
        amount = clear_tags(span).extend(clear_tags(div))
    elif span and (not div):
        amount = clear_tags(span)
    elif (not span) and div:
        amount = clear_tags(div)
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


def split_garbage(garb):
    """
    Garbage collection by regular expression
    For example: "n>.</s" or "v>34</d" or "v></s"
    """
    unnecessary_tags = get_amount_tags(span, div)

    split_garb = re.split(r'(\w>[0-9.]*<\w)', without_style_garb(garb))

    if unnecessary_tags:
        for each in unnecessary_tags:
            try:
                split_garb.remove(each)
            except ValueError:
                pass
    return split_garb


def split_ip_data(clear_elem):
    """
    Get ip with html tags
    """
    getting_content = list()

    for each_attr in clear_elem:
        for each_garb in split_garbage(garbage):
            try:
                if (re.search(r'^[0-9]+$', each_garb.split('"')[1])) and (not re.search(r'\.', each_garb)) and (each_garb not in getting_content):
                    getting_content.append(each_garb)
            except IndexError:
                pass
            finally:
                if (each_attr in each_garb or 'inline' in each_garb or re.search(r'\w>[0-9]+<\w', each_garb)) and (each_garb not in getting_content) and (not re.search(r'\.', each_garb)):
                    getting_content.append(each_garb)
                else:
                    pass
    return getting_content


def get_ip():
    """
    Finally part.Get IP.
    """
    cont_ip = list(map(lambda e: re.split(r'(>[0-9.]*<)', e), split_ip_data(clear_elements)))

    all_part_ip = list()

    for i in cont_ip:
        ip_part = i[1].replace('>', '').replace('<', '')
        all_part_ip.append(ip_part)

    ip = '.'.join(all_part_ip)
    return ip
print(get_ip())
# 200.29.191.149
# 88.80.113.9
