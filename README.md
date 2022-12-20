# steep-qa-agent
A quality assessment agent for the Ubisoft game Steep using Deep Q-learning.

## Overview
This is a implementation of Deep-Q learning on Steep , to automate gameplay
by maximising points scored through stunts , or actions.
To get started :
1. Have a brief idea of Reinforced Learning and Deep-Q learning , policy functions 
and q-functions.
2. Get some idea about CNN's , as I have used them for feature vector extraction

Overview-
1. Made a object classification model on the dataset in image_dataset, manually
   annotating approx. 150-200 images , on three prominent classes trees,
   rocks, trunks.
2. Made a Reinforced based model which feeds the game image to the CNN
   and takes the output vector and maps the image state to the vector.
3. Keeps learning based on rewards recieved , on actions implemented per
   state. 