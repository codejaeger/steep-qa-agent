import numpy as np
import pytesseract as pt
import cv2
from CNN import CNN
from PIL import Image
from keys import *
from grabscreen import *


class Steep(object):
    """
    This class acts as the intermediate "API" to the actual game. Double quotes API because we are not touching the
    game's actual code. It interacts with the game simply using screen-grab (input) and keypress simulation (output)
    using some clever python libraries.
    """
    #declare a CNN class object
    cnn_graph = CNN()
    def __init__(self):
        self.reset()

    """
    this function is the reward approximating function , given rewards captured from the screen using call to grabscreen.py we get the rewards 
    and scale them accordingly . Idlescore is a measure of the time the score remains idle in the screen.
    Totscore is a measure of total recorded score till now , tmepscore , is temproray score from the screen.
    """
    def _get_reward(self,totscore,tempscore):
        # screen = grab_screen(region=None)
        ingame_reward = 0
        if True:
            if totscore - self.reward > 0:
                self.reward = totscore
                # print(self.reward,totscore)
                # time.sleep(2)                        #remove this later
                ingame_reward = 1
                self.idlescore=0
            elif tempscore - self.temprew > 0:
                self.temprew = tempscore
                ingame_reward = 1
                self.idlescore = 0  
            elif tempscore - self.temprew < 0 and tempscore != 0:
                self.temprew = self.temprew
                ingame_reward = 1
                self.idlescore = 0
            elif totscore - self.reward < -1:
                self.reward = totscore
                ingame_reward = 0
                self.idlescore +=1
            elif self.idlescore <= 10 and self.idlescore > 2:
                self.idlescore+=1
                ingame_reward = 1/(pow(2,self.idlescore-1))
            elif self.idlescore <= 10:
                ingame_reward = 1/(self.idlescore+1)
                self.idlescore +=1
            elif totscore - self.reward ==0:
                ingame_reward = 0.5
                self.idlescore +=1
        else:
            return 1;
            # self.badac[0] = relim
        return ingame_reward
        # print('q-learning reward: ' + str(ingame_reward))
        # except:
        # ingame_reward = -1 if self._is_over(action) else 0 wddaw
        # print('exception q-learning reward: ' + str(ingame_reward))
    """
    This function gets the feature map from the CNN model after passing the captured image to it . This feature maps serves as the representation of the current 
    state.
    """
    def observe(self):
        im = grab_screen()
        relim = rel_mg(im)
        state = self.cnn_graph.get_image_feature_map(relim)
        return state
    """
     These functions reset the game to the start of the game after a Knock Out.
    """
    def rst(self):
        PressKey(tab)
        time.sleep(4)
        ReleaseKey(tab)
    def mrst(self):
        PressKey(M)
        time.sleep(4)
        ReleaseKey(M)
    # def gameov(self):
    #     if self.idlescore > 5:
    #         PressKey(tab)WWD
    #         time.sleep(6)W
    #     else:
    #         return
    """
    This is the main function which takes in command from the train.py file and preforms those actions and gets the feedback of performing those action from the
    game screen . 
    """            
    def act(self, action,action_do):
        if action_do==1:
            # display_action = ['forward', 'jump', 'left', 'right']
            """
            put actions to be performed here , maybe stunts , put them into the second position and change the commands to be pressed in the line 110-123
            here I have performed the flipping action
            """
            display_action = ['forward', 'stop', 'left', 'right']
            print('action: ' + str(display_action[action]))
            keys_to_press = [[W], [S], [A], [D]]
            # for key in keys_to_press[action]:
            #     PressKey(key)
            #     time.sleep(0.4)                                                  #<-delay
            #     ReleaseKey(key)
            if action ==0:                                                          #respective actions 
                PressKey(W)
                time.sleep(0.2)
                ReleaseKey(W)
            elif action ==1:                                                              
                PressKey(W)
                PressKey(spacebar)
                time.sleep(0.5)
                ReleaseKey(spacebar)
                ReleaseKey(W)
                PressKey(A)
                time.sleep(0.25)
                ReleaseKey(A)
                PressKey(D)
                time.sleep(0.25)
                ReleaseKey(D)
                time.sleep(0.4) 
            else:
                for key in keys_to_press[action]:
                    ReleaseKey(W)
                    PressKey(key)
                    time.sleep(0.5)
                    ReleaseKey(key)
                    ReleaseKey(W)
            # time.sleep(1) if action == 0 else time.sleep(0.8)
            # for key in keys_to_press[action]:
            #     ReleaseKey(key)
        # st = time.time()
        #get feedback from screen
        relim,totscore,tempscore,over = getinfo(self.reward,self.temprew)
        # en = time.time()
        # d = en - st
        # with open('time_dif.txt', 'a') as f:
        #     f.write("ocr_and_scree  %s" % d)
            # f.write('\n')
        # self.ch = booster
        reward = self._get_reward(totscore,tempscore)
        # self.gameov()
        print(self.idlescore)
        game_over = False
        if self.idlescore > 10:
            game_over = True
            self.rst()
        elif over:
            game_over = True
            self.mrst()
        else:
            time.sleep(0)
        return self.observe(), reward , game_over

    def reset(self):
        self.reward = 0
        self.temprew = 0
        self.idlescore = 0
        # self.action_stack = []
        self.ch = False
        self.rst()
        return
