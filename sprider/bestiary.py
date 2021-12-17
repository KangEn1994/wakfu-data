#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2021/12/16
import os, sys, re, json, traceback, time
from selenium import webdriver




def get_bestiarys_list(browser, page_size=24, page_num=45, save_path="..\\data\\bestiary_list.json", type="read"):
    # 获取数据
    if type == "read":
        with open(save_path, "rb") as f:
            result = json.loads(f.read())
    else:
        result = []
        for i in range(1, page_num + 1):
            browser.get("https://www.wakfu.com/en/mmorpg/encyclopedia/monsters?size={0}&page={1}".format(page_size, i))
            time.sleep(1)
            tbody = browser.find_element(by="xpath", value='/html/body/div[2]/div[2]/div/div/div/main/div[2]/div[4]/div[1]/div[2]/table/tbody')
            trs = tbody.find_elements(by="tag name", value="tr")
            for each_tr in trs:
                each_tds = each_tr.find_elements(by="tag name", value="td")
                each_id = each_tds[1].find_element(by="tag name", value="a").get_property("href").split("/")[-1].split("-")[0]
                each_name = each_tds[1].find_element(by="tag name", value="a").text
                each_family_name = each_tds[2].text
                each_level = each_tds[4].text
                print(each_id, "\t", each_name, "\t", each_family_name, "\t", each_level)
                result.append(
                    dict(
                        id=each_id,
                        name=each_name,
                        family_name=each_family_name,
                        level=each_level
                    )
                )
            print("累计{0}个".format(len(result)))
            print(result)
            with open(save_path, "wb") as f:
                f.write(json.dumps(result, ensure_ascii=False, indent=2))

    return result

