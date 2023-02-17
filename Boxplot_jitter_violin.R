install.packages(c("data.table", "dplyr"))
install.packages("ggpubr")
install.packages("rstatix")
install.packages("ggplot2")
install.packages("gridExtra")
install.packages("ggbeeswarm")

library(ggpubr)
library(rstatix)
library(ggplot2)
library(gridExtra)
library(dplyr)
library(data.table)
library(ggbeeswarm)

df2 <- read.csv("Resummarized2015_singleCol.csv",header=T)
df2 <- transform(df2, Sample=factor(Sample, levels = c("Control","Buffer","BSA (Low)","BSA (High)","EXLX1-WT (Low)","EXLX1-WT (High)","EXLX1-D82N (High)","EXLX1-S16A (High)","Acceralase (0.5 fpu)","Acceralase (1 fpu)")))
# Rearrange the order of the samples. Check the above prior to plotting!

p1_1 <- ggplot(df2, aes(x=Sample, y=R.OH))
p1_2 <- p1_1+
  geom_jitter(aes(color=Sample))+
  geom_boxplot(aes(alpha=0.1))+
  labs(x = "Sample", y = expression(italic(paste({R[OH]})))) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size=12))+
  theme(axis.text.y = element_text(size=12))+
  theme(axis.title = element_text(size=14, hjust = 0.5))+
  scale_y_continuous(limits = c(0, 1))
plot(p1_2)

p1_3 <- p1_1+geom_jitter(aes(color=Sample))+
  geom_violin(aes(color=Sample, alpha=0.1))+
  labs(x = "Sample", y = expression(italic(paste({R[OH]})))) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size=12))+
  theme(axis.text.y = element_text(size=12))+
  theme(axis.title = element_text(size=14, hjust = 0.5))+
  scale_y_continuous(limits = c(0, 1))
plot(p1_3)

p1_4 <- p1_1+geom_boxplot(aes(color=Sample))+
  geom_violin(aes(color=Sample, alpha=0.1))+
  labs(x = "Sample", y = expression(italic(paste({R[OH]})))) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size=12))+
  theme(axis.text.y = element_text(size=12))+
  theme(axis.title = element_text(size=14, hjust = 0.5))+
  scale_y_continuous(limits = c(0, 1))
plot(p1_4)

p1_5 <- p1_1+
  geom_quasirandom(size=1,aes(color=Sample))+
  geom_boxplot(aes(alpha=0.1),outlier.colour = NA)+
  stat_summary(geom = "point", fun = mean, color = "black", shape = "diamond", size = 3) +
  labs(x = "Sample", y = expression(italic(paste({R[OH]})))) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size=12))+
  theme(axis.text.y = element_text(size=12))+
  theme(axis.title = element_text(size=14, hjust = 0.5))+
  theme(legend.position = "none")+
  scale_y_continuous(limits = c(0, 1))
plot(p1_5)
ggsave('BoxplotQuasirandom.png', dpi=400)
