#coding:utf-8

from sms_v3_KRService import sms_v3_KRService
import requests,json,csv,sys,os

reload(sys)
sys.setdefaultencoding('utf-8')

input_word = sys.argv[1]

group1_dict = {
	'1':'结果少',
	'2':'潜在客户',
	'3':'黑马',
	'4':'同行动态',
	'5':'我的选择'
}

group2_dict = {
	'1':'黑马',
	'2':'百度相关搜索'
}

N = 0
while N < 1:
	N += 1

	outfile = open('word_data.csv','wb')

	service = sms_v3_KRService()

	service.setUsername("username")
	service.setPassword("password")
	service.setToken("token")

	for query in open('word.txt'):
		query = query.strip()

		'''一次配额请求一个词'''
		request = {
			'seedWord':'%s' % query,
			'seedFilter': {
							'pvLow':0,
							'maxNum':500,
							'hotMonth':'true'
							},
			'device':0
			}

		try:
			res = service.getKRbySeedWord(request)
			quota = service.getKRQuota()

			for line in res['body']['krResult']:
				exactPV = line['exactPV']			#最近一周日均搜索次数
				word = line['word']					#查询关键词
				hotMonthPV = line['hotMonthPV']		#搜索量最高月份的PV值
				competition = line['competition']	#竞争激烈度
				hotMonth = line['hotMonth']			#全年搜索量最高的月份
				group = line['group']				#分组

				try:
					flag1 = group1_dict[str(line['flag1'])]		#推荐理由1
				except:
					flag1 = line['flag1']
				try:
					flag2 = group2_dict[str(line['flag2'])]	#推荐理由2
				except:
					flag2 = line['flag2']

				if input_word in word:
					data = []
					data.append(word)
					data.append(exactPV)
					data.append(hotMonth)
					data.append(hotMonthPV)
					data.append(competition)
					data.append(group)
					data.append(flag1)
					data.append(flag2)
					writer = csv.writer(outfile,dialect='excel')
					writer.writerow(data)
		except:
			print 'error'

		print '已获取：%s' % query

	print '%s轮扩展完成' % N
	os.system("rm word.txt ")

	print '输出数据去重'
	os.system(" cat word_data.csv|egrep -v ' '|awk -F\",\" '!a[$1]++' > word_data_1.csv ")
	os.system(" rm word_data.csv ")
	os.system(" mv word_data_1.csv word_data.csv ")

	print '导入第%s轮扩展关键词' % (N+1)
	os.system(" cat word_data.csv|awk -F\",\" '{print $1}'|awk '!a[$0]++' > word.txt ")

os.system(" cat word_data.csv|egrep -v ' '|awk -F\",\" '!a[$1]++' > word_data_1.csv ")
os.system(" rm word_data.csv ")
os.system(" mv word_data_1.csv word_data.csv ")
