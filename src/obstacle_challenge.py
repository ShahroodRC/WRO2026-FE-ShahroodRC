#!/usr/bin/env python3
from ev3dev2.sensor import INPUT_2,INPUT_4,INPUT_3
from ev3dev2.sensor import Sensor, INPUT_1
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sound import Sound
from ev3dev2.motor import MediumMotor, OUTPUT_B, OUTPUT_D, SpeedPercent
from time import sleep
import time
import math
from ev3dev2.button import Button
from ev3dev2.led import Leds


rast = UltrasonicSensor(INPUT_2)
chap = UltrasonicSensor(INPUT_3)


door=12

pixy = Sensor(INPUT_1)
pixy.mode = 'ALL'

sig = pixy.value(1) * 256 + pixy.value(0)

motor_a = MediumMotor(OUTPUT_B)
motor_b = MediumMotor(OUTPUT_D)
motor_a.reset() 
motor_b.reset()

btn = Button()
leds = Leds()
leds.set_color('LEFT', 'ORANGE')
leds.set_color('RIGHT', 'ORANGE')


btn.wait_for_bump('enter')
leds.set_color('LEFT', 'GREEN')
leds.set_color('RIGHT', 'GREEN')





def clamp(value, minimum, maximum):
    if value > maximum : value=maximum
    if value < minimum : value=minimum
    return value

def amotor(degrese,cl=50):
        diff =degrese

        diff=(diff-motor_a.position)*0.7

        motor_a.on(clamp(diff,-cl,cl))
        motor_a



p=0
jahat=0
sleep(0.2)
while p!= 100:
    r=rast.distance_centimeters
    c=chap.distance_centimeters
    if r>c : jahat=1+jahat
    else:jahat=jahat-1
    print(jahat)
    p=p+1

al=0
if jahat>0 :
    al=-1
    green = 250
    red = 27
    rang=[5,5]
    rangdovom=[2,1]
else:
    al=1
    green = 223
    red = 3
    rang=[1,2]
    rangdovom=[5,5]

print(al)

lastsig=0
a_timer=0
b_timer=0
lastpos=0
fasele=33
ghabeliat=False
Yignor=85

motor_a.on_for_seconds((-40)*al, 0.5)
motor_b.on_for_rotations(80,1)
motor_a.stop(stop_action='coast')
#motor_a.on_for_degrees(40,-motor_a.position)
sleep(0.6)
sig = pixy.value(1) * 256 + pixy.value(0) 

y = pixy.value(3) 

if y<Yignor:
    sig=0

if al > 0 :
    if sig==0:
        motor_a.stop(stop_action='coast')
        motor_a.on_for_degrees((100)*al,60)
        motor_b.on_for_rotations(60,1.5)
        motor_a.stop(stop_action='coast')
        motor_a.on_for_degrees((100),-motor_a.position)
        

    elif (sig == 2 ) and y > 100:
        motor_a.stop(stop_action='coast')
        motor_a.on_for_degrees((40),-motor_a.position)

        

        
    elif (sig==1 ) and y > 100 :
        motor_b.on_for_degrees(30,500)
        motor_a.on_for_seconds((40), 0.5)
        motor_b.on_for_rotations(60,1.8)
        motor_a.on_for_degrees((40),-motor_a.position)
        motor_a.stop(stop_action='coast')
        motor_b.stop(stop_action='coast')
    
else:
    if sig==0:
        motor_a.stop(stop_action='coast')
        motor_a.on_for_degrees((100)*al,60)
        motor_b.on_for_rotations(60,1.5)
        motor_a.stop(stop_action='coast')
        motor_a.on_for_degrees((100),-motor_a.position)



    elif (sig == 1 ) and y > 100 :
        motor_a.stop(stop_action='coast')
        motor_a.on_for_degrees((40),-motor_a.position)
        

        
    elif (sig==2 ) and y > 100 :
        motor_b.on_for_degrees(30,550)
        motor_a.on_for_seconds((40)*al, 0.5)
        motor_b.on_for_rotations(60,1.5)
        motor_a.on_for_degrees((40),-motor_a.position)
        motor_a.stop(stop_action='coast')
        motor_b.stop(stop_action='coast')

sleep(0.5)
speed =20
a_timer=0
motor_b.reset()
a=0

