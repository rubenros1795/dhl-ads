df <- read_delim("C:/Users/Ruben/Downloads/metadata/metadata/1870-1880.csv", 
                 +     "\t", escape_double = FALSE, trim_ws = TRUE)

df_t = df[df$paper_title == "De T??d : godsdienstig-staatkundig dagblad",]

plot( c(0, max(df_t$w)), c(0, max(df_t$h)), type= "n", xlab = "", ylab = "")

for(i in seq(1,nrow(df_t))){
  
  rect(df_t$min_x[i], df_t$min_y[i], df_t$max_x[i], df_t$max_y[i], col= rgb(1,0,0,alpha=0.1), border=F)
  rect(df_t$min_x[i], df_t$min_y[i], df_t$max_x[i], df_t$max_y[i], col= rgb(0,0,1.0,alpha=0.1), border=F)
  
}

list_issues = c()
list_artid = c()

for(issue in unique(df$issue_id)){
  issue_ss = df[df$issue_id == issue,]
  
  dim_articles = c()
  
  for(art_no in 1:length(issue_ss)){
    dim = issue_ss$w * issue_ss$h
    
    dim_articles = c(dim_articles, dim)
    
    article_id = issue_ss$id[which.min(dim_articles)]
    list_issues = c(list_issues, issue)
    list_artid = c(list_artid, article_id)
    
  }
}

smallest = data.frame(list_issues, list_artid)
smallest = smallest[!duplicated(smallest),]

list_img_urls = c()
for(id in smallest$list_artid){
  tmp = df[df$id == id,]
  tmp = tmp$image_url[1]
  list_img_urls = c(list_img_urls, tmp)
  
}

smallest$img_url = list_img_urls
