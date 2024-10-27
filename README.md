# thermostatIO
Program to intercept and log thermostat commands to a US residential HVAC system. Specifically to prove that my 30yo furnace was oversized and should be downsized when replaced.

The code was specifically written for the BBB, but uses only digitalIO pins and should be simple to rewrite for any computer with GPIO like the Rpi.

I ran this on my furnace over the coldest week of the year and found the furnace to have less than a 50% duty cycle and very short average runtimes.


Some data I gathered - Context - my furnace was set to something like 68F durring the day, and allowed to coast down to 62F but I forget actual settings. Therfore every morning, it ran longer once, and every evening there was a period of not running. Furnace was 63/40k btu input @ 80% efficiency 2 stage furnace in a 1200sqft home with mostly updated insulation.

While running the experiment, I leanred that the furnace had been misconfigured by the previous owner/installer such that the furnace was basically always in the "low" stage. Specifically, it was in "adaptive 2 stage mode" which ignores thethermostats stage commands and uses logic "If previous burn lasted >= 16 minutes, the subsequent burn will be on the "high" stage. This was visible in the data where after the morning burn to get to daytime temp, the next furnace cycle would be extra short! Just fixing this setting made the house more comfortable in the mornings! 


I was also able to present this data to the HVAC contractors bidding on my replacement as proof that we can safely downsize to improve efficiency and comfort.

Total Time	3917.32
Total On	1779.93
Total Off	2137.38
Max On	82.35
Max Off	172.67
Min On	2.27
Min Off	0.33
Avg On	12.191301369863
Avg Off	14.6395890410959
Median On	10.33
Median Off	11.33
Average Duty Cycle	0.483871320946465
Median Duty Cycle	0.480076775723397
Avg Temp Delta	43.6243493150685
