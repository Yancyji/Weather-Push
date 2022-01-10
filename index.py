# -*- coding: utf8 -*-
import requests
import json
import yaml
import time


def getApi(name, url, params):
    '''
    get方式调用api
    :param name: api名称
    :param url: api链接
    :param params: api参数（dict）
    :return: api返回值
    '''
    res = json.loads(requests.get(url, params).text)
    print('【{}】接口测试正常✔'.format(name))
    return res


def getWeather(dirItem):
    '''
    调用api获取天气信息
    :param dirId: 地区编码
    :return: 今日天气信息
    '''
    weatherUrl = "https://v0.yiketianqi.com/api"
    weatherParams = {'key': 'c369a5115a88fe279e8c6de3ba5fd8c7', # 易客api接口，每个账号有2000次的测试使用机会，超过需要付费
                     'extensions': 'all',
                     'version': 'v61',
                     'appid': '68989296',
                     'appsecret': '20MTQHFn',
                     'province': dirItem[0],
                     'city': dirItem[1],
                     }
    return getApi('天气api', weatherUrl, weatherParams)


# def getYiyan():
#     '''
#     一言
#     :return: 一言
#     '''
#     yiyanUrl = 'https://api.uixsj.cn/hitokoto/get'
#     yiyanParams = {'type': 'hitokoto', 'code': 'json'}
#     return '【一言】' + str(getApi('一言', yiyanUrl, yiyanParams)['content']) + "\n"


def getInfo(res):
    '''
    从获取的天气信息中筛选要发送的数据
    :param res: 天气信息
    :return: 要发送的数据
    '''
    dataList = []
    date = res['date']
    week = res['week']
    wea = res['wea']
    wea_img = res['wea_img']
    tem = res['tem']
    tem1 = res['tem1']
    tem2 = res['tem2']
    win = res['win']
    win_speed = res['win_speed']
    visibility = res['visibility']
    air_level = res['air_level']
    air_tips = res['air_tips']
    pm25_desc = res['aqi']['pm25_desc']
    yundong = res['aqi']['yundong']

    dataList.extend(
        [date, week, wea, wea_img, tem, tem1, tem2, win, win_speed, visibility, air_level, air_tips, pm25_desc,
         yundong])  # python同时添加多个元素
    return dataList


def QQPusher(qqNum, dataList):
    '''
    调用QQPusher接口，给指定qq发送消息
    :param qqNum: qq
    :param dataList: 要发送的数据列表
    :param Token: 调用QQPusher所需的Token
    '''
    QQPusherUrl = 'http://api.qqpusher.yanxianjun.com/send_private_msg'
    QQPusherParams = {
        'token': 'ec74aea16af00cff8cf883d800bfc954',
        'user_id': qqNum,
        'message': '今日天气推送🍀 \n---\n{}，{}\n{} ， {}\n{}  {}，{}/{} ℃\n{}，{}\n空气质量：{}，pm2.5：{}\n运动指数：{}\n---\n{}\n---\n当前气温：{}℃，能见度：{}\n温馨提示：疫情期间，外出请佩戴口罩！'.format(
            dataList[0], dataList[1], dataList[14], dataList[15], dataList[2], dataList[16], dataList[6], dataList[5],
            dataList[7], dataList[8], dataList[10], dataList[12], dataList[13], dataList[11], dataList[4], dataList[9])
    }
    return getApi('QQPusher', QQPusherUrl, QQPusherParams)


def QQGroupPusher(qqNum, dataList):
    '''
    调用QQPusher接口，给指定qq群发送消息
    :param qqNum: qq群
    :param dataList: 要发送的数据列表
    :param Token: 调用QQPusher所需的Token
    '''
    QQPusherUrl = 'http://api.qqpusher.yanxianjun.com/send_group_msg'
    QQPusherParams = {
        'token': 'ec74aea16af00cff8cf883d800bfc954',
        'group_id': qqNum,
        'message': '今日天气推送 🍀 \n---\n{}，{}\n{} ， {}\n{}  {}，{}/{} ℃\n{}，{}\n空气质量：{}，pm2.5：{}\n运动指数：{}\n---\n{}\n---\n当前气温：{}℃，能见度：{}\n温馨提示：疫情期间，外出请佩戴口罩！'.format(
            dataList[0], dataList[1], dataList[14], dataList[15], dataList[2], dataList[16], dataList[6], dataList[5],
            dataList[7], dataList[8], dataList[10], dataList[12], dataList[13], dataList[11], dataList[4], dataList[9])
    }
    return getApi('QQPusher', QQPusherUrl, QQPusherParams)

