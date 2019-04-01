from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_phtomJs(agent):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = agent
    dcap["phantomjs.page.settings.loadImages"] = False
    # service_args = ['--proxy=127.0.0.1:9150', '--proxy-type=socks5']
    driver = webdriver.PhantomJS(desired_capabilities=dcap,executable_path='D:\phantomjs\phantomjs.exe')
    # D                                                                       :\phantomjs\phantomjs - 2.1.1 - windows\bin
    return driver
    
    
def get_firefox(agent):
    profile=webdriver.FirefoxProfile()
    profile.set_preference('permissions.default.stylesheet',2)
    profile.set_preference('permissions.default.image',2)
    profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
    profile.set_preference('network.proxy.type',1)
    profile.set_preference('network.proxy.socks','127.0.0.1')
    profile.set_preference('network.proxy.socks_port',9150)
    profile.set_preference('network.proxy.socks_version',5)
    profile.update_preferences()
    driver = webdriver.Firefox(profile)
    return driver

def get_chrome(agent):
    options=webdriver.ChromeOptions()

    #options.add_argument('--proxy-server=socks5://127.0.0.1:9150')
    #options.add_argument('--proxy-server=socks5://127.0.0.1:1080')
    #options.add_argument('--proxy-server=http://proxy.lfk.360es.cn:3128')
    options.add_argument("--window-size=1366,768")
    #options.add_argument('--user-agent=android')
    # options.add_argument('--user-agent={agent}'.format(agent=agent))
    prefs = {
        'profile.default_content_setting_values' : {
            'images' : 2
        }
    }
    options.add_experimental_option('prefs',prefs)
    driver=webdriver.Chrome(executable_path='D:\gdriver\chromedriver.exe',options=options)
    return driver

