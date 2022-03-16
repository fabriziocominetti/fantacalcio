library(tidyverse)
library(readr)
library(viridis)
require(hrbrthemes)
require(plotly)

load("Simulation dataset.RData")          # From simulations.Rdata

# Add final ranking

plotDf$rankFinal[plotDf$team=="Speck & Brizio"] <- 1
plotDf$rankFinal[plotDf$team=="Comi Etilico"] <- 2
plotDf$rankFinal[plotDf$team=="Olympique Marselio"] <- 3
plotDf$rankFinal[plotDf$team=="Herta Vernello"] <- 4
plotDf$rankFinal[plotDf$team=="FRANCESCO TOTTI"] <- 5
plotDf$rankFinal[plotDf$team=="Eiaculazio"] <- 6
plotDf$rankFinal[plotDf$team=="SSC Gomorra"] <- 7
plotDf$rankFinal[plotDf$team=="Costaminchia"] <- 8
plotDf$rankFinal[plotDf$team=="PIPPORAPINA"] <- 9
plotDf$rankFinal[plotDf$team=="Benevengo fc"] <- 10

cond <- plotDf$rankFinal == plotDf$rank

# Plots 
p <- plotDf %>%
  mutate(team = fct_reorder(team, rankFinal)) %>%
  ggplot(aes(x=rank, color=team, fill=team)) +
  geom_histogram(alpha=0.6, binwidth = 1) +
  geom_histogram(
    data=subset(plotDf, cond==TRUE), 
    binwidth=1, 
    fill="white") +
  scale_fill_viridis(discrete=TRUE) +
  scale_color_viridis(discrete=TRUE) +
  scale_x_continuous(
    name="Rank", 
    limits=c(0,11), 
    breaks=c(1,2,3, 4, 5, 6, 7, 8, 9, 10)) +
  theme_minimal() +
  theme(
    legend.position="none",
    panel.spacing = unit(0.1, "lines"),
    strip.text.x = element_text(size = 10)) +
  ylab("Simulations (tot: 10.000)") +
  facet_wrap(
    ~fct_reorder(team, rankFinal), 
    nrow = 2, 
    scales = "free_x",
    switch = "y") + 
  labs(
    title="Simulation results: frequency of final ranking by player for 10.000 randomly chosen permutations of initial drawing order",
    caption= "White bins correspond to the observed ranking for team")

p <- ggplotly(p)
htmlwidgets::saveWidget(as_widget(p), "Risultati simulazioni.html")