# QQPusher不可用，更换为Qmsg推送
def QmsgPusher(qq, dataList,group):
    KEY='3f12525c784ff61d79132d247035b5e2'#此处替换为你自己的KEY，在Qmsg酱官网登录后，在控制台可以获取KEY
    data={
        "msg":"今日天气推送 🍀 \n---\n{}，{}\n{} ， {}\n{}  {}，{}/{} ℃\n{}，{}\n空气质量：{}，pm2.5：{}\n运动指数：{}\n---\n{}\n---\n当前气温：{}℃，能见度：{}\n温馨提示：疫情期间，外出请佩戴口罩！".format(
            dataList[0], dataList[1], dataList[14], dataList[15], dataList[2], dataList[16], dataList[6], dataList[5],
            dataList[7], dataList[8], dataList[10], dataList[12], dataList[13], dataList[11], dataList[4], dataList[9]), #需要发送的消息
        "qq":qq #需要接收消息的QQ号码
    }
    url='https://qmsg.zendee.cn/send/'+KEY#私聊消息推送接口
    if group == 1:
        url='https://qmsg.zendee.cn/group/'+KEY#群消息推送接口
    response = requests.post(url,data=data)
    print(response.json())
    return response.json()

def main_handler(event, context):
    file = open('userData.yml', 'r', encoding="utf-8")  # 从配置文件中获取数据（str）
    file_data = file.read()
    file.close()

    data = yaml.load(file_data, Loader=yaml.FullLoader)  # str转dict

    userData = data['userData']

    dataDict = []  # 存放用户数据（地区，qq）
    for key, value in userData.items():
        dict = {'province': value[0], 'city': value[1], 'qq': str(value[2])}
        dataDict.append(dict)

    for i in range(len(dataDict)):
        print("---正在获取【{},{}】的天气！---".format(dataDict[i]['province'], dataDict[i]['city']))
        res = getWeather((dataDict[i]['province'], dataDict[i]['city']))  # 获取天气信息

        dataList = getInfo(res)  # 存放从api中获取的天气天气数据
        dataList.append(dataDict[i]['province'])
        dataList.append(dataDict[i]['city'])
        dataList.append(
            dataList[3].replace('xue', '❄').replace('lei', '⚡').replace('shachen', '🌪').replace('wu', '🌫').replace(
                'bingbao', '🌨').replace('yun', '☁').replace('yu', '🌧').replace('yin', '🌥').replace('qing', '☀'))
        time.sleep(2)

        # dataList.append(getYiyan())  # 一言
        # time.sleep(2)

        if 'g' in dataDict[i]['qq']:
            dataDict[i]['qq'] = dataDict[i]['qq'][1:]
            #QQGroupPusher(dataDict[i]['qq'], dataList)
            QmsgPusher(dataDict[i]['qq'], dataList,1)
        else:
            #QQPusher(dataDict[i]['qq'], dataList)
            QmsgPusher(dataDict[i]['qq'], dataList,0)
        print("---天气推送成功！---")
        time.sleep(20)
        

# 本地测试
if __name__=='__main__':
    file = open('userData.yml', 'r', encoding="utf-8")  # 从配置文件中获取数据（str）
    file_data = file.read()
    file.close()

    data = yaml.load(file_data, Loader=yaml.FullLoader)  # str转dict

    userData = data['userData']

    dataDict = []  # 存放用户数据（地区，qq）
    for key, value in userData.items():
        dict = {'province': value[0], 'city': value[1], 'qq': str(value[2])}
        dataDict.append(dict)

    for i in range(len(dataDict)):
        print("---正在获取【{},{}】的天气！---".format(dataDict[i]['province'], dataDict[i]['city']))
        res = getWeather((dataDict[i]['province'], dataDict[i]['city']))  # 获取天气信息

        # 易客的接口返回不是很友好，成功只给返回内容不给状态码，调用失败才有状态码
        print(res)
        # if res['errcode'] != None:
        #     print("Error:"+res['errmsg'])
        #     exit()  
        dataList = getInfo(res)  # 存放从api中获取的天气天气数据
        dataList.append(dataDict[i]['province'])
        dataList.append(dataDict[i]['city'])
        dataList.append(
            dataList[3].replace('xue', '❄').replace('lei', '⚡').replace('shachen', '🌪').replace('wu', '🌫').replace(
                'bingbao', '🌨').replace('yun', '☁').replace('yu', '🌧').replace('yin', '🌥').replace('qing', '☀'))
        time.sleep(2)

        # dataList.append(getYiyan())  # 一言
        # time.sleep(2)

        if 'g' in dataDict[i]['qq']:
            dataDict[i]['qq'] = dataDict[i]['qq'][1:]
            #QQGroupPusher(dataDict[i]['qq'], dataList)
            QmsgPusher(dataDict[i]['qq'], dataList,1)
        else:
            #QQPusher(dataDict[i]['qq'], dataList)
            QmsgPusher(dataDict[i]['qq'], dataList,0)
        print("---天气推送成功！---")
        time.sleep(20)

# 代码可以优化一下，后面再处理吧        