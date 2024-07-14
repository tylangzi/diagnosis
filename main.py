"""
获取driver,并访问百度
"""
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from driver.driver import driver

def switch_new_window():
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])

def open_url():
    driver.get("https://drplatform.deeproute.cn/#/diagnosis-management/issue/tag?path=%2Fissue%2Ftag")
    switch_new_window()



def switch_iframe():
    while True:
        try:
            driver.switch_to.frame('opsIframe')
            break
        except Exception as e:
            print(e)
            print("iframe找不到")
            time.sleep(1)


def query_tripname(tripname):
    # 输入tripname
    input_loc = (By.XPATH, "//*/span[contains(text(),'行程名称:')]/../..//input")
    input_ele = WebDriverWait(driver,10,1).until(EC.visibility_of_element_located(input_loc))
    input_ele.send_keys(Keys.COMMAND, 'a')
    input_ele.send_keys(Keys.BACKSPACE)
    input_ele.send_keys(tripname)

    # 点击查询
    time.sleep(1)
    query_loc = (By.XPATH, "//*/span[contains(text(),'查询')]/..")
    query_ele = driver.find_element(*query_loc)
    query_ele.click()

    # 点击离线诊断，显示等待
    query_loc = (By.XPATH, "//*/span[contains(text(),'离线诊断')]/..")
    while True:
        try:
            query_ele = driver.find_element(*query_loc)
            query_ele.click()
            break
        except Exception as e:
            print(e)
            print('数据未搜索到')
            time.sleep(1)
def click_tag_list():
    tag_list_loc = (By.XPATH, "//*/span[contains(text(),'所属trip的tag列表')]/..")
    while True:
        try:
            tag_list_ele = driver.find_element(*tag_list_loc)
            tag_list_ele.click()
            break
        except Exception as e:
            print(e)
            print("所属trip的tag列表找不到")
            time.sleep(1)
def filter_taglist():
    click_tag_list()
    # type 框
    type_loc = (By.XPATH, "//*/span[contains(text(),'tag类型')]/..//span[contains(text(),'event_trigger')]")
    # type_ele = driver.find_element(*type_loc)
    type_ele = WebDriverWait(driver,10,1).until(EC.visibility_of_element_located(type_loc))
    action = ActionChains(driver)
    # action.move_to_element(type_ele).perform()
    action.click(type_ele).perform()
    # action.scroll_to_element(type_ele).perform()

    #//*/div[@class='v-vl-visible-items']
    # 差掉 event_trigger
    item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
    item_ele = driver.find_element(*item_loc)
    type_loc = (By.XPATH, './div[1]')
    type_ele = item_ele.find_element(*type_loc)
    # 循环遍历下一个兄弟节点
    while True:
        try:
            if type_ele.text in ["event_trigger", "tag"]:
                # 滑动到目标位置了再点击
                action = ActionChains(driver)
                action.scroll_to_element(type_ele)
                type_ele.click()
                print(f'{type_ele.text}被点击了')
                time.sleep(1)
            print(f'{type_ele.text}没有被点击')
            next_loc = (By.XPATH, "following-sibling::div[1]")
            type_ele = type_ele.find_element(*next_loc)

        except Exception as e:
            print(e)
            print("兄弟节点已经没有了")
            break


def paging():
    # 点击分页按钮
    page_loc = (By.XPATH, "//*/div[contains(text(),'页')]")
    page_ele = driver.find_element(*page_loc)
    action = ActionChains(driver)
    action.scroll_to_element(page_ele).perform()
    action.click(page_ele).perform()

    # 点击100页面
    page_100_loc = (By.XPATH, "//*/div[contains(text(),'100 / 页')]")
    page_100_ele = WebDriverWait(driver,10,1).until(EC.visibility_of_element_located(page_100_loc))
    action = ActionChains(driver)
    action.scroll_to_element(page_100_ele).perform()
    action.click(page_100_ele).perform()

    # 划到最底部
    action.scroll_to_element(page_100_ele).perform()

