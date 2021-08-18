from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

all_seasons = ['1992/93', '1993/94', '1994/95', '1995/96', '1996/97', '1997/98',
		'1998/99', '1999/00', '2000/01', '2001/02', '2002/03', '2003/04', 
		'2004/05', '2005/06', '2006/07', '2007/08', '2008/09', '2009/10',
		'2010/11', '2011/12', '2012/13', '2013/14', '2014/15', '2015/16',
		'2016/17', '2017/18', '2018/19', '2019/20', '2020/21']
		
def set_up_driver(url):
	# opts = Options()
	# opts.set_headless = True
	# driver = webdriver.Firefox(options=opts)
	# driver.get(url)

	options = webdriver.ChromeOptions()
	options.add_argument("--no-sandbox")
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	options.add_argument("--start-maximized")
	driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
	driver.get(url)
	return driver