def get_bestiarys_detail(browser, save_path="..\\data\\bestiary_detail.json", type="read"):
    # 获取数据
    if type == "read":
        with open(save_path, "rb") as f:
            result = json.loads(f.read())
    else:
        # bestiarys_list = get_bestiarys_list(browser)
        with open(save_path, "rb") as f:
            bestiarys_list = json.loads(f.read())



        result = bestiarys_list
        for index, each_bestiary in enumerate(bestiarys_list):
            print("index={0}".format(index))
            if "png_path" in each_bestiary:
                continue
            each_name = "-".join([e.split('\'')[0].lower() for e in each_bestiary["name"].split(" ")])
            each_url_end = "{0}-{1}".format(each_bestiary["id"], each_name)
            each_url = "https://www.wakfu.com/en/mmorpg/encyclopedia/monsters/{0}".format(each_url_end)
            browser.get(each_url)
            time.sleep(1)
            each_png_path = browser.find_element(by="xpath", value="/html/body/div[2]/div[2]/div/div/div/main/div[2]/div/div[3]/div/div/div[1]/div[1]/img").get_property("src")
            catch_boo = browser.find_element(by="xpath", value="/html/body/div[2]/div[2]/div/div/div/main/div[2]/div/div[3]/div/div/div[1]/div[2]/strong").text
            each_divs = browser.find_elements(by="class name", value="ak-panel")
            each_divs_dict = dict()
            for each_div in each_divs:
                each_title = each_div.find_elements(by="class name", value="ak-panel-title")
                if each_title:
                    each_divs_dict[each_title[0].text.strip().upper()] = each_div
            each_bestiary["png_path"] = each_png_path
            each_bestiary["catch_boo"] = catch_boo
            if "CHARACTERISTICS" in each_divs_dict:
                # 基础属性
                each_element = each_divs_dict["CHARACTERISTICS"]
                each_characteristices = each_element.find_elements(by="class name", value="ak-title")
                each_characteristice_dict = dict()
                for each_characteristice in each_characteristices:
                    each_characteristice_name = each_characteristice.text.split(":")[0].strip().replace(" ", "_").lower()
                    each_characteristice_value = each_characteristice.text.split(":")[1].strip()
                    each_characteristice_dict[each_characteristice_name] = each_characteristice_value
                each_bestiary["characteristics"] = each_characteristice_dict
                print([e.text for e in each_characteristices])
            if "RESISTANCES" in each_divs_dict:
                # 攻防属性
                each_element = each_divs_dict["RESISTANCES"]
                each_resistances = each_element.find_elements(by="class name", value="ak-title")
                resistances_name_list = ["water", "earth", "air", "fire"]
                each_resistance_dict = dict()
                for i, each_each_resistance in enumerate(each_resistances):
                    each_resistance_dict[resistances_name_list[i]] = dict(attack=each_each_resistance.text.split(" ")[0], defense=each_each_resistance.text.split(" ")[1])
                each_bestiary["resistances"] = each_resistance_dict
                print([e.text for e in each_resistances])
            if "SPELLS" in each_divs_dict:
                # 技能
                each_element = each_divs_dict["SPELLS"]
                each_spells = each_element.find_elements(by="class name", value="ak-title")
                each_spell_list = list()
                for each_spell in each_spells:
                    each_spell_list.append(dict(name=each_spell.text))
                each_bestiary["spells"] = each_spell_list
                print([e.text for e in each_spells])
            if "DROPS" in each_divs_dict:
                # 掉落
                each_element = each_divs_dict["DROPS"]
                each_drops = each_element.find_elements(by="class name", value="ak-content")
                each_drop_list = list()
                for each_drop in each_drops:
                    # 根据链接获取id
                    each_drop_id = each_drop.find_element(by="tag name", value="a").get_property("href").split("/")[-1].split("-")[0]
                    each_drop_percent = each_drop.find_element(by="class name", value="ak-drop-percent").text
                    each_drop_list.append(dict(drop_id=each_drop_id, percent=each_drop_percent))
                    print(each_drop_id, each_drop_percent)
                each_bestiary["drops"] = each_drop_list
            if "ALLOWS HARVESTING" in each_divs_dict:
                # 畜牧物品
                each_element = each_divs_dict["ALLOWS HARVESTING"]
                each_allowsharvestings = each_element.find_elements(by="class name", value="ak-content")
                each_trapper_list = list()
                for each_allowsharvesting in each_allowsharvestings:
                    # 根据链接获取id
                    each_harvesting_id = each_allowsharvesting.find_element(by="tag name", value="a").get_property("href").split("/")[-1].split("-")[0]
                    each_harvesting_level = each_allowsharvesting.find_element(by="class name", value="ak-text").text.split("Level")[1].strip()
                    each_trapper_list.append(dict(trapper_id=each_harvesting_id, level=each_harvesting_level))
                    print(each_harvesting_id, each_harvesting_level)
                each_bestiary["trappers"] = each_trapper_list
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(bestiarys_list, ensure_ascii=False, indent=2))
        return result

def start():
    # 加启动配置
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    # 全屏效果
    # option.add_argument('--kiosk')
    # 打开chrome浏览器
    browser = webdriver.Chrome(options=option)
    # 设置窗口大小
    browser.set_window_size(1500, 1000)
    # ======以下是rpa流程======
    browser.get("https://www.wakfu.com/en/mmorpg/encyclopedia/monsters?size=24&page=1")
    time.sleep(2)
    # 点击同意cookie
    accept_all = browser.find_element(by="xpath", value='//*[@id="ui-id-1"]/div[1]/div[2]/button[3]')
    accept_all.click()
    time.sleep(2)
    # 获取数据
    get_bestiarys_detail(browser, type="123")

    time.sleep(2)
    browser.close()




"""
    ID = "id"
    XPATH = "xpath"
    LINK_TEXT = "link text"
    PARTIAL_LINK_TEXT = "partial link text"
    NAME = "name"
    TAG_NAME = "tag name"
    CLASS_NAME = "class name"
    CSS_SELECTOR = "css selector
    """

if __name__ == "__main__":
    start()