while True:

    if motor_b.position>1400 or (a==0):
        a=a+1

        motor_b.reset()



    



    print(a)
    
    sig = pixy.value(1) * 256 + pixy.value(0) 
    y = pixy.value(3) 
    if y<Yignor:
        sig=0
    x = pixy.value(2)
    size = pixy.value(4)
    motor_b.on(speed)

    
    if sig!=0:
        
        lastsig=sig

        


    if  a !=door :
            Yignor=95
           # fasele=32

            sig = pixy.value(1) * 256 + pixy.value(0)
            y = pixy.value(3) 

            if y<Yignor:
                sig=0
 
            if sig == 0:
             
                timeRang=time.time()
                navakht=-65
                while sig==0 and time.time()-timeRang <4:  

                    
                    if motor_b.position>1400:
                        motor_b.reset()
                        a=a+1


                    amotor(navakht*al)
                    if navakht<=-5:
                        navakht=navakht+1.5

                    sig = pixy.value(1) * 256 + pixy.value(0)
                    y = pixy.value(3) 
                    if y<Yignor:
                        sig=0
                    if sig != 0 :
                        print("hkar")
                        break

                    #print(time.time()-timeRang )
                    motor_b.on(20)
                    
                timeRang=time.time()
                while time.time()-timeRang <0.5 and sig ==0:
                    amotor(0)#ghhooooooooooooooooooooooooooooooooos
                    sig = pixy.value(1) * 256 + pixy.value(0)
                    y = pixy.value(3) 

                    if y<Yignor:
                        sig=0
                    if sig != 0 :
                        print("khar22")
                        break

                    motor_b.on((70))


            fasele = 33
            
    Yignor=85
    if y<110 and (sig==1):
        leds.set_color('LEFT', 'GREEN')
        leds.set_color('RIGHT', 'GREEN')
        target=(x-140)*0.7
        target=clamp(target,-20,20)
        amotor(target,35)
        speed = 40




    elif y<110 and (sig==2):
        leds.set_color('LEFT', 'RED')
        leds.set_color('RIGHT', 'RED')
        target=(x-110)*0.7
        target=clamp(target,-20,20)
        amotor(target,35)
        speed = 40


    elif sig == 1 :
         ghabeliat=True
         
         target=(x-green)*0.5
         leds.set_color('LEFT', 'GREEN')
         leds.set_color('RIGHT', 'GREEN')
         amotor(target,45)
         speed=22

    elif sig ==2:
         ghabeliat=True
         
         
         target=(x-red)*0.5
         leds.set_color('LEFT', 'RED')
         leds.set_color('RIGHT', 'RED')
         amotor(target,45)
         speed =22
        
   
        
    elif sig == 0:
        leds.all_off()
        speed = 33
        r=rast.distance_centimeters
        c=chap.distance_centimeters
        if al==1:
            oltra=c
        else:
            oltra=r  
        out= (fasele-oltra) *al
        out=clamp(out,-45,45)
        amotor(out)

    if lastsig ==2 and al>0 and sig ==0 :
        fasele =50


    if lastsig == 1 and al<0 and sig ==0 :
        fasele =50
        


    if fasele>33:
        
        fasele=fasele-0.09
    else: 
        fasele=33
   # print(fasele)
################################################


    
    if lastpos==motor_b.position:
        if b_timer==0:
            b_timer=time.time()
        #print(time.time()-b_timer)
        if time.time()-b_timer>0.3:
            print("khokafez")
            b_timer=0
            motor_a.on_for_degrees((40),-motor_a.position)
            motor_b.on_for_rotations(-100,1)

            motor_a.on_for_degrees((40),45*al)
            motor_b.on_for_rotations(100,0.8)



    lastpos=motor_b.position    
######################################
    if a==door:
        break
motor_a.off()
motor_b.off()



if al<0:
    navakht=45
    while True:
        motor_b.on(30)
        amotor(navakht)
        if navakht>=5:
            navakht=navakht-1.5


    motor_a.on_for_degrees((90),-120)
    motor_b.on_for_degrees((30),100)
    sleep(0.1)

    motor_a.on_for_degrees((90),-motor_a.position)

    sleep(0.1)

    while True:
        motor_b.on(-20)
        amotor(90)

    sleep(0.1)

    motor_a.on_for_degrees((90),-motor_a.position)
    motor_a.on_for_degrees((90),20)

    motor_b.on_for_degrees((30),150)

    sleep(0.1)

    while True:
        motor_b.on(10)
        amotor(-90)

    motor_a.stop(stop_action='coast')
    motor_a.on_for_degrees((60),-motor_a.position)
    sleep(0.4)

    motor_a.stop()
    motor_b.stop()
    out=0
    print(r)
    sleep(0.4)

    motor_a.on_for_degrees((90),20)

    motor_b.on_for_degrees((30),100)



    r=rast.distance_centimeters

    timeRang=time.time()
    speed=10
    while r>5 and time.time() - timeRang < 6:
        print(r)
        r=rast.distance_centimeters

        if r>5:
            out=-25                 ##################### line follwo
        else:
            out=25
        amotor(out)
        #speed=speed+0.1
        motor_b.on(speed)
    print(r)
     
    motor_a.on_for_degrees((60),-motor_a.position)
    motor_a.stop()

    motor_a.on_for_degrees((60),-motor_a.position)
    motor_a.stop()

    motor_b.on_for_degrees((-20),100)
    motor_b.stop()

    motor_a.on_for_degrees((60),150)
    motor_a.stop()

    motor_b.on_for_degrees((-20),495) ##
    motor_b.stop()

    motor_a.on_for_degrees((60),-motor_a.position)
    motor_a.stop()

    motor_a.stop(stop_action="coast")
    sleep(0.2)

    motor_a.on_for_degrees((60),-motor_a.position)
    motor_a.stop()

    motor_b.on_for_degrees((-20),332)
    motor_b.stop()

    motor_a.on_for_degrees((60),100)
    motor_a.stop()

    motor_b.on_for_degrees((-20),480)
    motor_b.stop()

    motor_a.on_for_degrees((60),-motor_a.position)
    motor_a.stop()

    motor_b.on_for_degrees((-20),280)
    motor_b.stop()

    motor_a.on_for_degrees((60),-200)
    motor_a.stop()

    motor_b.on_for_degrees((-20),300)
    motor_b.stop()

    motor_a.on_for_degrees((60),100)
    motor_a.stop()

    motor_b.on_for_degrees((15),100)
    motor_b.stop()

