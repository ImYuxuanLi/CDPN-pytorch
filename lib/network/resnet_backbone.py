import torch.nn as nn
import math
import torch
from torchvision.models.resnet import BasicBlock, Bottleneck

class ResNetBackboneNet(nn.Module):
    def __init__(self, block, layers, in_channel=3, freeze=False):
        super(ResNetBackboneNet, self).__init__()
        self.freeze = freeze
        self.inplanes = 64

        self.conv1 = nn.Conv2d(in_channel, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.layer1 = self._make_layer(block, 64, layers[0])
        self.layer2 = self._make_layer(block, 128, layers[1], stride=2)
        self.layer3 = self._make_layer(block, 256, layers[2], stride=2)
        self.layer4 = self._make_layer(block, 512, layers[3], stride=2)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.normal_(m.weight, mean=0, std=0.001)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

    def _make_layer(self, block, planes, blocks, stride=1):
        downsample = None
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(self.inplanes, planes * block.expansion,
                          kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(planes * block.expansion),
            )
        layers = []
        layers.append(block(self.inplanes, planes, stride, downsample))
        self.inplanes = planes * block.expansion
        for i in range(1, blocks):
            layers.append(block(self.inplanes, planes))

        return nn.Sequential(*layers)

    def forward(self, x):
        if self.freeze:
            with torch.no_grad():
                x = self.conv1(x)  
                x = self.bn1(x)
                x = self.relu(x)
                x = self.maxpool(x) 
                x = self.layer1(x) 
                x = self.layer2(x) 
                x = self.layer3(x) 
                x = self.layer4(x)  
                return x
        else:
            x = self.conv1(x)  
            x = self.bn1(x)
            x = self.relu(x)
            x = self.maxpool(x) 
            x = self.layer1(x) 
            x = self.layer2(x) 
            x = self.layer3(x) 
            x = self.layer4(x)  
            return x 