def diagnosis_list(id=2):
    tbody_loc = (By.XPATH, "//*/tbody[@class='n-data-table-tbody']")
    tbody_ele = WebDriverWait(driver,20,1).until(EC.visibility_of_element_located(tbody_loc))
    tr_loc = (By.XPATH, "./tr[1]")
    tr_ele = tbody_ele.find_element(*tr_loc)

    # event_id
    event_id_loc = (By.XPATH, "./td[@data-col-key='eventId']")
    event_id_ele = tr_ele.find_element(*event_id_loc)
    print("到这里了")
    try:
        while True:
            action = ActionChains(driver)
            action.scroll_to_element(event_id_ele).perform()
            print(event_id_ele.text)
            if int(id) == int(event_id_ele.text):
                print(f"id找到了{event_id_ele.text}")

                # 开始诊断
                diagnosis_loc = (By.XPATH, "./td[@data-col-key='action']/button")
                diagnosis_ele = tr_ele.find_element(*diagnosis_loc)
                diagnosis_ele.click()
                break
            # 没有找到，开始找下一个
            next_loc = (By.XPATH, "following-sibling::tr[1]")
            tr_ele = tr_ele.find_element(*next_loc)
            event_id_loc = (By.XPATH, "./td[@data-col-key='eventId']")
            event_id_ele = tr_ele.find_element(*event_id_loc)

    except Exception as e:
        print(e)
        print("找不到这个ID，可能是数据诊断结束或者数据丢失")

def input_desc(text="【[NCA]第一轮城区泛化测试-7.8】城区，多车道直行路段，自车向左变道过程中，点刹，影响体感"):
    # 将页面滑动可以诊断信息，为了让页面可见
    diagnosis_info_loc = (By.XPATH, "//*/div[contains(text(),'诊断信息')]")
    diagnosis_info_ele = driver.find_element(*diagnosis_info_loc)
    driver.execute_script('arguments[0].scrollIntoView();', diagnosis_info_ele)

    # 把内容清空
    input_dest_loc = (By.XPATH, "//*/span[contains(text(),'描述')]/../..//*/textarea")
    input_dest_ele = driver.find_element(*input_dest_loc)
    input_dest_ele.send_keys(Keys.COMMAND, 'a')
    input_dest_ele.send_keys(Keys.BACKSPACE)
    time.sleep(1)
    # 开始输入内容
    input_dest_ele.send_keys(text)

def create_work_item():
    create_loc = (By.XPATH,"//*/span[contains(text(),'创建飞书工作项')]/..")
    create_ele = driver.find_element(*create_loc)
    while True:
        try:
            status_loc = (By.XPATH,"//*/span[contains(text(),'创建飞书工作项')]/preceding-sibling::span[1]")
            driver.find_element(*status_loc)
            print("还在加载中，请等待。。。")
            time.sleep(1)
        except Exception as e:
            print("加载成功")
            break

    create_ele.click()