elif al > 0:
    navakht = 45
    while  True:
        motor_b.on(30)
        amotor(-navakht)
        if navakht <= 5:
            navakht = navakht - 1.5

   
    motor_a.on_for_degrees((90),120)
    motor_b.on_for_degrees((30),100)
    sleep(0.1)

    motor_a.on_for_degrees((90),-motor_a.position)

    sleep(0.1)

    while True:
        motor_b.on(-20)
        amotor(-90)

    sleep(0.1)

    motor_a.on_for_degrees((90), -motor_a.position)
    motor_a.on_for_degrees((90), -20)

    motor_b.on_for_degrees((30),150)

    sleep(0.1)

    while True:
        motor_b.on(10)
        amotor(90)

    motor_b.stop()
    motor_a.stop()

    motor_a.on_for_degrees((90), -motor_a.position)

    sleep(0.5)

    motor_a.on_for_degrees((90), -30)
    motor_b.on_for_degrees((30),150)


    out=0
    c = chap.distance_centimeters
    print(c)
    timeRang = time.time()
    speed = 15
    while time.time() - timeRang < 6:
        print(c)
        c = chap.distance_centimeters

        if time.time() - timeRang < 6:
            out = 25                   ##################### line follwo
        else:
            out = -25
        amotor(out)
        #speed = speed + 0.1
        motor_b.on(speed)
    motor_b.stop()
        
    motor_a.stop(stop_action='coast')
    motor_a.on_for_degrees((60),-motor_a.position)
    motor_a.stop()
    motor_a.stop(stop_action='coast')
    motor_a.on_for_degrees((60), 150)
    motor_a.stop()

    motor_b.on_for_degrees((-50), 500)
    motor_b.stop()
    sleep(0.1)
    motor_a.stop(stop_action='coast')
    motor_a.on_for_degrees((60), -300)
    motor_a.stop()

    motor_b.on_for_degrees((50), 500)
    motor_b.stop()

    fasele = 34
    r=rast.distance_centimeters
    motor_b.reset()
    speed = 15

    while motor_b.position < 1550:
        r=rast.distance_centimeters 
        print(r)
        if r <= fasele - 1:
            out = -35
        elif r >= fasele + 1:
            out = 35              ############### waaaaallll
        else:
            out = 0
        amotor(out)
        #speed = speed + 0.1
        motor_b.on(speed)

    print(r)
    motor_a.stop()
    motor_b.stop()
    sleep(1)
    motor_a.stop(stop_action='coast')
    motor_a.on_for_degrees((60), -300)
    motor_a.stop()

    motor_b.on_for_degrees((25), 550)
    motor_b.stop()
    sleep(0.2)
    motor_a.stop(stop_action='coast')
    motor_a.on_for_degrees((60), 80)
    motor_a.stop()
    sleep(0.2)

    motor_b.on_for_degrees((-15), 425)
    motor_b.stop()
    motor_a.stop(stop_action='coast')
    motor_a.on_for_degrees((60), 150)
    motor_a.stop()

    motor_b.on_for_degrees((-15), 625)
    motor_b.stop()
    motor_a.stop(stop_action='coast')
    motor_a.on_for_degrees((60), -300)
    motor_a.stop()

    motor_b.on_for_degrees((15), 121)
    motor_b.stop()
    motor_a.stop(stop_action='coast')
    motor_a.on_for_degrees((60),-motor_a.position)


motor_b.off()
motor_a.off()