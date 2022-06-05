data = read.csv("../data/full_features_linearregFRIENDLY.csv", header = TRUE)
data$X = NULL
data$Country = as.factor(data$Country)

set.seed(2022)
index <- sort(sample(nrow(data), nrow(data) * 0.7))

data_train = data[index, ]
data_test = data[-index, ]

## Model A: Only with Total Citation
plot(data_train$Cited.By, data_train$h_index, xlab = "Citation", ylab = "h_index"
     , main = "Scatterplot of Citation and h_index", col = data_train$Category)
model_A_1 = lm(h_index ~ Cited.By, data = data_train)
summary(model_A_1)
model_A_2 = lm(h_index ~ Cited.By + sqrt(Cited.By), data = data_train)
summary(model_A_2)
model_A_21 = lm(h_index ~ sqrt(Cited.By), data = data_train)
summary(model_A_21)
model_A_22 = lm(h_index ~ sqrt(Cited.By) + 0, data = data_train)
summary(model_A_22)
model_A_3 = lm(h_index ~ Cited.By + log(Cited.By), data = data_train)
summary(model_A_3)
AIC(model_A_1)
AIC(model_A_2)
AIC(model_A_21)
AIC(model_A_22)
AIC(model_A_3)
BIC(model_A_1)
BIC(model_A_2)
BIC(model_A_21)
BIC(model_A_22)
BIC(model_A_3)
# So we only inculde Cited.By^2 term in the regression model.

# Model B
model_B = lm(h_index ~ Documents + sqrt(Cited.By) +Preprints+Coauthor + Category
             +Topics + Awarded.Grants+max_cite+pub_div+recent_3 + academic_age, data = data_train)
summary(model_B)
AIC(model_B)
BIC(model_B)

# Model C
data_train$sqrt_cited = sqrt(data_train$Cited.By)
model_C = lm(h_index ~ sqrt_cited +Preprints+Category+max_cite + 0, data = data_train)
summary(model_C)
AIC(model_C)
BIC(model_C)

library(car)
#create vector of VIF values
vif_values <- vif(model_C)

#create horizontal bar chart to display each VIF value
barplot(vif_values, main = "VIF Values", horiz = TRUE, col = "steelblue", xlim=c(0,5))

#add vertical line at 5
abline(v = 5, lwd = 3, lty = 2)

plot(model_C)

# train MSE
mean((model_C$residuals)^2)

# test MSE
data_test$sqrt_cited = sqrt(data_test$Cited.By)
new = data.frame(sqrt_cited = data_test$sqrt_cited, Preprints = data_test$Preprints, Category = data_test$Category, max_cite = data_test$max_cite)
y_pred = predict(model_C, new, interval="confidence")
mean((y_pred[, 'fit'] - data_test$h_index)^2)