def input_operator(input_content='pinyihu'):
    global index

    operator_loc = (By.XPATH, "//*/span[contains(text(),'经办人')]/../..//*/input")
    operator_ele = WebDriverWait(driver,20,1).until(EC.visibility_of_element_located(operator_loc))
    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(operator_ele).perform()
    operator_ele.send_keys(input_content)

    item_loc = (By.XPATH,"//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]
    index = index + 1
    content_loc = (By.XPATH, ".//div")
    content_ele = item_ele.find_element(*content_loc)
    while True:
        try:
            print(content_ele.text)
            action = ActionChains(driver)
            action.scroll_to_element(content_ele).perform()
            if input_content == content_ele.text:
                print(f"{content_ele.text}为输入的值")
                action.click(content_ele).perform()
                break
            else:
                content_loc = (By.XPATH, "./following-sibling::div")
                content_ele = content_ele.find_element(*content_loc)
        except Exception as e:
            print(e)
            print(f"请检查表格中的值{input_content}是否有误")
    print(item_ele.text,f"可见的<div>元素数量: {len(item_ele_list)}")

def business(input_content="GWM"):
    global index

    business_loc = (By.XPATH, "//*/span[contains(text(),'业务线')]/../..//*/input")
    business_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(business_loc))
    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(business_ele).perform()

    business_ele.send_keys(input_content)

    item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]
    index = index + 1
    content_loc = (By.XPATH, ".//div")
    content_ele = item_ele.find_element(*content_loc)
    while True:
        try:

            print(content_ele.text)
            action = ActionChains(driver)
            action.scroll_to_element(content_ele).perform()
            if input_content == content_ele.text:
                print(f"{content_ele.text}为输入的值")

                action.click(content_ele).perform()
                break
            else:
                content_loc = (By.XPATH, "./following-sibling::div")
                content_ele = content_ele.find_element(*content_loc)
        except Exception as e:
            print(e)
            print(f"请检查表格中的值{input_content}是否有误")
    print(item_ele.text, f"可见的<div>元素数量: {len(item_ele_list)}")
def priority(input_content="P0"):
    global index

    priority_loc = (By.XPATH, "//*/span[contains(text(),'优先级')]/../..//*/input")
    priority_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(priority_loc))
    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(priority_ele).perform()

    priority_ele.send_keys(input_content)

    item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]
    index = index + 1
    content_loc = (By.XPATH, ".//div")
    content_ele = item_ele.find_element(*content_loc)
    while True:
        try:

            print(content_ele.text)
            action = ActionChains(driver)
            action.scroll_to_element(content_ele).perform()
            if input_content == content_ele.text:
                print(f"{content_ele.text}为输入的值")

                action.click(content_ele).perform()
                break
            else:
                content_loc = (By.XPATH, "./following-sibling::div")
                content_ele = content_ele.find_element(*content_loc)
        except Exception as e:
            print(e)
            print(f"请检查表格中的值{input_content}是否有误")
    print(item_ele.text, f"可见的<div>元素数量: {len(item_ele_list)}")
def module(input_content="prediction"):
    global index

    module_loc = (By.XPATH, "//*/span[contains(text(),'问题所属模块')]/../following-sibling::div[1]//div")
    module_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(module_loc))
    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(module_ele).perform()

    module_ele.click()

    item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]
    index = index + 1
    content_loc = (By.XPATH, ".//div")
    content_ele = item_ele.find_element(*content_loc)
    while True:
        try:
            print(content_ele.text)
            action = ActionChains(driver)
            action.scroll_to_element(content_ele).perform()
            if input_content == content_ele.text:
                print(f"{content_ele.text}为输入的值")

                action.click(content_ele).perform()
                break
            else:
                content_loc = (By.XPATH, "./following-sibling::div[1]")
                content_ele = content_ele.find_element(*content_loc)
        except Exception as e:
            print(e)
            print(f"请检查表格中的值{input_content}是否有误")
    print(item_ele.text, f"可见的<div>元素数量: {len(item_ele_list)}")

def what_time(input_content="白天"):
    global index

    what_time_loc = (By.XPATH, "//*/span[contains(text(),'时间')]/../..//*/input[@placeholder != '请从prophet拷贝对应时间戳']")
    what_time_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(what_time_loc))
    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(what_time_ele).perform()

    what_time_ele.send_keys(input_content)

    item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]
    index = index + 1
    content_loc = (By.XPATH, ".//div")
    content_ele = item_ele.find_element(*content_loc)
    while True:
        try:

            print(content_ele.text)
            action = ActionChains(driver)
            action.scroll_to_element(content_ele).perform()
            if input_content == content_ele.text:
                print(f"{content_ele.text}为输入的值")

                action.click(content_ele).perform()
                break
            else:
                content_loc = (By.XPATH, "./following-sibling::div[1]")
                content_ele = content_ele.find_element(*content_loc)
        except Exception as e:
            print(e)
            print(f"请检查表格中的值{input_content}是否有误")
    print(item_ele.text, f"可见的<div>元素数量: {len(item_ele_list)}")

