import sys

sys.path.append(r"./")
import math

import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
import torch.utils.data as data

import numpy as np
from numpy import *

from model.data_iterator import dataIterator
from model.Attention_RNN import AttnDecoderRNN
from model.Densenet_torchvision import densenet121

from PIL import Image


class InferModel:
    def __init__(self):
        self.dictionary = "./model/dictionary.txt"
        self.hidden_size = 256
        self.batch_size_t = 1
        self.maxlen = 100

        worddicts = self.load_dict(self.dictionary)
        self.worddicts_r = [None] * len(worddicts)
        for kk, vv in worddicts.items():
            self.worddicts_r[vv] = kk

        self.encoder = ""
        self.attn_decoder1 = ""
        self.load_models()

    def infer(self, x_t):
        attention, inference = self.query_model(x_t)
        inference_string = ""
        for i in range(attention.shape[0]):
            if inference[i] == "<eol>":
                continue
            else:
                inference_string = inference_string + inference[i]
        return inference_string

    def load_dict(self, dictFile):
        fp = open(dictFile)
        stuff = fp.readlines()
        fp.close()
        lexicon = {}
        for l in stuff:
            w = l.strip().split()
            lexicon[w[0]] = int(w[1])
        # print('total words/phones',len(lexicon))
        return lexicon

    def load_models(self):
        encoder_pt = densenet121()
        attn_decoder1_pt = AttnDecoderRNN(self.hidden_size, 112, dropout_p=0.5)
        self.encoder = torch.nn.DataParallel(encoder_pt)
        self.attn_decoder1 = torch.nn.DataParallel(attn_decoder1_pt)

        self.encoder.load_state_dict(
            torch.load(
                "./model/trained/encoder_v1.pkl", map_location=torch.device("cpu")
            )
        )
        self.attn_decoder1.load_state_dict(
            torch.load(
                "./model/trained/attn_decoder_v1.pkl", map_location=torch.device("cpu")
            )
        )

        self.encoder.eval()
        self.attn_decoder1.eval()

    def process(self, x_t):
        new_x_t = x_t / 255.0
        new_x_t = new_x_t.unsqueeze(0)
        new_x_t = new_x_t.unsqueeze(0)
        return new_x_t

    def query_model(self, x_t):
        h_mask_t = []
        w_mask_t = []

        x_t = self.process(x_t)
        # x_t = Variable(x_t)
        x_mask = torch.ones(x_t.size()[0], x_t.size()[1], x_t.size()[2], x_t.size()[3])
        x_t = torch.cat((x_t, x_mask), dim=1)
        x_real_high = x_t.size()[2]
        x_real_width = x_t.size()[3]
        h_mask_t.append(int(x_real_high))
        w_mask_t.append(int(x_real_width))
        x_real = x_t[0][0].view(x_real_high, x_real_width)
        output_highfeature_t = self.encoder(x_t)

        x_mean_t = torch.mean(output_highfeature_t)
        x_mean_t = float(x_mean_t)
        output_area_t1 = output_highfeature_t.size()
        output_area_t = output_area_t1[3]
        dense_input = output_area_t1[2]

        decoder_input_t = torch.LongTensor([111] * self.batch_size_t)

        decoder_hidden_t = torch.randn(self.batch_size_t, 1, self.hidden_size)
        decoder_hidden_t = decoder_hidden_t * x_mean_t
        decoder_hidden_t = torch.tanh(decoder_hidden_t)

        prediction = torch.zeros(self.batch_size_t, self.maxlen)

        prediction_sub = []
        label_sub = []
        decoder_attention_t = torch.zeros(
            self.batch_size_t, 1, dense_input, output_area_t
        )
        attention_sum_t = torch.zeros(self.batch_size_t, 1, dense_input, output_area_t)
        decoder_attention_t_cat = []

        for i in range(self.maxlen):
            (
                decoder_output,
                decoder_hidden_t,
                decoder_attention_t,
                attention_sum_t,
            ) = self.attn_decoder1(
                decoder_input_t,
                decoder_hidden_t,
                output_highfeature_t,
                output_area_t,
                attention_sum_t,
                decoder_attention_t,
                dense_input,
                self.batch_size_t,
                h_mask_t,
                w_mask_t,
                0,
            )

            decoder_attention_t_cat.append(decoder_attention_t[0].data.numpy())
            topv, topi = torch.max(decoder_output, 2)
            if torch.sum(topi) == 0:
                break
            decoder_input_t = topi
            decoder_input_t = decoder_input_t.view(self.batch_size_t)

            # prediction
            prediction[:, i] = decoder_input_t

        k = np.array(decoder_attention_t_cat)
        x_real = np.array(x_real.data)

        prediction = prediction[0]

        prediction_real = []
        for ir in range(len(prediction)):
            if int(prediction[ir]) == 0:
                break
            prediction_real.append(self.worddicts_r[int(prediction[ir])])
        prediction_real.append("<eol>")

        prediction_real_show = np.array(prediction_real)

        return k, prediction_real_show
