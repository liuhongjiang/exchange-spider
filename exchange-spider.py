import datetime
import re

import requests

non_exist_pattern = re.compile(r"您访问的中国银行网站页面不存在")
tr_pattern = re.compile(r'<tr>.*?</tr>', re.DOTALL)

td_name_maps = {'name': '货币名称',
                'xhmr': '现汇买入价',
                'xcmr': '现钞买入价',
                'xhmc': '现汇卖出价',
                'xcmc': '现钞卖出价',
                'zhzs': '中行折算价',
                'date': '发布日期',
                'time': '发布时间'}
td_names = ['name', 'xhmr', 'xcmr', 'xhmc', 'xcmc', 'zhzs', 'date', 'time']

############################
#  <tr>
#    <td>丹麦克朗</td>
#    <td>100.34</td>
#    <td>97.24</td>
#    <td>101.14</td>
#    <td>101.14</td>
#    <td>100.32</td>
#    <td>2016-10-01</td>
#    <td>10:30:00</td>
#  </tr>
############################
pattern_str = ''.join([r'<td.*?>(?P<' + key + '>.*?)</td>\s*?' for key in td_names])
quotation_pattern = re.compile(r'<tr.*?>\s*?' + pattern_str + r'</tr>', re.DOTALL)

highest = {}


def generate_quotation_obj(quotation_match):
    return {
        td_name_maps['name']: quotation_match.group('name'),
        td_name_maps['xhmr']: quotation_match.group('xhmr'),
        td_name_maps['xcmr']: quotation_match.group('xcmr'),
        td_name_maps['xhmc']: quotation_match.group('xhmc'),
        td_name_maps['xcmc']: quotation_match.group('xcmc'),
        td_name_maps['zhzs']: quotation_match.group('zhzs'),
        td_name_maps['date']: quotation_match.group('date'),
        td_name_maps['time']: quotation_match.group('time'),
    }


def get_data_from_url(url):
    print(url)
    r = requests.get(url)
    r.encoding = "utf-8"
    text = r.text.replace('\n', '')

    non_exist_match = non_exist_pattern.search(text)
    if non_exist_match:
        print("the page doesn't exist!")

    matches = tr_pattern.finditer(text)
    if matches:
        for m in matches:
            quotation_match = quotation_pattern.match(m.group())
            if quotation_match:
                a = quotation_match.group()
                if a.find("起始时间") == -1:
                    date = quotation_match.group('date')
                    name = quotation_match.group('name')
                    if date not in highest:
                        highest[date] = {}
                    if name not in highest[date]:
                        highest[date][name] = generate_quotation_obj(quotation_match)
                    else:
                        if highest[date][name][td_name_maps['xhmc']] < quotation_match.group('xhmc'):
                            highest[date][name] = generate_quotation_obj(quotation_match)
    else:
        print('not match!')


def output_csv(data):
    filename = datetime.datetime.now().strftime('%Y-%m-%d') + '.csv'
    with open(filename, mode='w') as f:
        f.write(u'\n中国银行外汇牌价， 日最高现汇卖出价\n\n')
        for date in sorted(data.keys(), reverse=True):
            f.write(date + '\n\n')
            for name in td_names:
                f.write(td_name_maps[name] + ',')
            f.write('\n')
            for money_name in sorted(data[date].keys()):
                quotation = data[date][money_name]
                for name in td_names:
                    f.write(quotation[td_name_maps[name]] + ',')
                f.write('\n')
            f.write('\n\n')
    return filename


first_url = "http://www.boc.cn/sourcedb/whpj/index.html"
base_url = "http://www.boc.cn/sourcedb/whpj/index_%d.html"

get_data_from_url(first_url)
for i in range(1, 10):
    get_data_from_url(base_url % i)

fn = output_csv(highest)

print("Done! 生成数据文件：%s\n" % fn)

input("按回车结束！")