def area(input_content="城区"):
    global index

    area_loc = (By.XPATH, "//*/span[contains(text(),'区域')]/../..//*/input")
    area_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(area_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(area_ele).perform()

    area_ele.send_keys(input_content)

    item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]
    index = index + 1
    content_loc = (By.XPATH, ".//div")
    content_ele = item_ele.find_element(*content_loc)
    while True:
        try:

            print(content_ele.text)
            action = ActionChains(driver)
            action.scroll_to_element(content_ele).perform()
            if input_content == content_ele.text:
                print(f"{content_ele.text}为输入的值")
                action.click(content_ele).perform()
                break
            else:
                content_loc = (By.XPATH, "./following-sibling::div[1]")
                content_ele = content_ele.find_element(*content_loc)
        except Exception as e:
            print(e)
            print(f"请检查表格中的值{input_content}是否有误")
    print(item_ele.text, f"可见的<div>元素数量: {len(item_ele_list)}")

def whether(input_content="晴天"):
    global index

    whether_loc = (By.XPATH, "//*/span[contains(text(),'天气')]/../..//*/input")
    whether_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(whether_loc))
    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(whether_ele).perform()

    whether_ele.send_keys(input_content)

    item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]
    index = index + 1
    content_loc = (By.XPATH, ".//div")
    content_ele = item_ele.find_element(*content_loc)
    while True:
        try:

            print(content_ele.text)
            action = ActionChains(driver)
            action.scroll_to_element(content_ele).perform()
            if input_content == content_ele.text:
                print(f"{content_ele.text}为输入的值")
                action.click(content_ele).perform()
                break
            else:
                content_loc = (By.XPATH, "./following-sibling::div[1]")
                content_ele = content_ele.find_element(*content_loc)
        except Exception as e:
            print(e)
            print(f"请检查表格中的值{input_content}是否有误")
    print(item_ele.text, f"可见的<div>元素数量: {len(item_ele_list)}")


def child_function(input_contents="纵向功能 / 融合限速 / 隧道限速"):
    global index
    fun_loc = (By.XPATH, "//*/span[contains(text(),'子功能')]/../..//div")
    fun_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(fun_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(fun_ele).perform()

    fun_ele.click()

    for input_content in [input_content for input_content in input_contents.split('/')]:
        item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]
        index = index + 1
        content_loc = (By.XPATH, ".//span")
        content_ele = item_ele.find_element(*content_loc)
        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                action = ActionChains(driver)
                action.scroll_to_element(content_ele).perform()
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    action.click(content_ele).perform()
                    break
                else:
                    content_loc = (By.XPATH, "./../following-sibling::div[1]/span")
                    content_ele = content_ele.find_element(*content_loc)
            except Exception as e:
                print(e)
                print(f"请检查表格中的值{input_content}是否有误")


def road_type(input_contents="道路用途 / 汇入汇出 / 匝道内选道 / 宽车道一分二选车道"):
    global index
    road_type_loc = (By.XPATH, "//*/span[contains(text(),'道路类型')]/../..//div")
    road_type_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(road_type_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(road_type_ele).perform()

    road_type_ele.click()

    for input_content in [input_content for input_content in input_contents.split('/')]:
        item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]
        # index = index + 1
        content_loc = (By.XPATH, ".//span")
        content_ele = item_ele.find_element(*content_loc)
        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                action = ActionChains(driver)
                action.scroll_to_element(content_ele).perform()
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    action.click(content_ele).perform()
                    break
                else:
                    content_loc = (By.XPATH, "./../following-sibling::div[1]/span")
                    content_ele = content_ele.find_element(*content_loc)
            except Exception as e:
                print(e)
                print(f"请检查表格中的值{input_content}是否有误")

