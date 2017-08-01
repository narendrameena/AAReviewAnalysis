#narumeena
#using SKAT on data

install.packages("skat")


source("http://www.bioconductor.org/biocLite.R")
biocLite("rhdf5")

install.packages(c("shiny","svDialogs","data.table","bit64"))
library(devtools)
install_github("mw55309/poRe_docs.git")
#https://github.com/mw55309/poRe_docs.git

library(rhdf5)
pore_rt()

library(svGUI)
