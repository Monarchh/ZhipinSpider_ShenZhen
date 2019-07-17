import json
import pygal

# 将文件定义为变量filename
filename = 'job_position.json'
# 读取JSON格式的工作数据
with open (filename, 'r', True, 'utf-8') as f:
    job_list = json.load(f)

# 定义job_dict来保存各行业的招聘职位数
job_dict = {}

# 遍历列表的每个元素，每个元素都是一个招聘信息
for job in job_list:
    if job['industry'] in job_dict:
        job_dict[job['industry']] += 1
    else:
        job_dict[job['industry']] = 1

# 创建pygal.Pie对象（饼图）
pie = pygal.Pie()
other_num = 0

# 采用循环为饼图添加数据
for k in job_dict.keys():
    # 如果该行业的招聘位数少于5个，则归类到“其它”中
    if job_dict[k] < 5:
        other_num += job_dict[k]
    else:
        pie.add(k, job_dict[k])

# 添加其它行业的招聘职位数
pie.add('其它', other_num)
pie.title = '深圳地区各行业热门招聘统计图'
# 设置将图例放到底部
pie.legend_at_bottom = True
# 指定将数据图输出到SVG文件中
pie.render_to_file('job_position.svg')