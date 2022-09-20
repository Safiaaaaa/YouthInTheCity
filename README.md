# Analizing child poverty in Berlin

Poverty is not only a material matter; it affects children’s everyday life, their social network, their educational chances, even their health. Associated with social segregation, which prevents children to be in touch with other milieus, it can become a hardly escapable trap. 

Is child poverty clustered in Berlin? If so, how and why? 

## Data collection and processing

We collected more than 100 geodata features from <a href="https://www.openstreetmap.org/#map=5/51.330/10.453">OpenStreetMap<a>  and <a href="https://daten.berlin.de/">Berlin Open Data platform<a>, including data on demographics, housing, urban planning and migration. 

Working with Geopandas and Pysal, we used spatial join and areal interpolation to aggregate our features to the level of the 542 Berliner planning areas, the smallest statistical areas on which social data is publicly available. Spatial vector data can have the form of a polygon, a line or a point. We transformed points data into polygons by applying a 500m buffer to it. This way, we made sure that the borders of the planning areas were smoother - having features situated close to another planning area impact it as well.

Our full dataset had 105 columns and 542 rows. 
We had to drop the 6 planning areas with the least residents because we did not have their child poverty rate and imputed other missing value with Sklearn KNN Imputer. 

<p align="center">
[<img alt="Wordcloud" src="Worldcloud.png"/>](https://appyouthinthecity.herokuapp.com/)
<p>
  
## Clustering 

We used K-means clustering to observe patterns in our data. We identified spatial patterns with regards to social data: there are clear (very) high child poverty clusters (see map below), planning areas with higher or lower social index (an index built by unemployement rate, child poverty and share of beneficiaries of social welfare) are not randomly distributed throughout space. They tend to form regions. 
We also observed a very clear infrastructural difference between center and periphery.

## Spatial regression

We decided to focus on the correlation between infrastructure and child poverty. In what context do children leave in poverty? Does child poverty correlate with infrastructural deficit? To answer these questions, we turned to regressions. 

- Target (dependent variable): Child poverty
- Features (independent / explanatory features): a selection of 10 infrastructural features (cultural institutions, schools and kindergartens, social housing, public housing, outdoor furnitures, parks and playgrounds, train stations, places for extracurricular education). 

### Baseline: OLS Regression
Our baseline model was a regular OLS regression (we used Pysal spreg OLS model). With an R2 from 0.36, it gave us fairly good results: we were able to explain 36% of the variablity of child poverty based on our selection of 10 infrastructural features. However, white test for heteroskedasticity was very significant, meaning our residuals where not randomly distributed, which violates a central assumption of an OLS regression and meant the calculated coefficients could not trusted. 

Moran's I test on the regression's residuals was also significant, which meant residuals were spatially autocorrelated.
    
### OLS Regression with regime
We added space manually to our model thanks to a regime, allowing it to output different coefficients between East and West Berlin. This gave a slightly higher R2 for East Berlin (0.37 vs. 0,36 for West Berlin). Furthermore, white test for both regimes were not significant anymore. Differentating between EAst and West Berlin improved our model. 
    
According to spatial diagnostics (Moran'I and Lagrange Multriplier tests) however, there were still lag spatial effects, so we turned to spatial regressions. 

### Spatial regression
We conducted both error and lag models, with and without regimes. Considering some planning areas are very small and might be impacted by infrastructures of planning areas which don't share a border, we used inverse distance weights.


#### Error models
In error models, spatial autocorrelation is considered as noise and added to the error term of the regression equation. Theoretically, this would imply that neighbouring observations are similar because they share the same characterics, and not because they influence each other. 
Error models did not perform much better than the OLS regression (Pseudo R2 of 0.38). 
    
#### Lag models
In lag model, spatial autocorrelation is considered as a feature: the y values of neighbours is added to the regression equation. 
By far, lag models outperformed all other models. Adding regimes still imprive the performance of the model, which implies that there are still significant infrastructural differences between East and West Berlin. 

<p align="center">
Summuray of the models performances
</p>
<p align="center">
<img alt="model metrics" width="400px" src="metrics.png"/>
</p>

Here is a comparison of the repartition and the value of our residuals between our baseline model and our best performing model. In red regions, the models underestimated child poverty. In blue regions, they overestimated it. 
    
<p align="center">
<img alt="residuals comparison" src="residuals_regimes.gif"/>
</p>

According to Lagrange multiplier tests for both error and lagged models were significant, even in thei robust version. TBC... 

Have a look at a selection of our data and results on our <a href="https://appyouthinthecity.herokuapp.com/">web app<a>!
  

This project was conducted by Maciej Szuba , Nichanok Auevechanichkul and Safia Ahmedou as part of a Data Science Bootcamp at Le Wagon (batch #874) in September 2022.