def obstacle(input_contents="障碍物类型 / 小障碍物 / 锥桶 / 倒地锥桶"):
    global index
    obstacle_loc = (By.XPATH, "//*/span[contains(text(),'障碍物交互')]/../..//div")
    obstacle_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(obstacle_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(obstacle_ele).perform()

    obstacle_ele.click()

    for input_content in [input_content for input_content in input_contents.split('/')]:
        item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]
        # index = index + 1
        content_loc = (By.XPATH, ".//span")
        content_ele = item_ele.find_element(*content_loc)
        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                action = ActionChains(driver)
                action.scroll_to_element(content_ele).perform()
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    action.click(content_ele).perform()
                    break
                else:
                    content_loc = (By.XPATH, "./../following-sibling::div[1]/span")
                    content_ele = content_ele.find_element(*content_loc)
            except Exception as e:
                print(e)
                print(f"请检查表格中的值{input_content}是否有误")

def task_type(input_contents="专项测试 / 场景验证"):
    global index
    task_type_loc = (By.XPATH, "//*/span[contains(text(),'任务类型')]/../..//div")
    task_type_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(task_type_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(task_type_ele).perform()

    task_type_ele.click()

    for input_content in [input_content for input_content in input_contents.split('/')]:
        item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]
        # index = index + 1
        content_loc = (By.XPATH, ".//span")
        content_ele = item_ele.find_element(*content_loc)
        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                action = ActionChains(driver)
                action.scroll_to_element(content_ele).perform()
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    action.click(content_ele).perform()
                    break
                else:
                    content_loc = (By.XPATH, "./../following-sibling::div[1]/span")
                    content_ele = content_ele.find_element(*content_loc)
            except Exception as e:
                print(e)
                print(f"请检查表格中的值{input_content}是否有误")

def secondary(input_content="二次启停"):
    global index
    secondary_loc = (By.XPATH, "//*/span[contains(text(),'问题类别（二级）')]/../..//div")
    secondary_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(secondary_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(secondary_ele).perform()

    secondary_ele.click()

    # for input_content in [input_content for input_content in input_contents.split('/')]:
    item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]
    # index = index + 1
    content_loc = (By.XPATH, ".//span")
    content_ele = item_ele.find_element(*content_loc)
    while True:
        try:
            print(f"content_ele.text的值为：{content_ele.text.strip()}")
            print(f"input_content的值为：{input_content.strip()}")
            action = ActionChains(driver)
            action.scroll_to_element(content_ele).perform()
            if input_content.strip() == content_ele.text.strip():
                print(f"{content_ele.text}为输入的值")
                action.click(content_ele).perform()
                break
            else:
                content_loc = (By.XPATH, "./../following-sibling::div[1]/span")
                content_ele = content_ele.find_element(*content_loc)
        except Exception as e:
            print(e)
            print(f"请检查表格中的值{input_content}是否有误")


def issue_type(input_contents="程序功能相关 / 策略合理性 / 车辆长时间靠右车道行驶"):
    global index
    issue_type_loc = (By.XPATH, "//*/span[text()='问题类别']/../..//div[@class='n-cascader']")
    issue_type_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(issue_type_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(issue_type_ele).perform()

    issue_type_ele.click()

    for input_content in [input_content for input_content in input_contents.split('/')]:
        item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]
        # index = index + 1
        content_loc = (By.XPATH, ".//span")
        content_ele = item_ele.find_element(*content_loc)
        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                action = ActionChains(driver)
                action.scroll_to_element(content_ele).perform()
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    action.click(content_ele).perform()
                    break
                else:
                    content_loc = (By.XPATH, "./../following-sibling::div[1]/span")
                    content_ele = content_ele.find_element(*content_loc)
            except Exception as e:
                print(e)
                print(f"请检查表格中的值{input_content}是否有误")


