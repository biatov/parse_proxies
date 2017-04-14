import re
# initial = ["<span>\n          <style>\n.uqsI{display:none}\n.EYZQ{display:inline}\n</style><span style=\"display:none\">110</span><span class=\"uqsI\">110</span><span></span>115<span style=\"display:none\">193</span><div style=\"display:none\">193</div><span class=\"91\">.</span><span class=\"EYZQ\">29</span><span style=\"display:none\">143</span><div style=\"display:none\">143</div><span class=\"uqsI\">246</span><div style=\"display:none\">246</div><span class=\"EYZQ\">.</span><span class=\"EYZQ\">76</span><span></span><span class=\"EYZQ\">.</span>112        </span>", "<span style=\"display:none\">110</span>", "<span class=\"uqsI\">110</span>", "<span></span>", "<span style=\"display:none\">193</span>", "<span class=\"91\">.</span>", "<span class=\"EYZQ\">29</span>", "<span style=\"display:none\">143</span>", "<span class=\"uqsI\">246</span>", "<span class=\"EYZQ\">.</span>", "<span class=\"EYZQ\">76</span>", "<span></span>", "<span class=\"EYZQ\">.</span>"]
initial = ["<span>\n          <style>\n.mcRt{display:none}\n.mBUR{display:inline}\n</style><span class=\"mBUR\">200</span>.<span class=\"mBUR\">29</span><span></span><span class=\"mcRt\">247</span><div style=\"display:none\">247</div><span class=\"20\">.</span><span class=\"mcRt\">14</span><span></span><span class=\"mcRt\">83</span><div style=\"display:none\">83</div>191<span style=\"display: inline\">.</span><span style=\"display:none\">75</span><div style=\"display:none\">75</div><span class=\"91\">149</span>        </span>", "<span class=\"mBUR\">200</span>", "<span class=\"mBUR\">29</span>", "<span></span>", "<span class=\"mcRt\">247</span>", "<span class=\"20\">.</span>", "<span class=\"mcRt\">14</span>", "<span></span>", "<span class=\"mcRt\">83</span>", "<span style=\"display: inline\">.</span>", "<span style=\"display:none\">75</span>", "<span class=\"91\">149</span>"]
# success = ["EYZQ"]
success = ["mBUR"]
gotentag = list(filter(lambda x: 'none' not in x, initial[:1][0].split()))
dirty_ip = []
for visible in success:
    for init in gotentag:
        print(init)
        try:
            if (visible in init) or ("display: inline" in init) or (re.search(r'[0-9.]+', init.split('>')[0])) and (init not in dirty_ip):
                dirty_ip.append(init)
            elif re.search(r'\.', init.split('>')[1]):
                # print(init.split('>')[1])
                # print('========')
                dirty_ip.append(init)
        except IndexError:
            pass
ip = []
for part in dirty_ip:
    try:
        ip_real = part.split('>')[1].split('<')[0].strip()
        ip.append(ip_real)
        # print(part.split('>'))
    except IndexError:
        pass
print(list(filter(None, ip)))
