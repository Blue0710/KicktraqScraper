library(ggplot2)
library(dplyr)
library(tidyr)
library(scales)
library(googleVis)

setwd("C:/Users/hilmiuysal/Desktop/NYC Data Science Academy/Projects/Kicktraq_Shiny/Kicktraq/data/source")

df = data.frame()

# Consolidate CSV files
for (file in list.files()) {
  print(file)
  df_dummy = read.csv(file, stringsAsFactors = FALSE)
  
#  if ('avg_pledge_per_backer' %in% colnames(df_dummy)) {
#    colnames(df_dummy)[colnames(df_dummy) == 'avg_pledge_per_backer'] = 'avg_pledge_amount_per_backer'
#  }
  
#  if (!('featured_project' %in% colnames(df_dummy))) {
#    df_dummy = df_dummy %>% mutate(featured_project = 'N/A')
#  }
  
  df = rbind(df, df_dummy)
  print('File read to DF')
}

# Eliminate duplicate rows  
df = data.frame(df %>% unique())

# Calculate campaign duration
df$campaign_start_date = as.Date(df$campaign_start_date)
df$campaign_end_date = as.Date(df$campaign_end_date)
df = df %>% mutate(duration = as.integer(df$campaign_end_date - df$campaign_start_date))

# Cast to integer
df$num_created_by_owner[df$num_created_by_owner == 'First created'] = 1
df$num_created_by_owner = as.integer(df$num_created_by_owner)

# Cancelled and suspended projects will not be regarded either as successful or unsuccessful.
# They will be eliminated from the analysis
df = df %>% filter(status %in% c('Funding Unsuccessful','Funding Successful'))

# Change status column values
df$status = if_else(df$status == 'Funding Successful', 'Success', 'Fail')

# Load US States
setwd("C:/Users/hilmiuysal/Desktop/NYC Data Science Academy/Projects/Kicktraq_Shiny/Kicktraq/data/")
us_states = read.csv('US_States.csv', stringsAsFactors = FALSE)

# Analysis will focus on US states only
df = merge(x = df,y = us_states,by = 'state')

# Lower state name chars and change column name to match with the map data
#df$state_name = tolower(df$state_name)
colnames(df)[which(colnames(df) == 'state_name')] = 'state.name'

# Add funding goal range
df = df %>% mutate(funding_goal_range = 
                if_else(funding_goal < 1000, '<1000', 
                        if_else(funding_goal < 10000, '<10000', 
                                if_else(funding_goal < 50000, '<50000', 
                                        if_else(funding_goal < 100000, '<100000', '>100000')))))

# Add funding percentage range
df = df %>% mutate(funding_percentage_range = 
                     if_else(funding_percentage < 1, '<1% Funded', 
                             if_else(funding_percentage < 20, '<20% Funded', 
                                     if_else(funding_percentage < 50, '<40% Funded',
                                                     if_else(funding_percentage < 100, '<100% Funded',
                                                             if_else(funding_percentage < 101, '<1% Over Funded',
                                                                     if_else(funding_percentage < 110, '<10% Over Funded',
                                                                             if_else(funding_percentage < 150, '<50% Over Funded',
                                                                                     if_else(funding_percentage < 200, '<2X Over Funded',
                                                                                             if_else(funding_percentage < 1000, '<10X Over Funded', '>10X Over Funded'))))))))))

# Add duration range
df = df %>% mutate(duration_range = 
                     if_else(duration <= 15, '<=15 Days', 
                             if_else(duration <= 30, '<=30 Days', 
                                     if_else(duration <= 45, '<=45 Days', '<=60 Days'))))

# Write 
setwd("C:/Users/hilmiuysal/Desktop/NYC Data Science Academy/Projects/Kicktraq_Shiny/Kicktraq/data")
write.csv(x = df, file = 'kicktraq_combined_R.csv', row.names = FALSE)



### Analysis begins ###

# EDA
df_project_counts = data.frame(df %>% group_by(status) %>% 
                                 summarise(CNT=n(), avg_goal=as.integer(mean(funding_goal)), 
                                           avg_raised=as.integer(mean(funding_raised)), 
                                           avg_updates=round(mean(num_updates), 2), 
                                           avg_backers=round(mean(num_backers), 2), 
                                           avg_comments=round(mean(num_comments), 2), 
                                           avg_faqs=round(mean(num_faqs, na.rm = TRUE), 2), 
                                           avg_camps_per_owner=round(mean(num_created_by_owner, na.rm = TRUE),2), 
                                           avg_duration=round(mean(duration, na.rm = TRUE), 2), 
                                           avg_proj_img=round(mean(project_img, na.rm = TRUE), 2),
                                           avg_proj_video=round(mean(project_video, na.rm = TRUE), 2),
                                           avg_featured=round(mean(featured_project, na.rm = TRUE), 2)) 
                               %>% mutate(PROP = CNT/sum(CNT)*100))


# What is the proportion of duration wrt campaign status?
df_ds = df %>% group_by(duration_range,status) %>% summarise(CNT = n()) %>% mutate(PROP = CNT/sum(CNT)*100)
ggplot(df_ds) + 
  geom_bar(aes(x = reorder(status, -CNT), y = CNT, fill = duration_range), position = "fill", stat = "identity") +
  scale_y_continuous(labels = scales::percent) + 
  xlab('Campaign Status') + 
  ylab('Proportion') + 
  ggtitle('Campaign Duration Ratio by Campaign Status')


