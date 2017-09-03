# Data-Mining Project
This directory contains work for the project of data mining in 2016.

## Motivation
In general, restaurant prices are usually positively related to the local average household income. Our question is: Could we also observe similar phenomenon when it comes to hospital charges and local poverty rates? Namely, does a hospital arrange its charges according to its location? We utilize the Inpatient Prospective Payment System (IPPS) Provider Summary and poverty rate statistical data to build a model to explore the relationship between hospital charges and local poverty rates.

## Dataset of the Project
We have the original data about hospitals, including DRG (Diagnosis-Related Group), hospital addresses, zip codes and charges. There are 163,065 records in the file, including 3,337 hospitals and the top 100 DRGs.

## Preliminary Data Processing
We processed the hospital data in two different ways.
1. For each hospital, we combine charges for all DRGs to generate a reasonable number representing its charge level. To do this, we first find the average charge for each DRG over the whole US. Then we divide the charge of the hospital by the average charge so that we have a charge level for each DRG and each hospital. This charge level can tell us how expensive the service provided by each hospital is for each DRG. Second we calculate the average level among all the DRGs one hospital provides service for. This average level is what we use to represent a hospital’s charge level.
2. We pick the hospital charges for 5 DRGs for analysis. First we find the top 5 most common DRGs (194, 690, 292, 392, 641) out of 100 DRGs. Second, since not all hospitals provide service for these 5 DRGs, for a fair comparison in our analysis we only include hospitals that provide service for all 5 DRGs. There are 2,664 such hospitals out of total 3,337 hospitals.

## Key Ideas in the Project
In the data collection stage, we found the local poverty rates corresponding to the hospital locations. However, this is not reasonable if a hospital is close to the boundary of its county and in fact closer to the centers of some other counties. For this reason, we update the original poverty rate corresponding to hospitals by using weighted poverty rates. To generate the weighted poverty rate for a hospital, we take into consideration all the counties that are within 50 miles of the hospital. The weight of the poverty rates of the neighboring counties is based on the distance between each county center and the hospital. More precisely, the closer the county center is to the hospital, the higher weight its poverty rate has in the weighted poverty rate.
To get better linear regression models, we separate hospitals into five groups based on their locations: west, midwest, northeast, southwest and southeast. We design the following algorithm:
1. Initialize 5 linear models corresponding to 5 region groups. See Section 4.1 for details.
2. For each state, find the closest model among the models generated in Step 1. Then put each state into the group that corresponds to its closest model. A model is the closest if the sum of L2 distance of all hospital points in that state to the model is minimized.
3. Apply the least squares method to each group and then update the coeffi- cients in the linear equations.
4. Repeat step 2 and step 3 until the clustering groups stay the same.

By this algorithm, we find 5 best "fit" least squares models. (Illustration of the models are in Project report.)
