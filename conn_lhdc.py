from get_excel_data import GetExcel
import pymysql


data = GetExcel("/Users/lamber/Documents/ilongfor_data.xlsx").get_data(0)
conn = pymysql.connect(
    host='192.168.11.17',
    port=9018,
    user='sxit',
    passwd='sxittest',
    db='lhdc',
    charset='utf8'
)

# data = ['aiyq', 'anxin1', 'aosijia', 'baibing']
# data = ['xulk']
#print(data)

# 失效用户列表
# disable_users = []
# cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
# for usercode in data:
#
#     cursor.execute('select id from user where usercode = %s', usercode)
#     result = cursor.fetchone()
#     if not result:
#         disable_users.append(usercode)
disable_users = ['chenyuzhu', 'guyuxia', 'csyewen', 'dangling',
                 'huyao', 'wanglei20', 'xiayuan', 'madan4', 'renjiao',
                 'zhengfurong', 'zhongqiuyue', 'tcfc1', 'tcfc2', 'tcfc3',
                 'tongce2014', 'wangli-lp', 'xujing-lp', 'xulk', '长沙业问房地产',
                 '陈兴荣', '分配', '郭宁', '杨少兰']

# 有效用户
effective_users = set(data) - set(disable_users)
for user in effective_users:
    print(user)
#cursor = conn.cursor()
# s = 0
# for i in data:
#     s = s+1
#
#     r = cursor.execute('select id from user where usercode = %s', i)
#     result = cursor.fetchall()

    # if r != 1 or result = :
    #     print(i)
    #print(result, s, i)