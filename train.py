import numpy as np
import time
import random
from getkeys import key_check
from ExperienceReplay import ExperienceReplay
from threading import Thread

# parameters
# epsilon = .2  # exploration
num_actions = 4  # [ FORWARD, ANY_STUNT, left_arrow, right_arrow]
max_memory = 1000  # Maximum number of experiences we are storing
batch_size = 4  # Number of experiences we use for training per batch

exp_replay = ExperienceReplay(max_memory=max_memory)
action_stack = []

def save_model(model):
    # serialize model to JSON
    model_json = model.to_json()
    with open("model_epoch1000/model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("model_epoch1000/model.h5")
    # print("Saved model to disk")

def keycomm_append(stop):
    while True:
        p = key_check()
        # print(p?)
        ch = 'W'
        if 'A' in p:
            ch = 'A'
        elif 'D' in p:
            # g.append('D')
            ch ='D'
        elif 'space' in p:
            # g.append('space')
            ch = 'space'
        if len(action_stack)==0:
            action_stack.append(ch)
        elif action_stack[len(action_stack)-1]!=ch:
            action_stack.append(ch)
        if stop():
            break

def train(game, model, epochs, verbose=1):
    # Train
    # Reseting the win counter
    win_cnt = 0
    # We want to keep track of the progress of the AI over time, so we save its score count history
    win_hist = []
    # Epochs is the number of games we play
    for e in range(epochs):
        loss = 0.
        eps = pow(2,-1-e)
        # epsilon = 1 / ((e + 1) ** (1 / 2))
        # Resetting the game
        game.reset()
        game_over = False
        stop = False
        t = Thread(target = keycomm_append , args=(lambda : stop, ))
        t.start()
        # get tensorflow running first to acquire cudnn handle
        input_t = game.observe()
        dik = {'A': 2, 'D': 3, 'space': 1,'W' : 0}
        # if e == 0:
        #     paused = True
        #     print('training is paused')
        # else:
        #     paused = False
        st = time.time()
        en = time.time()
        """
        We want to avoid that the learner settles on a local minimum. That is why 
        initially choose actions randomly.
        """
        while (not game_over) and en-st < 22:
            ar = []
            if True:
                input_tm1 = input_t
                if False:
                    print('pickup action')
                    time.sleep(0.5)
                    l = key_check()
                    action = 0
                    if 'A' in l:
                        action = 2
                    elif 'D' in l:
                        action = 3
                    elif 'space' in l:
                        action = 1
                    elif 'W' in l:
                        if len(action_stack)!=0:
                            action = dik[action_stack[0]]
                            del action_stack[0]
                        else:
                            action = 0
                    else:
                        action = 0
                    input_t, reward, game_over = game.act(action,0)
                    if 'P' in l:
                        game_over = True
                        game.rst()
                        game.reset()
                        break
                    print(action)
                    # action = int(np.random.randint(0, num_actions, size=1))
                    # print('random action')
                elif eps > random.random() :
                    # Pick something random
                    action = int(np.random.randint(0, num_actions, size=1))
                    # input_t, reward, game_over = game.act(action,1)
                    print('random action')
                    print(action)
                else:
                    print('predicted action')
                    # Choose yourself
                    # q contains the expected rewards for the actions
                    q = model.predict(input_tm1)
                    # We pick the action with the highest expected reward
                    action = np.argmax(q[0])
                    # input_t, reward, game_over = game.act(action,1)
                sta = time.time()
                # apply action, get rewards and new state
                input_t, reward, game_over = game.act(action,1)
                ena = time.time()
                # ar=[]
                ar.append(ena-sta-0.4)
                win_cnt += reward
                """
                The experiences < s, a, r, s’ > we make during gameplay are our training data.
                Here we first save the last experience, and then load a batch of experiences to train our model
                """

                # store experience
                exp_replay.remember([input_tm1, action, reward, input_t], game_over)
                # Load batch of experiences
                sta = time.time()
                inputs, targets = exp_replay.get_batch(model, batch_size=batch_size)
                ena = time.time()
                ar.append(ena-sta)
                # train model on experiences
                sta = time.time()
                batch_loss = model.train_on_batch(inputs, targets)
                ena = time.time()
                ar.append(ena-sta)
                with open('time_dif.txt', 'a') as f:
                    for idd in ar:
                        f.write(" %s" % idd)
                    f.write('\n')
                # print(loss)
                loss += batch_loss
                # print(str(en-st)+"Hi")
                # time.sleep(3)
                # 
        stop=True
        t.join()
            # keys = key_check()
            # if 'P' in keys:
            #     if paused:
            #         paused = False
            #         print('unpaused!')
            #         time.sleep(1)
            #     else:
            #         print('Pausing!')
            #         paused = True
            #         time.sleep(1)
            # elif 'O' in keys:
            #     print('Quitting!')
            #     return
        if verbose > 0:
            with open('times.txt', 'a+') as f:
                f.write("Epoch {:03d}/{:03d} | Loss {:.4f} | Win count {}".format(e, epochs, loss, win_cnt))
                f.write("\n")
            # print("Epoch {:03d}/{:03d} | Loss {:.4f} | Win count {}".format(e, epochs, loss, win_cnt))
        save_model(model)
        win_hist.append(win_cnt)
    return win_hist
