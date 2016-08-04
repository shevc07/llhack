#-*- coding: utf-8 -*-

import json

f=open('song_notes/youqin_nochange_ex.json','r')
fo=f.read()
s=json.loads(fo)

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
    print "notes_level",i["notes_level"],"effect",i["effect"],"position",i["position"],"notes_attribute",i["notes_attribute"],"timing_sec",i["timing_sec"],"effect_value",i["effect_value"]
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
for j in range(notes_num):

    if effect[j] != 3:
        effect_value[j] = 50
    #print effect[j],position[j],timing_sec[j],effect_value[j]
    #1是touchdown,0是touchup
    a.append((position[j],1,timing_sec[j]))
    a.append((position[j],0,timing_sec[j]+effect_value[j]))


#排序
a.sort(key=lambda x:x[2])

to_del = []
count = 0

for i in range(len(a)-1):
    if ((a[i+1][2] - a[i][2]) >= 0 and (a[i+1][2] - a[i][2]) <= 5 ) :
        count = count + 1
        print a[i]
        print a[i+1]
        print "111111111111111111111 %d, %d"%((a[i+1][2] - a[i][2]), count)
    else:
        to_del.append(a[i])
to_del.append(a[-1])
a=to_del

for i in range(len(a)-1):
    print a[i][0], a[i][1], a[i+1][2] - a[i][2]
print a[-1][0],a[-1][1],a[-1][2] - a[-2][2]


def Func(input):
    m = 1
    c=""
    if (input == 0):
        return "c0"
    for i in range(1,1024,1):
        if (m & input == m):
            c=c+"c%d+"%m
        m = m << 1
    return c[:-1]

hl=['LOW','HIGH']

#生成串行arduino执行码
for i in range(2,len(a)-1):
    print "digitalWrite(pin%d,%s);delay(%s);"%(a[i][0], hl[a[i][1]], Func(a[i+1][2] - a[i][2]))
print "digitalWrite(pin%d,%s);delay(%s);"%(a[-1][0],hl[a[-1][1]],Func(a[-1][2] - a[-2][2]))
#
for i in range(2,len(a)-1):
    print "digitalWrite(pin%d,%s);delay(%s);"%(a[i][0], hl[a[i][1]], a[i+1][2] - a[i][2])
print "digitalWrite(pin%d,%s);delay(%s);"%(a[-1][0],hl[a[-1][1]], a[-1][2] - a[-2][2])

# for i in range(len(a)-1):
#     print "arr[%d]"
#生成2进制形态的arduino执行码
byte2=['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']#从右至左1-9

for i in range(2,len(a)-1):
    byte2[16-a[i][0]] = str(a[i][1])
    #print "".join(byte2)
    print "PORTB = B%s;"%("".join(byte2[:8])),
    print "PORTD = B%s;delay(%d);"%("".join(byte2[8:]),a[i+1][2] - a[i][2])
byte2[16-a[-1][0]] = str(a[-1][1])
#print "".join(byte2)
print "PORTB = B%s;"%("".join(byte2[:8])),
print "PORTD = B%s;delay(%d);"%("".join(byte2[8:]),a[-1][2] - a[-2][2])