def takeover(input_contents="是 / 被动接管 / 功能性"):
    global index
    takeover_loc = (By.XPATH, "//*/span[text()='是否接管']/../..//div")
    takeover_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(takeover_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(takeover_ele).perform()

    takeover_ele.click()

    for input_content in [input_content for input_content in input_contents.split('/')]:
        item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]
        # index = index + 1
        content_loc = (By.XPATH, ".//span")
        content_ele = item_ele.find_element(*content_loc)
        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                action = ActionChains(driver)
                action.scroll_to_element(content_ele).perform()
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    action.click(content_ele).perform()
                    break
                else:
                    content_loc = (By.XPATH, "./../following-sibling::div[1]/span")
                    content_ele = content_ele.find_element(*content_loc)
            except Exception as e:
                print(e)
                print(f"请检查表格中的值{input_content}是否有误")
def issue_atribute(input_contents="合规"):
    global index
    if input_contents == "安全":
        issue_atribute_loc = (By.XPATH, "//*/div[text()='安全']")
    elif input_contents == "合规":
        issue_atribute_loc = (By.XPATH, "//*/div[text()='合规']")
    elif input_contents == "舒适":
        issue_atribute_loc = (By.XPATH, "//*/div[text()='舒适']")
    elif input_contents == "智能":
        issue_atribute_loc = (By.XPATH, "//*/div[text()='智能']")
    elif input_contents == "非问题":
        issue_atribute_loc = (By.XPATH, "//*/div[text()='非问题']")
    else:
        print("请输入正确的问题属性")

    issue_atribute_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(issue_atribute_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(issue_atribute_ele).perform()

    action.click(issue_atribute_ele).perform()

def related_plan(input_content="0725封板冒烟测试"):
    global index
    related_plan_loc = (By.XPATH, "//*/span[text()='关联计划']/../../div")
    related_plan_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(related_plan_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(related_plan_ele).perform()

    related_plan_ele.click()

    item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]
    # index = index + 1
    content_loc = (By.XPATH, "./div/div[@class='n-base-select-option__content']")
    content_ele = item_ele.find_element(*content_loc)
    while True:
        try:
            print(f"content_ele.text的值为：{content_ele.text.strip()}")
            print(f"input_content的值为：{input_content.strip()}")
            action = ActionChains(driver)
            action.scroll_to_element(content_ele).perform()
            if input_content.strip() == content_ele.text.strip():
                print(f"{content_ele.text}为输入的值")
                action.click(content_ele).perform()
                break
            else:
                content_loc = (By.XPATH, "./../following-sibling::div[1]/div")
                content_ele = content_ele.find_element(*content_loc)
        except Exception as e:
            print(e)
            print(f"请检查表格中的值{input_content}是否有误")

def submit():
    global index
    submit_loc = (By.XPATH, "//*/span[text()='提交飞书工作项']/..")
    submit_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(submit_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(submit_ele).perform()
    # 提交
    submit_ele.click()



if __name__ == '__main__':
    open_url()
    switch_iframe()
    query_tripname(tripname='YR-C01-46_20240712_042218')
    filter_taglist()
    paging()
    for i in [75,71]:
        index = 1
        diagnosis_list(i)
        # 输入描述
        input_desc()
        # 点击创建飞书项目
        create_work_item()
        input_operator()


        # 选择业务线
        business()
        # 设置优先级
        priority()

        # 问题所属模块
        module()

        # 时间
        what_time()

        # 区域
        area()

        # 天气
        whether()

        # 自功能
        child_function()

        # 道路类型

        road_type()

        # 障碍物
        obstacle()

        # 任务类型
        task_type()


        # 二级分类
        secondary()

        #问题类别

        issue_type()

        # 问题属性

        issue_atribute()

        # 是否接管

        takeover()


        # 关联计划
        related_plan()

        # 提交
        submit()
        time.sleep(4)
        driver.refresh()
        switch_iframe()
        click_tag_list()

