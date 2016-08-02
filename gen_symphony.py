#-*- coding: utf-8 -*-

import json

#竖屏坐标
screen = []
screen.append((0,0))
screen.append((560,1150))
screen.append((380,1100))
screen.append((230,1000))
screen.append((130,850))
screen.append((90,670))
screen.append((130,500))
screen.append((230,340))
screen.append((380,240))
screen.append((560,200))

f=open('nobrandgirl_easy.json','r')
fo=f.read()
s=json.loads(fo)

#print s
#print s.keys()
live_difficulty_id=s["response_data"]["live_info"][0]["live_difficulty_id"]
is_random=s["response_data"]["live_info"][0]["is_random"]
dangerous=s["response_data"]["live_info"][0]["dangerous"]
#use_quad_point=s["response_data"]["live_info"][0]["use_quad_point"]
notes_speed=s["response_data"]["live_info"][0]["notes_speed"]

print "live_difficulty_id",live_difficulty_id
print "is_random",is_random
print "dangerous",dangerous
#print "use_quad_point",use_quad_point
print "notes_speed",notes_speed


notes_list=s["response_data"]["live_info"][0]["notes_list"]

notes_num=len(notes_list)+1

notes_level=[0]*notes_num
effect=[0]*notes_num
position=[0]*notes_num
notes_attribute=[0]*notes_num
timing_sec=[0]*notes_num
effect_value=[0]*notes_num

step=1
#处理notes
for i in notes_list:
    #print "notes_level",i["notes_level"],"effect",i["effect"],"position",i["position"],"notes_attribute",i["notes_attribute"],"timing_sec",i["timing_sec"],"effect_value",i["effect_value"]
    notes_level[step]=int(i["notes_level"])
    effect[step]=int(i["effect"])
    position[step]=int(i["position"])
    notes_attribute[step]=int(i["notes_attribute"])
    timing_sec[step]=int(float(i["timing_sec"])*1000)
    effect_value[step]=int(float(i["effect_value"])*1000)
    step=step+1

    #notes_level:未知
    #effect:1普通单击,2活动物品,3普通长按,4星星单击
    #position:从右向左1-9
    #notes_attribute:未知
    #timing_sec:时序
    #effect_value:2单击,非2长按时间

    #notes_level,notes_attribute暂时不用
a= []

#转化为串行，同时将第一个节拍调整为0
for j in range(notes_num-1):

    if effect[j] != 3:
        effect_value[j] = 50
    #print effect[j],position[j],timing_sec[j],effect_value[j]
    #1是touchdown,0是touchup
    a.append((position[j],1,timing_sec[j]))
    a.append((position[j],0,timing_sec[j]+effect_value[j]))

#排序
a.sort(key=lambda x:x[2])

count = 0
for i in range(len(a)-1):
    if ((a[i+1][2] - a[i][2]) < 10 ) and ((a[i+1][2] - a[i][2]) > 0):
        count = count + 1
        print a[i]
        print a[i+1]
        print "111111111111111111111 %d",count

#转换为触动精灵脚本
for i in range(len(a)-1):
    if a[i][1] == 1:
        print "touchDown(%d, %d ,%d);"%(a[i][0],screen[a[i][0]][0],screen[a[i][0]][1])
    else:
        print "touchUp(%d, %d ,%d);"%(a[i][0],screen[a[i][0]][0],screen[a[i][0]][1])
    print "mSleep(%d);"%(a[i+1][2] - a[i][2])
print "touchUp(%d, %d ,%d);"%(a[-1][0],screen[a[i][0]][0],screen[a[i][0]][1])
print "mSleep(10000);"


#转换为按键精灵脚本
for i in range(len(a)-1):
    if a[i][1] == 1:
        print "TouchDownEvent %d, %d ,%d"%(screen[a[i][0]][0],screen[a[i][0]][1], a[i][0])
    else:
        print "touchUpEvent %d"%(a[i][0])
    print "Delay %d"%(a[i+1][2] - a[i][2])
print "touchUpEvent %d"%(a[-1][0])
print "Delay 10000"