# Top 10 categories by funding amount
cat_fund = df %>% group_by(category) %>% summarise(total_funding_raised = sum(funding_raised)) %>% arrange(desc(total_funding_raised)) %>% head(10)
ggplot(cat_fund) + 
  geom_col(aes(x = reorder(category, -total_funding_raised), y = total_funding_raised, fill = category)) +
  xlab('Category') + 
  ylab('Funding Raised ($)') + 
  ggtitle('Top 10 Categories By Funding Raised') +
  theme_bw() + 
  theme(axis.text.x = element_text(angle = 90), legend.position = 'none') +
  scale_y_continuous(labels = comma) # library(scales)


# Top 10 Categories With Highest Funding Raised by Success Rate
cat_succ = data.frame(df %>% group_by(category,status) %>% summarise(cnt = n()))
cat_succ2 = merge(cat_succ, cat_fund, by = 'category')
cat_succ3 = cat_succ2 %>% 
              spread(key = status, value = cnt, fill = 0) %>% 
              mutate(success_rate = (Success/(Success+Fail))*100) %>% 
              arrange(desc(success_rate))

ggplot(cat_succ3) + 
  geom_point(aes(x=category, y=success_rate, size=total_funding_raised), shape=21, color='#3dcb7a', fill='#3dcb7a') +
  theme_bw() + 
  theme(axis.text.x = element_text(angle = 90)) +
  #scale_y_continuous(labels = scales::percent)
  xlab('Category') + 
  ylab('Success Rate (%)') + 
  ggtitle('Top 10 Categories By Success Rate and Funding Raised') +
  ylim(c(30,100)) +
  scale_size_continuous(name = "Total Funding Raised", labels = comma)


# Success rate by funding goal range
# Less than 1000, 10000, 20000, 50000, 100000, 1M, >1M
goal_succ = df %>% group_by(funding_goal_range, status) %>% summarise(cnt = n())
goal_succ2 = goal_succ %>% spread(key = status, value = cnt, fill = 0) %>% mutate(success_rate = (Success/(Success+Fail))*100) %>% arrange(desc(success_rate)) %>% head(10)
ggplot(goal_succ2) + 
  geom_col(aes(x = reorder(funding_goal_range, -success_rate), y = success_rate, fill=funding_goal_range)) +
  theme_bw() + 
  theme(legend.position = 'none') +
  xlab('Funding Goal Range') + 
  ylab('Success Rate (%)') + 
  ggtitle('Success Rate By Funding Goal Range') +
  ylim(c(0,80))


# Failed projects and their funding_percentages
fail_fund_perc = df %>% filter(status == 'Fail') %>% group_by(funding_percentage_range) %>% summarise(CNT=n()) %>% mutate(RATIO = CNT/sum(CNT)*100)
succ_fund_perc = df %>% filter(status == 'Success' & !(funding_percentage_range %in% c('<1% Funded','<20% Funded'))) %>% group_by(funding_percentage_range) %>% summarise(CNT=n()) %>% mutate(RATIO = CNT/sum(CNT)*100)
ggplot(fail_fund_perc, aes(x = "", y = RATIO, fill = funding_percentage_range)) + 
        geom_bar(width = 1, stat = 'identity') + 
        coord_polar("y", start = 0) + 
        scale_fill_brewer(palette = "Set3") + 
        theme_classic() +
        theme(
          axis.line = element_blank(),
          axis.text = element_blank(),
          axis.ticks = element_blank(),
          plot.title = element_text(hjust = 0.5, color = "#666666")) +
        guides(fill = guide_legend(reverse = TRUE)) +
        labs(x = NULL, y = NULL, fill = NULL, title = "Funding Margin (Failed Campaigns)") + 
        geom_text(aes(label = paste0(round(RATIO), "%")), position = position_stack(vjust = 0.5))


ggplot(succ_fund_perc, aes(x = "", y = RATIO, fill = funding_percentage_range)) + 
  geom_bar(width = 1, stat = 'identity') + 
  coord_polar("y", start = 0) + 
  scale_fill_brewer(palette = "Set3") + 
  theme_classic() +
  theme(
    axis.line = element_blank(),
    axis.text = element_blank(),
    axis.ticks = element_blank(),
    plot.title = element_text(hjust = 0.5, color = "#666666")) +
  guides(fill = guide_legend(reverse = TRUE)) +
  labs(x = NULL, y = NULL, fill = NULL, title = "Funding Margin (Successful Campaigns)") + 
  geom_text(aes(label = paste0(round(RATIO), "%")), position = position_stack(vjust = 0.5))


# Most/least popular pledge tiers by category and by project size


# How many pledge tiers is optimum?


# Percentage of successful campaigns for each state
state_succ = df %>% group_by(state.name, status) %>% summarise(CNT=n())
state_succ2 = data.frame(
  state_succ %>% 
              spread(key = status, value = CNT, fill = 0) %>% 
              mutate(success_rate = (Success/(Success+Fail))*100) %>% 
              arrange(state.name)
)


# Plot campaign success rate by US States
require(datasets)
states <- data.frame(state.name, state.x77)
states2 = merge(states, state_succ2, by='state.name')


GeoStates <- gvisGeoChart(state_succ2, "state.name", "success_rate",
                          options=list(region="US", 
                                       displayMode="regions", 
                                       resolution="provinces",
                                       width=600, height=400))
plot(GeoStates)


