# -*- coding: utf-8 -*-

import pygame
import sys
from human import human
import time

class paintMod:

    def __init__(self, screenSize = (1280, 720), backgroundColor = (255, 255, 255)):
        self.floorColor = {
            "livingRoom"           :           (189, 33, 25),
            "masterBedroom"        :           (247, 148,99),
            "secondBedroom"        :           (255, 230, 8),
            "thirdBedroom"         :           (214, 148, 25),
            "bathroom"             :           (41, 181, 206),
            "kitchen"              :           (247, 255, 247),
            "diningRoom"           :           (115, 123, 181),
            "studyRoom"            :           (82, 82, 41)
        }

        self.wallColor = {
            "livingRoom"           :           (164, 8, 0),
            "masterBedroom"        :           (222, 123, 74),
            "secondBedroom"        :           (230, 205, 0),
            "thirdBedroom"         :           (189, 123, 0),
            "bathroom"             :           (16, 156, 181),
            "kitchen"              :           (222, 230, 222),
            "diningRoom"           :           (90, 98, 156),
            "studyRoom"            :           (57, 57, 17)
        }

        self.isRunning = True

        pygame.init()

        self.ratio = 15

        # self.manColor = (255, 0, 0)
        
        # self.textFont = pygame.font.SysFont('arial', 22)
        # self.textFont = pygame.font.Font(None, 20)
        # self.text = self.textFont.render('', 1, (0, 0, 0) )
        # self.textPos = text.get_rect()
        self.screenSize = screenSize
        self.backgroundColor = backgroundColor
        # pygame初始化
        
        # 创建一个窗口
        self.screen = pygame.display.set_mode(self.screenSize, 0, 32)
        pygame.display.set_caption('Draw rect and circle')
        #背景填充
        self.screen.fill(self.backgroundColor)
        self.manImage = pygame.image.load('./pic/head_small.png')

        # self.temp = 0

    def drawPicture(self, man):
        for pygameEvent in pygame.event.get():
            # 按下关闭按钮，退出程序
            if(pygameEvent.type == pygame.QUIT):
                sys.exit()
            if(pygameEvent.type == pygame.KEYDOWN):
                self.isRunning = not self.isRunning
        
        # 清屏
        from light import lightSimulator
        outDoorLight = lightSimulator()
        self.screen.fill( self.changeColor( outDoorLight.getPercentage( man.getCurrentTime() ) , self.backgroundColor ) )

        # 根据房间信息绘制图形
        for tempRoom in man.getHouse().getRoomList():
            tempLeft = tempRoom.getLeft() * self.ratio
            tempTop = tempRoom.getTop() * self.ratio
            tempWidth = (tempRoom.getRight() - tempRoom.getLeft() + 1) * self.ratio
            tempHeight = (tempRoom.getBottom() - tempRoom.getTop() + 1) * self.ratio
            tempFloorColor = self.floorColor.get(tempRoom.getType())
            tempFloorColor = self.changeColor(tempRoom.getLightPercentage(man.getCurrentTime()), tempFloorColor)
            tempWallColor = self.wallColor.get(tempRoom.getType())
            pygame.draw.rect(self.screen, tempFloorColor, [tempLeft, tempTop, tempWidth, tempHeight])
            pygame.draw.rect(self.screen, tempWallColor, [tempLeft, tempTop, tempWidth, tempHeight], 2)
            self.printOnScreen(str = tempRoom.getType(), pos = ( tempLeft+tempWidth/2, tempTop+tempHeight/2 ), color = (200, 200, 200))

        for tempRoom in man.getHouse().getRoomList():
            for tempDevice in tempRoom.getDeviceList():
                tempImage = tempDevice.getImage()
                tempPos = tempImage.get_rect()
                tempPos.centerx = tempDevice.getPosX()*self.ratio
                tempPos.centery = tempDevice.getPosY()*self.ratio
                self.screen.blit(tempImage, tempPos)


        tempPos = self.manImage.get_rect()
        tempPos.centerx = man.getPosX()*self.ratio
        tempPos.centery = man.getPosY()*self.ratio
        self.screen.blit(self.manImage, tempPos )
        # pygame.draw.circle(self.screen, self.manColor, (man.getPosX()*self.ratio, man.getPosY()*self.ratio), 5)      
        dayStr = time.strftime("%Y %m %d %A", time.localtime( man.getCurrentTime() )   )
        self.printOnScreen(str = u'Day:     %s' %dayStr, font = 'arial', pos = (40*self.ratio , 15), mode = 'LEFT_TOP', color = (150,150,150) )
        self.printOnScreen(str = u'Time:    %s' %man.getCurrentTimeStr(), font = 'arial', pos = (40*self.ratio , 35), mode = 'LEFT_TOP', color = (150,150,150) )
        self.printOnScreen(str = u'Temp:    %.2f'  %man.getSimT().getCurrentTemperature(), font = 'arial', pos = (40*self.ratio,55), mode = 'LEFT_TOP', color = (150,150,150))
            # pygame.draw.circle(self.screen, self.manColor, (int(self.temp), int(self.temp)), 5)
            # self.temp = self.temp + 0.1                

        # print(man.getCurrentTimeStr(), man.getPos())
       
        # self.screen.blint(text_screen)
        # 重画屏幕
        pygame.display.flip()
        time.sleep(0.001)
        # print('paint picture')
    
    def printOnScreen(self, str = '', font = None, size = 20, color = (0, 0, 0), pos = (0, 0), mode = 'CENTER'):
        textFont = pygame.font.SysFont(font, size)
        text = textFont.render(str, 1, color )
        textPos = text.get_rect()
        if( mode == 'LEFT_TOP' ):
            textPos.left = pos[0]
            textPos.top = pos[1]
        elif( mode == 'CENTER' ):
            textPos.centerx = pos[0]
            textPos.centery = pos[1]
        else:
            textPos.left = pos[0]
            textPos.top = pos[1]
        self.screen.blit(text, textPos)


    def changeColor(self, percentage = 1.00,  color = (255, 255, 255) ):
        r = color[0] * percentage
        g = color[1] * percentage
        b = color[2] * percentage
        return (r, g, b)

    def isRun(self):
        return self.isRunning